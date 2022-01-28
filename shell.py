from abc import abstractmethod
from    logging import FileHandler,Formatter, log
import  logging
import  shutil
from signal import SIGSTOP
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
import  subprocess
import  psutil
import ftplib

ruta  = ["/etc/passwd","/etc/shadow","/etc/group","/etc/skel","/etc/hostname","/etc/hosts"]

entra = str()
############################################################################
readline.parse_and_bind("tab: complete")
def complete(text, state):
    """
        función llamada por readline para completar el texto escrito
    """
    # Lista de posibilidades
    posibilidades = ["listar", "password", "ir", "copiar", "mover", "permisos", "propietario", "addusuario", "help",
    "creardir","renombrar", "pwd","grep","levantar", "matar","transferencias", "salir"]
     
    # Encontramos las coincidencias
    results = [x for x in posibilidades if x.startswith(text)] + [None]
     
    return results[state]
readline.set_completer(complete)
############################################################################
def log_usuarios(inicio,fin):
    """
        verfica que el horario de ingreso sea el adecuado y escribe  en el 
        archivo log_usuarios
    """
    try:
        lineas = []
        with open("/var/log/shell/horario_de_trabajo","r") as archivo:
            for linea in archivo:
                lineas.append(linea)
            entrada = lineas[0]
            salida  = lineas[1]
            if entrada == inicio:
                msg1 = " Ingreso en hora establecida "
             
            else:
                msg1 = " Ingreso fuera de la hora establecida "
               
            if salida == fin:
                msg2 = " Salio en hora establecida "
                
            else :
                msg2 = " Salio fuera de la  hora establecida "
            
    except Exception:
        print("problemas al verificar el horario")
    else:
        
        try:
            #Creacion del archivo.log
            LOG_USUARIOS_FILE = "/var/log/shell/usuario_horario.log"
            #Formato del msg
            LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s")
            LOG_LEVEL = logging.INFO
            messaging_logger = logging.getLogger("Registros")
            messaging_logger.setLevel(LOG_LEVEL)
            messaging_logger_file_handler = FileHandler(LOG_USUARIOS_FILE)
            messaging_logger_file_handler.setLevel(LOG_LEVEL)
            messaging_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
            messaging_logger.addHandler(messaging_logger_file_handler)
            messaging_logger.info(getuser() + msg1 + msg2)
        except Exception:
            print("No se pudo crear el arhcivo de logs por favor consulte la guia de instalacion de la shell")
############################################################################
def log_movimientos(msg):
    """
        Escribe en movimientos.log todos los comandos usados por el usuario
    """
    try:
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
    except Exception:
        print("No se pudo crear el arhcivo de logs por favor consulte la guia de instalacion de la shell")


############################################################################
def log_error(msg):
    """
        Escribe en sistema_error.log todos errores producidos
    """
    try:
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
    except Exception:
        print("No se pudo crear el archivo de logs por favor consulte la guia de instalacion de la shell")

def log_transferencias(msg):
    """
        Escribe en transferencias.log todos errores producidos por transferencias ftp
    """
    try:
        LOG_SISTEMA_ERROR_FILE = "/var/log/shell/transferencias.log"
        LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s")
        LOG_LEVEL = logging.ERROR
        messaging_logger = logging.getLogger("Errores de transterencias")
        messaging_logger.setLevel(LOG_LEVEL)
        messaging_logger_file_handler = FileHandler(LOG_SISTEMA_ERROR_FILE)
        messaging_logger_file_handler.setLevel(LOG_LEVEL)
        messaging_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
        messaging_logger.addHandler(messaging_logger_file_handler)
        messaging_logger.error(getuser() + msg)
    except Exception:
        print("No se pudo crear el archivo de logs transferencias por favor consulte la guia de instalacion de la shell")

    
############################################################################
def ir(entrada):
    """
        Permite cambiar de un direcitorio a otro
    """
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
    """
       Termina la ejecucion de la shell
    """
    sale = hora_fecha()
    log_usuarios(entra,sale)
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
    """
        Permite permite copiar un archivo a una carpeta o a otro archivo
    """
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
    """
        Permite permite mover un archivo a una carpeta 
    """
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
    """
        Modifica los permisos sobre un archivo o carpeta
    """
    archivo = entrada[1]
    if len(entrada[2])>3 and len(entrada[2])<3:print("permisos : Error al cargar los permisos")
    else:
        num = int(entrada[2],8)
        try:
            os.chmod(archivo,num)
        except Exception :
            msg = "permisos : Error no se puedo realizar la operacion."
            print(msg)
            log_error(msg)
        else:
            return "->permiso : se modifico el permiso del archivo " + archivo + " a " + str(num)
           
            
############################################################################

def propietario(entrada):
    """
        Cambia el propietario de un archivo como tambien el grupo al cual pertence
    """
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
    """
        Verifica si el usuario es root o tiene los privilegios de root
    """
    #os.getuid no retorna el id del grupo 
    #si os.getuid retorna true estonces  no es usuario root
    if os.getuid()== 0 :return True
    return False

############################################################################

def existe_usuario(usuario):
    """
        Retorna True si el usuario ya existe
        Rerorna False caso contrario
    """
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
    """
        Retorna True si el grupo ya existe
        Rerorna False caso contrario
    """
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
    """
        Obtiene el ultimo UID creado 
        Y rerorna un nuevo UID sumandole la unidad
    """

    with open(ruta[0]) as lineas:
        for linea in lineas:
            aux_linea = linea.split(":")
            uid = int(aux_linea[3]) if int(aux_linea[3])>1000 else 1000

    return uid + 1

############################################################################

def add_usuario(entrada):
    """
        Agrega un nuevo usuario al sistema
        
    """
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
            #validamos contrasenhas
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
                fin = input("Hora de inicio : ")
                if validar_h_trabajo(fin):break
                else:print("addusuario : respete el formato")
               
    
            resp = input("¿Es correcta la información? [S/n]")
            if resp == "S" or "s":
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
    """
       Cambia de forma recursiva el propietario y grupo
    """

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
    """
       Escribe en el archivo /etc/group el nuevo grupo creado
    """
    if existe_grupo(grupo):
        return False
    else:
        with open(ruta[2],"a") as lineas:
            nuevo_grupo = usuario + ":" + "x" + ":" + grupo + ":\n"
            lineas.write(nuevo_grupo)
        return True

############################################################################

def password(entrada):
    """
       Permite cambiar la contrasenha de un usuario 
    """
    usuario = entrada[1]
    if is_root():
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
    else :
        msg = "password : Necesitas ser usuario root"
        print(msg)
        log_error(msg)

############################################################################
#modificar 
def name_host(host_name):
    '''
        No los usamos
    '''
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
    """
       Busca patrones en un archivo 
    """
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
    """
      Valida que el horario de trabajo ingresado por el usuario 
      tenga el formato correcto
    """
    try:
        datetime.datetime.strptime(hora,'%H:%M')
    except Exception :
        print("addusuario: Respete el formato del la hora")
        return False
    else:
        return True
        
############################################################################
def otros_cmd(entrada):
    """
        Ejecuta comandos no implementados 
    """
    try:
        subprocess.run(entrada)
    except Exception:
        msg = "otroscmd : ocurrio un error "
        print(msg)
        log_error(msg)
    else:
        return
############################################################################

def hora_fecha():
    """
      Retorna la hora y fecha actual del sistema
    """
    return  datetime.datetime.now()

############################################################################

    """ 
        Diccionario con todos los comandos implementados
    """
############################################################################
def crearDir(entrada):
    """
        Crea directorios a partir de la entrada proporcionada por el usuario
    """
    ruta = entrada[1]
    try:
        os.mkdir(os.path.abspath(ruta))
    except Exception:
        msg = "creardir : no se pudo crear ruta"
        print(msg)
        log_error(msg)
    else:
        return "->creardir : se creo la ruta : " + ruta

############################################################################
def transFtp(entrada):
    id = 0
    #pedimos los datos necesarios para realizar la conexion
    hostname    = input("Ingrese el nombre del host : ")
    user        = input("Ingrese el nombre del usuario : ")
    passwd      = getpass.getpass()
    #hostname   = dlpuser
    #passwd     = 
    #Conectamos con el servidor ftp
    servidorFtp = ftplib.FTP(hostname,user,passwd)
    #lo configuramos en utf - 8
    servidorFtp.encoding = "utf-8"
    #Ingresamos el nombre del archivo con su extension
    archivo = input("Ingrese el nombre del archivo con su extension")
    opcion  = input("-1 Subir\n-2 Descargar \n-3 Ver")

    try:
        while True:
            if opcion == "1":
                with open(archivo,"rb") as file:
                    #Subimos el archivo 
                    servidorFtp.storbinary(f"STOR {archivo}",file)
                    print("Subida Existosa!!!")
                    
                    #Listamos el contenido del servidor
                    servidorFtp.dir()
                    #mensaje para el log
                    msg = "FTP Subida : " + archivo
                    status = 1 
                    #log_transferencias(msg)
                    #Cerramos conexion
                    servidorFtp.quit()
                    break
            elif opcion == "2":
                with open(archivo,"wb") as file:
                    #descargamos el archivo
                    servidorFtp.retrbinary(f"RETR {archivo}",file.write)
                    print("Descarga Exitosa")
                    servidorFtp.dir()
                    #Mostramos el contenido descargado
                    file = open(archivo,"r")
                    print("El contenido del archivo",file.read())
                    #mensajes para el log
                    msg = "FTP Descargado : " +  archivo
                    status =  1 #exitoso -> 1  #error -> 0
                    #log_transferencias(msg)
                    break
            elif opcion == "3":
                servidorFtp.dir()
                opcion = int(input("-1 Subir/n-2 Descargar /n-3 Ver"))
    except Exception:
        msg = "ftp : Ocurrio un error en la transferencia"
        #log_transferencias(msg)
        print(msg)
############################################################################
def ayudaa(entrada):
    print(" ir  [ruta] \n addusuario [usuario] \n listar [sin parametros] \n copiar [origen,destino] ")
    print(" renombrar [elemento seleccionado,elemento a modificar] \n mover  [origen][destino] \n propietario [ruta,usuario,grupo]")
    print(" salir [sin parametros] \n password [usuario] \n grep [palabra,ruta] \n pwd [sin parametros] ")
    print(" levantar [sin parametros] \n matar [pid] \n transferencias [sin parametros]  \n permisos[]")
    
############################################################################
def levantar(entrada):
    """
        Permite levantar demonios
    """
    try:
        os.fork()
    except Exception:
        msg = "ocurrio un problema al levanta el demonio"
        print(msg)
    else :
        return "->levantar : se levanto un proceso : " + str(os.fork())

def matar(entrada):
    """
        Permite matar Demonios
    """
    _pid = int(entrada[1])
    try:
        for process in psutil.process_iter():
            
            if process.pid == _pid:
                os.kill(_pid,9)
    except Exception:
        msg = "->matar : Ocurrio un error al intentar matar el demonio"
        print(msg)
    else:
       return "matar : Se mato el proceso : " + str(_pid)
def lsprocess(entrada):
    try:
        for process in psutil.process_iter():
            
            if process.pid == _pid:
                os.kill(_pid,9)
    except Exception:
        msg = "->matar : Ocurrio un error al intentar matar el demonio"
        print(msg)
    else:
       return "matar : Se mato el proceso : " + str(_pid)

############################################################################

dic_command= {"ir"       :[ir,2]        , "addusuario":[add_usuario,2] ,"listar"    :[ls,1],"copiar"        :[copiar,3],
              "renombrar":[renombrar,3] , "mover"     :[mover,3],"propietario"      :[propietario,4],"salir":[salir,1],
              "password" :[password,2]  , "grep"      :[grep,3] ,"creardir"         :[crearDir,2]   , "ftp" :[transFtp,1],
              "help"     :[ayudaa,1]    , "matar"     :[matar,2],"levantar"         :[levantar,1], "permisos" :[permiso,3],
              "transferencias":[transFtp,1]}
############################################################################
def main():
    ##Datos##
    entra = hora_fecha() 
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
                    msg = cmd + ": Error de argumentos consulte el comando help"
                    print(msg)
                    log_error(msg)
        if existe == False:
            otros_cmd(entrada)
main()