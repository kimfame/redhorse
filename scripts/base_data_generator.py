import logging

from option_code.models import OptionCode, OptionCodeGroup
from .base_data import option_code_list

logger = logging.getLogger(__name__)


def run():
    logger.info("Run base data generator")
    generate_option_codes()
    logger.info("Finished.")


def generate_option_codes():
    logger.info("Create option code data")
    for option_code in option_code_list:
        group_name = option_code[0]
        codes = option_code[1]

        if OptionCodeGroup.objects.filter(name=group_name).exists():
            continue

        option_code_group = OptionCodeGroup.objects.create(name=group_name)

        bulk_list = []

        for idx, code in enumerate(codes, 1):
            bulk_list.append(
                OptionCode(group=option_code_group, sub_id=idx, value=code)
            )

        OptionCode.objects.bulk_create(bulk_list)
