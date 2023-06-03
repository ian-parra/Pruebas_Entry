from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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
url = ""
cantidad_lugares = 10

automatizar_farmeo(url, cantidad_lugares)
