from django.db import models

class Work(models.Model):
    platform = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    buyer = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    url = models.CharField(max_length=255, primary_key=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.title)
    
    class Meta:
        ordering = ['-date']


