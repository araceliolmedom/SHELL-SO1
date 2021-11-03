#Listar
#execute_command
#ir
#renombrar
#pwd
#copiar m
#mover
#creadir
#hacer todos los comandos simples y luego los dificiles
#falta el help de algunos comandos
import os
import shutil
from  colorama import*
#from posixpath import split
path_defect = "/home/" + os.getlogin()

'''# Maneja el flujo del programa #'''
def main():
    while(True):
        
        command = input(Fore.GREEN + os.getlogin()+"@"+ os.uname().nodename  + Fore.BLUE + os.getcwd()+ ":"  + "$ " + Fore.WHITE )
        command = command.strip()
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
            print("ir [Comando]\nir [--help]\n")
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

main()

