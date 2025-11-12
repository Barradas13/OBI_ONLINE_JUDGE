from flask import Flask, render_template, url_for, jsonify
import os
import re
import json
import requests
import zipfile
import io


app = Flask(__name__)

JSON = {}

with open("./static/obi_problems.json", "r", encoding="utf-8") as f:
        
    json_data = json.load(f)
    JSON = json_data

@app.route("/")
def index():

    return render_template("index.html", anos=JSON)


@app.route("/<ano>/<fase>/<nivel>/<problema>")
def ir_para_problema(ano, fase, nivel, problema):
    # Get PDF URL and ZIP URL from JSON
    pdf_url = JSON[ano][fase][nivel].get('pdf', '')
    zip_url = JSON[ano][fase][nivel].get(problema, '')

    return render_template(
        "problems.html",
        ano=ano, fase=fase, nivel=nivel, problema=problema,
        pdf_url=pdf_url, zip_url=zip_url, JUDGE_URL="https://judge.darlon.com.br"
    )

import re
from pathlib import Path

import re
from pathlib import Path
from collections import defaultdict

def organize_test_files(paths: list[str]) -> list[str]:
    """
    Ordena e agrupa arquivos de testes (.in/.out/.sol ou entrada/saida)
    em formato compacto, como:
        .../teste1/1in, .../teste1/1out, .../teste1/2in, .../teste1/2out
    """
    # === Função auxiliar para extrair chave de agrupamento ===
    def extract_info(p: str):
        path = Path(p)
        name = path.name.lower()

        # tenta extrair números no caminho
        nums = [int(n) for n in re.findall(r'\d+', str(path))]
        test_num = nums[0] if nums else -1
        file_num = nums[-1] if nums else -1

        # tipo do arquivo (entrada, saída ou outro)
        if any(k in name for k in ["in", "entrada", ".in"]):
            io_type = "in"
        elif any(k in name for k in ["out", "saida", ".sol", ".out"]):
            io_type = "out"
        else:
            io_type = "?"

        return test_num, file_num, io_type, str(path)

    # === Agrupa por pasta base do teste ===
    groups = defaultdict(list)
    for p in paths:
        if p.endswith('/'):
            continue
        info = extract_info(p)
        parent = str(Path(p).parent)
        groups[parent].append(info)

    # === Ordena e monta a lista final ===
    final = []
    for parent, items in sorted(groups.items()):
        # ordena por número de arquivo e tipo (in antes de out)
        items.sort(key=lambda x: (x[1], 0 if x[2] == "in" else 1))
        for _, _, _, fullpath in items:
            final.append(fullpath)

    return final




@app.route("/api/get_test_cases/<ano>/<fase>/<nivel>/<problema>")
def get_test_cases(ano, fase, nivel, problema):
    """Download and extract test cases from ZIP URL"""
    try:
        zip_url = JSON[ano][fase][nivel].get(problema, '')
        
        if not zip_url:
            return jsonify({"error": "ZIP URL not found"}), 404
        
        # Download the ZIP file
        response = requests.get(zip_url, timeout=10)
        response.raise_for_status()
        
        # Extract to memory
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        
        # Get list of files
        files_list = zip_file.namelist()
        
        test_cases = {}

        sorted_files = organize_test_files(files_list)

        j = 0

        for i in range(0, len(sorted_files), 2):
            file_in = sorted_files[i]
            file_out = sorted_files[i + 1]

            test_cases[j] = {
                "input": zip_file.read(file_in).decode('utf-8'),
                "output": zip_file.read(file_out).decode('utf-8'),
            }

            j+= 1

        return jsonify({
            "success": True,
            "files": test_cases,
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to download ZIP: {str(e)}"}), 500
    except zipfile.BadZipFile:
        return jsonify({"error": "Invalid ZIP file"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)