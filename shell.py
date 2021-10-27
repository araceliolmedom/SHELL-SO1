import subprocess
import os

path_defect = "/home/" + os.getlogin()
##################################################################################
##################  Funcion que maneja el flujo del programa  ####################
##################################################################################
def main():
    while(True):
        
        command = input(os.getlogin()+"@"+ os.uname().nodename  + os.getcwd()+ ":"  + "$" )
        command = command.rstrip().lstrip()
        if command =="exit" :
            break
        elif command == "help":
            print("psh: shell py")
        else:
            execute_command(command)
            
##################################################################################
######## Verifica si el comando y llama a la funcion que lo ejecuta ##############
##################################################################################

def execute_command(path):
    if path[:3] == "ir " :
        if path.count(" ") == 2 :
            print("Demasidos parametros")
        elif path[3:] == "--help":
            print("ir [Comando]\nir [--help]\n")

        else:
            aux_path = path[3:]
            command_ir(aux_path)
    elif path == "ir":
        command_ir(path_defect)
    elif path[:7] == "listar":
        command_listar(path)
        
def command_listar(path):
    
    for x in os.listdir(os.getcwd()):
        print(x,end="  ")
    print("\n")
    #for x in os.listdir(aux_path):
        
main()