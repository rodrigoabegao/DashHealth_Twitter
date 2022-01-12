from pyngrok import ngrok
import os
from dotenv import load_dotenv
load_dotenv()

ngrok.kill()
Auth = os.getenv('Auth_ngrok')
ngrok.set_auth_token(Auth)
http_tunnel = ngrok.connect(8050)
print (ngrok.get_tunnels())