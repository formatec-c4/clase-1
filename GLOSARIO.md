# Glosario Simple

Este glosario acompaña la POC de `Vet Firulais Turnos` y explica, en lenguaje simple, las palabras técnicas que aparecen en el tutorial.

## Términos del laboratorio

### App

Es el programa que queremos usar. En esta clase, la app es el sistema web de turnos online.

### Bridge o Bridged Adapter

Es un modo de red de VirtualBox en el que la máquina virtual se conecta a la red local como si fuera otra computadora más.

### CPU

Es la parte de la computadora que procesa instrucciones. En una VM se le puede asignar una o más CPU virtuales.

### Host

Es la computadora física real donde está instalado VirtualBox y donde se crean las máquinas virtuales.

### Hostname

Es el nombre de una máquina dentro de una red. Sirve para identificarla.

### HTTP

Es el protocolo que usa el navegador para abrir páginas web y comunicarse con servidores.

### Hypervisor o Hipervisor

Es el software que permite crear y administrar máquinas virtuales. En esta práctica, VirtualBox cumple ese rol.

### IP

Es la dirección numérica de un equipo dentro de una red. Sirve para encontrarlo y conectarse a él.

### Máquina virtual o VM

Es una computadora simulada por software. Tiene sistema operativo, red, memoria y disco, aunque en realidad usa recursos de la máquina física.

### NAT

Es un modo de red de VirtualBox en el que la VM puede salir a internet, pero no siempre es fácil entrar a sus servicios desde otra máquina.

### On-premise

Significa que la infraestructura está instalada en un lugar físico propio, por ejemplo dentro de una empresa o institución, y no en la nube.

### Puerto

Es un número que usa una aplicación para escuchar conexiones de red. En esta POC el servidor usa el puerto `8000`.

### Red local

Es la red del lugar donde están conectadas las computadoras, por ejemplo la red de una casa, oficina o aula.

### Repositorio

Es la carpeta del proyecto guardada en GitHub junto con su historial de cambios.

### Servidor

Es el programa o equipo que responde pedidos de otros equipos. En esta guía, el servidor web corre dentro de la VM.

### Sistema operativo

Es el software principal de una computadora. En esta práctica se usa `Ubuntu Server`.

### VirtualBox

Es el programa que usamos para crear y ejecutar máquinas virtuales en la computadora host.

## Comandos que aparecen en la guía

### `git clone`

Descarga una copia del repositorio desde GitHub a la máquina virtual.

### `cd`

Cambia de carpeta en la terminal.

### `make init`

Prepara el entorno del proyecto para poder ejecutarlo.

### `make run`

Inicia la aplicación web para que quede disponible en la red.

### `hostname -I`

Muestra la IP de la máquina virtual para poder abrir la app desde el navegador.

## Idea clave de la clase

La clase busca mostrar que un nuevo servicio puede desplegarse en una VM sin comprar otro servidor físico, aprovechando mejor la infraestructura existente.
