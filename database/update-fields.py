import csv
import requests
import os
from dotenv import load_dotenv

# === CONFIGURAÇÕES ===
load_dotenv()
CSV_PATH = r"C:\Users\Luigi\Downloads\atualizacaomodeloeskuid.csv"
API_TOKEN = os.getenv("PIPEFY_API_TOKEN")
FIELD_ID = "ncm"

# === FUNÇÃO PARA ATUALIZAR UM CAMPO ===
def update_field_value(card_id, field_value):
    url = "https://api.pipefy.com/graphql"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    mutation = f"""
    mutation {{
      updateFieldsValues(input: {{
        nodeId: "{card_id}",
        values: [
          {{ fieldId: "{FIELD_ID}", value: "{field_value}" }}
        ]
      }}) {{
        success
        userErrors {{
          field
          message
        }}
        updatedNode {{
          ... on TableRecord {{
            id
          }}
        }}
      }}
    }}
    """

    response = requests.post(url, headers=headers, json={"query": mutation})
    result = response.json()

    if result.get("errors"):
        print(f"❌ Erro ao atualizar {card_id}: {result['errors']}")
    elif result["data"]["updateFieldsValues"]["userErrors"]:
        print(f"⚠️ Erro de validação no {card_id}: {result['data']['updateFieldsValues']['userErrors']}")
    else:
        print(f"✅ Atualizado com sucesso: ID {card_id}")

# === EXECUÇÃO PRINCIPAL ===
with open(CSV_PATH, newline='', encoding='latin1') as f:
    reader = csv.DictReader(f, delimiter=';')  # <- Aqui é o ponto crítico
    print(f"Cabeçalhos encontrados: {reader.fieldnames}")

    for row in reader:
        try:
            card_id = row["card_id"].strip()
            field_value = row["ncm"].strip()
            update_field_value(card_id, field_value)
        except Exception as e:
            print(f"⚠️ Erro inesperado no registro: {row} -> {e}")