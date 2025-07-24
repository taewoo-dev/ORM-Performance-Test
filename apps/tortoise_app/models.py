from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    
    # Reverse foreign key
    posts: fields.ReverseRelation["Post"]
    
    class Meta:
        table = "users"

class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, index=True)
    content = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="posts", index=True)
    
    class Meta:
        table = "posts" 