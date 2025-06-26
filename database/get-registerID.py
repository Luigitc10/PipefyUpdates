import requests 
import csv
import os
from dotenv import load_dotenv

# === CONFIGURAÇÕES ===
load_dotenv()
API_TOKEN = os.getenv("PIPEFY_API_TOKEN")
TABLE_ID = 302876685
URL = "https://api.pipefy.com/graphql"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# === COLETA DE REGISTROS COM PAGINAÇÃO ===
all_records = []
cursor = None

while True:
    after_clause = f', after: "{cursor}"' if cursor else ''
    query = f"""
    {{
      table_records(table_id: {TABLE_ID}, first: 50{after_clause}) {{
        pageInfo {{
          hasNextPage
          endCursor
        }}
        edges {{
          node {{
            id
            title
            record_fields {{
              name
              value
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(URL, headers=headers, json={"query": query})

    try:
        data = response.json()
    except Exception as e:
        print("❌ Erro ao converter resposta para JSON:", e)
        break

    if "errors" in data:
        print("❌ Erro na resposta da API:")
        for erro in data["errors"]:
            print("-", erro.get("message", erro))
        break

    try:
        records = data["data"]["table_records"]["edges"]
        for record in records:
            node = record["node"]
            skuid_value = ""

            for field in node.get("record_fields", []):
                if field["name"].lower() == "skuid (wms)".lower():
                    skuid_value = field.get("value", "")
                    break

            all_records.append({
                "id": node["id"],
                "title": node["title"],
                "skuid": skuid_value
            })

        page_info = data["data"]["table_records"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    except KeyError as e:
        print(f"❌ Estrutura de resposta inesperada. Chave ausente: {e}")
        break

# === SALVAR RESULTADO EM CSV ===
with open("registros_pipefy.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "skuid"])
    for record in all_records:
        writer.writerow([record["id"], record["title"], record["skuid"]])

print(f"✅ {len(all_records)} registros salvos em registros_pipefy.csv")