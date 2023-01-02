from django.db import models

class Work(models.Model):
    platform = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    buyer = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    work_lang = models.CharField(max_length=5, default='ru')
    create_date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.title)
    
    class Meta:
        ordering = ['-create_date']


