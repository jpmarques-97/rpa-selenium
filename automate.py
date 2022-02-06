from datetime import datetime
from pprint import pprint
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
from unidecode import unidecode


def str_to_num(num_str):
    """
    transforma um numero em formato str para um numero em formato int.

    :args:
        - num_str: numero em formato string
    """
    number = num_str.replace('.','')
    return int(number)

def format_data(data, strptime):
    """
    transforma a string de data para o formato YYYY-MM-dd.

    :args:
        - data: data em formato de string
        - strfdata: formato ao qual a string esta formatada
    """
    strftime = '%Y-%M-%d'
    datetime_obj = datetime.strptime(data, strptime)
    return datetime_obj.strftime(strftime)

#url correspondendo ao iframe de onde os dados sao realmente retirados
url = 'https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/?language=pt-br'
executable_path = 'chromedriver'

#configuracao de options para mascarar o bot
option = ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument("window-size=1280,800")
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
option.add_argument('--disable-blink-features=AutomationControlled')

#instanciando webdriver e utilizando um GET para a url
driver = Chrome(executable_path=executable_path,options=option)
driver.get(url)

#introduzindo o nome "petrobras" no campo de input e clickando em "buscar"
input = driver.find_element(By.XPATH, '//*[@id="keyword"]')
input.send_keys('petrobras')
buscar = driver.find_element(By.XPATH,'//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button')
buscar.click()
sleep(2)

#clickando na caixa que corresponde a petrobras
petr = driver.find_element(By.XPATH,'//*[@id="nav-bloco"]/div/div/div/div')
petr.click()
sleep(4)

#identificando tabela com dados que foram requisitados no desafio
dados_economicos = driver.find_element(By.XPATH,'//*[@id="accordionHeading"]')
dados_economicos.click()
table = driver.find_element(By.XPATH,'//*[@id="accordionBody"]/div/div[2]/table[1]')

#separando dados de cabecalho da tabela
thead = table.find_element(By.TAG_NAME, 'thead')
head_th = thead.find_elements(By.TAG_NAME,'th')
#separando dados do corpo da tabela
tbody = table.find_element(By.TAG_NAME, 'tbody')
body_tr = tbody.find_elements(By.TAG_NAME, 'tr')
sleep(1)

dicionario = {}

#preenchendo dados conforme requisitado no desafio
dicionario['data'] = format_data(head_th[1].text, '%d/%M/%Y')
for tr in body_tr:
    td = tr.find_elements(By.TAG_NAME, 'td')
    key = unidecode(td[0].text)
    key = key.lower().replace(',', '').replace(' ', '_')
    value = td[1].text
    dicionario[key] = str_to_num(value)

driver.quit()   
pprint(dicionario)

