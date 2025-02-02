import logging
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from .utils import check_imei, is_token_valid

app = Flask(__name__)
api = Api(app, version='1.0', title='IMEI Check API',
    description='A simple IMEI Check API',
)

ns = api.namespace('imei', description='IMEI operations')

imei_model = api.model('IMEI', {
    'imei': fields.String(required=True, description='The IMEI number'),
    'token': fields.String(required=True, description='The API token')
})

@ns.route('/check-imei')
class IMEICheck(Resource):
    @ns.expect(imei_model)
    def post(self):
        data = request.json
        imei = data.get('imei')
        token = data.get('token')

        logger.info(f"Received API request with IMEI {imei} and token {token}")

        if not is_token_valid(token):
            logger.warning(f"Invalid token: {token}")
            return {"error": "Invalid token"}, 401

        if not imei or not imei.isdigit() or len(imei) != 15:
            logger.warning(f"Invalid IMEI format: {imei}")
            return {"error": "Invalid IMEI format"}, 400

        try:
            result = check_imei(imei)
            logger.info(f"Successfully processed IMEI {imei}")
            return result
        except Exception as e:
            logger.error(f"Error processing IMEI {imei}: {e}")
            return {"error": "Internal server error"}, 500

api.add_namespace(ns, path='/api')

if __name__ == '__main__':
    app.run(debug=True)
