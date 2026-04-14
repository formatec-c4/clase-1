# vet-firulais-turnos

Mock simple de turnos online para la `Clinica Veterinaria Firulais`.

## Stack

- Python 3
- `http.server`
- Bootstrap 5 por CDN

## Ejecutar

```bash
make init
make run
```

Luego abrir `http://127.0.0.1:8000`.

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
