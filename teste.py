import json

JSON = {}

with open("./static/obi_problems.json", "r", encoding="utf-8") as f:
    
    json_data = json.load(f)
    JSON = json_data

for ano in JSON:
    for fase in JSON[ano]:
        for nivel in JSON[ano][fase]:
            problemas = JSON[ano][fase][nivel]
            print(f"Ano: {ano} | Fase: {fase} | Nível: {nivel} | Problemas: {list(problemas.keys())}")