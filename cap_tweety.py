import re
import tweepy
import datetime
import pandas as pd
import numpy as np
import os.path
import spacy
from datetime import date,timedelta
from unidecode import unidecode
from gensim.models import KeyedVectors
from nltk.probability import FreqDist


class Tweety:

  def __init__(self,chave_consumidor,segredo_consumidor,token_acesso,token_acesso_segredo,spacy_model ="pt_core_news_lg"):

    autenticacao = tweepy.OAuthHandler(chave_consumidor, segredo_consumidor)

    autenticacao.set_access_token(token_acesso, token_acesso_segredo)

    self.Api = tweepy.API(autenticacao, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=5, retry_delay=10)

    self.nlp = spacy.load(spacy_model)
    return

  def __limpeza_tweet(self, tweets_text):

    clean_text = re.sub(r'RT+', '', tweets_text) 
    clean_text = re.sub(r'@\S+', '', clean_text)  
    clean_text = re.sub(r'https?\S+', '', clean_text) 
    tweets_text = clean_text.replace("\n", " ")

    return tweets_text

  def search_tweets(self, keyword, count=300, result_type='recent', tweet_mode='extended',time_to_the_past = 6):

    today = datetime.datetime.now()
    today = today.replace(hour=23, minute=59, second=59, microsecond=999999) # set from the beggining of the day
    yesterday = today - datetime.timedelta(time_to_the_past) 
    time_to_the_future = 1
    next_day = yesterday + datetime.timedelta(time_to_the_future) 
    tweets_cursor= tweepy.Cursor(self.Api.search,
                          q=keyword, tweet_mode=tweet_mode,
                          rpp=count, geo = "-23.5019,-47.4578,100km",result_type=result_type,
                          since= yesterday.date(),
                          until = next_day.date(),
                          lang= 'pt',
                          include_entities=True).items(count)

    tweety_data_list = self.preparo_tweets_list(tweets_cursor)
    self.tweets_df = pd.DataFrame(tweety_data_list) 
    self.tweets_df.Date = pd.to_datetime(self.tweets_df['Date'])
    return self.tweets_df

  def preparo_tweets_list(self, tweets_cursor):

    tweets_data_list = []
    for tweet in tweets_cursor:
      if not 'retweeted_status' in dir(tweet):
          tweet_text = self.__limpeza_tweet(tweet.full_text)
          tweets_data = {
              'len' : len(tweet_text),
              'ID' : tweet.id,
              'User' : tweet.user.screen_name,
              'UserName' : tweet.user.name,
              'UserLocation' : tweet.user.location,
              'TweetText' : tweet_text,
              'Language' : tweet.user.lang,
              'Date' : tweet.created_at,
              'Source': tweet.source,
              'Likes' : tweet.favorite_count,
              'Retweets' : tweet.retweet_count,
              'Coordinates' : tweet.coordinates,
              'Place' : tweet.place 
          }
          tweets_data_list.append(tweets_data)
    return tweets_data_list

  def adiciona(self,tweets_csv,tweets_today):
    
    tweets_csv.Date = pd.to_datetime(tweets_csv['Date'])
    tweets_today.Date = pd.to_datetime(tweets_today['Date'])
    tweets_csv = pd.concat([tweets_csv,tweets_today]).drop_duplicates(subset=['TweetText']).sort_values(['Date']).reset_index(drop = True)
    return tweets_csv
  
  def tweets (self, count = 300,dia = 7):
    '''Cont é a quantidade de tweets capturados por palavras, o default é 300 e dia o default é 7'''

    self.dia = dia
    model = KeyedVectors.load_word2vec_format('glove_s100.txt')
    test = model.most_similar('saúde', topn=10)
    test1 = model.most_similar('hospital', topn=10)
    test2 = model.most_similar('doença', topn=10)

    palavras = []
    for i in range(0,9):
      palavras.append(test[i][0])
      palavras.append(test1[i][0])
      palavras.append(test2[i][0])

    self.year, self.week_num, self.day_of_week = date.today().isocalendar()

    palavras = pd.DataFrame(palavras,columns= ['embeddings']).drop_duplicates()
    self.nome_arquivo = "tweets_sorocabanos_pt_{}_{}".format(self.week_num,self.year)
    if not os.path.isfile(self.nome_arquivo):
      aux = open(self.nome_arquivo,'a')
      aux.write("len,ID,User,UserName,UserLocation,TweetText,Language,Date,Source,Likes,Retweets,Coordinates,Place")
      aux.close()

    for i in range(self.dia,0,-1):
          for ind,word in enumerate(palavras.values[:]):
            print("{}, palavra é a {} de {}".format(word,ind+1, len(palavras)))
            keyword = ("{}".format(word))
            dias_no_passado = i
            print("dia: ",i)            
            tweets_soro= pd.read_csv(self.nome_arquivo)
            tweets_df = self.search_tweets(keyword,count = count,time_to_the_past = dias_no_passado).drop_duplicates(subset=['TweetText']).sort_values(['Date']).reset_index(drop = True)
            tweets_soro = self.adiciona(tweets_soro,tweets_df)
            tweets_soro.to_csv(self.nome_arquivo,index = None)
    self.nlp_remove_semanal()
    return

  def arquivo_mensal(self):

    date= datetime.datetime.today()
    self.year, self.week_num, self.day_of_week = date.today().isocalendar()
    for i in range(1,4):
      year_before, semana_passada, day_of_week_before = (date - datetime.timedelta(weeks=i)).isocalendar()
      try:
        if i == 1 :
          year_be, semana_primeira, day_of_week_be = (date - datetime.timedelta(weeks=i-1)).isocalendar()
          arquivo_2 = pd.read_csv("tweets_sorocabanos_pt_{}_{}".format(semana_primeira,year_be))
        arquivo_1 = pd.read_csv("tweets_sorocabanos_pt_{}_{}".format(semana_passada,year_before))
        arquivo_2 = self.adiciona(arquivo_1,arquivo_2)

      except:
        print("não foi possivel encontrar o arquivo tweets_sorocabanos_pt_{}_{}".format(semana_passada,year_before))
    arquivo_2.to_csv("arquivo_compilado_das_semanas_{}_{}".format(self.week_num,self.year), index = None)
    return arquivo_2

  def nlp_remove_semanal(self):

    tweets_soro = self.arquivo_mensal()
    texto = tweets_soro.sample(n=1000,random_state = 5).dropna(subset=['Date']).sort_values(by=['Date'])

    inicial_date =  datetime.datetime.strptime(texto['Date'][:1].item(), '%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame(columns = ['Palavras',"Quantidade","Semana"])
    
    cumprimento= ["boa noite","ola","boa","noite","dia","bom dia","bom","boa tarde","oi","oie","paz e bem","obg","ok","ok!","okay","okey","tranquilo","brigado","brigada","obrigado","obrigada","esta bem","ta bom"]

    for semana in range(1,5):

      filtro = list(filter(lambda a: datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S') >= (inicial_date + timedelta(weeks =semana-1))  and datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S') < inicial_date + timedelta(weeks =semana), texto['Date']))
      date = texto.loc[texto['Date'].isin(filtro)]
      lista_sem_stop = []

      for idx,x in enumerate (date['TweetText']):
        x = unidecode(re.sub(r'[^\w\s(0-9+)]', '',str(x))).strip(" ")
        doc = self.nlp(x)
        for y in doc:
          if not y.is_stop and not (unidecode(str(y)) in cumprimento):
            lista_sem_stop = np.append(lista_sem_stop,str(y))
      lista_sem_stop = list(filter(lambda a: a != "   " and a !=" " and not len(a)<= 3, lista_sem_stop))
      freq = FreqDist(lista_sem_stop)
      data = pd.DataFrame.from_dict(dict(freq.most_common()),orient='index',columns=['Quantidade']).reset_index()
      data.columns = ['Palavras',"Quantidade"]
      data.insert(2, 'Semana', np.full(len(freq),semana))
      df = df.append(data)

    df = df.replace(r'\s+', np.nan, regex=True).dropna(subset=['Palavras']).sort_values(by=['Quantidade'],ascending = False).reset_index(drop=True)
    df.to_csv("arquivo_graficos_da_semana_{}_{}".format(self.week_num,self.year),index = None)
    print("-----------Terminou a execução-----------")
    return