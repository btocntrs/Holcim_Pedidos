from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import pytesseract

from functools import reduce
from PIL import Image

from entrada import Entrada

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')

# Inicializa el navegador Firefox con las opciones configuradas
driver = webdriver.Firefox(options=firefox_options)

driver.get("https://www.laseritsconline.com:47449/irj/portal/")
print("Portal cargado con exito")

# Colocamos el nombre de usuario
user_id_field = driver.find_element(By.ID, 'logonuidfield')
user_id_field.send_keys('4312283G')

# Este método guarda el captacha en la carpeta actual
def save_captcha():
    # Localiza el elemento HTML que contiene la imagen por su atributo src
    imagen_element = driver.find_element(By.CSS_SELECTOR, "img[src='/irj/servlet/prt/portal/prtroot/com.sap.portal.runtime.logon.ServletImageToken']")

    #Tomar un escreenshoot del elemento y nombrar el archivo como captcha
    imagen_element.screenshot("captcha.png")

# Esta función descifra el captcha y devuelve el texto correspondiente    
def get_text_captcha(src):
    # Abre la imagen en la que deseas realizar OCR
    imagen = Image.open(src)

    # Realiza OCR en la imagen. Se asegura que todas las letras sean minúsculas y elimina los espacios.
    return pytesseract.image_to_string(imagen).lower().replace(" ", "")

def read_frames():
    # Encuentra todos los elementos <iframe> dentro del frame actual
    frames = driver.find_elements(By.TAG_NAME, "iframe")

    # Itera a través de los frames y obtén sus IDs
    for frame in frames:
        frame_id = frame.get_attribute("id")
        print(f"ID del frame: {frame_id}")

# Intentamos resolver el caprcha en ingresar al portal las veces que sean necesarias
while True:
    # Invocamos a la función que guarda el captcha
    save_captcha()
    
    #Obtenemos el texto del captcha y lo guardamos en la variable texto_captcha
    texto_captcha = get_text_captcha("captcha.png")
    
    # Aquí encontramos el elemento donde va el texto del captcha y enviamos el texto
    captcha_response_field = driver.find_element(By.NAME, "j_captcha_response")
    captcha_response_field.send_keys(texto_captcha)
    
    # Damos clic para intentar pasar a la página siguiente
    utilizar_token_btn = driver.find_element(By.ID, "btnSubmitUtilizarToken")
    utilizar_token_btn.click()    
    
    # Intentamos acceder a los elementos de la página siguiente. Si obtenemos la excepción
    # quiere decir que no pudimos acceder correctamente.
    
    try:
        password_field = driver.find_element(By.ID, "logonpassfield")
        password_field.send_keys("Cardeli001.")

        token_field = driver.find_element(By.ID, "logontoken")
        token_field.send_keys("877060")

        access_btn = driver.find_element(By.NAME, "uidPasswordLogon")
        access_btn.click()
        break
    except NoSuchElementException:
        print("Intento erroneo de captcha.")
        
print("Se ha decifrado el captcha correctamente")

# Vamos al portal donde podemos consultar los pedidos
driver.get("https://www.laseritsconline.com/webdynpro/dispatcher/holcim.com/ha~0_directa~ui~wd_2/ConsultaPedidosPorFact;jsessionid=(srp1_SRP_00)ID1868737550DB617150c66c67aa0ddc91ba9f42703bcf36eaf2c0End")

# Establecemos una espera máxima de 20 seg
wait = WebDriverWait(driver, 20)

# Esperamos hasta que el input del receptor sea clicquueable
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="GFPF.ConsultaPedidosPorFacturarView.inputRFCReceptor"]')))
print("Input de RFC del Receptor esperado exitosamente")

# Aquí buscamos el elemento, enviamos el RFC y luego damos enter.
input_receptor = driver.find_element(By.XPATH, '//*[@id="GFPF.ConsultaPedidosPorFacturarView.inputRFCReceptor"]')
input_receptor.send_keys("CAP821208LQ3")
input_receptor.send_keys(Keys.RETURN)

# Luego damos clic en el botón consultar pedidos
btn_consultar = driver.find_element(By.XPATH, '//*[@id="GFPF.ConsultaPedidosPorFacturarView.ConsultarPedido"]')
btn_consultar.click()

# Esperamos que la tabla se cargue
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="GFPF.ConsultaPedidosPorFacturarView.GrupoListaPedidos"]')))
print("Tabla esperada con existo")

try:
    # Esta línea espera que haya por lo menos una fila de elementos en la tabla
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="GFPF.ConsultaPedidosPorFacturarView.EBELN_0_editor.0"]')))
    print("La tabla no está vacía")
except:
    print("La tabla está vacía")
    driver.quit()

# Si la tabla no está vacía, entonces ordenamos la tabla por fechas
btn_fecha = driver.find_element(By.XPATH, '//*[@id="GFPF.ConsultaPedidosPorFacturarView.FECHA_E_header"]')
btn_fecha.click()

#Esperamos a que la tabla recargue los elementos
wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="GFPF.ConsultaPedidosPorFacturarView.EBELN_0_editor.0"]'), ""))
print("Texto esperado con exito")

# Obtenemos la tabla que tiene los datos
tabla = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/div/div[1]/span/span[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[1]/table')

# Extraemos todas la filas de la tabla para luego trabajar en ellas
filas = tabla.find_elements(By.XPATH, '//tr[@rr]')
filas = filas[2:]

entradas = []

print(f"\nPedido      Fecha       Descripcion         Cantidad    Precio  Importe         Planta              Nota")

for fila in filas:
    celdas = fila.find_elements(By.TAG_NAME, "td")
    
    try:
        pedido = celdas[1].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").text
        fecha = celdas[2].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").text
        descripcion = celdas[5].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").text
        cantidad = celdas[6].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").text
        cantidad = float(cantidad.replace(",",""))
        importe = celdas[8].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").text
        importe = float(importe.replace(",",""))
        planta = celdas[12].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").text
        nota = celdas[15].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").text
        
        entrada = Entrada(pedido, fecha, descripcion, cantidad, importe, planta, nota)
        
        # Dado que por ahora existe una entrada de hielo con un precio incorrecto, por ahora parace ser mejor
        # ignorar esa entrada.
        if entrada.precio != 1.82:
            entradas.append(entrada)
        
        # Aun así la entrada de imprimirá, solo se ignorará de la lista de entradas a tener en cuenta los calculos totales
        print(entrada)

    except NoSuchElementException:
        break

print(f"\nHAY {len(entradas)} EN TOTAL\n")

# Filtramos las entradas correspondientes a la planta Escarcega
planta_escarcega = filter(lambda entrada: 'Esc' in entrada.planta, entradas)
planta_escarcega = list(planta_escarcega)

# Filtramos las entredas que correspondan a Agua para concreto
pipas_escarcega = filter(lambda entrada: 'AGUA' in entrada.descripcion, planta_escarcega)
pipas_escarcega = list(pipas_escarcega)
total_agua_escarcega = reduce(lambda x, entrada: x + entrada.cantidad, pipas_escarcega, 0)

# Filtramops las entredas correspondientes a Hielo para concreto
ollas_escarcega = filter(lambda entrada: 'HIELO' in entrada.descripcion, planta_escarcega)
ollas_escarcega = list(ollas_escarcega)
total_hielo_escarcega = reduce(lambda x, entrada: x + entrada.cantidad, ollas_escarcega, 0)

# Filtramops las entredas correspondientes a pago de Carga y descarga de Hielo para concreto
servicio_escarcega = filter(lambda entrada: 'Servicio' in entrada.descripcion, planta_escarcega)
servicio_escarcega = list(servicio_escarcega)
total_descarga_escarcega = reduce(lambda x, entrada: x + entrada.cantidad, servicio_escarcega, 0)


# Filtramos las entradas correspondientes a la planta Candelaria
planta_candelaria = filter(lambda entrada: 'Cande' in entrada.planta, entradas)
planta_candelaria = list(planta_candelaria)

# Filtramops las entredas correspondientes a Hielo para concreto
ollas_candelaria = filter(lambda entrada: 'HIELO' in entrada.descripcion, planta_candelaria)
ollas_candelaria = list(ollas_candelaria)
total_hielo_candelaria = reduce(lambda x, entrada: x + entrada.cantidad, ollas_candelaria, 0)

# Filtramops las entredas correspondientes a pago de Carga y descarga de Hielo para concreto
servicio_candelaria = filter(lambda entrada: 'Servicio' in entrada.descripcion, planta_candelaria)
servicio_candelaria = list(servicio_candelaria)
total_descarga_candelaria = reduce(lambda x, entrada: x + entrada.cantidad, servicio_candelaria, 0)


# Filtramos las entradas correspondientes a la planta Chetumal
planta_chetumal = filter(lambda entrada: 'Chetu' in entrada.planta, entradas)
planta_chetumal = list(planta_chetumal)

# Filtramops las entredas correspondientes a Hielo para concreto
ollas_chetumal = filter(lambda entrada: 'HIELO' in entrada.descripcion, planta_chetumal)
ollas_chetumal = list(ollas_chetumal)
total_hielo_chetumal = reduce(lambda x, entrada: x + entrada.cantidad, ollas_chetumal, 0)

# Filtramops las entredas correspondientes a pago de Carga y descarga de Hielo para concreto
servicio_chetumal = filter(lambda entrada: 'Servicio' in entrada.descripcion, planta_chetumal)
servicio_chetumal = list(servicio_chetumal)
total_descarga_chetumal = reduce(lambda x, entrada: x + entrada.cantidad, servicio_chetumal, 0)

# Esta variable guardara la suma de todo lo que se pueda facturar
importe_total_plantas = 0.0

# Imprimimos el resumen de la planta Escarcega
if len(planta_escarcega) > 0:
    
    importe_total_escarcega = 0.0
    
    print("HOLCIM ESCARCEGA")
    print(f"Hay {len(planta_escarcega)} entradas")
    
    if len(pipas_escarcega) > 0:
        precio = pipas_escarcega[0].precio
        importe_total = total_agua_escarcega * precio
        importe_total_escarcega += importe_total
        print(f"{total_agua_escarcega} m3 de Agua a $ {precio} = $ {importe_total:,.2f}")
        
    if len(ollas_escarcega) > 0:
        precio = ollas_escarcega[0].precio
        importe_total = total_hielo_escarcega * precio
        importe_total_escarcega += importe_total
        print(f"{total_hielo_escarcega:,.2f} kg de Hielo a $ {precio} = $ {importe_total:,.2f}")
        
    if len(servicio_escarcega) > 0:
        precio = servicio_escarcega[0].precio
        importe_total = total_descarga_escarcega * precio
        importe_total_escarcega += importe_total
        print(f"Servicio de Carga y descarga por {total_descarga_escarcega:,.2f} kg de Hielo a $ {precio} = $ {importe_total:,.2f}")
        
    print(f"TOTAL = $ {importe_total_escarcega:,.2f}")
    importe_total_plantas += importe_total_escarcega
        

# Imprimimos el resumen de la planta Candelaria
if len(planta_candelaria) > 0:
    
    importe_total_candelaria = 0.0
    
    print(f"\nHOLCIM CANDELARIA")
    print(f"Hay {len(planta_candelaria)} entradas")
        
    if len(ollas_candelaria) > 0:
        precio = ollas_candelaria[0].precio
        importe_total = total_hielo_candelaria * precio
        importe_total_candelaria = importe_total
        print(f"{total_hielo_candelaria:,.2f} kg de Hielo a $ {precio} = $ {importe_total:,.2f}")
        
    if len(servicio_candelaria) > 0:
        precio = servicio_candelaria[0].precio
        importe_total = total_descarga_candelaria * precio
        importe_total_candelaria = importe_total
        print(f"Servicio de Carga y descarga por {total_descarga_candelaria:,.2f} kg de Hielo a $ {precio} = $ {importe_total:,.2f}")
        
    print(f"TOTAL = $ {importe_total_candelaria:,.2f}")
    importe_total_plantas += importe_total_candelaria
        
        
# Imprimimos el resumen de la planta Chetumal
if len(planta_chetumal) > 0:
    
    importe_total_chetumal = 0.0
    
    print(f"\nHOLCIM CHETUMAL")
    print(f"Hay {len(planta_chetumal)} entradas")
        
    if len(ollas_chetumal) > 0:
        precio = ollas_chetumal[0].precio
        importe_total = total_hielo_chetumal * precio
        importe_total_chetumal += importe_total
        print(f"{total_hielo_chetumal:,.2f} kg de Hielo a $ {precio} = $ {importe_total:,.2f}")
        
    if len(servicio_chetumal) > 0:
        precio = servicio_chetumal[0].precio
        importe_total = total_descarga_chetumal * precio
        importe_total_chetumal += importe_total
        print(f"Servicio de Carga y descarga por {total_descarga_chetumal:,.2f} kg de Hielo a $ {precio} = $ {importe_total:,.2f}")
        
    print(f"TOTAL = $ {importe_total_chetumal:,.2f}")
    importe_total_plantas += importe_total_chetumal
    
if importe_total_plantas != 0.0:
    print(f"\nIMPORTE TOTAL = $ {importe_total_plantas:,.2f}")

driver.quit()