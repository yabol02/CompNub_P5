# Desarrollado por la asignatura Computación en la Nube del Grado de Ingeniería y Sistemas de Datos
# Universidad Politécnica de Madrid
# Curso 2023-24

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

import logging
import argparse
import os
import time
import random
import sys

PERIODO = 5
PUSH_GATEWAY_IP = "localhost"
PUSH_GATEWAY_PORT = 9091
LATITUD=40.38983
LONGITUD=-3.62924
NOMBRE_TRABAJO = 'city_env'
DESCRIPCION = "Sensor que proporciona temperatura y humedad, así como su longitud y latitud."
NOMBRE_SENSOR ="sin_nombre"
TEMPERATURA_MAX = 50.0
TEMPERATURA_MIN = -50.0
HUMEDAD_MAX = 100
HUMEDAD_MIN = 0

if __name__ == "__main__":
    # Recogida de parámetros de la aplicación a través de variables de entorno
    period = os.getenv("PERIODO", PERIODO)
    pushGWIP = os.getenv("PUSH_GATEWAY_IP", PUSH_GATEWAY_IP)
    pushGWPort = os.getenv("PUSH_GATEWAY_PORT", PUSH_GATEWAY_PORT)
    nombreJob = os.getenv('NOMBRE_TRABAJO', NOMBRE_TRABAJO)
    latitud = os.getenv('LATITUD', LATITUD)
    longitud = os.getenv('LONGITUD', LONGITUD)
    nombre_sensor = os.getenv('NOMBRE_SENSOR', NOMBRE_SENSOR)
    temp_max = os.getenv('TEMPERATURA_MAX', TEMPERATURA_MAX)
    temp_min = os.getenv('TEMPERATURA_MIN', TEMPERATURA_MIN)
    hum_max = os.getenv('HUMEDAD_MAX', HUMEDAD_MAX)
    hum_min = os.getenv('HUMEDAD_MIN', HUMEDAD_MIN)

    # Configuración del sistema de logging de mensajes
    FORMAT = '%(name)s - %(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger(__name__)

    # Recogida de parámetros de la aplicación a través de argumentos en la línea de comando.
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--periodo", help="Periodo de muestreo")
    parser.add_argument("-gip", "--gwIP", help="Dirección IP del gateway")
    parser.add_argument("-gp", "--gwPort", help="Puerto TCP del gateway")
    parser.add_argument("-j", "--nombreTrabajo", help="Nombre del trabajo de Prometheus")
    parser.add_argument("-la", "--latitud", help="Latitud del sensor")
    parser.add_argument("-lo", "--longitud", help="Longitud del sensor")
    parser.add_argument("-n", "--nombre", help="Nombre del sensor")
    parser.add_argument("-tmax", "--tempMax", help="Temperatura máxima")
    parser.add_argument("-tmin", "--tempMin", help="Temperatura mínima")
    parser.add_argument("-hmax", "--humMax", help="Humedad máxima")
    parser.add_argument("-hmin", "--humMin", help="Humedad mínima")
    
    args = parser.parse_args()
    if ( args.periodo ):
        period=args.periodo
    if ( args.gwIP ):
        pushGWIP=args.gwIP
    if ( args.gwPort ):
        pushGWPort=args.gwPort
    if ( args.nombreTrabajo ):
        nombreJob=args.nombreTrabajo
    if ( args.latitud ):
        latitud=args.latitud
    if ( args.longitud ):
        longitud=args.longitud
    if ( args.nombre ):
        nombre_sensor=args.nombre
    if ( args.tempMax ):
        temp_max = args.tempMax
    if ( args.tempMin ):
        temp_min = args.tempMin
    if ( args.humMax ):
        hum_max = args.humMax
    if ( args.humMin ):
        hum_min = args.humMin

    logger.info("Iniciando sensor")
    logger.debug("Periodo de muestreo: %d" % (int(period)))
    logger.debug("Dirección IP del GW: %s" % (pushGWIP))
    logger.debug("Puerto TCP del GW: %s" % (pushGWPort))
    logger.debug("Nombre del trabajo de Prometheus: %s" % (nombreJob))
    logger.debug("Nombre del sensor: %s" % (nombre_sensor))

    registro = CollectorRegistry() # Iniciamos un registro con sólo las medidas de los sensores,
                                   # sin registrar métricas de procesos, sistema, etc.
    # Se crean dos recursos de Prometheus de tipo Gauge (se puede incrementar o decrementar su valor
    # y también se puede fijar un valor concreto).
    # la métrica que se manda al PushGateway tiene la siguiente sintaxis, conforme al formato que acepta
    # Prometheus, y según se envíe una medida de temperatura o de humedad
    #   temperatura{'instance':'<id del sensor>', 'lon' :'<longitud de la coordenada GPS>',
    #               'lat': '<latitud de la coordenada GPS>', 'unidades' : '<unidad en medidad>'}
    #   humedad{'instance':'<id del sensor>', 'lon' :'<longitud de la coordenada GPS>',
    #           'lat': '<latitud de la coordenada GPS>', 'unidades' : '<unidad en medidad>'}
    medidor_temperatura = Gauge( "temperatura", DESCRIPCION, labelnames=['instance', 'lon', 'lat', 'unidades'], registry=registro)
    medidor_humedad = Gauge( "humedad", DESCRIPCION, labelnames=['instance', 'lon', 'lat', 'unidades'], registry=registro)
    
    while True:
            try:
                medidor_temperatura.labels(nombre_sensor, longitud, latitud, 'ºC').set(random.uniform(float(temp_min), float(temp_max)))
                medidor_humedad.labels(nombre_sensor, longitud, latitud, '%').set( random.uniform(float(hum_min), float(hum_max)))
                    
                push_to_gateway(pushGWIP+':'+str(pushGWPort), job=nombreJob, registry=registro)
                time.sleep(int(period))
                pass
            except BaseException as err:
                if isinstance(err, KeyboardInterrupt):
                    logger.info("Interrupción de teclado. Parando el sensor ...")
                    sys.exit(0)
                logger.error("%s." %(err))
                pass
