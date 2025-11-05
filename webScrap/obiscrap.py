import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OBIJudgeBot/1.0; +https://github.com/felipebarradas)"
}

# ============= FUNÇÕES AUXILIARES =============

def download_file(url: str, dest_folder: str, nome: str):
    """Baixa um arquivo e salva em uma pasta."""
    try:
        os.makedirs(dest_folder, exist_ok=True)

        filepath = os.path.join(dest_folder, nome)
        
        if os.path.exists(filepath):
            return filepath  # já baixado

        with requests.get(url, headers=HEADERS, stream=True, timeout=20) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            with open(filepath, "wb") as f, tqdm(
                total=total, unit="B", unit_scale=True, desc=nome
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
        return filepath

    except Exception as e:
        print(f"[ERRO] Falha ao baixar {url}: {e}")
        return None


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
    
    for caminho in CAMINHOS:
        
        ANO = caminho[caminho.find("OBI") + 3: caminho.find("OBI") + 7]
        FASE = caminho[caminho.find("fase"): caminho.find("fase") + 6] if "fase" in caminho else "fase1"
        FASE = FASE.replace("/", "").strip()

        try:
            # PEGA A PAGINA E PASSA PELOS LINKS
            response = requests.get(caminho, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")

            PDF = []
            GABARITOS = {}

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
                else:
                    continue

                ano_dir = os.path.join("./static/problems", ANO)
                nivel_dir = os.path.join(f"./static/problems/{ANO}", NIVEL)

                os.makedirs(ano_dir, exist_ok=True)
                os.makedirs(nivel_dir, exist_ok=True)

                if href.endswith(".pdf"):

                    download_file(file_url, nivel_dir, f"OBI{ANO}_{FASE}_{NIVEL}.pdf")

                elif href.endswith(".zip") or href.endswith(".rar"):
                    nome = os.path.basename(href)
                    nome = nome.replace(".zip", "").replace(".rar", "")

                    if "_" in nome:
                        nome = nome.split("_")[1]

                    nome_limpo = nome.replace("/", "_")
                    destino_nome = f"{nome_limpo}_{ANO}_{FASE}_{NIVEL}_gabarito.zip"
                    download_file(file_url, nivel_dir, destino_nome)

        except Exception as e:
            print(f"[ERRO] Falha ao acessar {caminho}: {e}")
            continue


if __name__ == "__main__":
    scrape_obi()
