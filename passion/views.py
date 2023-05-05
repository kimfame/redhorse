from rest_framework import viewsets, mixins

from passion.models import Passion
from passion.serializers import PassionSerializer


class PassionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PassionSerializer
    queryset = Passion.objects.all()
    http_method_names = ["get"]
