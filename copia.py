import sys,re

parrafos = dict()
iParrafos = 0
Tabla = dict()
Tabla['eucli'] = dict();
Tabla['cos'] = dict();

def processParrafo(parrafo):
	global iParrafos
	iParrafos+=1
	#Sacamos los caracteres no alphanumericos
	parrafo = re.sub(r'([^\s\w]|_)+', '', parrafo)
	parrafo = parrafo.lower()
	parrafo = parrafo.split()

	parrafos[iParrafos] = dict()
	for x in parrafo:
		if x in parrafos[iParrafos]:
			parrafos[iParrafos][x] +=1
		else:
			parrafos[iParrafos][x] = 1

	cantidadPalabras = float(sum(parrafos[iParrafos].values()))
	#Normalizamos
	for palabra,cantidad in parrafos[iParrafos].items():
		parrafos[iParrafos][palabra] = (cantidad/cantidadPalabras)
	return

def procesar(archivo):
	textarchivo = ''
	for linea in archivo:
		textarchivo+=linea
	textarchivo = textarchivo.split('\n\n')
	for parrafo in textarchivo:
		processParrafo(parrafo)

	def deucli(h1,h2,dominio):
		d = 0
		for palabra in dominio:
			h=h1[palabra]
			if h2==0:
				hl=0
			else:
				hl=h2[palabra]
			d+=(h-hl)**2
		dist=((d)**0.5)		
		return dist
	def dcos(h1,h2,dominio):
		d = 0
		for palabra in dominio:
			h=h1[palabra]
			hl=h2[palabra]
			d+=(h*hl)
		dist=1-(d)/(deucli(h1,0,h1.keys())*deucli(h2,0,h2.keys()))
		return dist 

	def comparar(i,ultimo):
		last = i
		while i < ultimo:
			i+=1
			aux = dict()
			aux[0] = dict()
			aux[1] = dict()
			# Comparamos
			dominio = set(set(parrafos[i].keys()) | set(parrafos[last].keys()))
			for palabra in dominio:
				if(palabra not in parrafos[last]):
					aux[1][palabra] = 0
				else:
					aux[1][palabra] = parrafos[last][palabra]
				if(palabra not in parrafos[i]):
					aux[0][palabra] = 0
				else:
					aux[0][palabra] = parrafos[i][palabra]	
			Tabla['eucli'][str(last)+'-'+str(i)] = dict()
			Tabla['eucli'][str(last)+'-'+str(i)] = deucli(aux[0],aux[1],dominio)
			Tabla['cos'][str(last)+'-'+str(i)] = abs(round(dcos(aux[0],aux[1],dominio),3))
			# print last,i
		if last != ultimo:
			comparar(last+1,ultimo)
	comparar(1,iParrafos)
	return
def crearTabla():
	# hacer una lista de las llaves, ordenarlas y recorrer esa lista, llamar diccionario dependiendo del index
	tabla=open("tabla.html","w")
	tabla.write('<!DOCTYPE html>\n')
	tabla.write('<html lang="es">\n')
	tabla.write('<head>\n')
	tabla.write('	<meta charset="UTF-8">\n')
	tabla.write('	<title>Tabla de Datos</title>\n')
	tabla.write('<link rel="stylesheet" type="text/css" href="style.css">')
	tabla.write("<link href='https://fonts.googleapis.com/css?family=Open+Sans:400,700' rel='stylesheet' type='text/css'>")
	tabla.write('</head>\n')
	tabla.write('<body>\n')
	tabla.write('<h2>Diferencia Coseno</h2>\n')
	tabla.write('<table>\n<tr>')
	# Creamos Cabecera
	i = 0
	while(i <= iParrafos):
		if(i == 0):
			tabla.write("<th> </th>")
		else:
			tabla.write("<th>"+str(i)+"</th>")
		i+=1
	i = 1
	td = '<td>{0}</td>'
	while(i <= iParrafos):
		i2 = 1
		tabla.write('<tr>')
		tabla.write('<th>'+str(i)+'</th>')
		while(i2 <= iParrafos):
			if(i == i2):
				tabla.write(td.format(0.0))
			elif(i2< i):
				tabla.write(td.format(Tabla['cos'][str(i2)+'-'+str(i)]))
			else:
				tabla.write(td.format(Tabla['cos'][str(i)+'-'+str(i2)]))
			i2+=1
		tabla.write('</tr>')
		i+=1


	tabla.write('	\n')
	tabla.write('</table>\n')


	#Tabla Euclidiana
	tabla.write('<h2>Diferencia Euclidiana</h2>\n')
	tabla.write('<table>\n<tr>')
	# Creamos Cabecera
	i = 0
	while(i <= iParrafos):
		if(i == 0):
			tabla.write("<th> </th>")
		else:
			tabla.write("<th>"+str(i)+"</th>")
		i+=1

	i = 1
	while(i <= iParrafos):
		i2 = 1
		tabla.write('<tr>')
		tabla.write('<th>'+str(i)+'</th>')
		while(i2 <= iParrafos):
			if(i == i2):
				tabla.write(td.format(0.0))
			elif(i2< i):
				tabla.write(td.format(round(Tabla['eucli'][str(i2)+'-'+str(i)],3)))
			else:
				tabla.write(td.format(round(Tabla['eucli'][str(i)+'-'+str(i2)],3)))
			i2+=1
		tabla.write('</tr>')
		i+=1
	tabla.write('	\n')
	tabla.write('</table>\n')

	#Tabla Copia
	tabla.write('<h2>Copia?</h2>\n')
	tabla.write('<table>\n<tr>')
	# Creamos Cabecera
	i = 0
	while(i <= iParrafos):
		if(i == 0):
			tabla.write("<th> </th>")
		else:
			tabla.write("<th>"+str(i)+"</th>")
		i+=1

	i = 1
	while(i <= iParrafos):
		i2 = 1
		tabla.write('<tr>')
		tabla.write('<th>'+str(i)+'</th>')
		while(i2 <= iParrafos):
			if(i == i2):
				distancia = 0
			elif(i2 < i):
				distancia = round(Tabla['cos'][str(i2)+'-'+str(i)],3)
			else:
				distancia = round(Tabla['cos'][str(i)+'-'+str(i2)],3)
			if(distancia < .146):
				#Copia
				tabla.write(td.format('Copia'))
			elif(distancia < .66):
				#Revisar
				tabla.write(td.format('Revisar'))
			else:
				#Pasa
				tabla.write(td.format(''))
			i2+=1
		tabla.write('</tr>')
		i+=1
	tabla.write('	\n')
	tabla.write('</table>\n')

	# Cerramos el archivo
	tabla.write('</body>\n')
	tabla.write('</html>\n')
	tabla.close()
	return


argumentos = sys.argv
if(len(argumentos) > 1):
	fileName = argumentos[1]
else:
	fileName = 'textoprueba.txt'
archivo = open(fileName)

procesar(archivo)
# print Tabla
print 'ARCHIVO '+fileName+' PROCESADO, archivo tabla.html GENERADO'
crearTabla()
