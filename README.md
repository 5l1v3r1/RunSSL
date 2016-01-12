# RunSSL.py
Avanzado SSL Verificador

La herramienta contiene las siguientes funcionalidades:<br>

<b>Valida Lo siguiente:</b>
- Comprueba si el dominio esta UP.
- comprueba La version (SSL/TLS).
- Fecha del scan.
- Fecha expiración.
- Sitio revisado.
- Certificado invalido.
- Certificado expirado.
- Comprueba fecha de expiracion.
- Muestra los dias restantes para caducidad del certificado.
- Guarda el html del sitio para el proximo scan y comparar si hubieron cambio.
- Genera reporte de alertas en formato syslog.

Uso para SysLog: (Se puede dejar como Daemon para obtener un reporte diario o semanal .etc<br> para luego implementarlo en alguna herramineta de monitoreo.)


<b>USO:</b>

- Agregar los nombres de dominios o ip en el archivo <b>lista_web.txt</b> sin <b>(https://)</b> ejemplo: sitioprueba.com
- Ejecutar el script: python RunSSL.py
