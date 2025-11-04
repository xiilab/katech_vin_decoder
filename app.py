from flask import Flask
from flask_restx import Api

from flask_vin import Flask_vin

app = Flask(__name__)
api = Api(app, version='0.0.6', title='KADaP (Korea Automotive Data Platform)', 
                                description='\n\n KADaP supports 5 types of API. \
                                            \n 1. VIN decoder - Decode vehicle identification number.' )

app.config.SWAGGER_UI_DOC_EXPANSION = 'list'  # None, list, full
app.config['JSON_AS_ASCII'] = False

api.add_namespace(Flask_vin, '/APIs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)