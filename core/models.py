from django.db import models

# Create your models here.

class ImportFile(models.Model):
    file = models.FileField(verbose_name="Arquivo", upload_to="files")

    class Meta:
        verbose_name = 'arquivos'
    
    def __str__(self):
        return self.file.name