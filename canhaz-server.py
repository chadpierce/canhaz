from flask import Flask, request
import logging
import datetime

# responds with client IP

'''
# nginx server reverse proxy config

    location / {
        proxy_set_header Host $host;
        #proxy_set_header X-Real-IP $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:5000/;
    }
'''

app = Flask(__name__)

logging.basicConfig(filename='request.log', level=logging.INFO)

# quick and dirty logging - this func will run before route is accessed 
@app.before_request
def log_request_info():
    #client_ip = request.remote_addr  # use if accessing directly
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    if request.path != '/' or request.method != 'GET':
        app.logger.info('\n\n##INVALID!!\nClient IP: %s', client_ip)
        app.logger.info('Request:\n %s', request)
        print(f"!NOTHAZ {datetime.datetime.now()} {client_ip}")
    else:
        app.logger.info('\n\n###########\nClient IP: %s', client_ip)
        app.logger.info('Request:\n %s', request)
        print(f"_CANHAZ {datetime.datetime.now()} {client_ip}")

@app.route('/')
def display_ip():
    #client_ip = request.remote_addr  # use if accessing directly
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    return f'{client_ip}\n'

@app.route('/<path:path>')
def catch_all(path):
    return 'URL does not exist', 404

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)  # use if accessing directly
    app.run(host='127.0.0.1', port=5000) # use if proxied 
