import json

from flask_restx import Resource, Namespace, fields
from flask import make_response

from decoder import Decode

Flask_vin = Namespace('1. VIN-Decoder')

# vin_model = Flask_vin.model('shape', {
#     'country': fields.String(description='제조국'),
#     'manufacturer': fields.String(description='제조사'),
#     'division': fields.String(description='차량구분'),
#     'model': fields.String(description='차종'),
#     'model_series': fields.String(description='세부차종'),
#     'body_style': fields.String(description='차체형상'),
#     'safty_belt': fields.String(description='안전장치'),
#     'displacement': fields.String(description='배기량'),
#     'security_code': fields.String(description='보안코드'),
#     'year': fields.String(description='제작연도'),
#     'plant': fields.String(description='생산공장'),
#     'number': fields.String(description='일련번호')
# })

description = "{ \
  \n'제조국': 'Korea', \
  \n'제조사': 'Hyundai', \
  \n'차량구분': 'Sedan', \
  \n'차종': 'Mid-size', \
  \n'세부차종': 'Advanced', \
  \n'차체형상': 'Number of doors', \
  \n'안전장치': 'Airbag', \
  \n'배기량': '2500cc', \
  \n'보안코드': 'LHD(Left Hand Drive)', \
  \n'제작연도': '2020', \
  \n'생산공장': 'Ulsan, Korea', \
  \n'일련번호': '123456' \
\n}"

parser = Flask_vin.parser()
parser.add_argument('VIN', required=True, help='Vehicle Identification Number')

@Flask_vin.route('/vin-decoder')
@Flask_vin.expect(parser)
@Flask_vin.response(200, description=description)
class VIN_decoder(Resource) :
    def get(self) :
        """
        VIN 해석 API
        ### VIN 입력 시 제조국, 제조사, 차종 등 정보를 json 형태로 제공합니다.
        - eg. KMHEM44CPLU123456
        """
        decode = Decode()
        arg = parser.parse_args()
        
        try :
            vin = arg['VIN']    #kmhem44cplu123456
            result = decode.decoder(vin)
        except :
            result = '잘못된 입력입니다.'

        result = json.dumps(result, ensure_ascii=False)
        return make_response(result)