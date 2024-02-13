import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import pyaudio

#opciones de vo y de idioma
id1 ='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

#escuchar microfono y tranformalo en texto
def transformar_audio_en_texto():

    #almacenar el reconocedor en un variable
    r = sr.Recognizer()

    #configuramos el microfono
    with sr.Microphone() as origen:

        #tiempo de espera cuando se activa para despues escuchar
        r.pause_threshold = 0.8

        #informar que comenzo la grabacion
        print("Ya puedes hablar")

        #guardar el audio ya grabado
        audio = r.listen(origen)

        try:
            #buscar en google lo escuchado
            pedido = r.recognize_google(audio, language="es-MX")

            #ver lo transformado
            print("Dijiste: " + pedido)

            #devolver pedido
            return pedido
        #en caso de no entender o asi
        except sr.UnknownValueError:

            #prueba de que no comprendio
            print("Ups,no hay nada")
            #devolver algo
            return "sigo esperando"

    #en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio
            print("Ups,no entendi")
            # devolver algo
            return "sigo esperando"

        except:

            # prueba de que no comprendio
            print("Ups,algo salio mal")
            # devolver algo
            return "sigo esperando"

#funcion para que el asistente sea escuchado
def hablar(mensaje):
    #encender el mtor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice',id1)

    #pronunciar el mensaje
    engine.say(mensaje)
    engine.runAndWait()

#informar el dia de la semana
def pedir_dia():

    #crear variables con datos de hoy
    dia = datetime.date.today()

    #crear una variable para le dia de semana
    dia_semana = dia.weekday()

    #diccionario que contenga el nombre de los dias
    calendario = {0:'Lunes',
                  1:'Martes',
                  2:'Miercoles',
                  3:'Jueves',
                  4:'Viernes',
                  5:'Sabado',
                  6:'Domingo'}
    #decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

#informar que hora es
def pedir_hora():

    #crear una variable con los datos de la hora
    hora = datetime.datetime.now()
    hora = (f'En este momento son las {hora.hour} horas , con {hora.minute} minutos,'
            f'y {hora.second}segundos')
    #decir la hora

    hablar(hora)

#funcion saludo inicial
def saludo_inicial():

    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas Noches'
    elif hora.hour >=6 or hora.hour < 13:
        momento = 'Buenos Dias'
    else:
        momento = 'Buenas Tardes'

    #decir el saludo
    hablar(f'Hola{momento},soy Helena, tu asistente de voz,¿Por favor dime, en que te puedo ayudar?')

#funcion central del asistente
def pedir_cosas():

    #activar saludo
    saludo_inicial()

    #variable de corte
    comenzar = True

    #loop central
    while comenzar:

        #activar micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro abriendo navegador')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es ' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia','')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences = 1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo, lo busco!')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es fue lo que encontre')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon':'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre,el precio de{accion} es {precio_actual}')
                continue
            except:
                hablar('Perdon pero no la eh encontrado')
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descanzar,cualquier cosa me avisas')
            break

            
pedir_cosas()
