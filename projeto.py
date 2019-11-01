import requests as req
import json

def indiceDeCalor(temperatura, umidade):
    temp = converteFahrenheit(float(temperatura))
    umidadePorcentagem = float(umidade)
    indiceCalor = str(((1.1*temp) + (0.047 * umidadePorcentagem)) - 10.3)
    indiceCalor = float(indiceCalor[0:5])
    if(indiceCalor < 80.0):
        return respostaPratica(indiceCalor)
    return respostaPratica(indiceAlarmante(temp,umidadePorcentagem))

def indiceAlarmante(T, RH):
    indiceCalor = -42.379 + 2.04901523*T + 10.14333127*RH - 0.22475541*T*RH - 0.00683783*T*T - 0.05481717*RH*RH + 0.00122874*T*T*RH + 0.00085282*T*RH*RH - 0.00000199*T*T*RH*RH
    if((T >= 80 or T <= 112) and RH <= 13):
        return indiceAlarmante2(T, RH, indiceCalor)
    elif((T >= 80 or T <= 87) and RH > 85):
        return indiceAlarmante3(T, RH, indiceCalor)
    return indiceCalor

def converteFahrenheit(temperatura):
    return (1.8*temperatura) + 32

def converteCelsius(HI):
    return ((HI - 32) / 1.8)

def indiceAlarmante2(T, RH, HI):
    variavel = T - 95
    if(variavel < 0):
        variavel *= -1
    variavel2 = 17 - variavel
    if(variavel2 < 0):
        variavel2 *= -1
    indiceCalor = HI - (3.25 - 0.25 * RH) * ((variavel2/17)**0.5)
    return indiceCalor

def indiceAlarmante3(T, RH, HI):
    indiceCalor = HI + 0.02 * (RH - 85) * (87-T)
    return indiceCalor

def respostaPratica(HI):
    HI = float(str(HI)[0:4])
    HI = converteCelsius(HI)
    if(HI <= 27):
        return ", " + str(HI)[0:4]+ "," + " Normal. Riscos: Nao ha problemas"
    elif(HI > 27 and HI <= 32):
        return ", " + str(HI)[0:4]+ ","+" Requer Cautela. Riscos: Possivel fadiga em casos de exposicoes prolongadas e pratica de atividades fisicas"
    elif(HI > 32 and HI <= 41):
        return ", " + str(HI)[0:4]+ ","+ " Requer Cautela Extrema. Riscos: Possibilidade de caimbras, de esgotamento fisico e insolacao para exposicoes prolongadas e atividades fisicas."
    elif(HI > 41 and HI <= 54):
        return ", " + str(HI)[0:4]+ ","+ " Indica Perigo. Riscos: Caimbras, insolacao, esgotamento fisico. Possibilidade de danos cerebrais (AVC) para exposicoes prolongadas com atividades fisicas."
    elif(HI > 54):
        return ", " + str(HI)[0:4]+ ","+ " Indica Perigo Extremo. Riscos: Insolacao; (AVC) iminente."

# entrada = "S"
# while(entrada != "N"):
#     print('\n')
#     latitude = input (">> Latitude: ").replace(',', '.')
#     longitude = input(">> Longitude: ").replace(',', '.')
    
    
#     user = 'arthurq' 

#     URL = "http://api.geonames.org/findNearByWeatherJSON?lat=%s&lng=%s&username=%s" %(latitude, longitude, user)
#     r = req.get(url = URL)

#     data = r.json()
#     try:
#         temperatura = float(data['weatherObservation']['temperature'])
#         umidade = float(data['weatherObservation']['humidity'])
#         print("Indice de calor" + str(indiceDeCalor(temperatura, umidade)))
#     except:
#         if(data['status']['value'] == 14):
#             print('\nOcorreu um erro. Por favor verifique se as coordenadas estao corretamente formatadas.\n')
#         elif(data['status']['value'] == 15):
#             print('\nNenhuma observacao foi encontrada.\n')
#     entrada = input(">> Deseja continuar o processo? (S/N)")
