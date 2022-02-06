from datetime import datetime
from pprint import pprint
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from unidecode import unidecode
from functools import partial


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

def esperar_elemento(webdriver, xpath):
    """
    retorna um booleando indicando se um determinado elemento 
    pertence a pagina.

    :args:
        - webdriver: driver para conectar com o browser
        - xpath: padrao xpath para localizar o elemento
    """
    elementos = webdriver.find_element(By.XPATH,xpath)
    return bool(elementos)

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
wdw = WebDriverWait(driver, timeout = 30)
driver.get(url)

#esperando input
input_xpath = '//*[@id="keyword"]'
input_wait = partial(esperar_elemento, xpath=input_xpath)
wdw.until(input_wait)
#introduzindo o nome "petrobras" no campo de input e clickando em "buscar"
input = driver.find_element(By.XPATH, input_xpath)
input.send_keys('petrobras')
buscar = driver.find_element(By.XPATH,'//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button')
buscar.click()

#esperando petrobras
petr_xpath = '//*[@id="nav-bloco"]/div/div/div/div'
petr_wait = partial(esperar_elemento, xpath=petr_xpath)
wdw.until(petr_wait)
#clickando na caixa que corresponde a petrobras
petr = driver.find_element(By.XPATH, petr_xpath)
petr.click()

#esperando por dados economicos
dados_economicos_xpath = '//*[@id="accordionHeading"]'
dados_economicos_wait = partial(esperar_elemento, xpath=dados_economicos_xpath)
wdw.until(dados_economicos_wait)
#identificando tabela com dados que foram requisitados no desafio
dados_economicos = driver.find_element(By.XPATH, dados_economicos_xpath)
dados_economicos.click()
table = driver.find_element(By.XPATH,'//*[@id="accordionBody"]/div/div[2]/table[1]')
#separando dados de cabecalho da tabela
thead = table.find_element(By.TAG_NAME, 'thead')
head_th = thead.find_elements(By.TAG_NAME,'th')
#separando dados do corpo da tabela
tbody = table.find_element(By.TAG_NAME, 'tbody')
body_tr = tbody.find_elements(By.TAG_NAME, 'tr')

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

