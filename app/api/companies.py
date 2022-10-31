from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Company
from . import api
from ..responses import bad_request, success, not_found, conflict
from ..exceptions import ValidationError
from sqlalchemy import exc


@api.route('/companies/')
@cross_origin()
def get_companies():
    companies = Company.query.filter(Company.is_active)
    return success({
        "companies": [company.to_json() for company in companies]
    })


@api.route('/companies/<uuid>')
@cross_origin()
def get_company(uuid):
    try:
        company = Company.query.get(uuid)
        if(company):
            return success(company.to_json())
        else:
            return not_found()
    except exc.DataError as de:
        return bad_request("invalid uuid")



@api.route('/companies/', methods=['POST'])
@cross_origin()
def new_company():
    try:
        company = Company.create_from_json(request.json)
        print("company",company.to_json())
        db.session.add(company)
        db.session.commit()
        return success(company.to_json(), 201)
    except ValidationError as ve:
        return bad_request(str(ve))
    except exc.IntegrityError as ie:
        return conflict(str(ie))



@api.route('/companies/<uuid>', methods=['PUT'])
@cross_origin()
def edit_company(uuid):
    try:
        company = Company.query.get(uuid)
        if(company):
            company.update_from_json(request.json)
            db.session.add(company)
            db.session.commit()
            return success(company.to_json())
        else:
            return not_found()
    except exc.DataError as de:
        return bad_request("invalid uuid")
    except ValidationError as ve:
        return bad_request(str(ve))
    except exc.IntegrityError as ie:
        return conflict(str(ie))


@api.route('/companies/<uuid>',methods=['DELETE'])
@cross_origin()
def del_company(uuid):
    try:
        company = Company.query.get(uuid)
        if(company):
            company.soft_delete()
            db.session.add(company)
            db.session.commit()
            return success(company.to_json(), 200, "Successfully deleted")
        else:
            return not_found()
    except exc.DataError as de:
        return bad_request("invalid uuid")