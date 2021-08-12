import requests
import json
import jsonpath
import random
#GRUPO 04 - 2021-1


#SECCIÓN DE RECURSOS
#SE AÑADEN 5 RECURSOS, 3 Cortadoras y 2 Impresoras

#########################################################################################################################################
print("\nAPLICANDO 5 MÉTODOS POST a RECURSOS\n")
urlR = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Add?tipoDeMaquina=Cortadora&url=www.fablab.cl/CORTLASS342"
payload = ""
headers = {}
response = requests.request("POST", urlR, headers=headers, data=payload)
print(response.text)

urlR = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Add?tipoDeMaquina=Cortadora&url=www.fablab.cl/cortadoralaser"
payload = ""
headers = {}
response = requests.request("POST", urlR, headers=headers, data=payload)
print(response.text)

urlR = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Add?tipoDeMaquina=Cortadora&url=www.fablab.cl/cortadoralaser2"
payload = ""
headers = {}
response = requests.request("POST", urlR, headers=headers, data=payload)
print(response.text)

urlR = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Add?tipoDeMaquina=Impresora&url=www.fablab.cl/impresora3D25S"
payload = ""
headers = {}
response = requests.request("POST", urlR, headers=headers, data=payload)
print(response.text)

urlR = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Add?tipoDeMaquina=Impresora&url=www.fablab.cl/impresora3DG32"
payload = ""
headers = {}
response = requests.request("POST", urlR, headers=headers, data=payload)
print(response.text)

#########################################################################################################################################
print("\nAPLICANDO 1 MÉTODOS GET a tabla RECURSOS\n")
#GET recursos de un tipo de maquina, EN ESTE CASO : CORTADORA#
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Cortadora"
response = requests.get(url)
response_json = json.loads(response.text)
print(json.dumps(response_json,indent = 4,sort_keys=True))


#########################################################################################################################################
#Elimina un recurso de Cortadora con DELETE mediante un GET previo para obtener un id de Recurso variable#
print("\nAPLICANDO 1 MÉTODOS DELETE en base a un GET a RECURSOS\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Cortadora"
		#Realiza una request al url de la API entregada
response = requests.get(url)

		#Transforma la respuesta anterior a formato Json
response_json = json.loads(response.text)

		#Obtiene el idReserva de la primer Reserva hecha (extraida para modo de ejemplo)
idRecurso  = response_json[0]["idRecurso"]

		#URL de la API
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Delete?idRecurso=/" + idRecurso
payload={}
headers = {}

		#Realiza un request al url de la API entregada
response = requests.request("DELETE", url, headers=headers, data=payload)


#GET nuevamente sobre Cortadora para verificar eliminación
#########################################################################################################################################
print("\nAPLICANDO 1 MÉTODOS GET sobre Cortadoras de tabla RECURSOS\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Recursos/Cortadora"
		#Realiza una request al url de la API entregada
response = requests.get(url)

		#Transforma la respuesta anterior a formato Json
response_json = json.loads(response.text)

#Muestra por pantalla lo obtenido anteriormente, pero de forma ordenada
print(json.dumps(response_json,indent = 4,sort_keys=True))
#########################################################################################################################################



#SECCIÓN DE MÁQUINAS

#Crear 2 máquinas de tipo Impresora
#########################################################################################################################################
print("\nAPLICANDO 2 MÉTODOS POST - tabla MÁQUINAS\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Maquina/Add?nombre=Kurt&ubicacion=San Joaquin&tipoDeMaquina=Impresora"
payload={}
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)


url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Maquina/Add?nombre=Justiniano&ubicacion=San Joaquin&tipoDeMaquina=Impresora"
payload={}
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

#########################################################################################################################################
#GET todas las maquinas
print("\nAPLICANDO MÉTODO GET - tabla MÁQUINAS\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Maquina/Search"
response = requests.get(url)
response_json = json.loads(response.text)
print(json.dumps(response_json,indent = 4,sort_keys=True))

#########################################################################################################################################



#SECCIÓN DE HABILITADOS

#POST 3 habilitados 3 no habilitados
#######################################################################################################################################
print("\nAPLICANDO 6 MÉTODO POST - tabla HABILITADOS\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Add?idMaker=123&tipoDeMaquina=Cortadora&Habilitado=true"
payload = ""
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Add?idMaker=332&tipoDeMaquina=Impresora&Habilitado=true"
payload = ""
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Add?idMaker=3302&tipoDeMaquina=Impresora&Habilitado=false"
payload = ""
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Add?idMaker=425&tipoDeMaquina=Cortadora&Habilitado=false"
payload = ""
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Add?idMaker=1000&tipoDeMaquina=Cortadora&Habilitado=false"
payload = ""
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Add?idMaker=7892&tipoDeMaquina=Cortadora&Habilitado=true"
payload = ""
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)


#########################################################################################################################################
#GET si es que cierta persona está o no habilitada
print("\nAPLICANDO MÉTODO GET - tabla HABILITADOS - persona si o no habilitada\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Search?idMaker=1&tipoDeMaquina=Cortadora"
response = requests.get(url)
response_json = json.loads(response.text)
print(json.dumps(response_json,indent = 4,sort_keys=True))

#########################################################################################################################################
#GET personas habilitadas en base a un tipo de maquina
print("\nAPLICANDO MÉTODO GET - tabla HABILITADOS - persona si habilitada\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Si?tipoDeMaquina=Cortadora"
response = requests.get(url)
response_json = json.loads(response.text)
print(json.dumps(response_json,indent = 4,sort_keys=True))

#########################################################################################################################################
#GET personas no habilitadas en base a un tipo de maquina
print("\nAPLICANDO MÉTODO GET - tabla HABILITADOS - persona no habilitada\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/No?tipoDeMaquina=Cortadora"
response = requests.get(url)
response_json = json.loads(response.text)
print(json.dumps(response_json,indent = 4,sort_keys=True))
#########################################################################################################################################
#PUT de toda la informacion de una Habilitacion en base a un GET de personas habilitadas
print("\nAPLICANDO MÉTODO PUT - tabla HABILITADOS - actualizar informacion de habilitacion\n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/test/search"
response = requests.get(url)
response_json = json.loads(response.text)
idHabilitacion  = response_json[0]["idHabilitacion"]

url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Update?idHabilitacion="+idHabilitacion+"&idMaker=09&tipoDeMaquina=Impresora&Habilitado=false"
payload={}
headers = {}
response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)

#########################################################################################################################################
#GET personas habilitadas en base a un tipo de maquina
print("\nAPLICANDO MÉTODO GET - tabla HABILITADOS \n")
url = "https://9dyw7qfjd8.execute-api.sa-east-1.amazonaws.com/dev/Habilitacion/Si?tipoDeMaquina=Cortadora"
response = requests.get(url)
response_json = json.loads(response.text)
print(json.dumps(response_json,indent = 4,sort_keys=True))