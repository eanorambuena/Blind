import json
import openai
import speech_recognition as sr
import pyttsx3

DEFAULT_SYSTEM_MESSAGE = """Eres un bot que responde con código lo que pido, para empezar a programar debo indicartelo con palabras similares a Programar, debes enviarme el codigo y esperar a ls siguiente instruccion en cada turno. Si no te pido nada, no respondas nada
Por ejemplos si digo, crea un programa en python, retorna: '{"code": "","human": "He creado un programa en python"}'
Despues te digo, crea una funcion suma con argumentos numero 1 y numero 2, entonces escribes:
'{"code": "def suma(numero1, numero2):\n\treturn numero1 + numero2","human": "He creado una funcion suma con argumentos numero 1 y numero 2, que retorna la suma de ambos"}'
No agregues comentarios ni respondas con nada más aparte del bloque de código. A continuación no hagas nada hasta esperar la primera instrucccion..."""

def speak (command) -> None:
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def get_response (user_message: str, system_message: str = DEFAULT_SYSTEM_MESSAGE) -> str:
    response = openai.ChatCompletion.create(
        engine = "gpt-35-turbo",
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    return response['choices'][0]['message']['content']

def setup_openai (file_name: str = "api_key.json") -> None:
    with open(file_name) as json_file:
        data = json.load(json_file)
        openai.api_key = data["api_key"]
        openai.api_base = data["api_base"]
        openai.api_version = data["api_version"]
        openai.api_type = data["api_type"]

def main () -> None:
    command = "¡Hola! Dime tu instrucción para programar"
    speak(command)

    r = sr.Recognizer()
    setup_openai()

    while True:   
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration = 0.2)
                user_input = r.listen(source2)
                text = r.recognize_google(user_input)
                user_message = text.lower()
                response = get_response(user_message)
                code = ""
                human = "Esperando instrucción..."
                try:
                    json.loads(response)
                    code = response["code"]
                    human = response["human"]
                    speak(human)
                except json.decoder.JSONDecodeError:
                    print("No se pudo decodificar el JSON")
                print(response)
        except sr.RequestError as e:
            print(e)
        except sr.UnknownValueError:
            print("Valor desconocido")

if __name__ == "__main__":
    main()
