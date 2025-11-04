from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route("/")
def index():
    files = os.listdir("static/problems")
    anos = {}

    files.sort()
    for ano in files:
        anos[ano] = {}
        for raiz, pastas, arquivos in os.walk(f"./static/problems/{ano}"):
            for arquivo in arquivos:
                if arquivo.endswith(".pdf"):
                    anos[ano][arquivo.split("_")[1][:-4]] = []
        for raiz, pastas, arquivos in os.walk(f"./static/problems/{ano}"):
            for arquivo in arquivos:
                if arquivo.endswith(".zip"):
                    fase = arquivo.split("_")[2]
                    anos[ano].setdefault(fase, []).append(arquivo.split("_")[0])
    
    return render_template("index.html", anos=anos)


@app.route("/<ano>/<fase>/<problema>")
def ir_para_problema(ano, fase, problema):
    # Gera os caminhos certos usando url_for('static')
    pdf_url = url_for('static', filename=f"problems/{ano}/OBI{ano}_{fase}.pdf")
    zip_url = url_for('static', filename=f"problems/{ano}/{problema}_{ano}_{fase}_gabarito.pdf")

    print(pdf_url)  # só pra depurar
    return render_template("problems.html", ano=ano, fase=fase, problema=problema,
                           pdf_url=pdf_url, zip_url=zip_url)


if __name__ == "__main__":
    app.run(debug=True)
