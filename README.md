# vet-firulais-turnos

Mock simple de turnos online para la `Clinica Veterinaria Firulais`.

## Stack

- Python 3
- `http.server`
- Bootstrap 5 por CDN

## Preparar la VM

Antes de correr la app en Ubuntu Server, instala VirtualBox y descarga la imagen ISO del sistema operativo.

### 1. Descargar VirtualBox

Entra a [VirtualBox](https://www.virtualbox.org/) y abre la opcion de descarga.

![Portada de VirtualBox](./img/virtualbox-home.png)

Selecciona el instalador que corresponda a tu sistema operativo host.

![Descarga de VirtualBox](./img/virtualbox-download.png)

### 2. Descargar Ubuntu Server

Entra a [Ubuntu Server](https://ubuntu.com/download/server) y descarga la version LTS mas reciente.

![Descarga de Ubuntu Server](./img/ubuntu-server-download.png)

### 3. Crear una nueva maquina virtual

Abre VirtualBox y presiona `New` para crear una VM nueva.

![Pantalla principal de VirtualBox](./img/virtualbox-manager.png)

Configura el nombre de la maquina y selecciona la ISO de Ubuntu Server que descargaste.

![Paso 1 de la VM: nombre e ISO](./img/vm-step-1-name-iso.png)

### 4. Configurar usuario de Ubuntu

Completa el usuario, la contrasena y el nombre del host para la instalacion desatendida.

![Paso 2 de la VM: usuario y host](./img/vm-step-2-user.png)

### 5. Configurar hardware

Ajusta memoria RAM y cantidad de CPU segun tu maquina. Para un laboratorio simple, `1024 MB` y `1 CPU` alcanzan, aunque puedes subir esos valores si tienes margen.

![Paso 3 de la VM: hardware](./img/vm-step-3-hardware.png)

### 6. Configurar disco virtual

Crea un disco virtual nuevo. Para este ejercicio alcanza con un disco dinamico de alrededor de `8 GB`, aunque puedes asignar mas espacio si quieres reutilizar la VM.

![Paso 4 de la VM: disco](./img/vm-step-4-disk.png)

### 7. Instalar Ubuntu Server

Finaliza el asistente, inicia la VM y deja que Ubuntu Server termine la instalacion. Cuando termine, ingresa con el usuario que definiste y continua con los pasos de este proyecto.

## Ejecutar

```bash
make init
make run
```

Luego abrir `http://127.0.0.1:8000`.

Por defecto la app escucha en `0.0.0.0:8000`, asi que desde otra maquina en la misma red podes entrar con `http://IP_DE_LA_VM:8000`.

Si necesitas cambiar host o puerto:

```bash
HOST=0.0.0.0 PORT=8080 make run
```

## Ubuntu Server

Prerequisitos minimos:

- `python3`
- `python3-venv`
- `make`

Instalacion tipica:

```bash
sudo apt update
sudo apt install -y python3 make
make init
make run
```

`make init` intenta instalar automaticamente el paquete `pythonX.Y-venv` si falta en la VM. Ese paso requiere permisos de `sudo`.

## Alcance

- Agenda publica de turnos
- Solicitud de turno sin autenticacion
- Reservas en memoria
- UI responsive con colores amigables
