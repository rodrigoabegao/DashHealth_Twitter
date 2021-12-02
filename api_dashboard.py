from dashboard import dashb

if __name__ == '__main__':
    dash = dashb(48,2021)    # selecionar a semana do ano e o ano 
    app = dash.app
    app.run_server(debug=True)
