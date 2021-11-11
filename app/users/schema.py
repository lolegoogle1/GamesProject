from marshmallow import Schema, validate, fields


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


