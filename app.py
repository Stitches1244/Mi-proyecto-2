import os
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from json import JSONDecodeError


def obtener_agentes():
    language = os.getenv("VALORANT_API_LANGUAGE", "es-ES")
    url = f"https://valorant-api.com/v1/agents?language={language}&isPlayableCharacter=true"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            print("Error 404: No se encontro el recurso solicitado en la API.")
            return []

        response.raise_for_status()

        try:
            data = response.json()
        except JSONDecodeError:
            print("Error: La respuesta de la API no tiene formato JSON valido.")
            return []

        agentes = data.get("data", [])

        if not agentes:
            print("No se encontraron agentes jugables en la API.")
            return []

        return agentes

    except Timeout:
        print("Error: La API tardo demasiado en responder.")
        return []

    except ConnectionError:
        print("Error: No se pudo conectar con la API. Revisa tu conexion a internet.")
        return []

    except HTTPError as error:
        print(f"Error HTTP al consultar la API: {error}")
        return []

    except RequestException as error:
        print(f"Error general al realizar la solicitud: {error}")
        return []


def buscar_agente_por_nombre(agentes, nombre_buscado):
    for agente in agentes:
        nombre_agente = agente.get("displayName", "").lower()

        if nombre_agente == nombre_buscado.lower():
            return agente

    return None


def mostrar_lista_agentes(agentes):
    print("\nAgentes disponibles:")

    nombres = []

    for agente in agentes:
        nombre = agente.get("displayName", "Sin nombre")
        nombres.append(nombre)

    nombres.sort()

    for nombre in nombres:
        print(f"- {nombre}")


def mostrar_agente(agente):
    try:
        nombre = agente["displayName"]
        descripcion = agente["description"]
        rol = agente["role"]["displayName"] if agente.get("role") else "Sin rol definido"
        developer_name = agente.get("developerName", "No disponible")
        habilidades = agente.get("abilities", [])

        print("\n======================================")
        print("      RESULTADO DE LA CONSULTA")
        print("======================================")
        print(f"Nombre: {nombre}")
        print(f"Rol: {rol}")
        print(f"Nombre tecnico en API: {developer_name}")
        print(f"Descripcion: {descripcion}")

        print("\nHabilidades:")
        for habilidad in habilidades:
            nombre_habilidad = habilidad.get("displayName", "Sin nombre")
            tipo = habilidad.get("slot", "Sin tipo")
            descripcion_habilidad = habilidad.get("description", "Sin descripcion")

            print("--------------------------------------")
            print(f"Habilidad: {nombre_habilidad}")
            print(f"Tipo: {tipo}")
            print(f"Descripcion: {descripcion_habilidad}")

        print("--------------------------------------")
        print("Consulta finalizada correctamente.")

    except KeyError as error:
        print(f"Error: Falta un campo esperado en los datos del agente: {error}")


def main():
    agentes = obtener_agentes()

    if not agentes:
        print("No fue posible mostrar informacion de agentes.")
        return

    print("======================================")
    print("      VALORANT AGENT ADVISOR")
    print("======================================")
    print("Esta herramienta permite consultar informacion de un agente de Valorant.")

    mostrar_lista_agentes(agentes)

    nombre_buscado = os.getenv("AGENTE_VALORANT")

    if nombre_buscado:
        print(f"\nAgente solicitado por variable de entorno: {nombre_buscado}")
    else:
        nombre_buscado = input("\nEscribe el nombre del agente que quieres consultar: ").strip()

    if not nombre_buscado:
        print("Error: No ingresaste ningun nombre de agente.")
        return

    agente = buscar_agente_por_nombre(agentes, nombre_buscado)

    if agente:
        mostrar_agente(agente)
    else:
        print(f"No se encontro el agente '{nombre_buscado}'.")
        print("Verifica que el nombre este escrito igual que en la lista.")


if __name__ == "__main__":
    main()