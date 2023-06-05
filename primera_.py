import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import subprocess

subprocess.call(['sudo', 'pip', 'install', 'pydub', 'SpeechRecognition', 'selenium'])
subprocess.call(['git', 'clone', 'https://github.com/eastee/rebreakcaptcha.git'])

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

    guardar_en_csv(data)


def guardar_en_csv(data):
    file_path = "/home/ianparra/Documentos/data.csv"  # Ruta del archivo CSV en Documentos

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID de fila"])  # Encabezado de la columna

        for item in data:
            writer.writerow([item])


# URL y cantidad de lugares a farmear
url = "https://dfentertainment.queue-it.net/?c=dfentertainment&e=ustedsenalemelo2023&cid=es-CL"
cantidad_lugares = 1


automatizar_farmeo(url, cantidad_lugares)
