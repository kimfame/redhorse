import logging

from common_code.models import CommonCode, CommonCodeGroup
from passion.models import Passion
from .base_data import common_code_list, passion_list

logger = logging.getLogger(__name__)


def run():
    logger.info("Run base data generator")
    generate_option_codes()
    generate_passion_data()
    logger.info("Finished.")


def generate_option_codes():
    logger.info("Create option code data")
    for common_code in common_code_list:
        group_name = common_code[0]
        codes = common_code[1]

        if CommonCodeGroup.objects.filter(name=group_name).exists():
            continue

        common_code_group = CommonCodeGroup.objects.create(name=group_name)

        bulk_list = []

        for idx, code in enumerate(codes, 1):
            bulk_list.append(
                CommonCode(group=common_code_group, sub_id=idx, value=code)
            )

        CommonCode.objects.bulk_create(bulk_list)


def generate_passion_data():
    logger.info("Create passion data")

    if Passion.objects.all().exists():
        return

    bulk_list = []

    for passion in passion_list:
        bulk_list.append(Passion(name=passion))

    Passion.objects.bulk_create(bulk_list)
