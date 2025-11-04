import os
from flask import Flask, redirect
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from flask_vin import Flask_vin

# SUBFOLDER 환경 변수 읽기
SUBFOLDER = os.getenv('SUBFOLDER', '')
if SUBFOLDER:
    # SUBFOLDER가 슬래시로 시작하지 않으면 추가
    if not SUBFOLDER.startswith('/'):
        SUBFOLDER = '/' + SUBFOLDER
    # SUBFOLDER가 슬래시로 끝나면 제거
    SUBFOLDER = SUBFOLDER.rstrip('/')

app = Flask(__name__)

# 리버스 프록시 설정 적용
if SUBFOLDER:
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1
    )

api = Api(app, 
          version='0.0.6', 
          title='KADaP (Korea Automotive Data Platform)', 
          description='\n\n KADaP supports 5 types of API. \
                      \n 1. VIN decoder - Decode vehicle identification number.',
          doc='/doc')

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'  # None, list, full
app.config['JSON_AS_ASCII'] = False

api.add_namespace(Flask_vin, '/APIs')

# 루트 경로(/)를 /doc으로 리다이렉트
@app.route('/')
def index():
    return redirect('/doc')

# SUBFOLDER가 설정되어 있으면 DispatcherMiddleware로 서브폴더에 마운트
if SUBFOLDER:
    from werkzeug.wrappers import Response
    
    # 루트 경로 접근 시 SUBFOLDER/doc로 리다이렉트
    def handle_root(environ, start_response):
        if environ.get('PATH_INFO', '/') == '/':
            response = Response(
                status=302,
                headers=[('Location', f'{SUBFOLDER}/doc')]
            )
        else:
            response = Response(
                f'Please access the API at {SUBFOLDER}/doc', 
                status=404
            )
        return response(environ, start_response)
    
    # SUBFOLDER 경로에 Flask 앱 마운트
    app.wsgi_app = DispatcherMiddleware(handle_root, {
        SUBFOLDER: app.wsgi_app
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)