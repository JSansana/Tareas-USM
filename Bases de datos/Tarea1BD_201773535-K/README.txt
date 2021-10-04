Nombre: José Sansana Parra
Rol: 201773535-K

*Se ejecuta por consola de manera: TAREA1BD_201773535-K.py

*La idea es ejecutar el programa solo una vez, ya que se crean las tablas y
luego se entra en un ciclo WHILE que corresponde a la aplicación, en la cual
se permanecerá y se podrán hacer todas las operaciones un numero ilimitado de veces
hasta que el usuario escriba SALIR.

	En caso de ejecutarlo por segunda vez hay que ejecutar las siguientes funciones:
	#drop_Sansanito()
	#drop_POYO()
	#drop_respaldo()
	Estas van justo antes del llamado a la funcion crear_POYO() y estan comentadas para 
	que no influyan en las ejecuciones a menos que se desee  lo contrario.

*Al ejecutar el programa la aplicación dará las instrucciones necesarias sobre que presionar
en el teclado para efectuar diversas acciones.

*El archivo CSV debe estar en la misma carpeta que el programa.

*La conexión con la BD es mediante el usuario HR ya que utilizando otro habia
problemas con el trigger.

*En caso de que se solicite ingresar un estado y se quiere que no tenga ninguno simplemente
se deja como: "" (string vacío) o el string None.
Por ejemplo:  "Bulbasaur,70,"
Donde al lado derecho de 70 va el campo correspondiente al estado.

*Se puede modificar la variable "ctope" de insertrandom con valores entre 1 y 50. Esta función llena 
la tabla SansanitoPokemon con la capacidad igual a "ctope" .

PD: Implementé el trigger creando una tabla adicional que funciona de respaldo en el
momento de hacer update. Lo menciono por si resulta extraña la presencia de una
tabla extra al momento de ejecutar el programa.  