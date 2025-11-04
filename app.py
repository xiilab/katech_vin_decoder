import os
import logging
from flask import Flask, redirect, jsonify
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from flask_vin import Flask_vin

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# SUBFOLDER 환경 변수 읽기
SUBFOLDER = os.getenv('SUBFOLDER', '').strip()
if SUBFOLDER:
    # SUBFOLDER가 슬래시로 시작하지 않으면 추가
    if not SUBFOLDER.startswith('/'):
        SUBFOLDER = '/' + SUBFOLDER
    # SUBFOLDER가 슬래시로 끝나면 제거
    SUBFOLDER = SUBFOLDER.rstrip('/')
    logger.info(f"SUBFOLDER 설정됨: {SUBFOLDER}")
else:
    logger.info("SUBFOLDER 미설정 (기본 모드)")

app = Flask(__name__)

# SUBFOLDER가 설정된 경우 APPLICATION_ROOT 설정
if SUBFOLDER:
    app.config['APPLICATION_ROOT'] = SUBFOLDER

api = Api(app, 
          version='0.0.6', 
          title='KADaP (Korea Automotive Data Platform)', 
          description='\n\n KADaP supports 5 types of API. \
                      \n 1. VIN decoder - Decode vehicle identification number.',
          doc='/doc')

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'  # None, list, full
app.config['JSON_AS_ASCII'] = False

api.add_namespace(Flask_vin, '/APIs')

# 헬스체크 엔드포인트
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'subfolder': SUBFOLDER if SUBFOLDER else 'none',
        'version': '0.0.6'
    })

# 루트 경로(/)를 /doc으로 리다이렉트
@app.route('/')
def index():
    if SUBFOLDER:
        # SUBFOLDER가 설정된 경우 절대 경로로 리다이렉트
        logger.info(f"Root path accessed with SUBFOLDER, redirecting to {SUBFOLDER}/doc")
        return redirect(f'{SUBFOLDER}/doc', code=302)
    else:
        # SUBFOLDER가 없는 경우 상대 경로로 리다이렉트
        logger.info(f"Root path accessed, redirecting to /doc")
        return redirect('/doc')

# SUBFOLDER가 설정되어 있으면 DispatcherMiddleware로 서브폴더에 마운트
if SUBFOLDER:
    from werkzeug.wrappers import Response
    import json
    
    # 루트 경로 및 헬스체크 처리
    def handle_root(environ, start_response):
        path = environ.get('PATH_INFO', '/')
        logger.info(f"handle_root called with path: {path}")
        
        # 헬스체크 엔드포인트 - SUBFOLDER 외부에서도 접근 가능
        if path == '/health':
            health_data = json.dumps({
                'status': 'healthy',
                'subfolder': SUBFOLDER,
                'version': '0.0.6'
            })
            response = Response(
                health_data,
                status=200,
                headers=[('Content-Type', 'application/json')]
            )
        elif path == '/':
            # 루트 경로는 SUBFOLDER/doc로 리다이렉트
            response = Response(
                status=302,
                headers=[('Location', f'{SUBFOLDER}/doc')]
            )
        # SUBFOLDER 루트 경로 (슬래시 포함/미포함) 접근 시 /doc으로 리다이렉트
        elif path == SUBFOLDER or path == f'{SUBFOLDER}/':
            logger.info(f"Redirecting SUBFOLDER root to {SUBFOLDER}/doc")
            response = Response(
                status=302,
                headers=[('Location', f'{SUBFOLDER}/doc')]
            )
        else:
            logger.warning(f"Path {path} not matched, returning 404")
            response = Response(
                f'Please access the API at {SUBFOLDER}/doc', 
                status=404
            )
        return response(environ, start_response)
    
    # SUBFOLDER 경로에 Flask 앱 마운트 (슬래시 없는 경로만)
    # SUBFOLDER/ 경로는 handle_root에서 처리하여 무한 리다이렉트 방지
    mounts = {SUBFOLDER: app.wsgi_app}
    
    logger.info(f"DispatcherMiddleware mounts: {list(mounts.keys())}")
    app.wsgi_app = DispatcherMiddleware(handle_root, mounts)
    
    # DispatcherMiddleware 이후에 ProxyFix 적용
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1
    )

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)