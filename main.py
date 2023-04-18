from configparser import ConfigParser

from flask import Flask
from flask import jsonify

from openpyxl import load_workbook

config = ConfigParser()
config.read("config.ini")

jadwalPath = config["JadwalSheet"]["FILE_PATH"]
wb = load_workbook(jadwalPath)

app = Flask(__name__)

def jadwal_mapel(data):
    jadwalWb = wb["Jadwal"]
    hariCol = ["B", "C", "D", "E", "F"]
    for hari in hariCol:
        hariData = {
            "hari": jadwalWb[f"{hari}1"].value,
            "jadwal": []
        }

        for i in range(2, 13+1):
            jadwal = jadwalWb[f"{hari}{i}"].value
            if jadwal:
                hariData["jadwal"].append(jadwal)

        data.append(hariData)

def jadwal_piket(data):
    piketWb = wb["Piket"]
    hariCol = ["B", "C", "D", "E", "F"]
    for hari in hariCol:
        hariData = {
            "hari": piketWb[f"{hari}1"].value,
            "jadwal": []
        }

        for i in range(2, 9+1):
            jadwal = piketWb[f"{hari}{i}"].value
            if jadwal:
                hariData["jadwal"].append(jadwal)

        data.append(hariData)

# (/) Home
# @app.route("/")
# def home():
#     return jsonify(message="Hello, World!")

# (/) Home
@app.route("/")
def home():
    # Full data
    jadwalData = []

    # Mapel
    mapelData = []
    jadwal_mapel(mapelData)
    jadwalData.append(mapelData)

    # Piket
    piketData = []
    jadwal_piket(piketData)
    jadwalData.append(piketData)

    return jsonify(jadwalData)

# (/mapel) Mapel
@app.route("/mapel")
def mapel():
    mapelData = []
    jadwal_mapel(mapelData)
    return jsonify(mapelData)

# (/piket) Piket
@app.route("/piket")
def piket():
    piketData = []
    jadwal_piket(piketData)
    return jsonify(piketData)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
