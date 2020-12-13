from marshmallow import Schema, fields, validate, ValidationError

def validate_role(n):
    if n > 2 or n < 0:
        raise ValidationError("No such role.")


class UserSchema(Schema):
    class Meta:
        ordered = False

    id = fields.Integer(dump_only=True)
    role = fields.Integer(required=True, validate=validate_role)
    username = fields.String(required=True, validate=[validate.Length(max=50)])
    password = fields.String(required=True, validate=[validate.Length(min=4,max=50)])
    is_active = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)