#
# *-*-*-*-*-*-*-*-*
# ARCHIVO: servidor.py
# FASE 2 - BACKEND (PYTHON + API REST)
#
# Este archivo es el "traductor" entre dos mundos que no se entienden entre si:
#
#   NAVEGADOR (habla HTTP y JSON)  <---->  SERVIDOR  <---->  PROLOG (habla logica)
#
# Lo que hace, en orden:
#   1) Levanta un servidor web con Flask.
#   2) Carga el archivo inventario.pl dentro de Prolog usando PySwip.
#   3) Expone una ruta GET que recibe el item escrito por el usuario.
#   4) Ejecuta la regla analizar_inventario/6 inyectando ese item.
#   5) Convierte las variables que Prolog unifico en un diccionario y lo manda como JSON.
#
# CORS: el navegador, por seguridad, bloquea las peticiones a un servidor de origen
# distinto al de la pagina. flask-cors agrega las cabeceras que le dan permiso.
# *-*-*-*-*-*-*-*-*
#

import os                                    # <-- os: para leer variables de entorno y armar rutas de archivos.
from flask import Flask, jsonify, request    # <-- Flask: servidor web. jsonify: convierte dict -> JSON. request: lee los parametros de la URL.
from flask import send_from_directory        # <-- send_from_directory: entrega los archivos del frontend (html, css, js).
from flask_cors import CORS                  # <-- CORS: middleware que autoriza las peticiones desde el navegador.
from pyswip import Prolog                    # <-- Prolog: el puente de PySwip que ejecuta consultas sobre SWI-Prolog.


#
# *-*-*-*-*-*-*-*-*
# BLOQUE 1: CONFIGURACION Y CARGA DEL MOTOR PROLOG
# Se hace UNA sola vez cuando arranca el servidor, no en cada peticion.
# *-*-*-*-*-*-*-*-*
#

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))   # <-- carpeta donde vive este .py (ruta absoluta, no depende de donde se ejecute).
RUTA_PROLOG = os.path.join(RUTA_BASE, "inventario.pl")   # <-- ruta absoluta al archivo de reglas de Prolog.
RUTA_WEB = os.path.join(RUTA_BASE, "web")                # <-- carpeta con el frontend (Fase 3).

app = Flask(__name__, static_folder=None)                # <-- se crea la aplicacion web. static_folder=None porque el frontend se sirve a mano mas abajo.
CORS(app)                                                # <-- se activa CORS para TODAS las rutas: sin esto el fetch del navegador seria rechazado.

prolog = Prolog()                                        # <-- se enciende el motor de SWI-Prolog incrustado dentro de este proceso de Python.
prolog.consult(RUTA_PROLOG)                              # <-- consult(): carga el archivo .pl con sus hechos y reglas en la memoria del motor.

print("[OK] Motor Prolog cargado desde:", RUTA_PROLOG, flush=True)   # <-- mensaje de arranque para confirmar en consola que el .pl si se leyo.


#
# *-*-*-*-*-*-*-*-*
# BLOQUE 2: FUNCIONES AUXILIARES
# Pequenas ayudas para limpiar la entrada y para traducir lo que devuelve Prolog.
# *-*-*-*-*-*-*-*-*
#

def limpiar_item(texto):
    # <-- Prolog entiende los items como ATOMOS y los atomos se escriben en minusculas.
    # <-- Por eso el texto del usuario se recorta (strip) y se pasa a minusculas (lower).
    return texto.strip().lower()


def escapar_item(texto):
    # <-- La comilla simple cerraria el atomo antes de tiempo y romperia la consulta de Prolog.
    # <-- Se duplica, que es la forma en que Prolog escapa una comilla dentro de un atomo.
    return texto.replace("'", "''")


def a_texto(valor):
    # <-- Segun la version, PySwip puede devolver un atomo como bytes o como objeto.
    # <-- Esta funcion lo deja siempre como texto plano, que es lo unico que JSON acepta.
    if isinstance(valor, bytes):
        return valor.decode("utf-8")
    return str(valor)


def a_lista_de_texto(lista):
    # <-- Recorre la lista que devolvio Prolog y convierte cada elemento a texto.
    return [a_texto(elemento) for elemento in lista]


#
# *-*-*-*-*-*-*-*-*
# BLOQUE 3: LA RUTA DE LA API (endpoint GET)
#
# URL:      GET /api/inventario?item=pocion
# Devuelve: un JSON con el total y las tres listas procesadas por Prolog.
# *-*-*-*-*-*-*-*-*
#

@app.route("/api/inventario", methods=["GET"])           # <-- @app.route: registra la URL y el metodo HTTP que atiende esta funcion.
def consultar_inventario():

    # <-- request.args lee los parametros que vienen despues del "?" en la URL.
    item_crudo = request.args.get("item", "")

    # <-- Validacion: si no mandaron nada, se responde 400 (peticion mal hecha) y no se molesta a Prolog.
    if not item_crudo.strip():
        return jsonify({"ok": False, "error": "Debe enviar el parametro 'item'."}), 400

    item = limpiar_item(item_crudo)                      # <-- se normaliza el texto para que Prolog lo acepte.
    item_seguro = escapar_item(item)                     # <-- version escapada, solo para meterla dentro de la consulta.

    # <-- Se arma la consulta INYECTANDO el item del usuario. Nada esta quemado a mano:
    # <-- las 5 variables van en Mayuscula y llegan vacias para que Prolog las unifique.
    consulta = "analizar_inventario('%s', TotalItems, Encontrado, Invertido, Unico, Ordenado)" % item_seguro

    print("\n[CONSULTA PROLOG]", consulta, flush=True)   # <-- se imprime en consola para evidenciar que la consulta es dinamica.

    # <-- prolog.query() ejecuta la regla. Devuelve un generador de soluciones,
    # <-- list() lo recorre completo y deja las soluciones en una lista de Python.
    # <-- Ojo: es aqui donde Prolog imprime el recorrido recursivo en ESTA misma consola.
    soluciones = list(prolog.query(consulta))

    # <-- Si la lista viene vacia significa que la regla fallo (no hubo unificacion posible).
    if not soluciones:
        return jsonify({"ok": False, "error": "Prolog no devolvio solucion."}), 500

    resultado = soluciones[0]                            # <-- se toma la primera (y unica) solucion: un diccionario Variable -> Valor.

    # <-- Se arma la respuesta traduciendo cada variable unificada a un tipo que JSON entienda.
    respuesta = {
        "ok": True,
        "itemBuscado": item,                                              # <-- eco del item consultado.
        "encontrado": a_texto(resultado["Encontrado"]) == "si",           # <-- 'si'/'no' de Prolog se vuelve true/false de JSON.
        "totalItems": int(resultado["TotalItems"]),                       # <-- length/2 devolvio un numero entero.
        "inventarioInvertido": a_lista_de_texto(resultado["Invertido"]),  # <-- resultado de reverse/2.
        "inventarioUnico": a_lista_de_texto(resultado["Unico"]),          # <-- resultado de sort/2 (sin duplicados).
        "inventarioOrdenado": a_lista_de_texto(resultado["Ordenado"]),    # <-- resultado de msort/2 (con duplicados).
    }

    print("[RESPUESTA JSON]", respuesta, flush=True)     # <-- se muestra en consola lo que se le devuelve al navegador.

    return jsonify(respuesta)                            # <-- jsonify convierte el diccionario a JSON y pone el header Content-Type correcto.


#
# *-*-*-*-*-*-*-*-*
# BLOQUE 4: SERVIR EL FRONTEND
# Opcional pero comodo: el mismo servidor entrega la pagina web de la Fase 3,
# asi se puede abrir todo desde http://localhost:5000 sin instalar nada mas.
# *-*-*-*-*-*-*-*-*
#

@app.route("/", methods=["GET"])
def pagina_principal():
    # <-- Entrega el index.html cuando se entra a la raiz del servidor.
    return send_from_directory(RUTA_WEB, "index.html")


@app.route("/<path:archivo>", methods=["GET"])
def archivos_web(archivo):
    # <-- Entrega cualquier otro archivo de la carpeta web (estilos.css, script.js).
    return send_from_directory(RUTA_WEB, archivo)


#
# *-*-*-*-*-*-*-*-*
# BLOQUE 5: ARRANQUE DEL SERVIDOR
# *-*-*-*-*-*-*-*-*
#

if __name__ == "__main__":                               # <-- solo se ejecuta si el archivo se corre directamente (no si se importa).
    # <-- El puerto se lee de una variable de entorno y 5000 es solo el valor por defecto:
    # <-- asi no queda quemado y se puede cambiar con  PORT=8080 python servidor.py
    puerto = int(os.environ.get("PORT", 5000))
    print("[OK] Servidor escuchando en http://localhost:%d" % puerto)
    # <-- host="0.0.0.0" permite conexiones externas (no solo desde esta misma maquina).
    app.run(host="0.0.0.0", port=puerto, debug=False)
