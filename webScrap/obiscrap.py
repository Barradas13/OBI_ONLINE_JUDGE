import os
import time
import hashlib
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from extract_obi_pdf import pdf_scrap

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
        try:
            print("[INFO] Acessando:", caminho)
            response = requests.get(caminho, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")

            PDF = ""
            GABARITOS = {}

            for link in links:
                href = link.get("href")
                if not href:
                    continue

                file_url = urljoin(caminho, href)

                if href.endswith(".pdf"):
                    PDF = file_url
                elif href.endswith(".zip") or href.endswith(".rar"):
                    nome = os.path.basename(href)
                    nome = nome.replace(".zip", "").replace(".rar", "")
                    if "_" in nome:
                        nome = nome.split("_")[1]
                    GABARITOS[nome.lower()] = file_url

            # Extrair ano e fase
            ANO = caminho[caminho.find("OBI") + 3: caminho.find("OBI") + 7]
            FASE = caminho[caminho.find("fase"): caminho.find("fase") + 6] if "fase" in caminho else "fase1"
            FASE = FASE.replace("/", "").strip()  # 🔧 remove qualquer barra ou espaço extra

            print(GABARITOS)

            # Criar pasta do ano
            ano_dir = os.path.join("./webScrap/downloads/problems", ANO)
            os.makedirs(ano_dir, exist_ok=True)

            # Baixar e processar PDF
            print(f"[INFO] Baixando PDF {PDF}")
            pdf_path = download_file(PDF, ano_dir, f"OBI{ANO}_{FASE}.pdf")

            print(f"ANO: {ANO} | FASE: {FASE}")
            print(f"[INFO] PDF salvo em {pdf_path}")

            for nome, url in GABARITOS.items():
                nome_limpo = nome.replace("/", "_")  # 🔧 segurança extra para nomes com barra
                destino_nome = f"{nome_limpo}_{ANO}_{FASE}_gabarito.zip"
                print(f"[INFO] Baixando gabarito {destino_nome} em {ano_dir}")
                download_file(url, ano_dir, destino_nome)

        except Exception as e:
            print(f"[ERRO] Falha ao acessar {caminho}: {e}")
            continue


if __name__ == "__main__":
    scrape_obi()
