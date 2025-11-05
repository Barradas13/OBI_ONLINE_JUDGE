# OBI Online Judge

A lightweight **open-source online judge** built to provide a stable alternative to the official **Pratique OBI** platform — which often experiences downtime.  
This project allows students and teachers to **practice programming problems from past OBI contests** directly through a simple web interface.

---

## Overview

The OBI Online Judge automatically scrapes and organizes problems, PDFs, and gabaritos (answer files) from the **official OBI website**, providing an independent environment to view statements and test solutions.

If any file appears missing or misplaced, it’s because the **original path on the OBI website was incorrect** at the time of scraping.


## Features

- Browse OBI problems by **year, phase, and level**  
- **Search bar** to find problems quickly  
- Embedded PDF statements  
- Upload and simulate **code submissions**  
- Supports all official OBI languages:
  - C (`.c`)
  - C++ (`.cpp`)
  - Pascal (`.pas`)
  - Java (`.java`)
  - Python 3 (`.py`)
  - JavaScript (`.js`)

---

## Running Locally (Development)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/obi-online-judge.git
cd obi-online-judge
````

### 2. Install Dependencies

Using **Poetry**:

```bash
poetry install
```

### 3. Run the Application 

```bash
poetry python3 webScrap/obiscrap.py // TO SCRAP THE PDFs and ZIPs
poetry python3 app.py
```

Once running, the web interface will be available at:

```
http://localhost:5000
```

---

## Folder Structure

```
obi-online-judge/
│
├── app.py                 # Main Flask app
├── static/
│   ├── problems/          # Downloaded OBI problem files
├── templates/
│   ├── base.html
│   ├── index.html
│   └── problems.html
├── webScrap/   # OBI scraping and organization script
│   └── obiScrap.py
└── README.md
```

---

## Scraping Notes

* The script uses `requests` + `BeautifulSoup` to collect old problem PDFs and gabaritos.
* File organization follows this pattern:

  ```
  static/problems/<year>/<nivel>/<files>
  ```
* If a problem is missing or duplicated, it usually means the **link on the OBI site** was broken or pointed to the wrong file.

---

## License

This project is open-source under the **MIT License**.
Created for educational purposes — not affiliated with the official **OBI (Olimpíada Brasileira de Informática)**.

