from django.db import models

# Create your models here.
class FacebookPage(models.Model):
    page_id = models.CharField(blank=False, max_length=100)
    name = models.CharField(blank=True, max_length=100)
    url = models.CharField(blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now=True)
