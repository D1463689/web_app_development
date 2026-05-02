from datetime import datetime
from . import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    category = db.Column(db.String(100))
    status = db.Column(db.String(50), nullable=False, default='unread')
    rating = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'status': self.status,
            'rating': self.rating,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    # --- CRUD 方法封裝 ---

    @classmethod
    def get_all(cls):
        """取得所有書籍，依建立時間反序排列"""
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, book_id):
        """根據 ID 取得書籍"""
        return cls.query.get(book_id)

    @classmethod
    def create(cls, **kwargs):
        """建立新書籍並儲存到資料庫"""
        book = cls(**kwargs)
        db.session.add(book)
        db.session.commit()
        return book

    def update(self, **kwargs):
        """更新書籍屬性並儲存到資料庫"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        """從資料庫刪除此書籍"""
        db.session.delete(self)
        db.session.commit()
