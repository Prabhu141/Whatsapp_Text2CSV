from django.db import models

class whatsapp(models.Model):
    chat = models.FileField(upload_to='media')

    def __str__(self):
        return self.chat

class Film(models.Model):
    title = models.TextField(blank=False)
    year = models.TextField(blank=False)
    filmurl = models.TextField(blank=False)
    # genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    genre = models.TextField(blank=False)
    
    def __str__(self):
        return self.title