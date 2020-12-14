from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    class Meta:
        ordered = False

    user_id = fields.Integer(dump_only=True)
    role = fields.Integer(default=0)
    username = fields.String(required=True, validate=[validate.Length(max=50)])
    password = fields.String(required=True)
    is_active = fields.Boolean(dump_only=True, default=False)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
