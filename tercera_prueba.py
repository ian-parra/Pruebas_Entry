import subprocess
import os
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Instalar las dependencias necesarias para ReBreakCaptcha
subprocess.call(['sudo', '-S', 'pip', 'install', 'pydub', 'SpeechRecognition', 'selenium'], stdin=subprocess.PIPE)

# Clonar el repositorio de ReBreakCaptcha
subprocess.call(['sudo', '-S', 'git', 'clone', 'https://github.com/eastee/rebreakcaptcha.git'], stdin=subprocess.PIPE)

# Cambiar al directorio del script clonado
os.chdir('rebreakcaptcha')

# Abrir el archivo rebreakcaptcha.py en modo de escritura
with open('rebreakcaptcha.py', 'r') as file:
    content = file.read()

# Reemplazar las rutas de Windows por las rutas de Linux
content = content.replace(r'"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"', r'"/usr/bin/firefox"')
content = content.replace(r'"C:\geckodriver.exe"', r'"/usr/bin/geckodriver"')

# Reemplazar la URL con la URL deseada
content = content.replace('RECAPTCHA_PAGE_URL = "https://www.google.com/recaptcha/api2/demo"',
                          'RECAPTCHA_PAGE_URL = "URL_DESEADA"')

# Guardar los cambios en el archivo rebreakcaptcha.py
with open('rebreakcaptcha.py', 'w') as file:
    file.write(content)


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

webdriver_path = "/usr/local/bin/chromedriver"


def automatizar_farmeo(url, cantidad_lugares):
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    data = []  # Lista para almacenar los datos de los lugares

    for _ in range(cantidad_lugares):
        lugar = driver.get_cookie("Queue-it-<ID-DE-FILA>")
        if lugar is not None and len(lugar["value"]) == 36:
            data.append(lugar["value"])

        driver.delete_all_cookies()
        driver.refresh()

    driver.quit()

    guardar_en_excel(data)


def guardar_en_excel(data):
    workbook = Workbook()
    sheet = workbook.active

    # Escribe los encabezados de columna en la primera fila
    sheet.append(["ID de fila"])

    # Escribe los datos en el archivo Excel
    for item in data:
        sheet.append([item])

    file_path = "/home/ianparra/Documentos/data.xlsx"  # Ruta del archivo Excel en tu equipo

    # Guarda el archivo Excel
    workbook.save(file_path)

    print("Datos guardados en el archivo Excel")


# URL y cantidad de lugares a farmear
url = "https://dfentertainment.queue-it.net/?c=dfentertainment&e=ustedsenalemelo2023&cid=es-CL&scv=%7B%22sessionId%22%3A%22741981ba-2aa7-4a59-8382-cbb312fbbdff%22%2C%22timestamp%22%3A%222023-06-04T23%3A23%3A28.1083787Z%22%2C%22checksum%22%3A%22cJaNpPR0t%2B3%2F6VBZpGCLSYvvFcO8tGt7RvgESS3NGsY%3D%22%2C%22sourceIp%22%3A%22190.122.213.227%22%2C%22challengeType%22%3A%22botdetect%22%2C%22version%22%3A6%2C%22customerId%22%3A%22dfentertainment%22%2C%22waitingRoomId%22%3A%22ustedsenalemelo2023%22%7D"
cantidad_lugares = 10

automatizar_farmeo(url, cantidad_lugares)
