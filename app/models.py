from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    records = db.relationship('Record', back_populates='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    records = db.relationship('Record', back_populates='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship('User', back_populates='records')
    category = db.relationship('Category', back_populates='records')

    def __repr__(self):
        return f"<Record {self.id} for User {self.user_id} in Category {self.category_id}>"

class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    code = db.Column(db.String(3), nullable=False, unique=True)

    def __repr__(self):
        return f"<Currency {self.name} ({self.code})>"