import sys
import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

def consultar_diario_oficial(termo_busca, dias_limite):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        url_busca = 'https://imprensaoficial.com.br'
        driver.get(url_busca)
        time.sleep(5)
        campo_busca = driver.find_element(By.ID,'content_txtPalavrasChave')
        campo_busca.clear()
        campo_busca.send_keys(termo_busca)

        botao_pesquisar = driver.find_element(By.ID, 'content_btnBuscar')
        botao_pesquisar.click()
        time.sleep(5)

        conteudo_pagina = driver.page_source

        if "Nenhum resultado" in conteudo_pagina or "0 resultado" in conteudo_pagina:
            print(f'Status: sem novidades para o termo "{termo_busca}".')
            return False

        xpath_resultados = "//a[contains(text(), 'Diário Oficial')]"
        links_resultado = driver.find_elements(By.XPATH, xpath_resultados)
        publicacoes_recentes = 0
        data_limite = datetime.now() - timedelta(days=dias_limite)

        for link in links_resultado:
            texto_link  = link.text

            try:
                string_data = texto_link.split(' - ')[0].strip()
                data_publicacao = datetime.strptime(string_data, '%d/%m/%Y')
                
                if data_publicacao >= data_limite:
                    print(f'ENCONTRADO! Publicação recente identificada em {string_data}')
                    print(f'Trecho: {texto_link}')
                    publicacoes_recentes += 1
                else:
                    print(f'Filtro: Publicação antiga ignorada ({string_data}).')
            except Exception as e:
                continue

        if publicacoes_recentes > 0:
            print(f'Sucesso: Total de {publicacoes_recentes} publicações nos últimos {dias_limite} dias foram encontradas.')
            return True

        else:
            print(f'Status: Foram achados alguns resultados para o termo, mas nenhum é dos últimos {dias_limite} dias.')
            return False

    except Exception as e:
        print(f'Ocorreu um erro ao tentar rodar o scrapper: {e}.')
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    load_dotenv()
    MEU_PROTOCOLO = os.getenv("MEU_PROTOCOLO")
    MEU_NOME = os.getenv("MEU_NOME")

    if not MEU_NOME:
        print('Erro: A variável "MEU_NOME" não foi encontrada!')
        sys.exit(1)

        dias_filtro = 5

    if len(sys.argv) > 1:
        try:
            dias_filtro = int(sys.argv[1])
        except ValueError:
            print('AVISO: O argumeto passado não é um número válido. Usando o valor padrão de 5 dias.')

    print(f'Iniciando a busca para o termo informado. Filtrando publicações dos últimos {dias_filtro} dias...')

    consultar_diario_oficial(MEU_NOME, dias_limite=dias_filtro)
