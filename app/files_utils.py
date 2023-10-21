import os

def check_folder_files():
    # Ruta de la carpeta que deseas verificar y crear si no existe
    carpeta = "/files"

    # Verificar si la carpeta existe
    if not os.path.exists(carpeta):
        # Si no existe, crearla
        os.makedirs(carpeta)