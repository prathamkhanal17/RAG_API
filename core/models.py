from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image text {self.created_at}"