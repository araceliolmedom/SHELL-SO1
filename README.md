# Desarrollo de Shell

Desarrollar una Shell para el sistema LFS que registre los movimientos y operaciones de los usuarios.

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **[los requerimientos](http://https://docs.google.com/document/d/1GbbyP_-mYtXvvseUTdt9zYdswfoo7GoXmYU0FxtmyxE/edit "Los requerimientos")** para conocer más sobre el proyecto.


### Pre-requisitos 📋

_Para el correcto funcionamiento de la shell, recomendamos instalar la siguiente libreria_
```
Python 3 -m pip install psutil
```

_Antes de empezar con la instalación es importante crear un log de usuarios del shell, en el directorio /var/log/shell_

```
$touch /var/log/shell/usario_horario.log
$touch /var/log/shell/horario_de_trabajo.log
$touch /var/log/shell/movimientos.log
$touch /var/log/shell/sistema_error.log
$touch /var/log/shell/transferencia.log
```
_Nos aseguramos de que el directorio tenga todos los permisos_
```
$chmod -R 777 /var/log/shell
```

### Instalación 🔧

_Una serie de  paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_


_Mediante el uso de un dispotivo de almacenamiento usb copiamos los archivos del Shell al directorio /_

```
$cp -r /media/usb/Shell_LFS-main/shell.py /
```

_Asumiendo que el dispositivo se encuentra montado en /media/usb
Desde el directorio / ($cd / ) creamos un script de ejecucion del shell_

```
$vi shell.sh
  #!/bin/bash
  python3 shell.py
```

_Ahora solo queda agregar el shell al archivo /etc/profile_
```
$echo "bash /shell.sh" >> /etc/profile
```
_Reiniciamos el sistema_
```
$shutdown -r now
```
_Ahora el shell deberia de cargarse automaticamente y esta listo para utilizar._

## Uso del Shell ⌨️


_El shell se maneja mediante una barra de comandos y posee una lista de funcionalidades que seran descriptas más adelante. Una vez ya instalado el Shell podemos ver una lista rapida de los comandos y su sintaxis ejecutando el comando $help_


### Comandos Basicos 🖇️
```
$help 
```
Nos proporciona una lista rapida de los comandos y sus tipo de parametros.
```
$ir [destino] 
```
Nos permite movernos de directorio del que estamos actualmente a uno especificado en [destino], destino puede ser un path a un directorio en especifico o puede ser el nombre de un directorio dentro del directorio actual.
```
$creardir [directorio]
```
Nos permite crear un directorio con el nombre que especifiquemos en su parametro [directorio] que puede ser un path a una ubicacion especifica o puede ser solo el nombre si es que deseamos que el nuevo directorio se cree en la ubicacion actual.
```
$listar
```
Nos permite ver los archivos o directorios ubicados en el directorio actual
```
$mover [origen]
```
Nos permite cambiar la ubicacion del archivo o directorio especificado en el parametro [origen], al ejecutar el comando este nos requiere especificar el path del directorio de destino, es decir, el lugar al cual vamos a mover nuestro archivo/directorio.
```
$renombrar [archivo]
```
Nos permite cambiar el nombre del archivo o directorio especificado en [archivo], al ejecutar necesitamos especificar cual sera el nuevo nombre del archivo.
```
$copiar [origen]
```
Nos permite copiar el archivo o directorio especificado en [origen] y al ejecutar nos requiere espeficicar el path o directorio de destino de la copia.
```
$permisos [archivo]
```
Nos permite modificar los permisos del archivo o directorio especificado en [archivo], para ello, al ejecutar el comando nos pide especificar que permisos tendra el archivo lo cual escribimos en octal. *(1)
```
$propietario [archivo]
```
Nos permite modificar el propietario del archivo o directorio especificado en [archivo], para ello al ejecutar el comando, nos requiere el UID y GID del usuario quien sera propietario del archivo/directorio. *(2)
```
$password
```
Nos permite cambiar la contraseña del usuario que estamos utilizando, primero nos pide la contraseña actual y luego elegimos la nueva contraseña
```
$addusuario
```
Nos permite crear un nuevo usuario, al ejecutar nos pide el nombre del nuevo usuario, la contraseña de este, su horario de trabajo y sus posibles IPs de conexion. *(3)
```
$pwd
```
_Nos permite conocer el directorio actual en el que estamos ubicados._
```
$grep 
```
_Imprime las líneas que contengan coincidencias_
```
$levantar [ejecutable]
```
Nos permite agregar un demonio, que sera un [ejecutable] ubicado en el directorio actual.
```
$matar [ejecutable]
```
Nos permite terminar el proceso ejecutado como demonio por [ejecutable].
```
$transferencia [address]
```
Nos permite realizar una transferencia ftp a la direccion especificada en [address]
```
$salir
```
Cierra el shell y actualiza los logs. Volvemos a utilizar el bash.

## Construido con 🛠️

_Herramientas utilizadas para crear el proyecto_

* Pyhton 3
* VSCode
* GitHub

## Versionado 📌

Usamos GitHub para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/araceliolmedom/SHELL-SO1.git).

## Autores ✒️

_Todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

* **Ramon Araujo** 
* **Araceli Olmedo**

## Expresiones de Gratitud 🎁

* Al profesor Felipe Stuardo
* A los ayudantes de catedra José y Cristobal 

