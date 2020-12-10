from marshmallow import Schema, fields, validate, ValidationError

storage_size = 100


def validate_place(n):
    if n < 0:
        raise ValidationError("Storage place must not be negative")


def validate_size(n):
    if n > storage_size:
        raise ValidationError("Size of the storage is maxed out")
    elif n < 0:
        raise ValidationError("Size of the storage cannot be negative.")


class StorageSchema(Schema):
    class Meta:
        ordered = True

    storage_id = fields.Integer(dump_only=True)
    storage_place = fields.Integer(validate=validate_place)
    storage_size = fields.Integer(validate=validate_size)
    description = fields.String(validate=[validate.Length(max=200)])

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
