from django.db import models

# Create your models here.

class ImportFile(models.Model):
    file = models.FileField(verbose_name="Arquivo", upload_to="files")

    class Meta:
        verbose_name = 'Arquivo'
    
    def __str__(self):
        return self.file.name


class APIConnections(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=60)
    url = models.CharField(verbose_name="URL", max_length=150) 
    slug = models.CharField(verbose_name="Código", max_length=100)

    class Meta:
        verbose_name = 'Site'
    
    def __str__(self):
        return self.name


class EndPointConnections(models.Model):
    url = models.ForeignKey(APIConnections, verbose_name="URL", on_delete=models.CASCADE)
    endpoint = models.CharField(verbose_name="Endpoint", max_length=100)

    class Meta:
        verbose_name = 'Endpoint'
    
    def __str__(self):
        return f'{self.url.url}-{self.endpoint}'


class AssetsType(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=60)
    slug = models.CharField(verbose_name="Código", max_length=100)

    class Meta:
        verbose_name = 'Tipo de ativo'
    
    def __str__(self):
        return self.name


class Assets(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=60)
    slug = models.CharField(verbose_name="Código", max_length=100)
    asset_type = models.ForeignKey(AssetsType, verbose_name="Tipo de Ativo", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Ativo'
    
    def __str__(self):
        return self.name
