from flask import Flask, send_file

app = Flask(__name__)


@app.route('/data.xlsx')
def get_excel_file():
    file_path = "/home/ianparra/Documentos/data.xlsx"  # Ruta del archivo Excel en tu equipo

    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run()
