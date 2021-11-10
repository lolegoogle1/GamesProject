from flask import jsonify, Blueprint
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required

from ..models import Company
from ..schemas import CompanySchema
from .. import logger


api = Blueprint('api', __name__)


# @doc(tags=['companies'])
@api.route('/companies', methods=['GET'])
@marshal_with(CompanySchema(many=True))
def get_companies():
    try:
        companies = Company.get_companies()
    except Exception as error:
        logger.warning(
            f'Read failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return companies


# @doc(tags=['companies'])
@api.route('/companies', methods=['POST'])
@jwt_required()
@use_kwargs(CompanySchema)
@marshal_with(CompanySchema)
def create_company(**kwargs):
    try:
        new_company = Company(**kwargs)
        new_company.save()
    except Exception as error:
        logger.warning(
            f'Create failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return new_company


# @doc(tags=['companies'])
@api.route('/companies/<int:company_id>', methods=['PUT'])
@jwt_required()
@use_kwargs(CompanySchema)
@marshal_with(CompanySchema)
def update_company(company_id, **kwargs):
    try:
        print('Inside put')
        item = Company.get(company_id)
        item.update(**kwargs)
    except Exception as error:
        logger.warning(
            f'Create failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return item


# @doc(tags=['companies'])
@api.route('/companies/<int:company_id>', methods=['DELETE'])
@jwt_required()
@marshal_with(CompanySchema)
def delete_company(company_id):
    try:
        item = Company.get(company_id)
        item.delete()
    except Exception as error:
        logger.warning(
            f'Delete failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return '', 204


@api.errorhandler(422)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


# docs.register(get_companies, blueprint='api')
# docs.register(update_company, blueprint='api')
# docs.register(create_company, blueprint='api')
# docs.register(delete_company, blueprint='api')
