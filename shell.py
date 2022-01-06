from    logging import FileHandler,Formatter
import  logging
import  shutil
from    colorama import Fore
from    getpass import getuser
import  os
import  sys
import  subprocess
from    shutil import copyfile,copytree, move, which
import  getpass
import  crypt
import  re
import  datetime
import  readline
ruta  = ["/etc/passwd","/etc/shadow","/etc/group","/etc/skel","/etc/hostname","/etc/hosts"]
log_format = "%(asctime)s %(message)s"

############################################################################
readline.parse_and_bind("tab: complete")
def complete(text, state):
    """
        función llamada por readline para completar el texto escrito
    """
    # Lista de posibilidades
    posibilidades = ["listar", "contrasenha", "ir", "copiar", "mover", "permisos", "propietario", "addusuario"]
     
    # Encontramos las coincidencias
    results = [x for x in posibilidades if x.startswith(text)] + [None]
     
    return results[state]
readline.set_completer(complete)
############################################################################
def log_movimientos(msg):
    LOG_MOVIMIENTOS_FILE = "/var/log/shell/movimientos.log"
    LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s")
    LOG_LEVEL = logging.INFO
    messaging_logger = logging.getLogger("Movimientos")
    messaging_logger.setLevel(LOG_LEVEL)
    messaging_logger_file_handler = FileHandler(LOG_MOVIMIENTOS_FILE)
    messaging_logger_file_handler.setLevel(LOG_LEVEL)
    messaging_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
    messaging_logger.addHandler(messaging_logger_file_handler)
    messaging_logger.info(getuser() + msg)


############################################################################
def log_error(msg):
    #error_ = getuser() + ":"  + msg
  
    LOG_SISTEMA_ERROR_FILE = "/var/log/shell/sistema_error.log"
    LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s")
    LOG_LEVEL = logging.ERROR



    messaging_logger = logging.getLogger("Errores de sistema")
    messaging_logger.setLevel(LOG_LEVEL)
    messaging_logger_file_handler = FileHandler(LOG_SISTEMA_ERROR_FILE)
    messaging_logger_file_handler.setLevel(LOG_LEVEL)
    messaging_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
    messaging_logger.addHandler(messaging_logger_file_handler)
    messaging_logger.error(getuser() + msg)

    
############################################################################
def ir(entrada):
    ruta = entrada[1]
    try:
        os.chdir(os.path.abspath(ruta))  
    except Exception:
        msg = "->ir: El fichero o directorio no existe: {}".format(ruta)
        print(msg)
        log_error(msg)
    else:
        return "->ir : accedio a la ruta " + ruta  
         

############################################################################

def ls(entrada):
    '''
        #os.listdir : lista los elementos de un registro
        #os.getcwd  : retorna en formato str el directorio de trabajo actual
    '''
    actual_path = os.getcwd()
    print("\n")
    for archivo in os.listdir(actual_path):
        if os.path.isdir(os.path.join(actual_path,archivo)):
            print(Fore.BLUE  + archivo ,end="  ")
        else:
            print(Fore.WHITE + archivo ,end="  ")
    print("\n")
    return "->listar: listo los elementos de la ruta " +  actual_path

############################################################################

def salir(entrada):   
 exit()

############################################################################

def renombrar(entrada):
    
    '''
    #os.rename : renombra los archivos o carpetas
    #os.path.join : nos permite juntar dos rutas y obtener una absoluta
    '''
    elem_selec = os.path.join(os.getcwd(),entrada[1])
    elem_modif = os.path.join(os.getcwd(),entrada[2])
  
    if os.path.exists(elem_selec):
        os.rename(elem_selec,elem_modif)
        return "->renombrar : se cambio el nombre de " +  elem_selec + " por " + elem_modif
    
    else:
        msg = "renombrar: El fichero o directorio no existe: {}".format(elem_selec)
        print(msg)
        log_error(msg)

############################################################################

def copiar(entrada):

    #os.path.join : permite juntar dos rutas
    #os.path.isfile : verifica si es un archivo retorna True o False
    #os.path.isdir : verifica si una ruta es una carpeta retorna True o False
    #shutil.copy : copia archivos y mantiene propiedad y permisos

    opcion =  entrada[1]
    if opcion != "-R":
        origen     = os.path.join(os.getcwd(), entrada[1])
        destino    = os.path.join(os.getcwd(), entrada[2])
        #Si existe y es un archivo
        if os.path.isfile(origen):
            shutil.copy(origen, destino)
            msg = "->copiar : se copio el archivo " + origen + " a " + destino
            
            log_movimientos(msg)
        else:
            msg = "copiar: El archivo no existe : " + origen
            print(msg)
            log_error(msg)
    else:
        origen     = os.path.join(os.getcwd(), entrada[2])
        destino    = os.path.join(os.getcwd(), entrada[3])
        if os.path.isdir(origen):
            if os.path.isdir(destino):
                shutil.copytree(origen,destino)
                return "->copiar : se copio el archivo " + origen + " a " + destino
            else:
                msg = "copiar: El  directorio no existe : " + destino 
                print(msg)
                log_error(str(msg))
        else:
           msg = "copiar: El directorio no existe : " + origen
           print(msg)
           log_error(msg)

############################################################################

def mover(entrada):
    origen  = os.path.join(os.getcwd(),entrada[1])
    destino = os.path.join(os.getcwd(),entrada[2])

    if os.path.exists(origen) and os.path.exists(destino):
        shutil.move(origen,destino)
        return "->mover : se movio el archivo " + origen + " a " + destino
    else:
        msg = "mover: no existe ese directorio o carpeta: {}".format(origen,destino)
        print(msg)
        log_error(msg)


############################################################################

def permiso(entrada):
    archivo = entrada[0]
    if len(entrada[1]>3 and len(entrada[1]<3)):print("permisos : Error al cargar los permisos")
    else:
        num = int(entrada[1],8)
        try:
            os.chmod(archivo,num)
        except Exception as er:
            msg = "permisos : Error no se puedo realizar la operacion."
            print(msg)
            log_error(msg)
        else:
            return "->permiso : se modifico el permiso del archivo " + archivo + " a " + num
           
            
############################################################################

def propietario(entrada):
   #root()
    path = os.path.abspath(entrada[1])
    usuario = entrada[2]
    grupo   = entrada[3]   
    if existe_usuario(usuario) :
        if existe_grupo(grupo) :    
            chown_recuersivo(path,usuario)
            return "->propietario : se cambio el duenho del archivo " + path 
        else:
            msg = "propietario : No existe el grupo : {} ".formatformat(grupo)
            print(msg)
            log_error(msg)
    else:
        msg = "propietario : No existe el usuario : {} ".format(usuario)
        print(msg)
        log_error(msg)

############################################################################

def root():
    #es una herramienta que usaremos mas tarde V:
    #args = ['sudo', sys.executable] + sys.argv + [os.environ]
    path  =  os.path.abspath("/bin/propietario.py")

    proc  =  subprocess.call(['sudo',sys.executable ,path])

############################################################################

def is_root():
    #os.getuid no retorna el id del grupo 
    #si os.getuid retorna true estonces  no es usuario root
    if os.getuid()== 0 :return True
    return False

############################################################################

def existe_usuario(usuario):
    lineas  = []
    i = 0
    with open(ruta[0]) as archivo:
        #modificar esta parte
        for linea in archivo:
            lineas.append(linea.strip().split(":"))
        for i in range(len(lineas)):
            if usuario == lineas[i][0]:
                return True
    return False

def existe_grupo(grupo):
    lineas  = []
    i = 0
    with open(ruta[2]) as archivo:
        #modificar esta parte
        for linea in archivo:
            lineas.append(linea.strip().split(":"))
        for i in range(len(lineas)):
            if grupo == lineas[i][0]:
                return True
    return False
def nuevo_uid():

    with open(ruta[0]) as lineas:
        for linea in lineas:
            aux_linea = linea.split(":")
            uid = int(aux_linea[3]) if int(aux_linea[3])>1000 else 1000

    return uid + 1

############################################################################

def add_usuario(entrada):
    usuario  = entrada[1]
    if is_root():
        if existe_usuario(usuario):
            msg = "addusuario : El usuario " + usuario + " ya existe"
            print(msg)
            log_error(msg)
        else:
            print("Añadiendo el usuario "            + "'" + usuario + "'....")
            print("Añadiendo el nuevo grupo "        + "'" + usuario + "'....")
            print("Añadiendo el nuevo usuario "      + "'" + usuario + "'" + "(" 
                    + str(nuevo_uid())+ ")" + "con grupo " + usuario + "....")
            while(True):
                contrashena  = getpass.getpass("Nueva contraseña : ")
                contrashena2 = getpass.getpass("Vuelva a escribir la nueva contraseña:")
                if contrashena == contrashena2: break 
                else:print("Las contrasenhas no coinciden")
            print("Introduzca el nuevo valor, o presione INTRO para el predeterminado")
            nombre              = input("               Nombre completo :")
            nro_tel             = input("               Numero de Telefono :")
            otro                = input("               Otro[] :")
            print("Ingrese su horario de trabajo : ")
            while(True):
                inicio = input("Hora de inicio : ")
                if validar_h_trabajo(inicio):break
                else:print("addusuario : respete el formato")
            while(True):
                inicio = input("Hora de inicio : ")
                if validar_h_trabajo(inicio):break
                else:print("addusuario : respete el formato")
                 
            while(True):
                local_host      = input("          Local host :")
                if local_host != " ": break
                else: print("Error al cargar los datos")
            resp = input("¿Es correcta la información? [S/n]")
            if resp == "S" :
                #name_host(local_host)
                #agg nuevo usuario#
                grupo           =  str(nuevo_uid())
                nameygroup      =  usuario   + ":x:" + grupo   + ":"  + grupo + ":" 
                other           =  nombre    +  ","  + nro_tel + ","  + otro  + "," + ":" 
                home            =  "/home/" + usuario
                interprete      =  ":/bin/bash\n"
                nuevo_usuario   = nameygroup + other + home    + interprete
                with open(ruta[0],"a") as linea: 
                    linea.write(nuevo_usuario)
                #agg nuevo contrasenha#
                cifrado         =  ":" + crypt.crypt(contrashena2,crypt.mksalt(crypt.METHOD_SHA512)) 
                adicionales     =  ":18944:0:99999:7:::\n"
                nueva_contra    = usuario + cifrado + adicionales
                with open(ruta[1], "a") as linea:
                    linea.write(nueva_contra)
                #agg nuevo grupo#
                add_grupo(usuario,grupo)
                shutil.copytree(ruta[3],home)
                chown_recuersivo(home,usuario)

                return "->addusuario : agrego al usuario " + usuario
            else:
                msg = print("addusuario : se cancelo el registro")
    else:
        msg = "addusuario : Sólo root puede añadir un usuario o un grupo al sistema."
        print(msg)
        log_error(msg)

############################################################################

def chown_recuersivo(home,usuario):


    for ruta_relativa,directorios,archivos in os.walk(home):
        ruta_absoluta = os.path.normpath(os.path.abspath(os.path.join(home,ruta_relativa)))
        shutil.chown(ruta_relativa,usuario,usuario)
        for items in directorios:
            ruta_absoluta = os.path.normpath(os.path.abspath(os.path.join(home,items)))
            shutil.chown(ruta_absoluta,usuario,usuario)
        for items in archivos:
            ruta_absoluta = os.path.normpath(os.path.abspath(os.path.join(home,items)))
            shutil.chown(ruta_absoluta,usuario,usuario)


def add_grupo(usuario,grupo):
    if existe_grupo(grupo):
        return False
    else:
        with open(ruta[2],"a") as lineas:
            nuevo_grupo = usuario + ":" + "x" + ":" + grupo + ":\n"
            lineas.write(nuevo_grupo)
        return True

############################################################################

def password(entrada):
    #root(entrada)
    usuario = entrada[1]
    lineas = []
    if existe_usuario(usuario):
        while(True):
            contrashena  = getpass.getpass("Nueva contraseña : ")
            contrashena2 = getpass.getpass("Vuelva a escribir la nueva contraseña:")
            if contrashena == contrashena2: break 
            else:print("Las contrasenhas no coinciden")
        cifrado =  crypt.crypt(contrashena2,crypt.mksalt(crypt.METHOD_SHA512)) 
        with open(ruta[1],"r+") as archivo:
            for linea in archivo:
                lineas.append(linea.strip().split(":"))
            archivo.seek(0)
            for i in range(len(lineas)):
                if usuario == lineas[i][0]:
                    lineas[i][1] = cifrado
                lineas[i] = ":".join(lineas[i])
                archivo.write(lineas[i]+ "\n")
        return "->contrasenha : se cambio la contrasenha del usuario  " + usuario 
    
                
    else:
        msg = "password : El usuario no existe"
        print(msg)
        log_error(msg)

############################################################################
#modificar 
def name_host(host_name):
    lineas   = []
    host     = os.uname().nodename
    with open(ruta[4],"w") as archivo:
        archivo.write(host_name)
    with open(ruta[5],"r+") as archivo:
        for linea in archivo:
            if host in linea:
                linea = linea.rename(host_name,host_name)
        print(lineas)
        
        for i in range(len(lineas)):
            lineas[i] = "\t".join(lineas[i])
            archivo.write[lineas[i] + "\n"]
            
############################################################################
def grep(entrada):
    palabra = entrada[1]
    ruta    = entrada[2]
    with open(ruta,"r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if re.search(palabra, linea):
                print(linea.replace(palabra,Fore.YELLOW + palabra + Fore.WHITE))
    return "->grep : se busco la palabra " + palabra + " en " + ruta

############################################################################
def validar_h_trabajo(hora):
   
    try:
        datetime.datetime.strptime(hora,'%H:%M')
    except Exception :
        print("addusuario: Respete el formato del la hora")
        return False
    else:
        return True
        
############################################################################

def hora_fecha():
    return  datetime.datetime.now()

############################################################################


    

dic_command= {"ir"       :[ir,2]        , "salir":[salir,1],"listar"     :[ls,1],"copiar":[copiar,3],
              "renombrar":[renombrar,3] , "mover":[mover,3],"propietario":[propietario,4],"addusuario":[add_usuario,2],
              "password" :[password,2]  , "grep" :[grep,3] ,"horario"    :[validar_h_trabajo,1]}
def main():
    ##Datos##
    
    while(True):
        existe = False
        entrada = input(Fore.GREEN + getuser() + "@" + os.uname().nodename +
                        Fore.WHITE +  ":"      +  Fore.BLUE + os.getcwd()  +  
                        "$ "       + Fore.WHITE).split()
        
        for cmd in dic_command:
            if cmd == entrada[0]:
                existe = True
                if len(entrada) == 1 and dic_command[entrada[0]][1] == 1:
                    log_movimientos(dic_command[cmd][0](entrada))
                elif len(entrada) == dic_command[entrada[0]][1]:
                    log_movimientos(dic_command[cmd][0](entrada))
                else:
                    msg = cmd + ": Error de argumentos"
                    print(msg)
                    log_error(msg)
        if existe == False:
            msg = "shell : comando no encontrado consulte --help"
            print(msg)
            log_error(msg)
        #else llamar a las otras funciones

main()