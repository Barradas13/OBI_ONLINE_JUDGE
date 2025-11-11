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
poetry run python3 webScrap/obiscrap.py // TO SCRAP THE PDFs and ZIPs
poetry run python3 app.py
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

# OBI Online Judge

Um **sistema online de correção de exercícios (online judge)** leve e **de código aberto**, criado para oferecer uma alternativa estável à plataforma oficial **Pratique OBI** — que frequentemente apresenta instabilidade.
Este projeto permite que alunos e professores **pratiquem problemas de programação de edições anteriores da OBI** diretamente por meio de uma interface web simples.

---

## Visão Geral

O OBI Online Judge coleta automaticamente e organiza os **problemas, PDFs e gabaritos (arquivos de resposta)** do **site oficial da OBI**, oferecendo um ambiente independente para visualizar enunciados e testar soluções.

Se algum arquivo parecer ausente ou incorreto, isso ocorre porque o **caminho original no site da OBI estava incorreto** no momento da coleta.

---

## Funcionalidades

* Navegue pelos problemas da OBI por **ano, fase e nível**
* **Barra de busca** para encontrar problemas rapidamente
* Visualização de **enunciados em PDF incorporados**
* Envio e simulação de **submissões de código**
* Suporte para todas as linguagens oficiais da OBI:

  * C (`.c`)
  * C++ (`.cpp`)
  * Pascal (`.pas`)
  * Java (`.java`)
  * Python 3 (`.py`)
  * JavaScript (`.js`)

---

## Executando Localmente (Ambiente de Desenvolvimento)

### 1. Clonar o Repositório

```bash
git clone https://github.com/your-username/obi-online-judge.git
cd obi-online-judge
```

### 2. Instalar Dependências

Usando o **Poetry**:

```bash
poetry install
```

### 3. Executar a Aplicação

```bash
poetry run python3 webScrap/obiscrap.py // PARA COLETAR OS PDFs e ZIPs
poetry run python3 app.py
```

Após iniciar, a interface web estará disponível em:

```
http://localhost:5000
```

---

## Estrutura de Pastas

```
obi-online-judge/
│
├── app.py                 # Aplicação principal Flask
├── static/
│   ├── problems/          # Arquivos de problemas da OBI baixados
├── templates/
│   ├── base.html
│   ├── index.html
│   └── problems.html
├── webScrap/              # Script de coleta e organização dos problemas
│   └── obiScrap.py
└── README.md
```

---

## Notas sobre a Coleta

* O script utiliza `requests` + `BeautifulSoup` para coletar os PDFs e gabaritos de edições anteriores.
* A organização dos arquivos segue o padrão:

  ```
  static/problems/<ano>/<nível>/<arquivos>
  ```
* Se algum problema estiver faltando ou duplicado, geralmente significa que o **link no site da OBI** estava quebrado ou apontava para o arquivo errado.

---

## Licença

Este projeto é open-source sob a **Licença MIT**.
Criado para fins educacionais — **sem afiliação com a OBI (Olimpíada Brasileira de Informática)** oficial.
