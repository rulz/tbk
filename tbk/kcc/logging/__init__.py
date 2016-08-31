import os
import datetime

import pytz

__all__ = ['logger', 'BaseHandler', 'NullHandler']


LOG_DATE_FORMAT = "%d%m%Y"
LOG_TIME_FORMAT = "%H%M%S"


class BaseHandler(object):

    def event_payment(self, date, time, pid, commerce_id, transaction_id, request_ip, token, webpay_server):
        '''Record the payment event

        Official handler writes this information to TBK_EVN%Y%m%d file.
        '''
        raise NotImplementedError("Logging Handler must implement event_payment")

    def event_confirmation(self, date, time, pid, commerce_id, transaction_id, request_ip, order_id):
        '''Record the confirmation event.

        Official handler writes this information to TBK_EVN%Y%m%d file.
        '''
        raise NotImplementedError("Logging Handler must implement event_confirmation")

    def event_error(self, date, time, pid, commerce_id, transaction_id, request_ip, order_id):
        '''Record the error event.

        Official handler writes this information to TBK_EVN%Y%m%d file.
        '''
        raise NotImplementedError("Logging Handler must implement event_confirmation")

    def log_confirmation(self, payload, commerce_id):
        '''Record confirmation event in another way (why?).

        Official handler writes this information to tbk_bitacora_TR_NORMAL_%m%d file.
        '''
        raise NotImplementedError("Logging Handler must implement log_confirmation")

    def log_error(self, payload, commerce_id):
        '''Record confirmation event in another way (why?).

        Official handler writes this information to tbk_bitacora_TR_NORMAL_%m%d file.
        '''
        raise NotImplementedError("Logging Handler must implement log_confirmation")


class NullHandler(BaseHandler):

    def event_payment(self, **kwargs):
        pass

    def event_confirmation(self, **kwargs):
        pass

    def event_error(self, **kwargs):
        pass

    def log_confirmation(self, **kwargs):
        pass

    def log_error(self, **kwargs):
        pass


class Logger(object):

    def __init__(self, handler):
        self.set_handler(handler)

    def set_handler(self, handler):
        self.handler = handler

    def payment(self, payment):
        santiago = pytz.timezone('America/Santiago')
        now = santiago.localize(datetime.datetime.now())
        self.handler.event_payment(
            date=now.strftime(LOG_DATE_FORMAT),
            time=now.strftime(LOG_TIME_FORMAT),
            pid=os.getpid(),
            commerce_id=payment.commerce.id,
            transaction_id=payment.transaction_id,
            request_ip=payment.request_ip,
            token=payment.token,
            webpay_server=self.get_webpay_server(payment.commerce)
        )

    def confirmation(self, confirmation):
        santiago = pytz.timezone('America/Santiago')
        now = santiago.localize(datetime.datetime.now())
        self.handler.event_confirmation(
            date=now.strftime(LOG_DATE_FORMAT),
            time=now.strftime(LOG_TIME_FORMAT),
            pid=os.getpid(),
            commerce_id=confirmation.commerce.id,
            transaction_id=confirmation.payload.transaction_id,
            request_ip=confirmation.request_ip,
            order_id=confirmation.order_id,
            webpay_server=self.get_webpay_server(confirmation.commerce)
        )
        self.handler.log_confirmation(
            payload=confirmation.payload,
            commerce_id=confirmation.commerce.id
        )

    def error(self, confirmation):
        santiago = pytz.timezone('America/Santiago')
        now = santiago.localize(datetime.datetime.now())
        self.handler.event_error(
            date=now.strftime(LOG_DATE_FORMAT),
            time=now.strftime(LOG_TIME_FORMAT),
            pid=os.getpid(),
            commerce_id=confirmation.commerce.id,
            transaction_id=confirmation.payload.transaction_id,
            request_ip=confirmation.request_ip,
            order_id=confirmation.order_id,
            webpay_server=self.get_webpay_server(confirmation.commerce)
        )
        self.handler.log_error(
            payload=confirmation.payload,
            commerce_id=confirmation.commerce.id
        )

    def get_webpay_server(self, commerce):
        return 'https://certificacion.webpay.cl' if commerce.testing else 'https://webpay.transbank.cl'

logger = Logger(NullHandler())


def configure_logger(handler):
    logger.set_handler(handler)
    return logger
