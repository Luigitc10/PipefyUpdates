import requests
import csv

TOKEN = "Bearer TOKEN" #UPDATE the TOKEN here
TABLE_ID = 302876685 #UPDATE the table ID here
URL = "https://api.pipefy.com/graphql"

headers = {
    "Authorization": "Bearer TOKEN",
    "Content-Type": "application/json"
}

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
          }}
        }}
      }}
    }}
    """
    response = requests.post(URL, headers=headers, json={"query": query})
    data = response.json()

    if "errors" in data:
        print("Erro:", data["errors"])
        break

    records = data["data"]["table_records"]["edges"]
    for record in records:
        all_records.append(record["node"])

    page_info = data["data"]["table_records"]["pageInfo"]
    if not page_info["hasNextPage"]:
        break
    cursor = page_info["endCursor"]

# Salvar CSV após coletar todos os dados
with open("registros_pipefy.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title"])
    for record in all_records:
        writer.writerow([record["id"], record["title"]])
