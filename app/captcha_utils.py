from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract

# Este método toma una screenshot del captcha y la guarda
def save_captcha(driver, file_name="files/captcha.png"):
    imagen_element = driver.find_element(By.CSS_SELECTOR, "img[src='/irj/servlet/prt/portal/prtroot/com.sap.portal.runtime.logon.ServletImageToken']")
    imagen_element.screenshot(file_name)
    return Image.open(file_name)

# Obtenemos el texto del captcha con una imagen como argumento
def get_text_captcha_by_imagen(imagen):
    return pytesseract.image_to_string(imagen).lower().replace(" ", "")

# Obtenemos el texto del captcha con un path de la imagen como argumento
def get_text_captcha_by_path(image_path):
    imagen = Image.open(image_path)
    return pytesseract.image_to_string(imagen).lower().replace(" ", "")