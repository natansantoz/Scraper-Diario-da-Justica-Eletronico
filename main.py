import datetime
import hashlib 
import sys
import requests
from bs4 import BeautifulSoup
import os


def cria_urls_finais(lista_parametros_urls):
    url_base = "http://www.stf.jus.br/portal/diariojusticaeletronico/verDiarioEletronico.asp?seq="
    lista_urls_finais = []
    for parametro in lista_parametros_urls:
        lista_urls_finais.append(url_base + parametro)
    
    return lista_urls_finais


def baixa_pdf(lista_urls_finais, nomes_cifrados, headers):
    count = 0

    for url in lista_urls_finais:
        response = requests.get(url, headers=headers)

        path = os.path.join('pdfs_output', f'{nomes_cifrados[count]}.pdf')
        
        if not os.path.exists('pdfs_output'):
            os.makedirs('pdfs_output')

        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
        else:
            response.raise_for_status()
        count += 1
    return 0


def get_date():
    date = sys.argv[-1]
    return date


def trata_date(date):
    check = data_validate(date)
    if check != "Data inválida, formato válido: DD-MM-YYYY":
        date = date.replace('-', '/')
        return date
    else: 
        return "Data inválida, formato válido: DD-MM-YYYY" 


def cifra_nomes(nomes):
    nomes_cifrados = []
    for nome in nomes:
        nome = nome.encode()
        hash = hashlib.md5(nome)
        
        hash_em_hexa = hash.hexdigest()
        nomes_cifrados.append(hash_em_hexa)

    return nomes_cifrados


def cria_lista_pdf_names(lista_urls_finais, headers):
    pdfs_names = []
    for url in lista_urls_finais:
        pdfs_names.append(get_pdf_name(url, headers))
    
    return pdfs_names


def get_pdf_name(url, headers):

    response = requests.get(url, headers=headers)
    pdf_name = response.url.split('/')[-1]
    pdf_name = pdf_name.split('.pdf')[0]
    
    return pdf_name


def get_parametros_para_url(response):

    soup = return_soup_object(response)
    lista_params_uteis = []
    
    for tag in soup.findAll('a'):
        if tag['href'].strip() != '#':
            lista_params_uteis.append(tag['href'].strip().split('seq=')[1])
            
    return lista_params_uteis


def do_first_request(data, headers):
    url = f'http://www.stf.jus.br/portal/diariojusticaeletronico/montarDiarioEletronico.asp?tp_pesquisa=0&dataD={data}'
    response = requests.get(url, headers=headers)
    
    return response


def data_validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        return "Data inválida, formato válido: DD-MM-YYYY"


def return_soup_object(response):
    content = response.content
    text = content.decode("utf-8")
    soup = BeautifulSoup(text, 'lxml')

    return soup
    

def salva_hashs_em_arquivo(nomes_cifrados):
    
    for nome in nomes_cifrados:
        path = os.path.join('nomes_cifrados', 'nomes_cifrados.txt')
        
        if not os.path.exists('nomes_cifrados'):
            os.makedirs('nomes_cifrados')

        with open(path, 'a') as file:
            file.write(nome)
            file.write('\n')


def main(data):

    date = trata_date(data)

    if date != "Data inválida, formato válido: DD-MM-YYYY": 

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

        response = do_first_request(date, headers)

        if response.status_code == 200:

            lista_parametros_urls = get_parametros_para_url(response)
            lista_urls_finais = cria_urls_finais(lista_parametros_urls)

            pdfs_names = cria_lista_pdf_names(lista_urls_finais, headers)
            nomes_cifrados = cifra_nomes(pdfs_names)
            
            baixa_pdf(lista_urls_finais, nomes_cifrados, headers)

            salva_hashs_em_arquivo(nomes_cifrados)
            print(nomes_cifrados)
            return nomes_cifrados
        else:
            print("Não foi possivel fazer a requisição")
            return "Não foi possivel fazer a requisição"
    else:
        print("Data inválida, formato válido: DD-MM-YYYY")
        return "Data inválida, formato válido: DD-MM-YYYY"

if __name__ == "__main__":
    data = get_date()
    main(data)
