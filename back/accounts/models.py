from djongo import models
from django.contrib.auth.models import User


class User(models.Model):
    objects = models.DjongoManager()

    id = models.ObjectIdField(db_column='_id', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.ListField()
