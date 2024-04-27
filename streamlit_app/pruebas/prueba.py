import requests

# URL del servicio al que se quiere acceder
url = "http://10.10.6.10:8081/generate"

# Datos JSON que se enviarán en la solicitud POST
data = {
    "inputs": "Cuáles son los pasos iniciales para tratar una quemadura leve"
}

# Encabezados de la solicitud
headers = {
    "Content-Type": "application/json"
}

# Realizando la solicitud POST
response = requests.post(url, json=data, headers=headers)

# Verificando si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear la respuesta JSON
    response_json = response.json()
    
    # Obtener el texto generado
    generated_text = response_json.get('generated_text', 'No generated text found')
    
    # Imprimir solo el texto generado
    print(generated_text)
else:
    print("Error in the request:", response.status_code)
