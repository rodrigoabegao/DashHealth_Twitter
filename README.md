# 
# __Análise de Tweets Sobre "Sáude" de Sorocaba__

## __Descrição Técnica__
Projeto no qual o objetivo é analisar o conteúdo de tweets sobre saúde na região de Sorocaba e apresentar visualmente em um dashboard os resultados encontrados [em Python3.8](#)

## __Teoria__

## **Arquivo Api_twitter.py e Cap_tweety.py**
Esses arquivos são responsáveis pela captura dos tweets. Foi utilizada uma biblioteca chamada Tweepy, na qual faz a função de acessar a API do Twitter e realizar a captura dos tweets. Como utilizamos uma versão gratuita da API do Twitter (Standard version), podemos somente fazer uma captura de 900 requests a cada 15 minutos, por isso temos uma relativa demora para o término do código.

## **Arquivo Api_dashboard.py e Dashboard.py**
Esses arquivos são responsáveis pela criação do Dashboard, gerado através dos arquivos criados após rodar o arquivo Api_twitter.py. Neste Dashboard são encontradas várias análises em referência das palavras relacionadas ao tema "Saúde" na região de Sorocaba. Utilizamos gráficos como o de barras, de dispersão, nuvem de palavras e etc... Como pode ser visto nas fotos encontradas no anexo **Fotos**.

## **Arquivo Ngrok**
Neste arquivo, é gerado um link para o acesso ao Dashboard, devido ao fato de que quando rodamos a Api_dashboard, é fornecido um link de Local Host. Por esse motivo, não conseguimos ter acesso ao dashboard em outra máquina, para isso, utilizamos o arquivo Ngrok.

### **Python 3 e suas bibliotecas**
[Python 3](https://docs.python.org/3/tutorial/index.html) é uma linguagem de programação, e utiliza identações para diferenciar seu contexto de execução. Neste projeto, ela foi utilizada para obter os dados da API do Twitter e gerar um Dashboard com os resultados obtidos. Neste projeto foram utilizados algumas bibliotecas do Python3: [Dash](https://plotly.com/dash/), [pyngrok](https://pypi.org/project/pyngrok/) e [wordcloud](https://amueller.github.io/word_cloud/). As bibliotecas de mais importancia e seu motivo para serem utilizadas serão explicados mais a frente no passo a passo. 

## __Guia de Instalação__
Instale o requirements.txt:

```
pip install -r requirements.txt
```

## __Guia de Implementação__
Primeiramente, o usuário deve criar uma conta no [Twitter Developer](https://developer.twitter.com/en/portal/dashboard), e depois deve criar um projeto para que possa ser gerado um Consumer Keys e Authentication Tokens como é mostrado abaixo.

> ![twitter_developer](https://user-images.githubusercontent.com/87439511/145449368-ea543944-a2eb-4362-b2d3-8f04a91f48df.png)

Essas informações devem ser colocadas no arquivo api_twitter.py, como é mostrado abaixo.

> ![image](https://user-images.githubusercontent.com/87439511/145450294-d9682a86-78d9-4f5a-b90c-874d5f8444b5.png)

Logo após colocadas essas informações, o usuário deve rodar o api_twitter.py, e será gerados 4 arquivos:

>- Arquivo_compilado_das_semanas_xx_xxxx (x representando a semana do ano e o ano)
>- Arquivo_graficos_da_semana_xx_xxxx (x representando a semana do ano e o ano)
>- Tweets_sorocabanos_pt_xx_xxxx (x representando a semana do ano e o ano)
>- Analise_semana

Logo após o termino da execução, deve ser rodado api_dashboard.py, desta forma, será gerado o Dashboard da semana.
OBS: pode ser selecionado qual semana desejável, basta editar no arquivo, como é mostrado abaixo:

> ![image](https://user-images.githubusercontent.com/87439511/145462260-9cb865b3-52d6-4faa-870b-6e8855821130.png)

> ![image](https://user-images.githubusercontent.com/87439511/145462457-23e1d6fe-d549-49e0-bddb-cc09babbde02.png)

Finalmente, abra um novo terminal e coloque o comando **ngrok http 8050**, e será gerado um link para acessar tanto no pc local quanto em outros computadores, basta usar o link.
> ![image](https://user-images.githubusercontent.com/87439511/145463741-55d5fc9c-95c3-4223-b31a-8c1d650ee7af.png)

## __Fotos__
![WhatsApp Image 2021-12-07 at 15 26 16](https://user-images.githubusercontent.com/87439511/145266062-35e08866-8b88-418a-9f88-7d3008a9e9ca.jpeg)

![grafico de dispersao](https://user-images.githubusercontent.com/87439511/145267200-919db758-b1ee-4f90-bb6f-0bec283a3678.jpeg)

![nuvem de palavra](https://user-images.githubusercontent.com/87439511/145267280-29c1f88f-6588-47c8-8987-fa711f94ed5f.jpeg)

![analise semanal](https://user-images.githubusercontent.com/87439511/145267331-2953bf0c-67b4-484f-a7a4-ba37507162e7.jpeg)
