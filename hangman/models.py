from django.db import models

class wordBank(models.Model):
    word = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.word
