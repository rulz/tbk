# encoding=UTF-8
from __future__ import unicode_literals

import os
import datetime
from contextlib import closing

import pytz


def event_payment_format(**kwargs):
    return PAYMENT_FORMAT.format(**kwargs)


def event_confirmation_format(**kwargs):
    return CONFIRMATION_FORMAT.format(**kwargs)


def event_error_format(**kwargs):
    return ERROR_FORMAT.format(**kwargs)


def log_confirmation_format(**kwargs):
    return JOURNAL_FORMAT % kwargs


def log_error_format(**kwargs):
    return JOURNAL_ERROR_FORMAT % kwargs


EVENTS_LOG_FILE_NAME_FORMAT = "TBK_EVN%s.log"
EVENTS_LOG_FILE_DATE_FORMAT = "%Y%m%d"
JOURNAL_LOG_FILE_NAME_FORMAT = "tbk_bitacora_TR_NORMAL_%s.log"
JOURNAL_LOG_FILE_DATE_FORMAT = "%m%d"


class WebpayOfficialHandler(object):

    def __init__(self, path=None, notification_url='http://127.0.0.1/notify'):
        self.path = path
        self.notification_url = notification_url

    def event_payment(self, **kwargs):
        with closing(self.events_log_file) as events_log_file:
            events_log_file.write(event_payment_format(**kwargs))

    def event_confirmation(self, **kwargs):
        format_params = {'notification_url': self.notification_url}
        format_params.update(kwargs)
        with closing(self.events_log_file) as events_log_file:
            events_log_file.write(event_confirmation_format(**format_params))

    def event_error(self, **kwargs):
        format_params = {'notification_url': self.notification_url}
        format_params.update(kwargs)
        with closing(self.events_log_file) as events_log_file:
            events_log_file.write(event_error_format(**format_params))

    def log_confirmation(self, payload, commerce_id):
        format_params = {'commerce_id': commerce_id}
        format_params.update(**payload.data)
        with closing(self.journal_log_file) as journal_log_file:
            journal_log_file.write(log_confirmation_format(**format_params))

    def log_error(self, payload, commerce_id):
        format_params = {'commerce_id': commerce_id}
        format_params.update(**payload.data)
        with closing(self.journal_log_file) as journal_log_file:
            journal_log_file.write(log_error_format(**format_params))


    @property
    def events_log_file(self):
        return self.log_file(EVENTS_LOG_FILE_NAME_FORMAT, EVENTS_LOG_FILE_DATE_FORMAT)

    @property
    def journal_log_file(self):
        return self.log_file(JOURNAL_LOG_FILE_NAME_FORMAT, JOURNAL_LOG_FILE_DATE_FORMAT)

    def log_file(self, log_file_name_format, log_file_date_format):
        santiago = pytz.timezone('America/Santiago')
        now = santiago.localize(datetime.datetime.now())
        file_name = log_file_name_format % now.strftime(log_file_date_format)
        return open(os.path.join(self.path, file_name), 'a+')


PAYMENT_FORMAT = (
    "          ;{pid:>12};   ;Filtro    ;Inicio                                  ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Inicio de filtrado\n"  # noqa
    "          ;{pid:>12};   ;Filtro    ;tbk_param.txt                           ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Archivo parseado\n"  # noqa
    "          ;{pid:>12};   ;Filtro    ;Terminado                               ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Datos Filtrados con exito\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;inicio                                  ;{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Parseo realizado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos en datos/tbk_config.dat\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Mac generado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Construccion TBK_PARAM\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};TBK_PARAM encriptado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos listos para ser enviados\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Medio 2: Por redireccion\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos validados\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Token={token:}\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Redireccion web\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Todo OK\n"  # noqa
)

CONFIRMATION_FORMAT = (
    "          ;{pid:>12};   ;Filtro    ;Inicio                                  ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Inicio de filtrado\n"  # noqa
    "          ;{pid:>12};   ;Filtro    ;tbk_param.txt                           ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Archivo parseado\n"  # noqa
    "          ;{pid:>12};   ;Filtro    ;Terminado                               ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Datos Filtrados con exito\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;inicio                                  ;{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Parseo realizado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos en datos/tbk_config.dat\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Mac generado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Construccion TBK_PARAM\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};TBK_PARAM encriptado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos listos para ser enviados\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Medio 2: Por redireccion\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos validados\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Redireccion web\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Todo OK\n"  # noqa
    "          ;{pid:>12};   ;resultado ;Desencriptando                          ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;TBK_PARAM desencriptado\n"  # noqa
    "          ;{pid:>12};   ;resultado ;Validacion                              ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Entidad emisora de los datos validada\n"  # noqa
    "          ;{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Parseo de los datos\n"  # noqa
    "          ;{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;                    ;{notification_url}\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;transacc  ;{transaction_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};conectandose al port :(80)\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;logro abrir_conexion                    ;{date:<14};{time:<6};{request_ip:<15}; 0 ;{commerce_id:<20};Abrio socket para conex-com\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;transacc  ;{transaction_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};POST a url {notification_url}\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;transacc  ;{transaction_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};mensaje enviado\n"  # noqa
    "          ;{pid:>12};   ;check_mac ;                                        ;{date:<14};{time:<6};EMPTY          ;OK ;                    ;Todo OK\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;transacc  ;{transaction_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Llego ACK del Comercio\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};tienda acepto transaccion\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};respuesta enviada a TBK (ACK)\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Todo OK\n"  # noqa
)

ERROR_FORMAT = (
        "          ;{pid:>12};   ;Filtro    ;Inicio                                  ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Inicio de filtrado\n"  # noqa
    "          ;{pid:>12};   ;Filtro    ;tbk_param.txt                           ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Archivo parseado\n"  # noqa
    "          ;{pid:>12};   ;Filtro    ;Terminado                               ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Datos Filtrados con exito\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;inicio                                  ;{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Parseo realizado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos en datos/tbk_config.dat\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Mac generado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Construccion TBK_PARAM\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};TBK_PARAM encriptado\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos listos para ser enviados\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Medio 2: Por redireccion\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Datos validados\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Redireccion web\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;pago      ;{webpay_server:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Todo OK\n"  # noqa
    "          ;{pid:>12};   ;resultado ;Desencriptando                          ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;TBK_PARAM desencriptado\n"  # noqa
    "          ;{pid:>12};   ;resultado ;Validacion                              ;{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Entidad emisora de los datos validada\n"  # noqa
    "          ;{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;                    ;Parseo de los datos\n"  # noqa
    "          ;{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;                    ;{notification_url}\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;transacc  ;{transaction_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};conectandose al port :(80)\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;logro abrir_conexion                    ;{date:<14};{time:<6};{request_ip:<15}; 0 ;{commerce_id:<20};Abrio socket para conex-com\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;transacc  ;{transaction_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};POST a url {notification_url}\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;transacc  ;{transaction_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};mensaje enviado\n"  # noqa
    "          ;{pid:>12};   ;check_mac ;                                        ;{date:<14};{time:<6};EMPTY          ;OK ;                    ;Todo OK\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;                    ;tienda NO acepto transaccion\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};OK ;                    ;respuesta enviada a TBK (ERR)\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;datoscom                                ;{date:<14};{time:<6};{request_ip:<15};OK ;{commerce_id:<20};Error al obtener ack (46)\n"  # noqa
    "{transaction_id:<10};{pid:>12};   ;resultado ;{order_id:<40};{date:<14};{time:<6};{request_ip:<15};ERR;                    ;46\n"  # noqa
) # replace with error format

JOURNAL_FORMAT = (
    "ACK; "
    "TBK_ORDEN_COMPRA=%(TBK_ORDEN_COMPRA)s; "
    "TBK_CODIGO_COMERCIO=%(commerce_id)s; "
    "TBK_TIPO_TRANSACCION=%(TBK_TIPO_TRANSACCION)s; "
    "TBK_RESPUESTA=%(TBK_RESPUESTA)s; "
    "TBK_MONTO=%(TBK_MONTO)s; "
    "TBK_CODIGO_AUTORIZACION=%(TBK_CODIGO_AUTORIZACION)s; "
    "TBK_FINAL_NUMERO_TARJETA=%(TBK_FINAL_NUMERO_TARJETA)s; "
    "TBK_FECHA_CONTABLE=%(TBK_FECHA_CONTABLE)s; "
    "TBK_FECHA_TRANSACCION=%(TBK_FECHA_TRANSACCION)s; "
    "TBK_HORA_TRANSACCION=%(TBK_HORA_TRANSACCION)s; "
    "TBK_ID_SESION=%(TBK_ID_SESION)s; "
    "TBK_ID_TRANSACCION=%(TBK_ID_TRANSACCION)s; "
    "TBK_TIPO_PAGO=%(TBK_TIPO_PAGO)s; "
    "TBK_NUMERO_CUOTAS=%(TBK_NUMERO_CUOTAS)s; "
    "TBK_VCI=%(TBK_VCI)s; "
    "TBK_MAC=%(TBK_MAC)s\n"
)

JOURNAL_ERROR_FORMAT = (
    "ERR; "
    "TBK_ORDEN_COMPRA=%(TBK_ORDEN_COMPRA)s; "
    "TBK_TIPO_TRANSACCION=%(TBK_TIPO_TRANSACCION)s; "
    "TBK_RESPUESTA=%(TBK_RESPUESTA)s; "
    "TBK_MONTO=%(TBK_MONTO)s; "
    "TBK_CODIGO_AUTORIZACION=%(TBK_CODIGO_AUTORIZACION)s; "
    "TBK_FINAL_NUMERO_TARJETA=%(TBK_FINAL_NUMERO_TARJETA)s; "
    "TBK_FECHA_CONTABLE=%(TBK_FECHA_CONTABLE)s; "
    "TBK_FECHA_TRANSACCION=%(TBK_FECHA_TRANSACCION)s; "
    "TBK_HORA_TRANSACCION=%(TBK_HORA_TRANSACCION)s; "
    "TBK_ID_SESION=%(TBK_ID_SESION)s; "
    "TBK_ID_TRANSACCION=%(TBK_ID_TRANSACCION)s; "
    "TBK_TIPO_PAGO=%(TBK_TIPO_PAGO)s; "
    "TBK_NUMERO_CUOTAS=%(TBK_NUMERO_CUOTAS)s; "
    "TBK_VCI=%(TBK_VCI)s; "
    "TBK_MAC=%(TBK_MAC)s\n"
)

