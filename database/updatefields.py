import csv
import requests

# === CONFIGURAÇÕES ===
CSV_PATH = r"C:\Users\Luigi\Downloads\atualizacaomodeloeskuid.csv" # PATH TO THE CSV FILE WITH THE VALUES TO UPDATE 
PIPEFY_TOKEN = "TOKEN"  # INSERT YOUR TOKEN
FIELD_ID = "tipo_de_compra"      # FIELD ID TO BE UPDATED

# === FUNÇÃO DE ATUALIZAÇÃO COM updateFieldsValues ===
def update_field_value(card_id, tipo_valor):
    url = "https://api.pipefy.com/graphql"
    headers = {
        "Authorization": f"Bearer {PIPEFY_TOKEN}",
        "Content-Type": "application/json"
    }

    mutation = f"""
    mutation {{
      updateFieldsValues(input: {{
        nodeId: {card_id},
        values: [
          {{ fieldId: "{FIELD_ID}", value: "{tipo_valor}" }}
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

# === EXECUÇÃO ===
with open(CSV_PATH, newline='', encoding='latin1') as f:
    reader = csv.DictReader(f, delimiter=';')
    print(f"Cabeçalhos encontrados: {reader.fieldnames}")

    for row in reader:
        try:
            card_id = row["Código"].strip()
            tipo = row["tipo"].strip()
            update_field_value(card_id, tipo)
        except Exception as e:
            print(f"⚠️ Erro inesperado no registro: {row} -> {e}")
