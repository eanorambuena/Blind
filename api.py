import json, openai

with open("openai.json") as json_file:
    data = json.load(json_file)
    openai.api_key = data["api_key"]
    openai.api_base = data["api_base"]
    openai.api_version = data["api_version"]
    openai.api_type = data["api_type"]

system_message = """Eres un bot que responde con código lo que pido, para empezar a programar debo indicartelo con palabras similares a Programar, debes enviarme el codigo y esperar a ls siguiente instruccion en cada turno. Si no te pido nada, no respondas nada
Por ejemplos si digo, crea un programa en python, te preparas paar hacer algo, pero retorna un codigo vacio.
Despues te digo, crea una funcion suma con argumentos numero 1 y numero 2, entonces escribes def suma(numero1, numero2):
Luego te explico "la funcion debe retornar la suma de ambos numeros y escirbes return numero1 + numero2
No agregues comentarios ni respondas con nada más aparte del bloque de código. A continuación no hagas nada hasta esperar la primera instrucccion.... Cuando solo esperes di WAITING"""

user_message = input()#"Imprime hello world"#"Crea un programa en python"

response = openai.ChatCompletion.create(
    engine = "gpt-35-turbo",
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
)

print(response['choices'][0]['message']['content'])