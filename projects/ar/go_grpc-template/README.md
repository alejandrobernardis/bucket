# go_grpc-template

Template para proyectos con GRPC en GO (full-stack).

## First Steps

Lo primero que se debe hacer es:

```bash
> make first
```

> Crea el compilador y trata de compilar la base del proyecto.

Para iniciar el servicio...

```bash
> make grpc
```

> Port: 50051

... en caso de necesitar inicializar el gateway 

```bash
> make gateway
```

> Port: 8080

# Makefile

Las acciones en el proyecto se pueden gestionar mediante `make`.

```bash
> make help

 Project `go_grpc-template` help -

 + build                Compile service (alias `b`)
 + build-no-cache       Compile service without cache (alias `bnc`)
 + build-minimal        Compile service with minimal approach
 + build-compiler       Make compiler (COMPILER_IMAGE)
 + proto                Compile all protocols (alias `p`)
 + proto-build-compiler Make compiler first and then compile all protocols
 + grpc                 Run GRPC server
 + grpc-help            Run GRPC server help
 + gateway              Run GATEWAY server
 + tidy                 Add missing and remove unused modules
 + vendor               Make vendored copy of dependencies
 + tidy-vendor          Add the missing modules and remove the unused ones, then make a copy of the dependencies
 + certs                Creates SSL certificates
 + clean                Cleans go and generated files
 + first                Creates compiler and tries to compile the project (start here)
 + dotenv               Creates (dot)env file

```

# Server

Argumentos que acepta el servidor:

```bash
> docker run --rm -ti go_grpc-template:local server -help
```
