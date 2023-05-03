import logging

logger = logging.getLogger(__name__)


def send_sms_message(phone_number, message):
    logger.info("Call send_sms_message function")
    logger.info(f"Phone number : {phone_number}")
    logger.info(f"Message : {message}")
