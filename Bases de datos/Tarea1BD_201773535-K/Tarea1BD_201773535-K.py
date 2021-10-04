import cx_Oracle
import csv
import random
import datetime

conn = cx_Oracle.connect("HR","megadeth3","localhost:1521/orcl")
cur = conn.cursor()

#Función drop_POYO() ejecuta el comando DROP TABLE de SQL y elimina la tabla POYO
#no recibe parámetros ni retorna valores
def drop_POYO():
	cur.execute("DROP TABLE POYO")
	#

#Función crear_POYO() ejecuta el comando CREATE TABLE de SQL y crea la tabla POYO
#con los campos que se deseen
#no recibe parametros ni retorna valores
def crear_POYO():
	cur.execute( "CREATE TABLE POYO (N_POKEDEX NUMBER, NOMBRE VARCHAR(255) PRIMARY KEY, TYPE1 VARCHAR(255), TYPE2 VARCHAR(255), HP_TOTAL NUMBER, LEGENDARY VARCHAR(255) )")
	#

#Función crear_respaldo() ejecuta el comando CREATE TABLE de SQL y crea la tabla respaldo
#utilizada para el TRIGGER 
#no recibe parametros ni retorna valores
def crear_respaldo():
	cur.execute("CREATE TABLE respaldo(ID_P NUMBER,HP_AT NUMBER,ESTADO_P VARCHAR(20),FECHA_H TIMESTAMP,PRIORIDAD_P NUMBER)")
	#

#Función drop_respaldo() ejecuta el comando DROP TABLE de SQL y elimina la tabla
#respaldo
#no recibe parámetros ni retorna valores
def drop_respaldo():
	cur.execute("DROP TABLE respaldo")
	#

#Función CSVPOYO_BD() recorre el csv e introduce toda la información de este
#en la tabla POYO
#no recibe parametros ni retorna valores
def CSVPOYO_BD():
	with open("pokemon.csv", "r") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		next(csv_reader)
		for lines in csv_reader:
			cur.execute("INSERT INTO POYO (N_POKEDEX, NOMBRE, TYPE1, TYPE2, HP_TOTAL, LEGENDARY) VALUES (:1, :2, :3, :4, :5, :6)", (lines[0], lines[1], lines[2], lines[3], lines[5],lines[12]))

#Función crear_Sansanito() ejecuta el comando CREATE TABLE de SQL y crea la tabla
#SansanitoPokemon con los campos que se deseen
#no recibe parametros ni retorna valores
def crear_Sansanito():     
	cur.execute( "CREATE TABLE SansanitoPokemon(ID NUMBER PRIMARY KEY , N_PDEX NUMBER, NAME VARCHAR(255), TYPE_1 VARCHAR(255), TYPE_2 VARCHAR(255), HP_ACTUAL NUMBER, HP_MAX NUMBER, LEGENDARIES VARCHAR(255), ESTADO VARCHAR(255), FECHA_HORA_INGRESO TIMESTAMP, PRIORIDAD NUMBER, FOREIGN KEY(NAME) REFERENCES POYO(NOMBRE))")
	#

#Función drop_Sansanito() ejecuta el comando DROP TABLE de SQL y elimina la tabla
#SansanitoPokemon
#no recibe parametros ni retorna valores
def drop_Sansanito():
	cur.execute("DROP TABLE SansanitoPokemon")
	#

#Función insertrandom(ctope) inserta en la tabla SansanitoPokemon pokemones aleatorios
#desde la tabla POYO hasta un tope
#recibe ctope como parametro, el cual es un entero que funciona de capacidad tope
#no retorna valores
def insertrandom(ctope):
	estados=["Envenenado","Paralizado","Quemado","Dormido","Congelado", None]
	capacidad_usada=0
	ran=0
	leg=0
	idd=1
	cur.execute("SELECT N_POKEDEX, NOMBRE, TYPE1, TYPE2, HP_TOTAL, LEGENDARY FROM POYO")
	result = cur.fetchall()
	lista=random.sample(range(802),801)
	while capacidad_usada < ctope:
		r1=random.randint(0,5)
		r2=random.randint(0,result[lista[ran]][4])
		if "False" in result[lista[ran]][5]:
			if estados[r1]==None:	
				cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",
				(idd,result[lista[ran]][0],result[lista[ran]][1],result[lista[ran]][2],result[lista[ran]][3],r2,result[lista[ran]][4],result[lista[ran]][5], estados[r1] ,datetime.datetime.now(),result[lista[ran]][4] - r2))
				ran+=1
				idd+=1
				capacidad_usada+=1
			else:
				cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",(idd,result[lista[ran]][0],result[lista[ran]][1],result[lista[ran]][2],result[lista[ran]][3],r2,result[lista[ran]][4],result[lista[ran]][5], estados[r1] ,datetime.datetime.now(),result[lista[ran]][4] - r2 + 10))
				ran+=1
				idd+=1
				capacidad_usada+=1

		elif ("True" in result[lista[ran]][5]) and leg < 10 and (capacidad_usada+5<50):
			if estados[r1]==None:
				cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",
				(idd,result[lista[ran]][0],result[lista[ran]][1],result[lista[ran]][2],result[lista[ran]][3],r2,result[lista[ran]][4],result[lista[ran]][5], estados[r1] ,datetime.datetime.now(),result[lista[ran]][4] - r2))
				ran+=1
				idd+=1
				capacidad_usada+=5
				leg+=1
			else:
				cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",
				(idd,result[lista[ran]][0],result[lista[ran]][1],result[lista[ran]][2],result[lista[ran]][3],r2,result[lista[ran]][4],result[lista[ran]][5], estados[r1] ,datetime.datetime.now(),result[lista[ran]][4] - r2 + 10))
				ran+=1
				idd+=1
				capacidad_usada+=5
				leg+=1
		else:
			ran+=1

	print("\nTabla SansanitoPokemon llenada aleatoriamente")
	print("capacidad usada: ", capacidad_usada)
	print("numero de legendarios en SansanitoPokemon: ", leg)

#Función CREATE_Sansanito(crear) crea registros en la tabla SansanitoPokemon con todos los campos 
#Solo algunos se ingresan manualmente, el resto se crean de manera automática
#recibe crear como parametro, el cual es un string de 3 palabras separadas por coma
#no retorna valores
def CREATE_Sansanito(crear):
	capacidad=0
	prioridad=0
	legendarios=[]
	normales=[]
	ress = []	#lista de nombres de pokemon en Sansanito
	lista = crear.strip().split(",")

	cur.execute("SELECT ID FROM  SansanitoPokemon ORDER BY ID DESC")
	result = cur.fetchall()
	idd = result[0][0] + 1		#Nuevo ID a ingresar
	
	cur.execute("SELECT NAME FROM SansanitoPokemon")
	res=cur.fetchall()
	for i in res:
		ress.append(i[0])

	cur.execute("SELECT N_POKEDEX,TYPE1,TYPE2,HP_TOTAL,LEGENDARY FROM POYO WHERE NOMBRE =:1",{"1":lista[0]})
	datos = cur.fetchall()   #Datos automáticos ingresados
	if lista[2]!=None and lista[2]!="" and lista[2]!="None":
		prioridad = datos[0][3] - int(lista[1]) + 10
	else:
		prioridad = datos[0][3] - int(lista[1])

	cur.execute("SELECT * FROM SansanitoPokemon")
	todo = cur.fetchall()
	for tupla in todo:
		if tupla[7]=="True":
			capacidad+=5
			legendarios.append((tupla[10],tupla[0])) 
		else:
			capacidad+=1
			normales.append((tupla[10],tupla[0]))

	legendarios.sort()
	normales.sort()

	if (lista[0] in ress) and ("True" in datos[0][4]):
		print("\nPokemon legendario no ingresado.Se encontraba en la tabla desde antes.\n")

	elif (capacidad+5 > 50) and ("True" in datos[0][4]):
		if prioridad >= legendarios[0][0]:
			cur.execute("DELETE FROM SansanitoPokemon WHERE ID = :1", {"1":legendarios[0][1]})
			cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",(idd,datos[0][0],lista[0],datos[0][1],datos[0][2],int(lista[1]),datos[0][3],datos[0][4],lista[2],datetime.datetime.now(),prioridad))
			capacidad+=1
		else:
			print("\nPokemon no ingresado. No cumplía requisito de prioridad en caso de tabla llena\n")

	elif (capacidad+1 > 50) and ("False" in lista[7]):
		if lista[10] >= normales[0][0]:
			cur.execute("DELETE FROM SansanitoPokemon WHERE ID = :1", {"1":normales[0][1]})
			cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",(idd,datos[0][0],lista[0],datos[0][1],datos[0][2],int(lista[1]),datos[0][3],datos[0][4],lista[2],datetime.datetime.now(),prioridad))
			capacidad+=1
		else:
			print("\nPokemon no ingresado. No cumplía requisito de prioridad en caso de tabla llena\n")

	else:
		cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",(idd,datos[0][0],lista[0],datos[0][1],datos[0][2],int(lista[1]),datos[0][3],datos[0][4],lista[2],datetime.datetime.now(),prioridad))
		capacidad+=1
		print("\n¡Pokemon ingresado!, su ID es: ",idd)

#Función READ_Sansanito(arg_1) lee un registro de la tabla SansanitoPokemon y lo imprime por pantalla
#Se aplica mediante una VISTA 
#recibe arg_1 como parametro, el cual corresponde al ID del registro a leer
#no retorna valores
def READ_Sansanito(arg_1):
	cur.execute("DROP VIEW lectura")
	cur.execute("CREATE VIEW lectura AS SELECT ID, N_PDEX, NAME, TYPE_1, TYPE_2, HP_ACTUAL, HP_MAX, LEGENDARIES, ESTADO, FECHA_HORA_INGRESO, PRIORIDAD FROM SansanitoPokemon ")
	cur.execute("SELECT * FROM lectura WHERE ID = :arg_1 ",{"arg_1":arg_1})
	lect = cur.fetchall()
	for i in lect:
		print (i)

#Función DELETE_Sansanito(arg_2) borra un registro de la tabla SansanitoPokemon
#recibe arg_2 como parametro, el cual corresponde al ID del registro a borrar
#no retorna valores
def DELETE_Sansanito(arg_2):
	cur.execute("SELECT ID FROM SansanitoPokemon")

	result = cur.fetchall()
	ids=[]
	
	for i in result:
		ids.append(i[0])
	
	if int(arg_2) not in ids:
		print("El pokemon que se desea borrar no está en la tabla")
	else:
		cur.execute("SELECT NAME FROM SansanitoPokemon WHERE ID = :arg_2",{"arg_2":int(arg_2)} )
		res =cur.fetchall()	
		cur.execute("DELETE FROM SansanitoPokemon WHERE ID = :arg_2",{"arg_2":int(arg_2)})
		print("Pokemon Borrado de ID:",arg_2, "y nombre:",res[0][0])
	#

#Función UPDATE_Sansanito(idd, actualizar) actualiza un registro de la tabla Sansanito Pokemon
#recibe idd y actualizar como parametros. idd corresponde al id de la fila a actualizar
#actualizar corresponde a los atributos nuevos de ciertos campos. En esta función se implementa el
#TRIGGER justo antes de realizar algun UPDATE, el cual guarda los valores antiguos en una tabla extra
#llamada RESPALDO
#no retorna valores
def UPDATE_Sansanito(idd, actualizar):
	lista = actualizar.strip().split(",")
	hpmax=0
	cur.execute("SELECT HP_MAX FROM SansanitoPokemon WHERE ID = :1", {"1":idd})
	result = cur.fetchall()
	hpmax =int(result[0][0])

	cur.execute("CREATE OR REPLACE trigger informacion BEFORE UPDATE OF HP_ACTUAL, ESTADO, FECHA_HORA_INGRESO, PRIORIDAD ON SansanitoPokemon FOR EACH ROW BEGIN INSERT INTO respaldo(ID_P,HP_AT,ESTADO_P,FECHA_H,PRIORIDAD_P) VALUES (:OLD.ID,:OLD.HP_ACTUAL,:OLD.ESTADO,:OLD.FECHA_HORA_INGRESO,:OLD.PRIORIDAD); END;")


	if lista[1]!=None and lista[1]!="" and lista[1]!= "None":
		cur.execute("UPDATE SansanitoPokemon SET HP_ACTUAL = :H, ESTADO = :E, FECHA_HORA_INGRESO = :F, PRIORIDAD = :P WHERE ID = :I ", {"H":lista[0],"E":lista[1],"F":datetime.datetime.now(),"P":hpmax-int(lista[0]) + 10,"I":idd})
		print("\n Se ha actualizado la fila de ID = ",idd)
	else:
		cur.execute("UPDATE SansanitoPokemon SET HP_ACTUAL = :H, ESTADO = :E, FECHA_HORA_INGRESO = :F, PRIORIDAD = :P WHERE ID = :I ", {"H":lista[0],"E":lista[1],"F":datetime.datetime.now(),"P":hpmax-int(lista[0]) ,"I":idd})
		print("\n Se ha actualizado la fila de ID =",idd)

#Función ingresar_pokemon(ingresar) ingresa pokemones en la tabla SansanitoPokemon
#Solo algunos campos se ingresan manualmente, el resto se crean de manera automática
#recibe ingresar como parametro, el cual es un string de 3 palabras separadas por coma
#no retorna valores
def ingresar_pokemon(ingresar):
	capacidad=0
	prioridad=0
	legendarios=[]
	normales=[]
	ress = []	#lista de nombres de pokemon en Sansanito
	lista = ingresar.strip().split(",")

	cur.execute("SELECT ID FROM  SansanitoPokemon ORDER BY ID DESC")
	result = cur.fetchall()
	idd = result[0][0] + 1		#Nuevo ID a ingresar
	
	cur.execute("SELECT NAME FROM SansanitoPokemon")
	res=cur.fetchall()
	for i in res:
		ress.append(i[0])

	cur.execute("SELECT N_POKEDEX,TYPE1,TYPE2,HP_TOTAL,LEGENDARY FROM POYO WHERE NOMBRE =:1",{"1":lista[0]})
	datos = cur.fetchall()   #Datos automáticos ingresados
	if lista[2]!=None and lista[2]!="" and lista[2]!="None":
		prioridad = datos[0][3] - int(lista[1]) + 10
	else:
		prioridad = datos[0][3] - int(lista[1])

	cur.execute("SELECT * FROM SansanitoPokemon")
	todo = cur.fetchall()
	for tupla in todo:
		if tupla[7]=="True":
			capacidad+=5
			legendarios.append((tupla[10],tupla[0])) 
		else:
			capacidad+=1
			normales.append((tupla[10],tupla[0]))

	legendarios.sort()
	normales.sort()

	if (lista[0] in ress) and ("True" in datos[0][4]):
		print("\nPokemon legendario no ingresado.Se encontraba en la tabla desde antes.\n")

	elif (capacidad+5 > 50) and ("True" in datos[0][4]):
		if prioridad >= legendarios[0][0]:
			cur.execute("DELETE FROM SansanitoPokemon WHERE ID = (:1)", (legendarios[0][1]))
			cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",(idd,datos[0][0],lista[0],datos[0][1],datos[0][2],int(lista[1]),datos[0][3],datos[0][4],lista[2],datetime.datetime.now(),prioridad))
			capacidad+=1
			("\n¡Pokemon ingresado!\n")
		else:
			print("\nPokemon no ingresado. No cumplía requisito de prioridad en caso de tabla llena\n")

	elif (capacidad+1 > 50) and ("False" in lista[7]):
		if lista[10] >= normales[0][0]:
			cur.execute("DELETE FROM SansanitoPokemon WHERE ID = (:1)", (normales[0][1]))
			cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",(idd,datos[0][0],lista[0],datos[0][1],datos[0][2],int(lista[1]),datos[0][3],datos[0][4],lista[2],datetime.datetime.now(),prioridad))
			capacidad+=1
			print("\n ¡Pokemon ingresado!\n")
		else:
			print("\nPokemon no ingresado. No cumplía requisito de prioridad en caso de tabla llena\n")

	else:
		cur.execute("INSERT INTO SansanitoPokemon VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",(idd,datos[0][0],lista[0],datos[0][1],datos[0][2],int(lista[1]),datos[0][3],datos[0][4],lista[2],datetime.datetime.now(),prioridad))
		capacidad+=1
		print("\n¡Pokemon ingresado!, su ID es: ",idd)

#Función mayores10() muestra los 10 pokemon con mayor prioridad mediante el comando
#SELECT ORDER BY DESC de SQL
#no recibe parametros ni retorna valores
def mayores10():
	mayores = []
	cur.execute("SELECT * FROM SansanitoPokemon ORDER BY PRIORIDAD DESC ")
	resultado = cur.fetchall()
	c=0
	while c<10:
		mayores.append(resultado[c][2])
		c+=1
	print("\n")
	print(mayores)

#Función menores10() muestra los 10 pokemon con menor prioridad mediante el comando
#SELECT ORDER BY  ASC de SQL
#no recibe parametros ni retorna valores
def menores10():
	menores = []
	cur.execute("SELECT * FROM SansanitoPokemon ORDER BY PRIORIDAD ASC")
	resultado = cur.fetchall()
	c=0
	while c<10:
		menores.append(resultado[c][2])
		c+=1
	print ("\n")
	print (menores)

#Función EstadoEspecifico(estado) muestra los pokemon con cierto estado mediante
#el comando SELECT de SQL 
#recibe de parametro estado, el cual es un string que representa el estado considerado
#como criterio de orden. No retorna valores
def EstadoEspecifico(estado):
	cur.execute("SELECT NAME FROM SansanitoPokemon WHERE ESTADO = :estado",{"estado":estado})
	resultado = cur.fetchall()
	lista = []
	for i in resultado:
		lista.append(i[0])
	print("\n")
	print(lista)

#Función Legendarios(booleano) muestra los nombres de los pokemon legendarios
#dentro de la tabla SansanitoPokemon mediante SELECT y WHERE
#recibe booleano de parametro, el cual siempre es un "True". No retorna valores
def Legendarios(booleano):
	cur.execute("SELECT NAME FROM SansanitoPokemon WHERE LEGENDARIES = :booleano",{"booleano":booleano})
	resultado = cur.fetchall()
	lista = []
	for i in resultado:
		lista.append(i[0])
	print("\n")
	print(lista)

#Función TiempoIngresado() muestra el pokemon mas antiguo en la tabla
#SansanitoPokemon mediante SELECT - ORDER BY - ASC 
#no recibe parametros ni retorna valores
def TiempoIngresado():
	cur.execute("SELECT ID,NAME FROM SansanitoPokemon ORDER BY FECHA_HORA_INGRESO ASC")
	resultado = cur.fetchall()
	print("\n")
	print(resultado[0])

#Función MasRepetido() muestra el pokemon mas repetido en la 
#tabla SansanitoPokemon basado en una cadena de SELECT
#no recibe parametros ni retorna valores
def MasRepetido():
	cur.execute("SELECT cnt1.NAME FROM (SELECT COUNT(*) as total,NAME FROM SansanitoPokemon GROUP BY NAME) cnt1, (SELECT MAX(total) as maxtotal FROM (SELECT COUNT(*) as total, NAME from SansanitoPokemon GROUP BY NAME)) cnt2 WHERE cnt1.total = cnt2.maxtotal ")
	resultado = cur.fetchall()
	lista = []
	for i in resultado:
		lista.append(i[0])
	print("\n")
	print("Pokemon mas repetido: ", lista[0])

#Función OrdenPrioridad() muestra todos los pokemones ordenados por prioridad,
#esto mediante los comandos SELET, FROM, ORDER BY y DESC
#norecibe parametros ni retorna valores
def OrdenPrioridad():
	cur.execute("SELECT NAME,HP_ACTUAL,HP_MAX,PRIORIDAD FROM SansanitoPokemon ORDER BY PRIORIDAD DESC")
	resultado = cur.fetchall()
	for i in resultado:
		print(i)

#drop_Sansanito()
#drop_POYO()
#drop_respaldo()
crear_POYO()
CSVPOYO_BD()
crear_Sansanito()
crear_respaldo()
insertrandom(47)
conn.commit()

ingresar = True
while ingresar:
	print("\n\nMENU DE OPCIONES\n")
	print("Menú CRUD presionando A \n")
	print("Consultas particulares presionando B\n")
	opcion = input("Ingrese una letra o SALIR :")
	if "SALIR" in opcion:
		ingresar = False
	elif opcion == "A":
		print("Para ejecutar CREATE presione A ")
		print("Para ejecutar READ presione B ")
		print("Para ejecutar DELETE presione C ")
		print("Para ejecutar UPDATE presione D\n ")
		opcion2 = input("Ingrese una letra, SALIR o BACK : ")
		if "SALIR" in opcion2:
			ingresar = False
		elif "BACK" in opcion2:
			print("Volviendo al menú\n")
		elif opcion2 == "A":
			cr = input("Ingrese nombre, vida actual y estado separados por comas: \n(El resto de atributos se crearan automaticamente) ")
			CREATE_Sansanito(cr)
		elif opcion2 == "B":
			idr = input("Ingrese el ID del registro a leer: ")
			READ_Sansanito(idr)
		elif opcion2 == "C":
			idl = input("Ingrese el ID del registro a borrar: ")
			DELETE_Sansanito(idl)
		elif opcion2 == "D":
			idu = input("Ingrese el ID del campo a actualizar: ")
			act = input("Ingrese vida actual y estado separados por comas : \n(Fecha y prioridad se actualizaran automaticamente)")
			UPDATE_Sansanito(idu,act)
	elif opcion == "B":
		print("Para ingresar pokemon presione A")
		print("Para visualizar 10 pokemones con mayor prioridad presione B")
		print("Para visualizar 10 pokemones con menor prioridad presione C")
		print("Para visualizar pokemones con estado específico presione D")
		print("Para visualizar pokemones legendarios presione E")
		print("Para visualizar el pokemon mas antiguo presione F ")
		print("Para visualizar el pokemon mas repetido presione G")
		print("Para ordenar por prioridad presione H")
		opcion3 = input("Ingrese una letra, SALIR o BACK: ")
		if "SALIR" in opcion3:
			ingresar = False
		elif "BACK" in opcion3:
			print("Volviendo al menú\n")
		elif opcion3 == "A":
			ing = input("Ingrese nombre, vida actual y estado separados por comas: \n(El resto de atributos se ingresaran automaticamente) ")
			print("\n")
			ingresar_pokemon(ing)
		elif opcion3 == "B":
			print("\n")
			mayores10()
		elif opcion3 == "C":
			print("\n")
			menores10()
		elif opcion3 == "D":
			est = input("Ingrese estado:")
			print("\n")
			EstadoEspecifico(est)
		elif opcion3 == "E":
			print("\n")
			Legendarios("True")
		elif opcion3 == "F":
			print("\n")
			TiempoIngresado()
		elif opcion3 == "G":
			print("\n")
			MasRepetido()
		elif opcion3 == "H":
			print("\n")
			OrdenPrioridad()
	conn.commit()
cur.close()
conn.commit()
conn.close()
