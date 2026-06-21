from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

class TenantSecurityMiddleware:
    """
    Secures cross-tenant boundary routing when utilizing a shared global user table.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Grab current active workspace tenant determined by the domain routing
        active_tenant = getattr(request, 'tenant', None)
        
        # 2. Process gatekeeping rule definitions for authenticated sessions
        if request.user.is_authenticated and not request.user.is_superuser:
            user_tenant = getattr(request.user, 'tenant', None)
            
            # If the user's bound tenant does not match the workspace domain they are visiting
            if active_tenant and user_tenant != active_tenant:
                # Bypass restriction ONLY if accessing the main base landing portal (public schema)
                if active_tenant.schema_name != 'public':
                    logout(request)
                    messages.error(
                        request, 
                        f"Security Isolation Notice: Your account does not have access to this workspace."
                    )
                    return redirect('login')

        response = self.get_response(request)
        return response

