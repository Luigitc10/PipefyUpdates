import csv
import requests
import time

# === CONFIGURAÇÕES ===
CSV_PATH = r"C:\Users\Luigi\Downloads\atualizacaomodeloeskuid.csv"  # Caminho do CSV com os dados
FIELD_ID_PRECO_FOB = "tipo_de_fornecimento"  # ID do campo a ser atualizado
API_URL = "https://api.pipefy.com/graphql"
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv("PIPEFY_API_TOKEN")


headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# === FUNÇÃO PARA ATUALIZAR UM CARD ===
def atualizar_card(card_id, preco_fob):
    print(f"Atualizando card {card_id} com preço FOB {preco_fob}...")

    mutation = f'''
    mutation {{
      updateFieldsValues(input: {{
        nodeId: {card_id},
        values: [
          {{ fieldId: "{FIELD_ID_PRECO_FOB}", value: "{preco_fob}" }}
        ]
      }}) {{
        success
        userErrors {{
          field
          message
        }}
        updatedNode {{
          ... on Card {{
            id
          }}
        }}
      }}
    }}
    '''

    # Tentativas automáticas com retry
    for tentativa in range(3):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json={"query": mutation},
                timeout=10  # Timeout de 10 segundos
            )
            result = response.json()

            if response.status_code != 200 or not result.get("data", {}).get("updateFieldsValues", {}).get("success", False):
                print(f"❌ Erro ao atualizar card {card_id}: {result}")
            else:
                print(f"✅ Card {card_id} atualizado com sucesso.")
            break  # Se deu certo, sai do loop

        except requests.exceptions.ConnectTimeout:
            print(f"⚠️ Tentativa {tentativa+1}: timeout ao atualizar card {card_id}. Retentando em 5 segundos...")
            time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erro inesperado ao atualizar card {card_id}: {e}")
            break

# === LEITURA DO CSV ===
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    print("Iniciando atualização...")
    for row in reader:
        print(f"Lendo linha: {row}")
        card_id = row.get("card_id", "").strip()
        preco_fob = row.get("preco_tvs_fob", "").strip()

        if card_id and preco_fob:
            atualizar_card(card_id, preco_fob)
            time.sleep(0.2)
        else:
            print(f"⚠️ Linha ignorada. card_id: '{card_id}', preco_fob: '{preco_fob}'")
