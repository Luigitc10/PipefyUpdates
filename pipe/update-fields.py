import csv
import requests
import time

# === CONFIGURAÇÕES ===
CSV_PATH = r"C:\Users\Luigi\Downloads\atualizacaomodeloeskuid.csv" # WHERE THE CSV WITH THE VALUES TO UPDATED IS STORED
FIELD_ID_PRECO_FOB = "copy_of_pre_o_atual_fob"  # USE THE CARD ID TO BE UPDATED
API_TOKEN = "TOKEN" # UPDATE HERE WITH YOUR TOKEN
API_URL = "https://api.pipefy.com/graphql" PIPEFY API URL

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
    response = requests.post(API_URL, headers=headers, json={"query": mutation})
    result = response.json()

    if response.status_code != 200 or not result.get("data", {}).get("updateFieldsValues", {}).get("success", False):
        print(f"❌ Erro ao atualizar card {card_id}: {result}")
    else:
        print(f"✅ Card {card_id} atualizado com sucesso.")

# === LEITURA DO CSV ===
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    print("Iniciando atualização...")
    for row in reader:
        print(f"Lendo linha: {row}")
        card_id = row.get("card_id", "").strip() #NAME OF THE COLUMN WITH THE CARD ID
        preco_fob = row.get("preco_tvs_fob", "").strip() #NAME OF THE COLUMN WITH THE VALUE TO UPDATE

        if card_id and preco_fob:
            atualizar_card(card_id, preco_fob)
            time.sleep(0.2)
        else:
            print(f"⚠️ Linha ignorada. card_id: '{card_id}', preco_fob: '{preco_fob}'")
