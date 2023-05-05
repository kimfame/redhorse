from rest_framework.response import Response
from rest_framework.views import APIView

from common_code.models import CommonCode


class CommonCodeList(APIView):
    def __init__(self, category):
        super(CommonCodeList, self).__init__()
        self.category = category

    def get(self, request):
        common_codes = list(
            CommonCode.objects.filter(group__name=self.category).values_list(
                "value",
                flat=True,
            )
        )
        return Response(common_codes)


class GenderList(CommonCodeList):
    def __init__(self):
        super(GenderList, self).__init__(category="gender")


class PreferredGenderList(CommonCodeList):
    def __init__(self):
        super(PreferredGenderList, self).__init__(category="preferred_gender")


class MBTIList(CommonCodeList):
    def __init__(self):
        super(MBTIList, self).__init__(category="mbti")


class DrinkingStatusList(CommonCodeList):
    def __init__(self):
        super(DrinkingStatusList, self).__init__(category="drinking_status")


class ReligionList(CommonCodeList):
    def __init__(self):
        super(ReligionList, self).__init__(category="religion")


class LocationList(CommonCodeList):
    def __init__(self):
        super(LocationList, self).__init__(category="location")
