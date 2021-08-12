TAREA 3 REDES DE COMPUTADORES 2021-1

Álvaro Ortiz Hermosilla
José Sansana Parra


RED ANILLO
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
INSTANCIA 1: Comunicación de cada host entre sí

Comando utilizado para la topología 1  (ejecutar en misma carpeta donde se encuentre dicha topología):

	 sudo mn --custom topologia1.py --topo red --controller remote --switch ovsk --mac

Comando utilizado en pox (dentro de carpeta POX):

	python3 pox.py --verbose openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.l2_learning
	
Cabe destacar que l2_learning es el que viene POR DEFECTO en la carpeta forwarding

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
INSTANCIA 2: Eliminación de link (en este caso entre switch 1 y switch 4)

Comando utilizado para la topología 1_2 (ejecutar en misma carpeta donde se encuentre dicha topología):
	
	sudo mn --custom topologia1_2.py --topo red --controller remote --switch ovsk --mac

Comando utilizado en pox (dentro de carpeta POX):

	python3 pox.py --verbose openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.l2_learning
	
Siendo l2_learning también el archivo por defecto 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
INSTANCIA 3: Reparación de link y ruta antihoraria

Comando utilizado para la topología 1 (ejecutar en misma carpeta donde se encuentre dicha topología):
	
	sudo mn --custom topologia1.py --topo red --controller remote --switch ovsk --mac

Comando utilizado en pox (dentro de carpeta POX):

	python3 pox.py --verbose openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.l2_antihorario
	
Siendo l2_antihorario un archivo learning modificado para el fin antihorario. ESTE DEBE INCLUIRSE EN LA CARPETA FORWARDING DE POX

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

RED DOS CAMINOS

Comando utilizado para la topología 2 (ejecutar en misma carpeta donde se encuentre dicha topología):
	
	sudo mn --custom topologia2.py --topo red2 --controller remote --switch ovsk --mac

Comando utilizado en pox (dentro de carpeta POX):

	python3 pox.py --verbose openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.l2_HTTP

Siendo l2_HTTP un archivo learning modificado para el fin requerido. ESTE DEBE INCLUIRSE EN LA CARPETA FORWARDING DE POX

Comandos consecutivos utilizados para transformar HOST en servidor HTTP :

	h5 python -m SimpleHTTPServer 80 &
	h6 python -m SimpleHTTPServer 80 &

Comando utilizado para hacer wget entre host de partida y servidor de llegada:

	hp wget -O - hll
Donde "hp" es host de partida y "hll" host de llegada

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	