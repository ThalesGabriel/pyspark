import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import csv
from Fila import FilaDePrioridade as fila

def genPriority():

    priority=fila()

    for f in listdir("csv/"):
        df = pd.read_csv("csv/" + f)

        data = ['']*4
        for index, linha in df.iterrows():
            if linha.isnull().values.any() == True:
                continue
            time=linha["timestamp"]
            data[0]= linha["umid_max"]
            data[1]= linha["umid_min"]
            data[2]= linha["temp_max"]
            data[3]= linha["temp_min"]
            priority.inserir(data, time)
    return priority

