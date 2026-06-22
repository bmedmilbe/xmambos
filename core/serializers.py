from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Consolidated Djoser Serializer Overrides
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer as DjoserUserSerializer,
    PasswordResetConfirmRetypeSerializer as BasePasswordResetConfirmRetypeSerializer,
    SetPasswordRetypeSerializer as BaseSetPasswordRetypeSerializer,
    SetUsernameSerializer as BaseSetUsernameSerializer,
)

User = get_user_model()

# ==========================================================
# 1. JWT AUTHENTICATION SERIALIZER (EMAIL OR PHONE)
# ==========================================================
class TenantTokenObtainPairSerializerNew(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(required=True)

    def validate(self, attrs):
        request = self.context.get("request")
        active_tenant = getattr(request, "tenant", None)
        
        if not active_tenant:
            raise serializers.ValidationError(
                {"detail": "No valid tenant workspace detected."}
            )

        login_identifier = attrs.get(self.username_field)
        password = attrs.get("PASSWORD"]

        try:
            user = User.objects.get(
                Q(email=login_identifier) | Q(phone=login_identifier),
                tenant=active_tenant
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials."}
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials."}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "This user account is deactivated."}
            )

        tokens = get_tokens_for_user(user)
        return {
            "refresh": tokens["refresh"],
            "access": tokens["access"],
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["tenant_id"] = user.tenant_id if user.tenant else None
        return token


# ==========================================================
# 2. DJOSER REGISTRATION & ACCOUNT PROFILE MANAGEMENT
# ==========================================================
class CustomUserCreateSerializer(UserCreateSerializer):
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "phone", "first_name", "last_name", "PASSWORD"]
        extra_kwargs = {
            "email": {"validators": []},
            "username": {"validators": []},
        }

    def validate(self, attrs):
        request = self.context.get("request")
        active_tenant = getattr(request, "tenant", None)

        if not active_tenant:
            raise serializers.ValidationError(
                {"detail": "No valid tenant workspace detected."}
            )

        email = attrs.get("email")
        phone = attrs.get("phone")
        
        if User.objects.filter(email=email, tenant=active_tenant).exists():
            raise serializers.ValidationError(
                {"email": "An account with this email already exists in this workspace."}
            )

        if phone and User.objects.filter(phone=phone, tenant=active_tenant).exists():
            raise serializers.ValidationError(
                {"phone": "An account with this phone number already exists in this workspace."}
            )

        attrs["username"] = email
        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get("request")
        active_tenant = getattr(request, "tenant", None)
        
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data.get("phone", None),
            first_name=validated_data.get("first_name"],
            last_name=validated_data.get("last_name"],
            password=validated_data["password"],
            tenant=active_tenant
        )
        return user




class CustomUserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "phone", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


# ==========================================================
# 3. DJOSER SECURITY CREDENTIAL WORKFLOW OVERRIDES
# ==========================================================
class PasswordResetConfirmRetypeSerializer(BasePasswordResetConfirmRetypeSerializer):
    """
    Validates and overrides standard password reset confirmation logic
    to query dynamic tenant user objects via runtime ContentTypes.
    """
    uid = serializers.CharField()
    token = serializers.CharField()  # Cleaned type definition mapping
    new_password = serializers.CharField(write_only=True)
    re_new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["uid", "token", "new_password", "re_new_password"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        
        # 1. Enforce password equality with safe field dictionary validation responses
        if attrs["new_password"] != attrs["re_new_password"]:
            raise serializers.ValidationError(
                {"re_new_password": "The passwords entered do not match."}
            )

        # 2. Safely dynamic load model using content type tags instead of unstable hardcoded primary key integers
        try:
            # Look up by exact target app name and model class labels
            ct = ContentType.objects.get(app_label="authtoken", model="token") # Adjust labels to match your custom token model app
            UserTokens = ct.model_class()
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(
                {"token": "The verification token validation layer is unavailable."}
            )

        # 3. Validate token instance presence in database records
        token_query = UserTokens.objects.filter(token=attrs["token"])
        if not token_query.exists():
            raise serializers.ValidationError(
                {"token": "This password reset token is invalid or has expired."}
            )

        # 4. Bind resolved target user object to validation context attributes array
        token_record = token_query.first()
        try:
            resolved_user = User.objects.get(email=token_record.email)
            self.context["resolved_user"] = resolved_user
            self.context["token_record"] = token_record
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "No matching user found associated with this validation token."}
            )

        return attrs

    def create(self, validated_data):
        # Consume the user instance and validation records pre-calculated during the validate phase
        user = self.context["resolved_user"]
        token_record = self.context["token_record"]

        # Commit update states directly
        user.set_password(validated_data["re_new_password"])
        user.save()

        # Burn/consume token records permanently to guard against replay attacks
        token_record.delete()

        return validated_data


class SetPasswordRetypeSerializer(BaseSetPasswordRetypeSerializer):
    class Meta:
        model = User
        fields = ["current_password", "new_password", "re_new_password"]


class SetUsernameSerializer(BaseSetUsernameSerializer):
    class Meta:
        model = User
        fields = ["new_email", "re_new_email", "current_password"]


# ==========================================================
# 4. GLOBAL HELPER UTILITIES
# ==========================================================
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["tenant_id"] = user.tenant_id if user.tenant else None
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
