import os
import sys
import pdfkit
import numpy as np
import matplotlib.pyplot as plt
from numpy import log as ln
from math import e
import csv


PLOT=True
PLOT=False

SAVE=True
SAVE=False

def addToCSV(*columns: list[float], filename: str) -> None:
    maxColLen: int = 0
    for column in columns:
        if len(column) > maxColLen:
            maxColLen = len(column)

    header: list[str] = ["ΤΑΣΗ (V)", "ΡΕΥΜΑ (mA)", "ΤΑΣΗ (V)", "ΡΕΥΜΑ (mA)"]
    table: list[list[float]] = [[0 for i in range(4)] for j in range(maxColLen)]
    for i in range(maxColLen):
        for j in range(4):
            try:
                table[i][j] = columns[j][i]
            except IndexError:
                continue

    with open(filename, "w") as fh:
        write = csv.writer(fh)

        write.writerow(header)
        write.writerows(table)

def diode(pVolts: list[float], current: list[float], diodeName: str, num: int) -> None:
    dir = os.path.join(os.getcwd(), "graphs")
    if not os.path.exists(dir):
        os.mkdir(dir)
    filename = diodeName.replace(" ", "")

    # I - V Graph
    plt.figure(1)
    plt.plot(pVolts, current)
    plt.title(f"{diodeName}\n Χαρακτηριστική I - V")
    plt.xlabel("V(V)", fontsize=16)
    plt.ylabel("I(A)", fontsize=16)
    if SAVE:
        plt.savefig(f"{dir}/{filename}_I_V.png")

    lnI: list[float] = [ln(i) for i in current]

    min: list[float] = []
    max: list[float] = []
    if num == 1:
        min = [0.507, -7.88] # x, y
        max = [0.618, -5.74] # x, y
    else:
        # WRONG
        # min = [0.0947, -9.737] # x, y
        # max = [0.1552, -8.476] # x, y

        min = [0.15, -8.5] # x, y
        max = [0.175, -7.343] # x, y

    trendX = [i for i in pVolts if(i > min[0] and i < max[0])]
    trendY = [i for i in lnI if(i > min[1] and i < max[1])]

    m, lnIs = np.polyfit(trendX, trendY, 1)

    # Find n 1.9644096969748301 diode 1
    n: float = 1/(m * 0.026)
    Is: float = e**lnIs
    print(f"{n=}")

    print(f"{Is=}")


    # LnI - V Graph
    plt.figure(2)
    plt.plot(pVolts, lnI, "x-")
    # TrendLine
    plt.plot(pVolts, (m*(np.array(pVolts)) + lnIs))
    textLoc: list[float] = [0.557, -8.68]
    if num != 1:
        plt.ylim(-12, -4)
        textLoc = [0.2439, -8.84]

    plt.title(f"{diodeName}\n Ln I - V")
    plt.text(textLoc[0], textLoc[1], f"n = {n:.2f}\nIs = {np.format_float_scientific(np.float32(Is))} A", fontsize=14)
    plt.xlabel("V(V)", fontsize=16)
    plt.ylabel("ln I(A)", fontsize=16)

    if SAVE:
        plt.savefig(f"{dir}/{filename}_lnI_V.png")

    if PLOT:
        plt.show()

if __name__=="__main__":
    if sys.argv[1] == "pdf":
        options = {
            'enable-local-file-access': '',
            'page-size': 'A4',
            'margin-top': '1cm',
            'margin-bottom': '1cm',
            'margin-left': '2cm',
            'margin-right': '2cm'
        }

        pdfkit.from_file("58633.html", "58633.pdf", options=options)
    else:
        # Voltages
        volts: list[float] = [round((0.315 + (0.03)*i), 3) for i in range(15)]; volts.append(0.739)
        volts2: list[float] = [round((0.034 + (0.02)*i), 3) for i in range(22)]

        # Curents
        iDiode: list[float] = [0.01, 0.02, 0.03, 0.05, 0.09, 0.17, 0.29, 0.52, 0.92, 1.67, 3.02, 5.69, 10.93, 21.76, 44.81, 50.54]
        iDiode2: list[float] = [0.01, 0.02, 0.03, 0.06, 0.09, 0.14, 0.21, 0.64, 0.92, 1.30, 1.74, 2.20, 2.68, 3.20, 3.72, 4.25, 6.76, 7.29, 7.77, 8.51, 8.92, 10.22]

        addToCSV(volts, iDiode, volts2, iDiode2, filename="table.csv")

        # Convert Curents to Amps
        iDiode = [(iDiode[i] * (10**-3)) for i in range(len(iDiode))]
        iDiode2 = [(iDiode2[i] * (10**-3)) for i in range(len(iDiode2))]

        diode(volts, iDiode, "Δίοδος Ι", num=1)
        diode(volts2, iDiode2, "Δίοδος ΙΙ", num=2)
