#!/usr/bin/env python
import OpenSSL
import datetime
import os
import ssl
import urllib2

def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])
cls()

YELLOW = '\033[93m'
RED1 = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
OTRO = '\033[36m'
BOLD = '\033[1m'
ENDC = '\033[0m'

logo = YELLOW + '''
		                                                      ,--,    
		                                                   ,---.'|    
	,-.----.                              .--.--.    .--.--.   |   | :    
	\    /  \                            /  /    '. /  /    '. :   : |    
	;   :    \          ,--,      ,---, |  :  /`. /|  :  /`. / |   ' :    
	|   | .\ :        ,'_ /|  ,-+-. /  |;  |  |--` ;  |  |--`  ;   ; '    
	.   : |: |   .--. |  | : ,--.'|'   ||  :  ;_   |  :  ;_    '   | |__  
	|   |  \ : ,'_ /| :  . ||   |  ,"' | \  \    `. \  \    `. |   | :.'| 
	|   : .  / |  ' | |  . .|   | /  | |  `----.   \ `----.   \'   :    ; 
	;   | |  \ |  | ' |  | ||   | |  | |  __ \  \  | __ \  \  ||   |  ./  
	|   | ;\  \:  | : ;  ; ||   | |  |/  /  /`--'  //  /`--'  /;   : ;    
	:   ' | \.''  :  `--'   \   | |--'  '--'.     /'--'.     / |   ,/     
	:   : :-'  :  ,      .-./   |/        `--'---'   `--'---'  '---'      
	|   |.'     `--`----'   '---'                                         
	`---'  
	By @s1kr10s
	                                                  
''' + ENDC
print logo

fecha_hoy = datetime.datetime.utcnow() # fecha actual

#LEEMOS EL ARCHIVO DE LISTA DE SITIOS WEB
archi_web = open('lista/lista_web.txt', 'r')
linea = archi_web.readline()
while linea != "":
    if '' == linea:
      continue
    
    check_info = []
    cert_info = ''

    host0 = linea.split()
    host = host0[0]
    port = int(443)
    connect_protocol = 'TLSv1'

    #COMPROBAMOS LA VERSION
    if 'TLSv1' == connect_protocol:
        proto = ssl.PROTOCOL_TLSv1
    if 'SSLv3' == connect_protocol:
        proto = ssl.PROTOCOL_SSLv3

    #OBTENEMOS EL CERTIFICADO
    try:
        print  BOLD + "	SITIO " + ENDC + YELLOW + "-> " + ENDC + BOLD + "(https) " + ENDC + YELLOW + "-> " + ENDC + BLUE + host + ":" + ENDC + GREEN + str(port) + ENDC
        cert_info = ssl.get_server_certificate((host, port), proto)
    except Exception, e:
        print RED1 + "	Restableciendo conexion..." + ENDC
        continue
    
    #DESENCRIPTA ELCERTIFICADO
    cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_info)
    cn = cert_obj.get_subject().get_components()
    
    #OBTENEMOS LAS FECHAS DE EXPIRACION
    cert_desde = datetime.datetime.strptime(cert_obj.get_notBefore(), '%Y%m%d%H%M%SZ')
    cert_hasta = datetime.datetime.strptime(cert_obj.get_notAfter(), '%Y%m%d%H%M%SZ')
    
    #SI LA FECHA DESDE ES MAYOR QUE LA ACTUAL
    if cert_desde > fecha_hoy:
        #ALERTA DE ERROR INVALIDO
        def grabarcertInvalid():
            alert_fecha = open('log_alert/error_reporte.log', 'a')
            alert_fecha.write('fecha_actual ' + str(fecha_hoy.strftime("%d-%m-%Y")) + ' | fecha_expi ' + str(cert_hasta) + ' | site ' + str(host) + ' | error_certificado_invalido\n')
            alert_fecha.close()
        grabarcertInvalid()

    #SI LA FECHA HASTA ES MENOR QUE LA ACTUAL
    if cert_hasta < fecha_hoy:
        #ALERTA DE ERROR EXPIRACION
        def grabarcertCaduca():
            alert_fecha = open('log_alert/error_reporte.log', 'a')
            alert_fecha.write('fecha_actual ' + str(fecha_hoy.strftime("%d-%m-%Y")) + ' | fecha_expi ' + str(cert_hasta) + ' | site ' + str(host) + ' | error_certificado_expirado\n')
            alert_fecha.close()
        grabarcertCaduca()

    #SE RESTAN LAS FECHAS PARA OBTENER LOS DIAS ANTES DE CADUCAR
    dia_para_expi = cert_hasta - fecha_hoy

    if cert_hasta > fecha_hoy:
        if dia_para_expi.days > 21:
            
            #GUARDAMOS EL HTML
            try:
              req = urllib2.Request('https://' + host)
              req.add_header('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0')
              contents = urllib2.urlopen(req)
              code = contents.getcode()
              html = contents.read()
              contents.close()
            except Exception, e:
              print RED1 + "	Restableciendo conexion..." + ENDC
              pass
             
            if html <> '':
              def grabarcertCode():
                archi_html = open('output/cert_' + host + '.crt_code_' + fecha_hoy.strftime("%d-%m-%Y") + '.txt', 'a')
                archi_html.write(html)
                archi_html.close()
              grabarcertCode()  

            #DIFF DE ARCHIVOS
            ayer = datetime.datetime.now() - datetime.timedelta(days=1)
            file1 = 'output/cert_' + host + '.crt_code_' + ayer.strftime("%d-%m-%Y") + '.txt'
            file2 = 'output/cert_' + host + '.crt_code_' + fecha_hoy.strftime("%d-%m-%Y") + '.txt'

            #SI EXISTE ARCHIVO DE AYER QUE COMPARE CON EL DE HOY
            if os.path.isfile(file1):
                filesize1 = os.path.getsize(file1)
                filesize2 = os.path.getsize(file2)

                if filesize1 < filesize2:
                    archi_web1 = open(file1, 'r')
                    archi_web2 = open(file2, 'r')
                    linea1 = archi_web1.readline()
                    linea2 = archi_web2.readline()
                    contador_linea = 0
                    line_valor = ''
                    nom_file = ''
                    while linea1 != "":
                        if linea1 == linea2:
                            estado = 0
                        else:
                            estado = 1
                            if len(linea1) > len(linea2):
                                line_valor = linea1
                                nom_file = file1
                            elif len(linea2) > len(linea1):
                                line_valor = linea2
                                nom_file = file2
                            break
                        linea1 = archi_web1.readline()
                        linea2 = archi_web2.readline()
                        contador_linea = contador_linea + 1

                    #ALERTA DE ERROR DIFF
                    if estado == 1:
                        def grabarDiff():
                            alert_diff = open('log_alert/error_reporte.log', 'a')
                            alert_diff.write('fecha_actual ' + str(fecha_hoy.strftime("%d-%m-%Y")) + ' : site ' + str(host) + ' : File ' + str(nom_file) + ' : Linea ' + str(contador_linea + 1) + ' : string ' + str(line_valor.strip()) + ': html_modificado\n')
                            alert_diff.close()
                        grabarDiff()
                os.remove('output/cert_' + host + '.crt_code_' + ayer.strftime("%d-%m-%Y") + '.txt')    
            #FIN DIFF
        else:
            #ALERTA DE ERROR FECHA EXPIRACION
            def grabarcertFecha():
                alert_fecha = open('log_alert/error_reporte.log', 'a')
                alert_fecha.write('fecha_actual ' + str(fecha_hoy.strftime("%d-%m-%Y")) + ' : fecha_expi ' + str(cert_hasta) + ' : site ' + str(host) + ' : cn ' + str(host) + ' : dias ' + str(dia_para_expi.days) + ': error_fecha_caduca\n')
                alert_fecha.close()
            grabarcertFecha()

            #GUARDAMOS EL HTML
            try:
              req = urllib2.Request('https://' + host)
              req.add_header('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0')
              contents = urllib2.urlopen(req)
              code = contents.getcode()
              html = contents.read()
              contents.close()
            except Exception, e:
              print RED1 + "	Restableciendo conexion..." + ENDC
              pass
             
            if html <> '':
              def grabarcertCode():
                archi_html = open('output/cert_' + host + '.crt_code_' + fecha_hoy.strftime("%d-%m-%Y") + '.txt', 'a')
                archi_html.write(html)
                archi_html.close()
              grabarcertCode()

            #DIFF DE ARCHIVOS
            ayer = datetime.datetime.now() - datetime.timedelta(days=1)
            file1 = 'output/cert_' + host + '.crt_code_' + ayer.strftime("%d-%m-%Y") + '.txt'
            file2 = 'output/cert_' + host + '.crt_code_' + fecha_hoy.strftime("%d-%m-%Y") + '.txt'

            #SI EXISTE ARCHIVO DE AYER QUE COMPARE CON EL DE HOY
            if os.path.isfile(file1):
                filesize1 = os.path.getsize(file1)
                filesize2 = os.path.getsize(file2)

                if filesize1 < filesize2:
                    archi_web1 = open(file1, 'r')
                    archi_web2 = open(file2, 'r')
                    linea1 = archi_web1.readline()
                    linea2 = archi_web2.readline()
                    contador_linea = 0
                    line_valor = ''
                    nom_file = ''
                    while linea1 != "":
                        if linea1 == linea2:
                            estado = 0
                        else:
                            estado = 1
                            if len(linea1) > len(linea2):
                                line_valor = linea1
                                nom_file = file1
                            elif len(linea2) > len(linea1):
                                line_valor = linea2
                                nom_file = file2
                            break
                        linea1 = archi_web1.readline()
                        linea2 = archi_web2.readline()
                        contador_linea = contador_linea + 1

                    #ALERTA DE ERROR DIFF
                    if estado == 1:
                        def grabarDiff():
                            alert_diff = open('log_alert/error_reporte.log', 'a')
                            alert_diff.write('fecha_actual ' + str(fecha_hoy.strftime("%d-%m-%Y")) + ' : site ' + str(host) + ' : File ' + str(nom_file) + ' : Linea ' + str(contador_linea + 1) + ' : string ' + str(line_valor.strip()) + ': html_modificado\n')
                            alert_diff.close()
                        grabarDiff()
                os.remove('output/cert_' + host + '.crt_code_' + ayer.strftime("%d-%m-%Y") + '.txt')    
            #FIN DIFF
    
    linea = archi_web.readline()
archi_web.close()
