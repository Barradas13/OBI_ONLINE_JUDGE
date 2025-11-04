import io
import re
import requests
import pdfplumber
from tqdm import tqdm
from PyPDF2 import PdfWriter, PdfReader
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OBIJudgeBot/1.0; +https://github.com/felipebarradas)"
}

# Regex melhorado para identificar início de um problema
TITLE_PATTERN = re.compile(
    r"^(.+)\n0\nArquivo fonte:",
    re.MULTILINE
)


def save_problem_pdf(pdf_bytes, pages, title, year):
    """Salva um subconjunto de páginas do PDF em disco."""
    output = PdfWriter()
    
    # Limpa o título para usar como nome de diretório
    clean_title = re.sub(r'[<>:"/\\|?*]', '', title).strip()
    os.makedirs(f"webScrap/downloads/problems/{year}/{clean_title}", exist_ok=True)
    
    output_filename = f"{year}_{clean_title.replace(' ', '_').lower()}.pdf"
    outpath = f"./webScrap/downloads/problems/{year}/{clean_title}/{output_filename}"

    reader = PdfReader(pdf_bytes)
    for page_num in pages:
        output.add_page(reader.pages[page_num])

    with open(outpath, "wb") as f:
        output.write(f)

    return outpath


def pdf_scrap(pdf_url: str):
    """
    Lê um PDF da OBI, identifica cada problema, e salva PDFs separados.
    Retorna lista de dicionários: {title, pages, file}
    """
    print(f"[INFO] Baixando PDF de {pdf_url} ...")
    response = requests.get(pdf_url, headers=HEADERS, stream=True, timeout=30)
    response.raise_for_status()
    pdf_bytes = io.BytesIO(response.content)

    problems = []
    pages_text = []
    with pdfplumber.open(pdf_bytes) as pdf:
        for i, page in enumerate(tqdm(pdf.pages, desc="Lendo páginas")):
            text = page.extract_text() or ""
            pages_text.append((i, text))

    print("[DEBUG] Texto extraído das páginas:")
    for i, text in pages_text:
        print(f"--- Página {i} ---")
        print(text[:200] + "..." if len(text) > 200 else text)
        print()

    # Detecta linhas que indicam títulos
    titles_found = []
    for i, text in pages_text:
        matches = TITLE_PATTERN.findall(text)
        for match in matches:
            title = match.strip()
            # Filtra falsos positivos
            excluded_keywords = ["OBI", "CADERNO", "Sociedade", "LEIA ATENTAMENTE", "RESTRIÇÕES", "EXEMPLO"]
            if (len(title) > 3 and 
                not any(keyword in title.upper() for keyword in excluded_keywords) and
                not title.upper().isupper()):  # Evita títulos totalmente em maiúsculo
                titles_found.append((title, i))
                print(f"[DEBUG] Título encontrado: '{title}' na página {i}")

    if not titles_found:
        print("[AVISO] Nenhum título detectado. Tentando padrão alternativo...")
        # Tentativa com padrão alternativo
        for i, text in pages_text:
            lines = text.split('\n')
            for j, line in enumerate(lines):
                if (line.strip().endswith('0') and j + 1 < len(lines) and 
                    'Arquivo fonte:' in lines[j + 1]):
                    title = lines[j - 1].strip() if j > 0 else lines[j].strip()
                    if title and len(title) > 3:
                        titles_found.append((title, i))
                        print(f"[DEBUG ALT] Título encontrado: '{title}' na página {i}")

    if not titles_found:
        print("[AVISO] Nenhum título detectado após tentativa alternativa.")
        return []

    # Remove duplicatas e ordena por página
    titles_found = sorted(list(set(titles_found)), key=lambda x: x[1])
    
    print(f"[INFO] {len(titles_found)} títulos encontrados:")
    for title, page in titles_found:
        print(f"  - '{title}' (página {page})")

    # Define intervalos de páginas de cada problema
    for idx, (title, start_page) in enumerate(titles_found):
        end_page = (
            titles_found[idx + 1][1] - 1 if idx + 1 < len(titles_found) else len(pages_text) - 1
        )
        problems.append({"title": title, "pages": list(range(start_page, end_page + 1))})
        print(f"[INFO] Problema '{title}': páginas {start_page} a {end_page}")

    # Extrai ano (caso esteja no link)
    match_year = re.search(r"OBI(\d{4})", pdf_url)
    year = match_year.group(1) if match_year else "unknown"

    # Salva PDFs separados
    results = []
    for p in problems:
        print(f"[INFO] Salvando problema: {p['title']}")
        path = save_problem_pdf(io.BytesIO(response.content), p["pages"], p["title"], year)
        results.append({"title": p["title"], "pages": p["pages"], "file": path})

    print(f"[INFO] {len(results)} problemas salvos em ./webScrap/downloads/problems/")
    
    return results

