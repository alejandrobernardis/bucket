#!/usr/bin/env bash

# help
function help() {
  cat <<EOF

≋ Welcome to frank deployment tool.

 $: deploy [OPTIONS] <services>
    (ex): deploy -r 1 -D ms_platform-service-name

 [OPTIONS]
  
  [NO-*]:
    --no-build, -B           NO compilar la imagen.
    --no-clone, -C           NO clonar o actulizar el repo.
    --no-configmap, -M       NO crear el configmap.
    --no-debug, -X           NO depurar el proceso.
    --no-deploy, -D          NO deployar.
    --no-push, -P            NO pushear la imagen.
    --no-tag, -T             NO taguear la imagen.
  
  [ONLY-*]:
    --artifacts, -a          Solo crear los artefactos.
    --build, -b              Solo compilar las imágenes.
    --clone, -c              Solo clonar los repositorios.
    --deploy, -d             Solo deployar los artefactos.
    --push, -s               Solo pushear las imágenes.
  
  [DEPLOY]:
    --debug, -x              Depurar el proceso.
    --network, -n string     Nombre de la red (default: services).
    --ports, -p string       Puerto a publicar (default: 50051).
                               - ex: XXX:XXX, XXX
    --prune, -q              Remueve todo los artefactos antes de desplegar.
    --replica, -r integer    Número de replicas (default: 3).
    --global, -g             Servicio en modo global (default, no global)

  <SERVICES>
    ms_platform-*            Microservicio
    gw_platform-*            Gateway
    jb_platform-*            job
    sr_platform-*            Servicio

EOF
  exit 1
}
