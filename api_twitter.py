from cap_tweety import Tweety
import os
import requests 
from zipfile import ZipFile

#Colocar as informações da Api do Twitter(deve ser feito uma conta na API do TWITTER para ter acesso a ele)

chave_consumidor = ' '
segredo_consumidor = ' '
token_acesso = ' '
token_acesso_segredo = ' '

analise = Tweety(chave_consumidor, segredo_consumidor, 
token_acesso, token_acesso_segredo)

def baixar_arquivo(url, endereco):
    resposta = requests.get(url, stream=True)
    print("Download Inicializado")
    if resposta.status_code == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
                for parte in resposta.iter_content(chunk_size=256):
                    novo_arquivo.write(parte)
        print("Download finalizado. Arquivo salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()
    return

if not os.path.isfile("glove.zip") or not os.path.isfile("glove_s100.txt"):

    remote_url = 'http://143.107.183.175:22980/download.php?file=embeddings/glove/glove_s100.zip'
    local_file = 'glove.zip'
    baixar_arquivo(remote_url,local_file)
    zf = ZipFile('glove.zip', 'r')
    zf.extractall('')
    zf.close()
analise.tweets(count = 300,dia = 7)    #selecione a quantidade de tweets por palavras relacionadas e pode selecinar os dias que quer executar
