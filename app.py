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
        pdf_url=pdf_url, zip_url=zip_url
    )


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

        for file_name in files_list:

            print(f"Processing file: {file_name}")

            
            if not file_name.endswith('/'):
                folder = file_name.split('/')[1]

                test_cases[folder] = test_cases.get(folder, {})
                print(f"Processing file: {file_name}")

                match = re.search(r'\d+', file_name.split('/')[2])

                if match:
                    case_number = int(match.group())

                    test_cases[folder][case_number] = test_cases[folder].get(case_number, {})

                    print(f"Processing number: {case_number}")


                else:
                    case_number = -1
                    test_cases[folder][case_number] = test_cases[folder].get(case_number, {})


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