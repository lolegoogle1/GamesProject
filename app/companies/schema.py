from marshmallow import Schema, validate, fields


class CompanySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=250)])
    description = fields.String(required=True, validate=[validate.Length(max=500)])
    founded_date = fields.Date(required=True)

    games = fields.List(fields.Nested("GameSchema", exclude=("company_id", "id")), dump_only=True)
    message = fields.String(dump_only=True)


"""class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()

    # Make sure to use the 'only' or 'exclude'
    # to avoid infinite recursion
    author = fields.Nested(lambda: AuthorSchema(only=("id", "title")))


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()

    books = fields.List(fields.Nested(BookSchema(exclude=("author",))))"""

# TODO
# problem with lambda in nested
