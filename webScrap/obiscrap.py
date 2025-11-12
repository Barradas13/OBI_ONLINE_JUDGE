import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OBIJudgeBot/1.0; +https://github.com/felipebarradas)"
}


def pegandoCaminhos():
    BASE_URL = "https://olimpiada.ic.unicamp.br/passadas/"
    anos = list(range(2000, 2006))
    CAMINHOS = [BASE_URL + f"OBI{ano}/programacao/" for ano in anos]

    anos = list(range(2006, 2024))
    for ano in anos:
        CAMINHOS.append(BASE_URL + f"OBI{ano}/fase1/programacao/")
        CAMINHOS.append(BASE_URL + f"OBI{ano}/fase2/programacao/")
        if ano >= 2017:
            CAMINHOS.append(BASE_URL + f"OBI{ano}/fase3/programacao/")

    # URLs de 2024 (estrutura diferente)
    for fase in ("fase1", "fase2", "fase3"):
        CAMINHOS.append(BASE_URL + f"OBI2024/{fase}/programacao/cadernos/")

    return CAMINHOS


def scrape_obi():
    CAMINHOS = pegandoCaminhos()
    JSON = {}
    
    for caminho in CAMINHOS:
        
        ANO = caminho[caminho.find("OBI") + 3: caminho.find("OBI") + 7]
        FASE = caminho[caminho.find("fase"): caminho.find("fase") + 6] if "fase" in caminho else "fase1"
        FASE = FASE.replace("/", "").strip()

        JSON[ANO] = JSON.get(ANO, {})
        JSON[ANO][FASE] = JSON[ANO].get(FASE, {})


        try:
            # PEGA A PAGINA E PASSA PELOS LINKS
            response = requests.get(caminho, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")


            for link in links:
                href = link.get("href")
                if not href:
                    continue

                file_url = urljoin(caminho, href)

                if file_url.find("p1") != -1:
                    NIVEL = "P1"
                elif file_url.find("p2") != -1:
                    NIVEL = "P2"
                elif file_url.find("pu") != -1:
                    NIVEL = "PU"
                elif file_url.find("pj") != -1:
                    NIVEL = "PJ"
                elif file_url.find("p0") != -1:
                    NIVEL = "P0"
                else:
                    continue
                
                JSON[ANO][FASE][NIVEL] = JSON[ANO][FASE].get(NIVEL, {})


                if href.endswith(".pdf"):
                    
                    #download_file(file_url, nivel_dir, f"OBI{ANO}_{FASE}_{NIVEL}.pdf")
                    JSON[ANO][FASE][NIVEL]["pdf"] = file_url
                    
                    pass
                elif href.endswith(".zip") or href.endswith(".rar"):
                    nome = os.path.basename(href)
                    nome = nome.replace(".zip", "").replace(".rar", "")

                    if "_" in nome:
                        nome = nome.split("_")[1]

                    nome_limpo = nome.replace("/", "_")
                    JSON[ANO][FASE][NIVEL][nome_limpo] = file_url
                    

        except Exception as e:
            print(f"[ERRO] Falha ao acessar {caminho}: {e}")
            continue
    return JSON

if __name__ == "__main__":
    JSON = scrape_obi()

    with open("./static/obi_problems.json", "w", encoding="utf-8") as f:
        import json
        json.dump(JSON, f, ensure_ascii=False, indent=4)