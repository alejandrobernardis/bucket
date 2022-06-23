#!/usr/bin/env sh

# definimos el host
SERVER_CN=localhost
DST_PATH="${PWD}/certs"

# verificamos que exista el directorio de los certificados o lo creamos
[ -d "${DST_PATH}" ] || mkdir -p "${DST_PATH}"

# limpiamos en caso de que existan certificados
rm -f "${DST_PATH}/*"

# generamos los certificados
openssl genrsa -passout pass:frank -des3 \
  -out "${DST_PATH}/ca.key" 4096
openssl req -passin pass:frank -new -x509 -days 3650 \
  -key "${DST_PATH}/ca.key" \
  -out "${DST_PATH}/ca.crt" \
  -subj "/CN=${SERVER_CN}"
openssl genrsa -passout pass:frank -des3 -out \
  "${DST_PATH}/server.key" 4096
openssl req -passin pass:frank -new \
  -key "${DST_PATH}/server.key" \
  -out "${DST_PATH}/server.csr" \
  -subj "/CN=${SERVER_CN}" \
  -config "${PWD}/ssl.cnf"
openssl x509 -req -passin pass:frank -days 3650 \
  -in "${DST_PATH}/server.csr" \
  -CA "${DST_PATH}/ca.crt" \
  -CAkey "${DST_PATH}/ca.key" \
  -set_serial 01 \
  -out "${DST_PATH}/server.crt" \
  -extensions req_ext \
  -extfile "${PWD}/ssl.cnf"
openssl pkcs8 -topk8 -nocrypt -passin pass:frank \
  -in "${DST_PATH}/server.key" \
  -out "${DST_PATH}/server.pem"
chmod 644 ${DST_PATH}/*.pem
