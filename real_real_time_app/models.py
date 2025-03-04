from django.db import models

class ConnectedUser(models.Model):
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username
