import openpyxl
import os

def generar_reporte(lista):
    # Crea un nuevo archivo de Excel
    work_book = openpyxl.Workbook()

    # Selecciona la hoja activa (por defecto, es la primera hoja)
    sheet = work_book.active
    
    # Número de filas
    numero_fila = 2

    # Estos son los encabezados
    sheet["A1"] = "Pedido"
    sheet["B1"] = "Fecha Entrada"
    sheet["C1"] = "Descripcion"
    sheet["D1"] = "Cantidad"
    sheet["E1"] = "Precio"
    sheet["F1"] = "Importe"
    sheet["G1"] = "Planta"
    sheet["H1"] = "Nota"
    
    # Estos son los datos
    for entrada in lista:
        sheet[f"A{numero_fila}"] = entrada.pedido
        sheet[f"B{numero_fila}"] = entrada.fecha
        sheet[f"C{numero_fila}"] = entrada.descripcion
        sheet[f"D{numero_fila}"] = entrada.cantidad
        sheet[f"E{numero_fila}"] = entrada.precio
        sheet[f"F{numero_fila}"] = entrada.importe
        sheet[f"G{numero_fila}"] = entrada.planta
        sheet[f"H{numero_fila}"] = entrada.nota
        
        numero_fila += 1
        
    # Ajustamos el tamaño de la columna  
    sheet.column_dimensions['A'].width = len(sheet["A2"].value) + 2
    sheet.column_dimensions['B'].width = len(sheet["B2"].value) + 3
    sheet.column_dimensions['C'].width = len(sheet["C2"].value) + 2
    sheet.column_dimensions['D'].width = len(str(sheet["D2"].value)) + 2
    sheet.column_dimensions['E'].width = len(str(sheet["E2"].value)) + 4
    sheet.column_dimensions['F'].width = len(str(sheet["F2"].value)) + 4
    sheet.column_dimensions['G'].width = len(sheet["G2"].value) + 2
    sheet.column_dimensions['H'].width = len(sheet["H2"].value) + 3
        
    # Guardamos el libro de excell
    work_book.save("mi_tabla.xlsx")

    # Cerramos el libro
    work_book.close()
    
    # Utiliza el comando 'start' en Windows para abrir el archivo con el programa predeterminado
    if os.name == 'nt':  # Verifica si el sistema operativo es Windows
        os.system('start excel "mi_tabla.xlsx"')
    else:
        # Para otros sistemas operativos (como macOS y Linux), utiliza el comando 'open'
        os.system(f'open -a "Microsoft Excel" "mi_tabla.xlsx"')
    
    