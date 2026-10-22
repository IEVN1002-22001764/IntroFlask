from flask import Flask, jsonify, request #convierte  estructuras de datos a JSON/ request (peticioness attp es
#un objeto almacena informacion del cliente
 
from flask_mysqldb import MySQL
from flask_cors import CORS
 
from config import config #importa las configuraciones de contraseñas
 
app = Flask(__name__)
 
CORS(app)#libreria de comunicacion cliente-servidor
 
con = MySQL(app)#conexion
 
#--------
 
@app.route("/alumnos",methods=['GET'])
def lista_alumnos():
    try:
        cursor=con.connection.cursor()
        sql="select * from alumnos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos=[]
        for fila in datos:
            alumno={"matricula":fila[0],"nombre":fila[1],
                    "apaterno":fila[2],"amaterno":fila[3],
                    "correo":fila[4]}
            alumnos.append(alumno)
        return  jsonify({'alumnos':alumnos,'mensaje':'Lista de alumnos',
                         'exito':True})
 
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex),'exito':False})
 
#------------
 
#metodo creado el 21-10-26
 
def leer_alumno_bd(matricula):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula={0}".format(matricula)
        cursor.execute(sql)
        datos = cursor.fetchone()
 
        if datos != None:
            alumno = {
                "matricula": datos[0],
                "nombre": datos[1],
                "apaterno": datos[2],
                "amaterno": datos[3],
                "correo": datos[4]
            }
            return alumno
        else:
            return None
           
    except Exception as ex:
        raise ex
       
#primera ruta creada 21-10-26
 
@app.route("/alumnos/<int:matricula>", methods=['GET'])#metodo que nos permite encontrar a un alumno por matricula
def leer_alumno(matricula):
    try:
        alumno = leer_alumno_bd(matricula)
        if alumno != None:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado', 'exito': True})
        else:
            return jsonify({'mensaje': 'Alumno no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "error {}".format(ex), 'exito': False})
def pagina_no_encontrada(error):#funcion hecha por flask para enconttrar errores de url desconocida
    return "<h1>Pagina no encontrada</h1>", 404
 
#segunda ruta creada 21.10-26 #se usa res comillas para que sepa pasamos 3 parametros
@app.route("/alumnos", methods=['POST'])
def registra_alumno():
    try:
        alumno = leer_alumno_bd(request.json['matricula'])
        if alumno != None:
            return jsonify({'message': 'Alumno ya existe', 'exito': False})
        else:
            cursor = con.connection.cursor()
            sql = """INSERT INTO alumnos (matricula,nombre,apaterno,amaterno,correo)
                     VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                request.json['matricula'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            )
            cursor.execute(sql)#ejecutar consulta
            con.connection.commit() #guarda la consulta en la base de datos
            return jsonify({'message': 'Alumno registrado con éxito', 'exito': True})#trasforamar el arreglo a JSON
           
    except Exception as ex:
        return jsonify({'message': "error {}".format(ex), 'exito': False})

@app.route("/alumnos/<mat>", methods=['PUT'])
def actualizar_cursor(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor=con.connection.cursor()
            sql="""UPDATE alumnos SET nombre='{}',
            apaterno='{1}',amaterno='{2}',correo='{3}'
            WHERE matricula='{4}'""".format(
            request.json['nombre'],
            request.json['apaterno'],
            request.json['amaterno'],
            request.json['correo'],mat)
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado', 
            'exito': True})
        else:
            return jsonify({'mensaje': 'Alumno no encontrado',
            'exito': False})
    except Exception as ex:
            return jsonify({'mensaje': "error {}".format(ex), 
            'exito': False})
#-----------
 
if __name__ == "__main__":
    app.config.from_object(config['development'])#Carga las configuraciones del entorno de desarrollo
    #desde el objeto config que importamos del archivo config.py y verifica que haya una conexion
    app.register_error_handler(404, pagina_no_encontrada)#Registra oficialmente la función que creamos arriba. Le indica a la aplicación de Flask que,
    #cada vez que un usuario intente entrar a una URL que no existe
    app.run(host='0.0.0.0', port=5000)#servidor escucha peticiones y usa puerto 5000 ip de la maquina y local host