from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = "M", _("남성")
    FEMALE = "F", _("여성")


class PreferredGender(models.TextChoices):
    MALE = "M", _("남성")
    FEMALE = "F", _("여성")
    ALL = "A", _("모두")


class DrinkingStatus(models.TextChoices):
    NO = "안함", _("안함")
    LIGHT = "가끔", _("가끔")
    HEAVY = "자주", _("자주")


class Religion(models.TextChoices):
    NO = "없음", _("없음")
    CHRISTIAN = "기독교", _("기독교")
    BUDDHIST = "불교", _("불교")
    CATHOLIC = "천주교", _("천주교")


class Location(models.TextChoices):
    SEOUL = "서울", _("서울")
    BUSAN = "부산", _("부산")
    DAEGU = "대구", _("대구")
    INCHEON = "인천", _("인천")
    GWANGJU = "광주", _("광주")
    DAEJEON = "대전", _("대전")
    ULSAN = "울산", _("울산")
    SEJONG = "세종", _("세종")
    GYEONGGI = "경기", _("경기")
    GANGWON = "강원", _("강원")
    CHUNGBUK = "충북", _("충북")
    CHUNGNAM = "충남", _("충남")
    JEONBUK = "전북", _("전북")
    JEONNAM = "전남", _("전남")
    GYEONGBUK = "경북", _("경북")
    GYEONGNAM = "경남", _("경남")
    JEJU = "제주", _("제주")
