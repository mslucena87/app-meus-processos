import requests
import os

class DataJudClient:
    BASE_URL = "https://api-publica.datajud.cnj.jus.br"

    def __init__(self):
        self.api_key = os.getenv("DATAJUD_API_KEY", "")
        self.headers = {
            "Authorization": f"APIKey {self.api_key}",
            "Content-Type": "application/json"
        }

    def buscar_por_oab(self, oab_numero: str, oab_uf: str, tribunal: str = "tjsp") -> list[dict]:
        url = f"{self.BASE_URL}/api_publica_{tribunal.lower()}/_search"
        payload = {
            "size": 50,
            "query": {
                "match": {
                    "advogado.numeroOab": oab_numero
                }
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            hits = response.json().get("hits", {}).get("hits", [])
            return [hit["_source"] for hit in hits]
        except Exception:
            return []