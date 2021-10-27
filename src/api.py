from logging import debug
import re
from flask import Flask,render_template, request, redirect, url_for, flash, jsonify, Blueprint
from flask_mysqldb import MySQL
from datetime import datetime
import math
from flask_restx import Api, Resource


#instancia 
app = Flask(__name__)
#api

api = Api(app,title='Cultivos API',description='Cultivos API')




#configurar conexion base de datos
app.config['MYSQL_HOST'] = '104.238.176.226'
app.config['MYSQL_PORT'] = 33061
app.config['MYSQL_USER'] = 'biobot'
app.config['MYSQL_PASSWORD'] = 'o)dCart34'
app.config['MYSQL_DB'] = 'biobot'

#conexion base de datos
mysql = MySQL(app)

#rutas
@api.route('/', defaults={'page':0})
@api.route('/page/<int:page>' )
class Usuarios(Resource):
    def get(self,page):
        #tamano lista
        perpage=20
        #pagina inicio
        startat=page*perpage
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users limit %s, %s;', (startat,perpage))
        data = cur.fetchall()
        
        return jsonify(data)

#ruta ver cultivo de usuario

@api.route('/cultivos/<string:id>',defaults={'pageC':0})
@api.route('/cultivos/<string:id>/page/<int:pageC>')
class Cultivos(Resource):
    def get(self,id,pageC):
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

    
        return jsonify({'data':data})

#ruta ver dispositivos usuarios
@api.route('/dispositivos/<int:id>',defaults={'pageD':0})
@api.route('/dispositivos/<string:id>/page/<int:pageD>')
class Dispositivos(Resource):
    def get(self,id,pageD):
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
    
        
        return jsonify({'data':data}) 
#cultivos y dispositivos
@api.route('/cultivo_dispositivos/<string:id>',defaults={'pageCD':0})
@api.route('/cultivo_dispositivos/<string:id>/page/<int:pageCD>')
class CultivosDisp(Resource):
    def get(self,id,pageCD):
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
    app.run( debug=True)