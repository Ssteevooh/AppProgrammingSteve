from extensions import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    size = db.Column(db.Integer)

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    product_name = db.Column(db.Integer(), db.ForeignKey("product_id"))

    @classmethod
    def get_by_name(cls, product_name):
        return cls.query.filter_by(product_name=product_name).first()

    @classmethod
    def get_by_id(cls, product_id):
        return cls.query.filter_by(id=product_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
