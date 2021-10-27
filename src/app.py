from logging import debug
import re
from flask import Flask,render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_mysqldb import MySQL
from datetime import datetime
import math


#instancia 
app = Flask(__name__)




#configurar conexion base de datos
app.config['MYSQL_HOST'] = '104.238.176.226'
app.config['MYSQL_PORT'] = 33061
app.config['MYSQL_USER'] = 'biobot'
app.config['MYSQL_PASSWORD'] = 'o)dCart34'
app.config['MYSQL_DB'] = 'biobot'

#conexion base de datos
mysql = MySQL(app)

#rutas
@app.route('/', defaults={'page':0})
@app.route('/page/<int:page>' )
def Principal(page):
    #tamano lista
    perpage=20
    #pagina inicio
    startat=page*perpage
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users limit %s, %s;', (startat,perpage))
    data = cur.fetchall()
    cur.execute('SELECT * FROM users')
    tot = cur.fetchall()
    #paginas totales
    tam = len(tot)
    paginas = math.ceil(tam/perpage)
    return render_template('index.html', usuarios= data, total=len(tot), totalP=len(data), pages= paginas)

#ruta ver cultivo de usuario
@app.route('/cultivos/<string:id>',defaults={'pageC':0})
@app.route('/cultivos/<string:id>/page/<int:pageC>')
def ver_usuario(id,pageC):
    #tamano lista
    perpageC=5
    #pagina inicio
    startatC=pageC*perpageC
    cur = mysql.connection.cursor()
    cur.execute('SELECT c.nombre, c.ciclo_cultivo_id, c.ambiente_cultivo_id, c.fecha_inicio, c.fecha_final, c.clave_cultivo,c.creador_id,c.id, c.predios_id, c.tipos_cultivo_id, tc.nombre FROM cultivos AS c INNER JOIN users_has_cultivos AS uhc ON c.id = uhc.cultivos_id INNER JOIN tipos_cultivo AS tc ON c.tipos_cultivo_id = tc.id  WHERE uhc.users_id = %s limit %s, %s;',(id,startatC,perpageC,))
    res = cur.fetchall()
    data =[]
    contenido = {}
    for resultado in res:
        contenido={'nombre': resultado[0],'ciclo_cultivo_id':resultado[1], 'ambiente_cultivo_id':resultado[2], 'fecha_inicio':resultado[3].strftime('%Y-%m-%d'), 'fecha_final':resultado[4].strftime('%Y-%m-%d'),'clave_cultivo':resultado[5],'creador_id':resultado[6],'id':resultado[7], 'predios_id':resultado[8], 'tipos_cultivo_id':resultado[9], 'tipo_cultivo':resultado[10] }
        data.append(contenido)

    cur.execute('SELECT c.nombre, c.ciclo_cultivo_id, c.ambiente_cultivo_id, c.fecha_inicio, c.fecha_final, c.clave_cultivo,c.creador_id,c.id, c.predios_id, c.tipos_cultivo_id, tc.nombre FROM cultivos AS c INNER JOIN users_has_cultivos AS uhc ON c.id = uhc.cultivos_id INNER JOIN tipos_cultivo AS tc ON c.tipos_cultivo_id = tc.id  WHERE uhc.users_id = %s',(id,))
    totC = cur.fetchall()
    #paginas totales
    tamC = len(totC)
    paginasC = math.ceil(tamC/perpageC)    
    return render_template('cultivos.html',cultivos =data,  pagesC= paginasC, cultivo= id)

#ruta ver dispositivos usuarios
@app.route('/dispositivos/<int:id>',defaults={'pageD':0})
@app.route('/dispositivos/<string:id>/page/<int:pageD>')
def ver_dispositivos(id,pageD):
    #tamano lista
    perpageD=850
    #pagina inicio
    startatD=pageD*perpageD
    cur = mysql.connection.cursor()
    cur.execute('select bd.nombre, bd.clave, bd.id, bd.tipo_biodispositivos_id , shbd.sensores_id,sl.created_at, tp.tipo, tp.modulos  from bio_dispositivos AS bd INNER JOIN users_has_biodispositivos AS uhb on bd.bio_dispositivos_id = uhb.bio_dispositivos_id INNER JOIN  sensores_has_bio_dispositivos AS shbd ON bd.bio_dispositivos_id = shbd.bio_dispositivos_id INNER JOIN sensores_log AS sl ON sl.sensores_id = shbd.sensores_id INNER JOIN tipo_biodispositivos AS tp ON bd.tipo_biodispositivos_id = tp.id WHERE uhb.users_id = %s limit %s, %s;',(id,startatD,perpageD,))
    res = cur.fetchall()
    data =[]
    contenido = {}
    for resultado in res:
        contenido={'nombre': resultado[0], 'clave':resultado[1], 'id':resultado[2], 'tipo_biodispositivos_id':resultado[3], 'last_log':{'value_datetime':resultado[5].strftime('%Y-%m-%d %H:%M:%S'),'pivot':{'sensores_id':resultado[4], 'bio_dispositivos_id':resultado[2]}},'device_type':{'id':resultado[3], 'nombre':resultado[6],'modulos':resultado[7]} }
        data.append(contenido)
    
    cur.execute('select bd.nombre, bd.clave, bd.id, bd.tipo_biodispositivos_id , shbd.sensores_id,sl.created_at, tp.tipo, tp.modulos  from bio_dispositivos AS bd INNER JOIN users_has_biodispositivos AS uhb on bd.bio_dispositivos_id = uhb.bio_dispositivos_id INNER JOIN  sensores_has_bio_dispositivos AS shbd ON bd.bio_dispositivos_id = shbd.bio_dispositivos_id INNER JOIN sensores_log AS sl ON sl.sensores_id = shbd.sensores_id INNER JOIN tipo_biodispositivos AS tp ON bd.tipo_biodispositivos_id = tp.id WHERE uhb.users_id = %s',(id,))
    totD = cur.fetchall()
    #paginas totales
    tamD = len(totD)
    paginasD = math.ceil(tamD/perpageD)    
    return render_template('dispositivos.html', dispositivos=data,pagesD= paginasD, disp= id) 

#cultivos y dispositivos
@app.route('/cultivo_dispositivos/<string:id>',defaults={'pageCD':0})
@app.route('/cultivo_dispositivos/<string:id>/page/<int:pageCD>')
def cultivosDispositivos(id,pageCD):
    #tamano lista
    perpageCD=20
    #pagina inicio
    startatCD=pageCD*perpageCD
    cur = mysql.connection.cursor()
    cur.execute('SELECT c.nombre, c.ciclo_cultivo_id, c.ambiente_cultivo_id, c.fecha_inicio, c.fecha_final, c.clave_cultivo,c.creador_id,c.id, c.predios_id, c.tipos_cultivo_id,bd.nombre, bd.clave, bd.id, bd.tipo_biodispositivos_id , shbd.sensores_id,sl.created_at, tp.tipo, tp.modulos  FROM cultivos AS c INNER JOIN users_has_cultivos AS uhc ON c.id = uhc.cultivos_id INNER JOIN tipos_cultivo AS tc ON c.tipos_cultivo_id = tc.id INNER JOIN users_has_biodispositivos AS uhb ON uhb.users_id = uhc.users_id INNER JOIN bio_dispositivos AS bd ON bd.bio_dispositivos_id = uhb.bio_dispositivos_id  INNER JOIN  sensores_has_bio_dispositivos AS shbd ON bd.bio_dispositivos_id = shbd.bio_dispositivos_id INNER JOIN sensores_log AS sl ON sl.sensores_id = shbd.sensores_id INNER JOIN tipo_biodispositivos AS tp ON bd.tipo_biodispositivos_id = tp.id WHERE uhc.users_id=%s limit %s, %s;',(id,startatCD,perpageCD,))
    res = cur.fetchall()
    data =[]
    contenido = {}
    for resultado in res:
        contenido={'nombre': resultado[0],'ciclo_cultivo_id':resultado[1], 'ambiente_cultivo_id':resultado[2], 'fecha_inicio':resultado[3].strftime('%Y-%m-%d'), 'fecha_final':resultado[4].strftime('%Y-%m-%d'),'clave_cultivo':resultado[5],'creador_id':resultado[6],'id':resultado[7], 'predios_id':resultado[8], 'tipos_cultivo_id':resultado[9],  'devices':{'nombre':resultado[10],'clave':resultado[11], 'id':resultado[12],'tipo_biodispositivos_id':resultado[13],'last_log':{'value_datetime':resultado[15].strftime('%Y-%m-%d %H:%M:%S'),'pivot':{'sensores_id':resultado[14], 'bio_dispositivos_id':resultado[12]}},'device_type':{'id':resultado[13], 'nombre':resultado[16],'modulos':resultado[17]}} }
        data.append(contenido)
    
    return jsonify({'data':data})

#correr y puerto
if __name__ == '__main__':
    app.run(port=3000, debug=True)