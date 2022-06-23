#!/usr/bin/env sh

# definimos el host
SERVER_CN=localhost
DST_PATH="${PWD}/certs"

# verificamos que exista el directorio de los certificados o lo creamos
[ -d "${DST_PATH}" ] || mkdir -p "${DST_PATH}"

# limpiamos en caso de que existan certificados
rm -f "${DST_PATH}/*"

# generamos los certificados
# Step 1: Generate Certificate Authority + Trust Certificate (server-ca.crt)
openssl genrsa -passout pass:frank -des3 \
  -out "${DST_PATH}/server-ca.key" 4096
openssl req -passin pass:frank -new -x509 -days 3650 \
  -key "${DST_PATH}/server-ca.key" \
  -out "${DST_PATH}/server-ca.crt" \
  -subj "/CN=${SERVER_CN}"
# Step 2: Generate the Server Private Key (server.key)
openssl genrsa -passout pass:frank -des3 -out \
  "${DST_PATH}/server.key" 4096
# Step 3: Get a certificate signing request from the CA (server.csr)
openssl req -passin pass:frank -new \
  -key "${DST_PATH}/server.key" \
  -out "${DST_PATH}/server.csr" \
  -subj "/CN=${SERVER_CN}" \
  -config "${PWD}/ssl.cnf"
# Step 4: Sign the certificate with the CA we created (it's called self signing) - server.crt
openssl x509 -req -passin pass:frank -days 3650 \
  -in "${DST_PATH}/server.csr" \
  -CA "${DST_PATH}/server-ca.crt" \
  -CAkey "${DST_PATH}/server-ca.key" \
  -set_serial 01 \
  -out "${DST_PATH}/server.crt" \
  -extensions req_ext \
  -extfile "${PWD}/ssl.cnf"
# Step 5: Convert the server certificate to .pem format (server.pem) - usable by gRPC
openssl pkcs8 -topk8 -nocrypt -passin pass:frank \
  -in "${DST_PATH}/server.key" \
  -out "${DST_PATH}/server.pem"
chmod 644 "${DST_PATH}/server.pem"
