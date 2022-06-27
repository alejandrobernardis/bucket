#!/usr/bin/env python

import time
from abc import ABC
from enum import Enum
from functools import cache
from typing import Optional, Union, Any

from aiohttp import ClientSession, hdrs
from aiohttp.typedefs import StrOrURL
from core.clients import ApiClientABC, RequestContext
from core.web import Application

from bind.schemas import CreateCvuModel, CreateCvuAliasModel, DeleteCvuModel, \
    MakeCvuTxnModel, TxnStatusTypes, TxnOriginTypes

__all__ = ['BindClient', 'Paginator', 'BANK_ID', 'VIEW_ID', 'ACCOUNT_ID',
           'DEFAULT_PAGE', 'WalletClient']

# vars
CLIENT_NAME: str = 'bind'
CLIENT_ENDPOINT: str = 'https://sandbox.bind.com.ar/'

# consts (sandbox)
BANK_ID: int = 999
VIEW_ID: str = 'owner'
ACCOUNT_ID: str = '00-0-00000-0-0'


class BindClient(ApiClientABC, ABC):

    def __init__(
            self,
            name: str,
            app: Application,
            bank_id: int = BANK_ID,
            account_id: str = ACCOUNT_ID,
            endpoint: Optional[StrOrURL] = None,
            auth_endpoint: Optional[StrOrURL] = None,
            session: Optional[ClientSession] = None,
            headers: Optional[dict] = None
    ) -> None:
        """
        :param name: nombre del cliente.
        :param app: aplicación de referencia.
        :param bank_id: Código de identificación de la entidad.
        :param account_id: Código de identificación de la cuenta
                        (formato: XX-X-XXXX-X). Esta es la cuenta recaudadora
                        que se vincula a la billetera virtual. Esta cuenta
                        debe haber sido dada de alta previamente como
                        recaudadora para el proveedor de billetera virtual.
        :param endpoint: endpoint base.
        :param auth_endpoint: endpoint de autenticación.
        :param session: sesión existente de referencia.
        :param headers: cabeceras base
        """

        # TODO(berna): mejorar la configuración del cliente.

        name = f'{CLIENT_NAME}_{name}'
        endpoint = endpoint or CLIENT_ENDPOINT
        auth_endpoint = auth_endpoint or 'v1/login/jwt'

        super().__init__(name, app, endpoint, auth_endpoint, session, headers)

        # account-data
        self._bank_id: int = bank_id
        self._account_id: str = account_id

        # session-data
        self._token: Optional[str] = None
        self._token_expires_in: Optional[float] = None
        self._token_process: Optional[str] = None

    async def login(self, force: bool = False, **kwargs) -> Optional[str]:
        """
        Inicia sesión contra el endpoint de la API del BIND y devuelve el token.

        NOTAS:
        ~~~~~

        - De momento el token es almacenado en memoria, la idea es persistirlo
          en redis.

        :param force: fuerza la generación del token.
        :param kwargs: argumento adicionales.
        :return: str
        """
        if force is True or not self.is_logged or (
                time.time() > self._token_expires_in
        ):
            self.counters.req.increment()
            self.counters.log.increment()

            async with self._sess.post(self._auth_endpoint, json={
                'username': self._app.cfg.bind.username,
                'password': self._app.cfg.bind.password
            }, **kwargs) as res:

                data = await res.json()

                if res.status != 200:
                    self.counters.err.increment()
                    self.counters.log_err.increment()

                    msg: str = f'{self.name} LOGIN {res.status} -> {data}'
                    self._app.logger.error(msg)
                    self.logout()

                else:
                    self._token = data['token']
                    self._token_expires_in = time.time() + data['expires_in']
                    self._token_process = res.headers['process']
                    self._sess.headers[hdrs.AUTHORIZATION] \
                        = f'JWT {self._token}'

        return self._token

    def logout(self) -> None:
        self._token = None
        self._token_expires_in = None
        self._token_process = None

        if hdrs.AUTHORIZATION in self._sess.headers:
            del self._sess.headers[hdrs.AUTHORIZATION]

    @property
    def is_logged(self) -> bool:
        return self._token is not None


# Paginator

def _check_enum(x: Any, y: Any) -> Any:
    return x[y.upper()] if isinstance(y, str) else y


class Paginator:
    def __init__(
            self,
            status: Union[str, TxnStatusTypes] = None,
            limit: int = 50,
            offset: int = 1,
            from_date: Optional[str] = None,
            to_date: Optional[str] = None,
            origin: Union[str, TxnOriginTypes] = None
    ) -> None:
        """
        Modelo de paginación para las operaciones realizados en la API
        del Banco Industrial.

        Todos los argumentos con de carácter opcional.

        ---

        :param status: `obp_status` Estado de la transferencia.
                        - `COMPLETED`: Completada.
                        - `PENDING`: Pendiente de firma.
                        - `IN_PROGRESS`: En curso.
                        - `UNKNOWN`: Desconocido.
                        - `FAILED`: Con error.
                        - `UNKNOWN_FOREVER`: Desconocido y no se va a
                                             reintentar actualizar.
                        - `AWAITING_CONFIRMATION`: Pendiente de aceptación
                                                   del comprador (DEBIN).
                        - `CANCELED`: Cancelada (DEBIN).
                        - `EXPIRED`: Expirado (DEBIN).
                        - `REFUNDED`: Devolución del monto por contracargo
                                      (DEBIN).
                        - `REJECTED_CLIENT`: Rechazo del comprador (DEBIN).
                        - `REJECTED`: Rechazo del comprador
                                      (SUSCRIPCION DE DEBIN).
                        - `ACTIVE`: Aceptación del comprador
                                    (SUSCRIPCION DE DEBIN).
                        - `INACTIVE`: Cancelación del comprador
                                      (SUSCRIPCION DE DEBIN).
        :param limit: `obp_limit` Tamaño de página.
                       - Valor por defecto: `1`
        :param offset: `obp_offset` Número de página. Acepta obp_offset=0
                       como válido pero se comporta como si se hubiera enviado
                       obp_offset=1.
                        - Valor por defecto: `1`
        :param from_date: `obp_from_date` Fecha desde. ISO.
                           - Por ejemplo: `2017-01-01`
                           - Valor por defecto: última semana
        :param to_date: `obp_to_date` Fecha Hasta. ISO.
                         - Por ejemplo: `2017-01-01`
                         - Valor por defecto: `ahora`
        :param origin: `obp_origin` Origen de la transferencia.
                        - `TRANSFERENCIAS_ENVIADAS`: Las transferencias
                                                     emitidas a terceros
                                                     (Valor por defecto).
                        - `TRANSFERENCIAS_RECIBIDAS`: Las transferencias
                                                      recibidas de terceros.
        """

        # assigns
        self._status: Optional[TxnStatusTypes] = None
        self._limit: int = max(1, limit)
        self._offset: int = max(1, offset)
        self._from_date: Optional[str] = from_date
        self._to_date: Optional[str] = to_date
        self._origin: Optional[TxnOriginTypes] = None

        # set values
        self.set_status(status)
        self.set_origin(origin)

    # properties

    def set_status(self, value: Optional[TxnStatusTypes]):
        self._status = _check_enum(TxnStatusTypes, value)

    def set_origin(self, value: Optional[TxnOriginTypes]):
        self._origin = _check_enum(TxnOriginTypes, value)

    # methods

    def next_page(self) -> dict:
        self._offset += 1
        return self.headers

    def set_page(self, value: int) -> dict:
        self._offset = value
        return self.headers

    def prev_page(self) -> dict:
        if self._offset > 1:
            self._offset -= 1
        return self.headers

    # helper

    @property
    def page(self) -> int:
        return self._offset

    @property
    def headers(self) -> dict:
        """
        Formatea un diccionario con los valores requeridos en la cabecera.

        :return: dict
        """
        default: dict = {'obp_limit': self._limit, 'obp_offset': self._offset}
        for x in ('_status', '_from_date', '_to_date', '_origin'):
            y = getattr(self, x, None)
            if y is not None:
                if isinstance(y, Enum):
                    y = y.value
                default[f'obp{x}'] = y
        return default


DEFAULT_PAGE: Paginator = Paginator()


@cache
def _base_url(bank_id: int, account_id: str, view_id: str) -> str:
    return f'/v1/banks/{bank_id}/accounts/{account_id}/{view_id}'


@cache
def _crud_cvu(bank_id: int, account_id: str, view_id: str) -> str:
    return _base_url(bank_id, account_id, view_id) + '/wallet'


@cache
def _txn_cvu(bank_id: int, account_id: str, view_id: str) -> str:
    return _base_url(bank_id, account_id, view_id) \
        + f'/transaction-request-types/TRANSFER-CVU'


class WalletClient(BindClient):

    def __init__(
            self,
            app: Application,
            bank_id: int = BANK_ID,
            account_id: str = ACCOUNT_ID,
            **kwargs
    ) -> None:
        """
        Wallet Client. https://sandbox.bind.com.ar/apidoc/#api-Billetera
        :return: None
        """
        super().__init__(
            'wallet',
            app,
            bank_id=bank_id,
            account_id=account_id,
            **kwargs
        )
        
    def create_cvu(
            self,
            data: CreateCvuModel,
            view_id: str = VIEW_ID
    ) -> RequestContext:
        """
        Alta CVU cliente
        ~~~~~~~~~~~~~~~~

        Crea un CVU a partir del id de cliente enviado y el identificador
        del proveedor de billetera virtual.

        Este servicio valida que la cuenta enviada por parámetro (account_id)
        está definida como cuenta recaudadora del proveedor de billetera
        virtual y se asigna esa cuenta como recaudadora para el CVU.

        En caso que el CVU ya exista para la billetera y client_id, se
        devuelve respuesta OK como si se hubiera creado el CVU, junto con
        el valor del CVU y un mensaje de duplicado. En ese caso se devuelve
        el AliasCVU como un string vacío.

        Se debe tener en cuenta que una vez que se da de alta una CVU,
        el CUIT asociado a la misma no puede ser modificado.

        https://sandbox.bind.com.ar/apidoc/#api-Billetera-CrearCVU

        ---

        :param data: Ver request en el link de la documentación.
        :param view_id: Código de identificación de la vista.
        :return: RequestContext
        """
        return self.post(
            f'{_crud_cvu(self._bank_id, self._account_id, view_id)}'
            f'/cvu',
            data=data.json()
        )

    def create_cvu_alias(
            self,
            data: CreateCvuAliasModel,
            view_id: str = VIEW_ID
    ) -> RequestContext:
        """
        Asignar/Modificar Alias CVU
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Crear o modificar un alias para un CVU existente.

        Este servicio valida que la cuenta enviada por parámetro (account_id)
        sea la cuenta recaudadora del CVU.

        https://sandbox.bind.com.ar/apidoc/#api-Billetera-AsignarAliasCVU

        ---

        :param data: Ver request en el link de la documentación.
        :param view_id: Código de identificación de la vista.
        :return: RequestContext
        """
        return self.post(
            f'{_crud_cvu(self._bank_id, self._account_id, view_id)}'
            f'/alias',
            data=data.json()
        )

    def delete_cvu(
            self,
            data: DeleteCvuModel,
            view_id: str = VIEW_ID
    ) -> RequestContext:
        """
        Baja de CVU
        ~~~~~~~~~~~

        Eliminar CVU existente.

        Se valida que el CVU pertenezca al cuit informado y a la billetera.

        La baja es lógica y no se puede volver a dar de alta esa CVU para
        otro CUIT.

        https://sandbox.bind.com.ar/apidoc/#api-Billetera-EliminarCVU

        ---

        :param data: Ver request en el link de la documentación.
        :param view_id: Código de identificación de la vista.
        :return: RequestContext
        """
        return self.delete(
            f'{_crud_cvu(self._bank_id, self._account_id, view_id)}'
            f'/cvu/{data.cvu}/{data.cuit}',
        )

    def make_cvu_trx(
            self,
            data: MakeCvuTxnModel,
            view_id: str = VIEW_ID
    ) -> RequestContext:
        """
        Realizar transferencia desde un CVU
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Realiza una transferencia desde una cuenta de un cliente
        de billetera virtual a un CVU, CBU o Alias.

        https://sandbox.bind.com.ar/apidoc/#api-Billetera-CrearTransferenciaCVU

        ---

        :param data: Ver request en el link d ela documentación.
        :param view_id: Código de identificación de la vista.
        :return: RequestContext
        """
        return self.post(
            f'{_txn_cvu(self._bank_id, self._account_id, view_id)}'
            f'/transaction-requests',
            data=data.json()
        )

    def list_cvu_trx(
            self,
            page: Paginator = DEFAULT_PAGE,
            view_id: str = VIEW_ID
    ) -> RequestContext:
        """
        Obtener listado de transferencias
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Obtiene un listado de transferencias realizadas desde una
        billetera virtual o hacia una billetera virtual.

        El parámetro account_id debe ser la cuenta recaudadora.

        https://sandbox.bind.com.ar/apidoc/#api-Billetera-ObtenerPedidosTransferenciasCvu

        ---

        :param page: Configuración de la página.
        :param view_id: Código de identificación de la vista.
        :return: RequestContext
        """
        return self.get(
            _txn_cvu(self._bank_id, self._account_id, view_id),
            headers=page.headers
        )

    def fetch_cvu_trx(
            self,
            transaction_id: str,
            view_id: str = VIEW_ID
    ) -> RequestContext:
        """
        Obtener una transferencia
        ~~~~~~~~~~~~~~~~~~~~~~~~~

        Obtener el detalle de una transferencia de CVU (o hacia CVU)
        en particular. El estado IN_PROGRESS se intentará resolver al final
        del día cuando se concilien todas las operaciones, pero esta consulta
        intentará resolverlo en el momento.

        https://sandbox.bind.com.ar/apidoc/#api-Billetera-ObtenerPedidoTransferenciaCvu

        ---

        :param transaction_id: Identificador de la transferencia. Puede ser
                               el generado por el usuario o el devuelto por
                               Realizar transferencias desde un CVU o el id
                               devuelto en la consulta de transferencias.
        :param view_id: Código de identificación de la vista.
        :return: RequestContext
        """
        return self.get(
            f'{_txn_cvu(self._bank_id, self._account_id, view_id)}'
            f'/{transaction_id}'
        )
