from marshmallow import Schema, fields, validate, ValidationError

# TODO get this from the storage table
storage_free = 10000


def validate_stock(n):
    # TODO calculate stock * size
    if n > storage_free:
        raise ValidationError("No storage space left.")


def validate_price(n):
    if n < 0:
        raise ValidationError("Price cannot be negative.")


def validate_size(n):
    if n < 0:
        raise ValidationError("Size cannot be negative.")


class ProductSchema(Schema):
    class Meta:
        ordered = True

    product_id = fields.Integer(dump_only=True)
    product_name = fields.String(required=True, validate=[validate.Length(max=50)])
    description = fields.String(validate=[validate.Length(max=200)])
    stock = fields.Integer(validate=validate_stock)
    price = fields.Float(validate=validate_price)
    size = fields.Integer(validate=validate_size)
    #created_at = fields.DateTime(dump_only=True)
    #updated_at = fields.DateTime(dump_only=True)
