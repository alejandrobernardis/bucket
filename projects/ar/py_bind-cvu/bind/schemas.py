#!/usr/bin/env python

from enum import auto
from typing import Optional

from core.fields import ClientID, CUIT, CVU, CVUAlias, OriginID
from core.schemas import AutoName
from pydantic import BaseModel, validator, constr, EmailStr


# Schemas

class TxnStatusTypes(AutoName):
    """
    Estado de transacciones (Transferencia - DEBIN)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    https://sandbox.bind.com.ar/apidoc/#api-Referencias-EstadoTX
    """

    # Completada
    COMPLETED = auto()
    # Pendiente de firma
    PENDING = auto()
    # En curso
    IN_PROGRESS = auto()
    # Desconocido
    UNKNOWN = auto()
    # Con error
    FAILED = auto()
    # Desconocido y no se va a reintentar actualizar
    UNKNOWN_FOREVER = auto()
    # Pendiente de aceptación del comprador (DEBIN)
    AWAITING_CONFIRMATION = auto()
    # Cancelada (DEBIN)
    CANCELED = auto()
    # Expirado (DEBIN)
    EXPIRED = auto()
    # Devolución del monto por contracargo (DEBIN)
    REFUNDED = auto()
    # Rechazo del comprador (DEBIN)
    REJECTED_CLIENT = auto()
    # Rechazo del comprador (SUSCRIPCION DE DEBIN)
    REJECTED = auto()
    # Aceptación del comprador (SUSCRIPCION DE DEBIN)
    ACTIVE = auto()
    # Cancelación del comprador (SUSCRIPCION DE DEBIN)
    INACTIVE = auto()


class TxnOriginTypes(AutoName):
    """
    Origen de la transacción
    ~~~~~~~~~~~~~~~~~~~~~~~~
    https://sandbox.bind.com.ar/apidoc/#api-Referencias-OriginTX
    """

    # Las transferencias emitidas a terceros (default)
    TRANSFERENCIAS_ENVIADAS = auto()
    # Las transferencias recibidas de terceros
    TRANSFERENCIAS_RECIBIDAS = auto()


class TxnConceptTypes(AutoName):
    """
    Tipos de concepto (Transferencia)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    https://sandbox.bind.com.ar/apidoc/#api-Referencias-ConceptoTX
    """

    # Alquiler
    ALQ = auto()
    # Cuota
    CUO = auto()
    # Expensas
    EXP = auto()
    # Factura
    FAC = auto()
    # Préstamo
    PRE = auto()
    # Seguro
    SEG = auto()
    # Honorarios
    HON = auto()
    # Haberes
    HAB = auto()
    # Varios (default)
    VAR = auto()


class CurrencyTypes(AutoName):
    """
    Tipos de monedas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    https://sandbox.bind.com.ar/apidoc/#api-Referencias-Currency
    """

    # Peso argentino
    ARS = auto()
    # Dólar americano
    USD = auto()


# Models

class CreateCvuModel(BaseModel):

    # Identificador numérico único del cliente de la billetera virtual.
    # Máximo 12 dígitos, debe ser un número entero sin decimales.
    client_id: ClientID

    # CUIT asociado a la billetera virtual. Sólo números.
    cuit: CUIT

    # Moneda de la transacción. Por ahora solo se acepta 'ARS'. (*)
    currency: Optional[CurrencyTypes] = CurrencyTypes.ARS

    # Nombre o denominación del cliente de la billetera virtual.
    name: str


class CreateCvuAliasModel(BaseModel):

    # CUIT asociado a la billetera virtual. Sólo números.
    cuit: Optional[CUIT]

    # CVU asociado a la billetera virtual. Sólo números.
    cvu: CVU

    # Nombre o denominación del alias que se asignará.
    label: CVUAlias


class DeleteCvuModel(BaseModel):

    # CUIT asociado a la billetera virtual. Sólo números.
    cuit: Optional[CUIT]

    # CVU asociado a la billetera virtual. Sólo números.
    cvu: CVU


class ReadCvuModel(BaseModel):

    # CUIT/CVU asociado a la billetera virtual. Sólo números.
    value: constr(min_length=11, max_length=22, strip_whitespace=True)


class FetchCvuModel(BaseModel):

    # Fecha de creación (timestamp).
    since: str


# --- helper ---

class OriginDebitModel(BaseModel):

    # CUIT asociado a la billetera virtual. Sólo números.
    cuit: Optional[CUIT]

    # CVU asociado a la billetera virtual. Sólo números.
    cvu: CVU


class ToModel(BaseModel):

    # CVU del destinatario. Sólo números. (*)
    cvu: Optional[CVU]

    # Nombre o denominación del alias del destinatario. (*)
    label: Optional[CVUAlias]

    @validator('label', 'cvu')
    def check_cvu_or_label(cls, v, values):
        if any(values.values()):
            raise ValueError('Must be to define only one: CVU or LABEL')
        return v


class ValueModel(BaseModel):

    # Monto asociado a la transacción.
    amount: float

    # Moneda de la transacción. Por ahora solo se acepta 'ARS'. (*)
    currency: Optional[CurrencyTypes] = CurrencyTypes.ARS


class MakeCvuTxnModel(BaseModel):

    # Identificador unívoco de la transacción definido por el usuario.
    # Máximo 15 caracteres. Si se envía un identificador existente devuelve
    # la información de dicha transacción.
    origin_id: OriginID

    # Datos de la cuenta del cliente de la billetera virtual origen
    origin_debit: OriginDebitModel

    # Destinatario
    to: ToModel

    # Especificaciones de la transacción
    value: ValueModel

    # Descripción de la transacción (Máximo 100 caracteres).
    description: Optional[constr(max_length=100)]

    # Concepto de la transacción.
    concept: TxnConceptTypes = TxnConceptTypes.VAR

    # Lista de emails de los destinatarios para enviar comprobante. En caso
    # de usar esta opción de envío de mail, el remitente será la cuenta
    # de envío de mails del Banco industrial (@bancoindustrial.com.ar).
    emails: Optional[list[EmailStr]]
