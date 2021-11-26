################################Hechos##################################
#Listar
#execute_command
#ir
#renombrar
#pwd
#copiar m
#mover
#creadir
#usuario
#contrasena
#hacer todos los comandos simples y luego los dificiles
#falta el help de algunos comandos
import os
import getpass
import shutil

from typing import AsyncIterable,Tuple
from  colorama import*
import crypt
#from posixpath import split
path_defect = "/home/" + os.getlogin()

'''# Maneja el flujo del programa #'''
def main():
    while(True):
        
        command = (input(Fore.GREEN + os.getlogin()+"@"+ os.uname().nodename  + Fore.BLUE + os.getcwd()+ ":"  + "$ " + Fore.WHITE )).strip()
        if command =="exit" :
            break
        elif command == "help":
            print("psh: shell py")
        else:
            execute_command(command)
            

'''# Verifica si el comando y llama a la funcion que lo ejecuta  #'''

def execute_command(command):

    ## Comando ir ##

    if command[:3] == "ir " :
        if command.count(" ") > 1 :
            print("Demasidos parametros")
        elif command[3:] == "--help":
            print("ir [Directorio]\nir [--help]\n")
            #posible error 
        else:
           command_ir(command[3:])
    elif command == "ir":
        command_ir(path_defect)

    ##Comando listar ##

    elif command[:7] == "listar ":
        if command.count(" ") >1:
            print("listar : Demasiados parametros\nConsulte listar --help")
        elif command[7:] == "--help":
            print("listar : lista los elementos del directorio actual")
        else:
            print("listar : Argumento invalido")
    elif command =="listar":
        command_listar()

    ##Comando renombrar##

    elif command[:10] == "renombrar ":
        if command.count(" ") > 2:
            print("listar : Demasiados parametros\nConsulte listar --help")
        else:
            command_renombrar(command)
    elif command == "renombrar":    
        print("renombrar : faltan argumentos") 
    
    ##Comando copiar ##

    elif command[:7] == "copiar ":
        if command.count(" ") >3:
            print("listar : Demasiados parametros\nConsulte listar --help")
        elif command[7:9] == "-R":
            num = 0
            command_copiar(command,num)
            print("copiar directorio")
        else:
            num = 1
            command_copiar(command,num)
    elif command == "copiar":
        print("copiar : Faltan argumentos")
    
    ##Comando mover ##

    elif command[:6] == "mover " :
        if command.count(" ") >3:
            print("mover : Demasiados parametros\nConsulte listar --help")
        else:
            command_mover(command)
    elif command == "mover":
        print("mover: Faltan argumentos")

    ##Comando pwd ##

    elif command == "pwd":
        command_pwd()

    ##Comando crear_dir ##

    elif command[:9] == "creardir ":
        if command.count(" ") >2:
            print("creardir : Demasiados parametros\nConsulte listar --help")
        else:
            command_creardir(command)
    ## usario ##
    elif command[:8] == "usuario ":
        if command.count(" ") >2:
            print("usuario : Demasiados parametros\nConsulte usuario --help")
        elif command[8:] == "--help":
            print("printear ayuda")
        else:
            command_usuario(command)

    else:
        print("shell : comando no encontrado consulte --help")

def command_listar():
    '''
        #os.listdir : lista los elementos de un registro
        #os.getcwd  : retorna en formato str el directorio de trabajo actual
    '''
    for x in os.listdir(os.getcwd()):
        if os.path.isdir(os.path.join(os.getcwd(),x)):
            print(Fore.BLUE + x ,end="  ")
        else:
            print(Fore.WHITE + x ,end="  ")
    print("\n")

''' # Nos permite acceder a un directorio dada una variable path  #'''

def command_ir(command):
    '''
        #os. chdir : se utiliza para cambiar el directorio de trabajo actual a la ruta especificada.
        #os.path.abspath : obtenemos el path absoluto
        #os.path : nos permite gestionar diferentes opciones relativas al sistema de ficheros .
    '''
    try:
        os.chdir(os.path.abspath(command))
    except Exception:
        print("ir: El fichero o directorio no existe: {}".format(command))

''' # Permite renombrar un archivo o un directorio #'''

def command_renombrar(command):
    '''
        #os.rename : renombra los archivos o carpetas
        #os.path.join : nos permite juntar dos rutas y obtener una absoluta
    '''
    aux_command = command.split()
  
    if os.path.exists(os.path.join(os.getcwd(),aux_command[1])):
        os.rename(aux_command[1],aux_command[2])
    else:
       print("ir: El fichero o directorio no existe: {}".format(aux_command[1]))

''' # Permite renombrar un archivo o un directorio #'''
def command_copiar(command,num):

    #os.path.join : permite juntar dos rutas
    #os.path.isfile : verifica si es un archivo retorna True o False
    #os.path.isdir : verifica si una ruta es una carpeta retorna True o False
    #shutil.copy : copia archivos y mantiene propiedad y permisos

    aux_command = command.split()
    if num:
        #Si existe y es un archivo
        if os.path.isfile(os.path.join(os.getcwd(), aux_command[1])):
        
            if os.path.isdir(os.path.join(os.getcwd(),aux_command[2])) or os.path.isfile(os.path.join(os.getcwd(),aux_command[2])):
                shutil.copy(os.path.join(os.getcwd(),aux_command[1]), os.path.join(os.getcwd(),aux_command[2]))
            else:
                print("copiar: El fichero o directorio no existe: {}".format(os.path.join(os.getcwd(),aux_command[2])))
        else:
            print("copiar: El fichero o directorio no existe: {}".format(os.path.join(os.getcwd(),aux_command[1])))
    else:
        if os.path.isdir(os.path.join(os.getcwd(),aux_command[2])) :
            if os.path.isdir(os.path.join(os.getcwd(),aux_command[3])):
                shutil.copytree(os.path.join(os.getcwd(),aux_command[2]),os.path.join(os.getcwd(),aux_command[3]))
            else:
                print("copiar: El fichero o directorio no existe: {}".format(os.path.join(os.getcwd(),aux_command[3])))
        else:
           print("copiar: El fichero o directorio no existe: {}".format(os.path.join(os.getcwd(),aux_command[2])))

def command_mover(command):
    aux_command = command.split()
    if os.path.exists(os.path.join(os.getcwd(),aux_command[1])) and os.path.exists(os.path.join(os.getcwd(),aux_command[2])):
        shutil.move(os.path.join(os.getcwd(),aux_command[1]),os.path.join(os.getcwd(),aux_command[2]))
    else:
        print("mover: no existe ese directorio o carpeta: {}".format(command[1],command[2]))

def command_pwd():
    print(os.getcwd())

def command_creardir(command):
    aux_command = command.split()
    try:
        os.mkdir(os.path.join(os.getcwd(),aux_command[1]))
    except Exception:
        print("creardir: no se pudo crear el directorio. El directorio ya existe: ")

def is_root():
    #os.getuid no retorna el id del grupo 
    #si os.getuid retorna true estonces  no es usuario root
    print(os.getuid())
    if os.getuid()== 0 :
        return True
    return False
def command_usuario(command):
    ban = True
    if is_root():
        etc_passwd = open("/etc/passwd" ,"r+")
        for linea in etc_passwd:
            aux_linea = linea.split(":")
            usuario = aux_linea[0]
            if int(aux_linea[2]) >=1000 and int(aux_linea[2])<2000:
                uid = aux_linea[2]
                if usuario[0] == command[8:]:
                    print("usuario : El usuario " + command[8:] +"ya exite ")
                    ban = False
                    break
        if ban :
            nuevo_uid = int(uid) + 1

            print("Añadiendo el usuario " + "'" + command[8:]+ "'..../n")
            print("Añadiendo el nuevo grupo " + "'" + command[8:]+ "'..../n")
            print("Añadiendo el nuevo usuario " + "'" + command[8:] + "'" + "(" + str(uid)+ ")" + "con grupo " + command[8:] + "....")
            contrashena  = getpass.getpass("Nueva contraseña : ")
            contrashena2 = getpass.getpass("Vuelva a escribir la nueva contraseña:")
            if contrashena2 != contrashena:
                print("Las contraseñas no coinciden.")
            else:
                print("Introduzca el nuevo valor, o presione INTRO para el predeterminado")
                nombre_completo    = input("          Nombre completo :")
                nro_telefono  = input("         Numero de Telefono :")
                otro = input("         Otro :")
                while(True):
                    horario_trabajo = input("          Horario de Trabajo:")
                    local_host= input("          Local host :")
                    if horario_trabajo !=" " and local_host != " ":
                        break
            etc_group = open("/etc/group" ,"r+")

            for linea in etc_group:
                aux_linea = linea.split(":")
                if int(aux_linea[2]) >=1000 and int(aux_linea[2])<2000:
                    guid = aux_linea[2]
            nuevo_guid = int(guid) + 1
            nuevo_grupo = command[8:] + ":x:" + str(nuevo_guid) + "\n" 
            etc_group.write(nuevo_grupo)
            etc_group.close()

            nuevo_usuario = command[8:] + ":" + str(nuevo_uid) + ":" + str(nuevo_guid) + ":" + nombre_completo  + "," + nro_telefono + "," + otro + "/home/" + command[8:] + "/bin/bash\n"
            etc_passwd.write(nuevo_usuario)
            etc_passwd.close()
            etc_shadow = open("/etc/shadow","a")
            nueva_contrasenha = command[8:] + ":" + crypt.crypt(contrashena2, crypt.mksalt(crypt.METHOD_SHA512)) + ":18944:0:99999:7:::\n"
            etc_shadow.write(nueva_contrasenha)
            etc_shadow.close()
            #os.mkdir("/home/" + command[8:] )
            shutil.copytree("/etc/skel","/home/" + command[8:])
    else:
        print("Sólo root puede añadir un usuario o un grupo al sistema.")
def command_password(command):
    ban = True
    existe = False
    etc_passwd = open("/etc/passwd" ,"r")
    for linea in etc_passwd:
        aux_linea = linea.split(":")
        usuario = aux_linea[0]
        if usuario[0] == command[11:]:
            existe = True
            break
    if existe:
        while(ban):
            password = input("Nueva contraseña : ")
            if not password :
                print("contraseña  : Error la contrasena no puede estar vacia") 
                ban = True
            ban = False
        ban = True
        while(ban):
            new_password = input("Vuelva a ingresar la contraseña : ")
            if not new_password :
                print("contraseña  : Error la contraseña no puede estar vacia")
                ban = True
            elif new_password != password:
                print("contraseña : las contraseña no coinciden  ")
            else: ban = False
        print("contraseña actualizada")
        etc_shadow = open("/etc/shadow","a")
        nueva_contrasenha = command[11:] + ":" + crypt.crypt(new_password, crypt.mksalt(crypt.METHOD_SHA512)) + ":18944:0:99999:7:::\n"
        etc_shadow.write(nueva_contrasenha)
        etc_shadow.close()
    else:
        print("contraseña : no existe el usuario " + command[11:])

main()


