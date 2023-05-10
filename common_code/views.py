from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import get_common_code_list


class GenderList(APIView):
    def get(self, request):
        return Response(get_common_code_list("gender"))


class PreferredGenderList(APIView):
    def get(self, request):
        return Response(get_common_code_list("preferred_gender"))


class MBTIList(APIView):
    def get(self, request):
        return Response(get_common_code_list("mbti"))


class DrinkingStatusList(APIView):
    def get(self, request):
        return Response(get_common_code_list("drinking_status"))


class ReligionList(APIView):
    def get(self, request):
        return Response(get_common_code_list("religion"))


class LocationList(APIView):
    def get(self, request):
        return Response(get_common_code_list("location"))
