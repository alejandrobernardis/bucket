#!/usr/bin/env python

from typing import Optional

from core import config
from pydantic import BaseModel, Field


class BindModel(BaseModel):

    # Nombre de usuario para el servicio de las API del BIND.
    username: str

    # Contraseña de usuario para el servicio de las API del BIND.
    password: str

    # Endpoint para el servicio de las API del BIND.
    endpoint: str

    # Endpoint de autenticación para el servicio de las API del BIND.
    endpoint_auth: str

    # Código de identificación de la entidad.
    bank_id: int

    # Código de identificación de la cuenta (formato: XX-X-XXXX-X).
    # Ésta es la cuenta recaudadora que se vincula a la billetera virtual.
    # Esta cuenta debe haber sido dada de alta previamente como recaudadora
    # para el proveedor de billetera virtual.
    account_id: str

    # Configuración de la TLS
    tls: bool = False

    # Certificado
    tls_crt: Optional[str]

    # Clave
    tls_key: Optional[str]

    # Contraseña
    tls_pss: Optional[str]


class ConfigModel(config.ConfigModel):

    # Banco Industrial (BIND) configuración.
    bind: BindModel
