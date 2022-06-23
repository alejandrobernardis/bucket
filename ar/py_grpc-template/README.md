# py_grpc-template

Template para proyectos con GRPC en Python (full-stack). 

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

# Makefile

Las acciones en el proyecto se pueden gestionar mediante `make`.

```bash
> make help

 Command `py_grpc-template` help -

 + build                Compile service (alias `b`)
 + build-no-cache       Compile service without cache (alias `bnc`)
 + build-compiler       Make compiler (COMPILER_IMAGE)
 + grpc                 Run GRPC server
 + check-deps           List of dependencies
 + proto                Compile all protocols (alias `p`)
 + proto-build-compiler Make compiler first and then compile all protocols
 + clean                Cleans generated files
 + first                Creates compiler and tries to compile the project (start here)
 + dotenv               Creates (dot)env file

```
