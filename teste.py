import pandas as pd

url = 'https://olimpiada.ic.unicamp.br/passadas/OBI2024/cfqmerito//cfobi_p1/'
tables = pd.read_html(url)

tables[0].to_csv('tabela.csv', index=False)

print(tables[0])