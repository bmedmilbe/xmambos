# Create your views here.
import logging

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import UserTokens
from .serializers import PasswordResetConfirmRetypeSerializer, SendEmailResetSerializer

logger = logging.getLogger(__name__)


class PasswordConfirmViewSet(CreateModelMixin, GenericViewSet):
    http_method_name = ["post"]
    queryset = UserTokens.objects.all()

    serializer_class = PasswordResetConfirmRetypeSerializer

    # def get_serializer_class(self):
    #     # pprint(self.request.method)
    #     if self.request.method == "POST":
    #         return SendEmailResetSerializer
    #         # if serializer.is_valid():
    #         #     return SendEmailResetSerializer


class PasswordViewSet(CreateModelMixin, GenericViewSet):
    http_method_name = ["post"]
    queryset = UserTokens.objects.all()

    serializer_class = SendEmailResetSerializer
