import numpy as np
import matplotlib.pyplot as plt
from numpy import log as ln
from math import e
import csv


DEBUG=True
# DEBUG=False

def addToCSV(*columns: list[float], filename: str) -> None:
    header: list[str] = ["ΤΑΣΗ (V)", "ΡΕΥΜΑ (mA)", "ΤΑΣΗ (V)", "ΡΕΥΜΑ (mA)"]
    table: list[list[float]] = [[0 for i in range(4)] for j in range(16)]
    print(table)
    for i in range(16):
        for j in range(4):
            table[i][j] = columns[j][i]

    with open(filename, "w") as fh:
        write = csv.writer(fh)

        write.writerow(header)
        write.writerows(table)

# Voltages
volts: list[float] = [round((0.315 + (0.03)*i), 3) for i in range(15)]; volts.append(0.739)
volts2: list[float] = [round((0.034 + (0.02)*i), 3) for i in range(22)]

# Curents
iDiode: list[float] = [0.01, 0.02, 0.03, 0.05, 0.09, 0.17, 0.29, 0.52, 0.92, 1.67, 3.02, 5.69, 10.93, 21.76, 44.81, 50.54]
iDiode2: list[float] = [0.01, 0.02, 0.03, 0.06, 0.09, 0.14, 0.21, 0.64, 0.92, 1.30, 1.74, 2.20, 2.68, 3.20, 3.72, 4.25, 6.76, 7.29, 7.77, 8.51, 8.92, 10.22]

# addToCSV(volts, iDiode, volts, iDiode, filename="test.csv")

# Convert Curents to Amps
iDiode = [(iDiode[i] * (10**-3)) for i in range(len(iDiode))]
iDiode2 = [(iDiode2[i] * (10**-3)) for i in range(len(iDiode2))]

def diode(pVolts: list[float], current: list[float], diodeName: str, num: int) -> None:

    # I - V Graph
    plt.figure(1)
    plt.plot(pVolts, current)
    plt.title(f"{diodeName}\n Χαρακτηριστική I - V")
    plt.xlabel("V(V)", fontsize=16)
    plt.ylabel("I(A)", fontsize=16)

    lnI: list[float] = [ln(i) for i in current]

    min: list[float] = []
    max: list[float] = []
    if num == 1:
        min = [0.507, -7.88] # x, y
        max = [0.618, -5.74] # x, y
    else:
        # min = [0.0947, -9.737] # x, y
        # max = [0.1552, -8.476] # x, y

        min = [0.1552, -8.476] # x, y
        max = [0.174, -7.363] # x, y

    trendX = [i for i in pVolts if(i > min[0] and i < max[0])]
    trendY = [i for i in lnI if(i > min[1] and i < max[1])]
    print(len(trendX))
    print(len(trendY))

    m, lnIs = np.polyfit(trendX, trendY, 1)

    # Find n 1.9644096969748301 diode 1
    n: float = 1/(m * 0.026)
    print(f"{n=}")

    print(f"Is={e**lnIs}")


    # LnI - V Graph
    plt.figure(2)
    plt.plot(pVolts, lnI, "x-")
    # TrendLine
    plt.plot(pVolts, (m*(np.array(pVolts)) + lnIs))
    plt.title(f"{diodeName}\n Ln I - V")
    plt.xlabel("V(V)", fontsize=16)
    plt.ylabel("ln I(A)", fontsize=16)

    if DEBUG:
        plt.show()

# diode(volts, iDiode, "diode1", num=1)
diode(volts2, iDiode2, "diode 2", num=2)
