import json
import requests

class Mindicador:
    def __init__(self, indicador, year):
        self.indicador = indicador
        self.year = year

    def get_values(self):
        url = f'https://mindicador.cl/api/{self.indicador}/{self.year}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener valores de la API: {e}")
            return None