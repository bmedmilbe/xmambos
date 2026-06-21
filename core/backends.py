from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q  # Added for OR queries

User = get_user_model()

class MultiTenantJWTAuthentication(JWTAuthentication):
    """
    Validates tokens based on precise tenant scoping rules:
    - If context is Public (No real tenant): User MUST be a staff/admin member.
    - If context is a Workspace (Tenant provided): Token MUST match the active tenant.
    """
    def authenticate(self, request):
        auth_data = super().authenticate(request)
        if not auth_data:
            return None

        user, token = auth_data
        active_tenant = getattr(request, 'tenant', None)

        # Determine if we are in a tenant workspace or public context
        is_public_context = active_tenant is None or active_tenant.schema_name == 'public'

        if is_public_context:
            # RULE 1: Public context -> Block standard clients, only allow global admins
            if not (user.is_staff or user.is_superuser):
                raise AuthenticationFailed(
                    "Access Denied: Only administration accounts can access this context."
                )
        else:
            # RULE 2: Tenant workspace context -> Token must match the active workspace exactly
            token_tenant_id = token.payload.get('tenant_id')

            if token_tenant_id != active_tenant.id:
                raise AuthenticationFailed(
                    "Security Isolation Breach: This token was issued for a different tenant workspace."
                )

        return user, token
    




class SharedModelTenantBackend(ModelBackend):
    """
    Authenticates shared-table users based on precise tenant scoping rules:
    - Supports authentication via email OR phone.
    - If context is Public (No real tenant): User MUST be a staff/admin member.
    - If context is a Workspace (Tenant provided): User MUST belong strictly to it.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if request is None:
            return None

        # Treat the incoming identifier as either email or phone
        login_identifier = username or kwargs.get(User.USERNAME_FIELD)
        if login_identifier is None:
            return None
            
        current_tenant = getattr(request, 'tenant', None)
        user = None

        # Determine if we are in a tenant workspace or public context
        is_public_context = current_tenant is None or current_tenant.schema_name == 'public'

        # Build query to match either email or phone field
        lookup_query = Q(email=login_identifier) | Q(phone=login_identifier)

        if is_public_context:
            # RULE 1: No tenant provided/public context -> Look for matching admins globally
            potential_admins = User.objects.filter(lookup_query, is_staff=True) | User.objects.filter(lookup_query, is_superuser=True)
            
            for potential_user in potential_admins.distinct():
                if potential_user.check_password(password):
                    user = potential_user
                    break
        else:
            # RULE 2: Tenant provided -> Must match the active workspace exactly
            try:
                user = User.objects.get(lookup_query, tenant=current_tenant)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass

        # Validate password, active state, and final role restrictions
        if user and user.check_password(password) and self.user_can_authenticate(user):
            if is_public_context and not (user.is_staff or user.is_superuser):
                return None  # Safety fallback rejection
            return user
            
        # Protect against timing analysis leaks if lookup fails completely
        if not user:
            User().set_password(password)
        return None
