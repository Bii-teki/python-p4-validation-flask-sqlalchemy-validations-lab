from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('name')
    def validate_name(self, key, name):
        if name is None or name.strip() == '':
            raise ValueError("Name is required")
        
        if name and Author.query.filter_by(name=name).first():
            raise ValueError("Name already exists")
        return name
    
    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        phone_pattern = r'^\d{10}$'
        if not re.match(phone_pattern, phone_number):
            raise ValueError("Phone number is not in a valid format")
        return phone_number
            

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content should have at least 250 characters.")
        return content
    
    @validates('summary')
    def validate_content(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("More than 250 chars")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):      
        valid_categories = ['category1', 'category2', 'category3']
        if category not in valid_categories:
            raise ValueError("Invalid category")
        return category 

    @validates('title')
    def validate_title(self, key, title):
        if title is None or title.strip() == '':
           raise ValueError("Title is required")
    
        forbidden_words = ['clickbait', 'sensational']
        if any(word in title.lower() for word in forbidden_words):
            raise ValueError("Title should not contain forbidden words.")
        return title



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
