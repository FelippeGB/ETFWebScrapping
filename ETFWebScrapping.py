from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

url = "https://www.etf.com/etfanalytics/etf-screener"

driver.get(url)

# Expandindo visualização da tabela para 100 itens

# time.sleep(15)

botao_100 = driver.find_element("xpath", "/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]/div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[5]/button")

driver.execute_script("arguments[0].click();", botao_100)

# Pegando número total de tabelas que o site possuir

numero_paginas = driver.find_element("xpath", "/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]/div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/ul/li[8]/a")
numero_paginas = numero_paginas.text.strip()
numero_paginas = int(numero_paginas)

print(numero_paginas)

# Realizando primeira extração de todos os dados

lista_dados = []

for pagina in range(1, numero_paginas+1):

    tabela = driver.find_element("xpath", "/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]/div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/div[1]/div/div[1]/table")
    html_tabela = tabela.get_attribute("outerHTML")
    tabela_final = pd.read_html(html_tabela)[0]
    
    lista_dados.append(tabela_final)
    
    if pagina < numero_paginas:
        avancar = driver.find_element("xpath", "//a[@class='page-link' and text()='Next']")
        driver.execute_script("arguments[0].click();", avancar)

# Mudando para a aba de performance

botao_performance = driver.find_element("xpath", "/html/body/div[2]/div/div[1]/main/div/section/div[2]/div[2]/div[3]/div/article/div/div[3]/div/div[1]/div/div/div/div[3]/div[2]/div/ul/li[2]")

driver.execute_script("arguments[0].click();", botao_performance)

# Lendo todas as tabelas novamente

lista_performance = []

for pagina in range(1, numero_paginas+1):

    tabela = driver.find_element("xpath", "//table[@id='screener-output-table']")
    html_tabela = tabela.get_attribute("outerHTML")
    tabela_final = pd.read_html(html_tabela)[0]

    lista_performance.append(tabela_final)
    
    if pagina < numero_paginas:
        avancar = driver.find_element("xpath", "//a[@class='page-link' and text()='Next']")
        driver.execute_script("arguments[0].click();", avancar)

#fechando navegador

driver.quit()

# Utilizando o Concat

base_dados = pd.concat(lista_dados, axis=0, join='outer', ignore_index=True)
display(base_dados)

base_performance = pd.concat(lista_performance, axis=0, join='outer', ignore_index=True)
display(base_performance)

# Alternando index para o Ticker do ETF

base_dados = base_dados.set_index("Ticker")
display(base_dados)

base_performance = base_performance.set_index("Ticker")
display(base_performance)

base_dados = base_dados[['Fund Name', 'Segment', 'Expense Ratio', 'AUM']]
base_performance = base_performance[['1 YR', '3 YR', '5 YR', '10 YR']]

display(base_dados)
display(base_performance)

base_completa = base_dados.merge(base_performance, how='inner', on="Ticker")
display(base_completa)

base_completa.to_excel("base_completa.xlsx")
