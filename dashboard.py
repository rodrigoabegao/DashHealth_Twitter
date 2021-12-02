import dash
import dash.dependencies as dd
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from io import BytesIO
from wordcloud import WordCloud
import base64


class dashb:

  def __init__(self,semana,ano):

    self.semana = semana
    self.ano = ano
    tweets_soro= pd.read_csv("arquivo_compilado_das_semanas_{}_{}".format(self.semana,self.ano)).dropna(subset=['Date']).sort_values(by=['Date'])

    df = pd.read_csv("arquivo_graficos_da_semana_{}_{}".format(self.semana,self.ano)).replace(r'\s+', np.nan, regex=True).dropna(subset=['Palavras']).sort_values(by=['Quantidade'],ascending = False).reset_index(drop=True)

    analise = pd.DataFrame(columns= ['Palavras','Quantidade','Semana'])
    for i in range(1,5):
      t = df[(df['Semana'] == i)].sort_values(by=['Quantidade'],ascending=False).reset_index(drop=True)[:10]
      analise = analise.append(t).reset_index(drop=True)
    analise.to_excel('analise_semana.xls',index=None)

    BS = "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sandstone/bootstrap.min.css"

    app = dash.Dash(__name__,external_stylesheets=[BS], suppress_callback_exceptions=True)

    df_graficos = df.groupby(['Palavras'])["Quantidade"].sum().reset_index().sort_values(by=["Quantidade"],ascending = False)
    fig = px.bar(df_graficos[:10], x="Palavras", y="Quantidade", color="Palavras", barmode="group",title='As 10 palavras mais usadas no tema saúde').update_layout(showlegend=False)

    scatter_fig = px.scatter(
        df_graficos[:20], x="Palavras", y="Quantidade", size="Quantidade", color="Palavras",size_max=50, title= "Gráfico de dispersão sobre as palavras mais usadas em relação sobre saúde"
    ).update_traces(marker_opacity=0.8).update_layout(showlegend=False)


    @app.callback(dd.Output("graph_semana", "figure"),[ dd.Input('semanas','value')])

    def update_graph_semana(semanas):

      palavras = df[((df['Semana']>=semanas[0]) & (df['Semana']<=semanas[1]))].groupby(['Palavras']).sum().sort_values(by=['Quantidade'],ascending=False).reset_index()['Palavras'][:10].values
      data = df[((df['Semana']>=semanas[0]) & (df['Semana']<=semanas[1]))].loc[df['Palavras'].isin(palavras)].sort_values(by= ['Semana'],ascending = False).reset_index(drop=True)
      figure = px.line(data, x='Semana', y='Quantidade', color='Palavras', symbol="Palavras", title= "Gráfico das 10 palavras mais usadas em relação sobre saúde")
      return figure

    def plot_wordcloud(data):

      d = {a: x for a, x in data.values}
      wc = WordCloud(background_color='black', width=900, height=700)
      wc.fit_words(d)
      return wc.to_image()

    @app.callback(dd.Output('image_wc', 'src'), [dd.Input('image_wc', 'id')])

    def make_image(b):
      
      img = BytesIO()
      plot_wordcloud(data=df_graficos).save(img, format='PNG')
      return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

    heading = html.Div(
          [
            html.Div(
                [
                  html.H1("HealthDash", className="bg-primary text-white p-2", 
                  style = {'textAlign': 'center',
                                        'fontFamily': 'Roboto', 
                                        'paddingTop': 20}),
                  html.Div('''

                  DashBoard criado para apresentar visualmente uma analise de tweets relacionado sobre o tema "saúde" na região de Sorocaba.

                  ''',
                  style={'color': 'black', 'fontSize': 22})
                ]
              ),

          ]        
    )

    tab1_content = dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                      dcc.Graph(figure=fig)
                    ]
                    ),
            ],
        ),
        className="mt-3",
    )

    tab2_content = dbc.Card(
        dbc.CardBody(
            [
              dcc.Graph(figure=scatter_fig)
            ]
        ),
        className="mt-3",
    )

    tab3_content = dbc.Card(
        dbc.CardBody(
            [
              html.Img(id="image_wc")
            ]
        ),
        className="mt-3",
    )

    tab4_content = dbc.Card(
        dbc.CardBody(
            [
              
              dcc.Graph(id="graph_semana"),
              html.P("Selecione a semana desejavel:"),
              dcc.RangeSlider(
                    id="semanas",
                    marks={i: 'Semana{}'.format(i) for i in range(1, 5)},
                    min=1,
                    max=4,
                    value=[1, 4]
                    )
            ]
        ),
        className="mt-3",
    )


    tabs = html.Div(
        [
          dbc.Tabs(
            [
              dbc.Tab(tab1_content, label="Gráfico de Barras"),
              dbc.Tab(tab2_content, label="Gráfico de Dispersão"),
              dbc.Tab(tab3_content, label="Nuvem de Palavras"),
              dbc.Tab(tab4_content, label="Analise Semanal"),
            ]
          ),
          html.Div(
            [
              html.Div("Pesquisa referente do dia {} até {}".format("".join([str(_) for _ in tweets_soro['Date'].sort_values()[:1].values]),"".join([str(_) for _ in tweets_soro['Date'].sort_values()[-1:].values])),
              style={'color': 'black', 'fontSize': 22})
            ]
        )
        ]
    )

    app.layout = dbc.Container(fluid=True, children=[heading, tabs])
    self.app = app
