import subprocess
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Instalar las dependencias necesarias para ReBreakCaptcha
subprocess.call(['pip', 'install', 'pydub', 'SpeechRecognition', 'selenium', 'gspread', 'oauth2client'],
                stdin=subprocess.PIPE)

# Clonar el repositorio de ReBreakCaptcha
subprocess.call(['git', 'clone', 'https://github.com/eastee/rebreakcaptcha.git'], stdin=subprocess.PIPE)

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
                          'RECAPTCHA_PAGE_URL = "https://dfentertainment.queue-it.net/?c=dfentertainment&e=tsbcopat&cid=es-CL"')

# Guardar los cambios en el archivo rebreakcaptcha.py
with open('rebreakcaptcha.py', 'w') as file:
    file.write(content)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

webdriver_path = "/usr/local/bin/chromedriver"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

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

    guardar_en_google_sheets(data)


def guardar_en_google_sheets(data):
    sheet_name = "NOMBRE_DE_LA_HOJA"  # Nombre de la hoja de cálculo en Google Sheets
    worksheet = client.open("NOMBRE_DE_LA_PLANILLA").worksheet(sheet_name)  # Abrir la hoja de cálculo

    # Escribe los datos en la hoja de cálculo
    for i, item in enumerate(data):
        worksheet.update_cell(i + 2, 2, item)

    print("Datos guardados en Google Sheets")


# URL y cantidad de lugares a farmear
url = "https://dfentertainment.queue-it.net/?c=dfentertainment&e=rogerwaters&cid=es-CL&q="
cantidad_lugares = 10

automatizar_farmeo(url, cantidad_lugares)
