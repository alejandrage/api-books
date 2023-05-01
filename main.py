from flask import Flask, g
import psycopg2 #aunque aparece resaltado esta bien instalado

app = Flask(__name__)

# Configuración de la conexión a la base de datos
def get_db():
    db = getattr(g, '_database', None)
    if db is None: 
        db = psycopg2.connect(
                                user="postgres",
                                password="PIKqPhxx35Ymhm3MIgdR",
                                host="containers-us-west-17.railway.app",
                                port="5679",
                                database="railway"
                                )
    return db

#al final de cada solicitud va ejecutar los siguiente, es para seguridad para que se cierre
@app.teardown_appcontext_
def close_connecion(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/',methods =['GET']) #GET para obtener información
def home():
    conn = get_db() #me conecto a la base datos, para no repetir todo lo que esta arriba, por eso se crea la función
    cursor = conn.cursor() #apunta al principio de la tabla
    cursor.execute("SELECT * FROM books_table") #ejecutamos la query y estamos pidiendo que nos devuelva todo por eso ponemos *
    totalrows = cursor.fetchall() #para tener acceso a todo

    #Lo que queremos hacer es mostrar la cantidad de libros que tengo

    num_libros = len(totalrows)

    #cierro el cursor:

    cursor.close()

    #definimos lo que vamos a mostrar en nuestro home:

    home_display = f"""
    <h1>API Libros </h1><p>Esta es una API que contiene {num_libros} libros.</p>"""

    #terminamos haciendo un return

    return home_display