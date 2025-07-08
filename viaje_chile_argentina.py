import requests

API_KEY = "6fcf46b0-1899-4694-8596-20dbfa46ce05" 
KM_A_MILLAS = 0.621371

def geocode(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json()['hits']:
        lat = response.json()['hits'][0]['point']['lat']
        lon = response.json()['hits'][0]['point']['lng']
        return f"{lat},{lon}"
    else:
        print(f" No se encontró la ciudad: {ciudad}")
        return None

def obtener_datos_viaje(coord_origen, coord_destino, transporte):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [coord_origen, coord_destino],
        "vehicle": transporte,
        "locale": "es",
        "instructions": "true",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        ruta = response.json()['paths'][0]
        distancia_km = ruta['distance'] / 1000
        distancia_millas = distancia_km * KM_A_MILLAS
        duracion_segundos = ruta['time'] / 1000
        narrativa = ruta['instructions']
        return distancia_km, distancia_millas, duracion_segundos, narrativa
    else:
        print(f" Error al obtener la ruta: {response.status_code}")
        return None, None, None, None

def formato_duracion(segundos):
    h = int(segundos // 3600)
    m = int((segundos % 3600) // 60)
    s = int(segundos % 60)
    return f"{h}h {m}m {s}s"

def mostrar_narrativa(narrativa):
    print("\n Narrativa del viaje:")
    for paso in narrativa:
        print(f"- {paso['text']} ({paso['distance']:.2f} m)")

def main():
    print("===  Calculadora de Ruta Chile – Argentina ===")

    while True:
        origen = input("\nCiudad de Origen (Chile) [s para salir]: ")
        if origen.lower() == 's':
            break

        destino = input("Ciudad de Destino (Argentina) [s para salir]: ")
        if destino.lower() == 's':
            break

        print("Tipo de transporte:")
        print("1. Auto")
        print("2. Bicicleta")
        print("3. A pie")
        opcion = input("Seleccione una opción (1-3): ")

        transporte = {
            '1': 'car',
            '2': 'bike',
            '3': 'foot'
        }.get(opcion)

        if transporte is None:
            print("Opción inválida.")
            continue

        coord_origen = geocode(origen)
        coord_destino = geocode(destino)

        if coord_origen and coord_destino:
            km, millas, duracion, narrativa = obtener_datos_viaje(coord_origen, coord_destino, transporte)
            if km is not None:
                print(f"\n Distancia: {km:.2f} km / {millas:.2f} millas")
                print(f" Duración estimada: {formato_duracion(duracion)}")
                mostrar_narrativa(narrativa)

    print("\n Programa finalizado.")

if __name__ == "__main__":
    main()
