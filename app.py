from flask import Flask, render_template, url_for
import os
import re

app = Flask(__name__)

@app.route("/")
def index():
    base_dir = "static/problems"
    anos = {}

    for ano in sorted(os.listdir(base_dir)):
        ano_path = os.path.join(base_dir, ano)
        if not os.path.isdir(ano_path):
            continue

        anos[ano] = {}

        # percorre os níveis (p1, p2, etc)
        for nivel in sorted(os.listdir(ano_path)):
            nivel_path = os.path.join(ano_path, nivel)
            if not os.path.isdir(nivel_path):
                continue

            for arquivo in os.listdir(nivel_path):
                if arquivo.endswith(".pdf"):

                    fase = arquivo.split("_")[1]

                    if fase not in anos[ano]:
                        anos[ano][fase] = {}
                    if nivel not in anos[ano][fase]:
                        anos[ano][fase][nivel] = []
            
            for arquivo in os.listdir(nivel_path):
                if arquivo.endswith(".zip"):    
                    problema = os.path.splitext(arquivo)[0]
                    
                    fase = problema.split("_")[2]

                    try:
                        anos[ano][fase][nivel].append(arquivo)
                    except:
                        anos[ano][fase][nivel] = []
                        anos[ano][fase][nivel].append(arquivo)


    return render_template("index.html", anos=anos)


@app.route("/<ano>/<fase>/<nivel>/<problema>")
def ir_para_problema(ano, fase, nivel, problema):
    # Gera caminhos usando url_for('static')
    pdf_url = url_for('static', filename=f"problems/{ano}/{nivel}/OBI{ano}_{fase}_{nivel.upper()}.pdf")
    zip_url = url_for('static', filename=f"problems/{ano}/{nivel}/{problema}.zip")

    return render_template(
        "problems.html",
        ano=ano, fase=fase, nivel=nivel, problema=problema,
        pdf_url=pdf_url, zip_url=zip_url
    )


if __name__ == "__main__":
    app.run(debug=True)
