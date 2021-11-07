from marshmallow import Schema, validate, fields


class GameSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    company_id = fields.Integer(required=False)
    description = fields.String(required=True, validate=[validate.Length(max=500)])
    release_date = fields.Date(required=True)


class CompanySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=250)])
    description = fields.String(required=True, validate=[validate.Length(max=500)])
    founded_date = fields.Date(required=True)

    games = fields.Nested(GameSchema, many=True, dump_only=True)
    message = fields.String(dump_only=True)


class UserSchema(Schema):
    name = fields.String(required=True, validate=[
        validate.Length(max=250)]
                         )
    login = fields.String(required=True, validate=[
        validate.Length(max=250)]
                         )
    password = fields.String(required=True, validate=[
        validate.Length(max=250)], load_only=True
                         )


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
