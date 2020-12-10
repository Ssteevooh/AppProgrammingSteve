from extensions import db


class Storage(db.Model):
    __tablename__ = 'storage'

    storage_id = db.Column(db.Integer, primary_key=True)
    stotage_place = db.Column(db.Integer, nullable=False)
    storage_size = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_all(cls):
        return cls.query.filter_by().all()

    @classmethod
    def get_by_id(cls, storage_id):
        return cls.query.filter_by(storage_id=storage_id).first()

    @classmethod
    def get_by_place(cls, storage_place):
        return cls.query.filter_by(storage_place=storage_place).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
