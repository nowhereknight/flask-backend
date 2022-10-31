from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask import current_app, request, url_for
from . import db
from .validators import validate_post_company, validate_put_company
from .exceptions import ValidationError
from .utils import is_symbol_available



# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     body_html = db.Column(db.Text)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     comments = db.relationship('Comment', backref='post', lazy='dynamic')

#     @staticmethod
#     def on_changed_body(target, value, oldvalue, initiator):
#         allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
#                         'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
#                         'h1', 'h2', 'h3', 'p']
#         target.body_html = bleach.linkify(bleach.clean(
#             markdown(value, output_format='html'),
#             tags=allowed_tags, strip=True))

#     def to_json(self):
#         json_post = {
#             'url': url_for('api.get_post', id=self.id),
#             'body': self.body,
#             'body_html': self.body_html,
#             'timestamp': self.timestamp,
#             'author_url': url_for('api.get_user', id=self.author_id),
#             'comments_url': url_for('api.get_post_comments', id=self.id),
#             'comment_count': self.comments.count()
#         }
#         return json_post

#     @staticmethod
#     def from_json(json_post):
#         body = json_post.get('body')
#         if body is None or body == '':
#             raise ValidationError('post does not have a body')
#         return Post(body=body)


#db.event.listen(Post.body, 'set', Post.on_changed_body)


# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     body_html = db.Column(db.Text)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     disabled = db.Column(db.Boolean)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

#     @staticmethod
#     def on_changed_body(target, value, oldvalue, initiator):
#         allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
#                         'strong']
#         target.body_html = bleach.linkify(bleach.clean(
#             markdown(value, output_format='html'),
#             tags=allowed_tags, strip=True))

#     def to_json(self):
#         json_comment = {
#             'url': url_for('api.get_comment', id=self.id),
#             'post_url': url_for('api.get_post', id=self.post_id),
#             'body': self.body,
#             'body_html': self.body_html,
#             'timestamp': self.timestamp,
#             'author_url': url_for('api.get_user', id=self.author_id),
#         }
#         return json_comment

#     @staticmethod
#     def from_json(json_comment):
#         body = json_comment.get('body')
#         if body is None or body == '':
#             raise ValidationError('comment does not have a body')
#         return Comment(body=body)


# db.event.listen(Comment.body, 'set', Comment.on_changed_body)


class Company(db.Model):
    __tablename__ = 'companies'
    company_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = db.Column(db.Text)
    description = db.Column(db.Text)
    symbol = db.Column(db.Text)
    market_values = db.Column(db.ARRAY(db.Integer))
    is_active = db.Column(db.Boolean, default=True)


    def __init__(self, data):
        self.company_name=data['name']
        self.description=data['description']
        self.symbol=data['symbol']
    
    @staticmethod
    def create_from_json(body):
        if body is None or body == '':
            raise ValidationError('Request does not have a body')
        validation = validate_post_company(body)
        if(validation["error"]):
            raise ValidationError(validation["error"])
        elif(not is_symbol_available(body["symbol"].split(":")[1])):
            raise ValidationError("Symbol is not available for use")
        else:
            return Company(body)
    

    def update_from_json(self, body):
        if body is None or body == '':
            raise ValidationError('Request does not have a body')
        validation = validate_put_company(body)
        if(validation["error"]):
            raise ValidationError(validation["error"])
        elif(body.get('symbol') and not is_symbol_available(body["symbol"].split(":")[1])):
            raise ValidationError("Symbol is not available for use")
        else:
            self.company_name = body.get('name') if body.get('name') else self.company_name
            self.description = body.get('description') if body.get('description') else self.description
            self.symbol = body.get('symbol') if body.get('symbol') else self.symbol


    def soft_delete(self):
        self.is_active = False


    def to_json(self):
        json_company = {
            'company_uuid': self.company_uuid,
            'company_name': self.company_name,
            'description': self.description,
            'symbol': self.symbol,
            'is_active': self.is_active,
        }
        return json_company

            


