from marshmallow import Schema, validate, fields


class GameSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True, validate=[validate.Length(max=500)])
    release_date = fields.Date(required=True)

    company_id = fields.Integer(required=False)
    message = fields.String(dump_only=True)

