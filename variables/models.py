from django.db import models
import hashlib

class Variable(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='Colombia')
    city = models.CharField(max_length=50, default='Bogota')
    phone = models.IntegerField(default=123456789)
    mail = models.CharField(max_length=50, default='@bancodelosalpes.com.co')
    namehasheado = models.CharField(max_length=50, default='')
    lastnamehasheado = models.CharField(max_length=50, default='')
    countryhasheado = models.CharField(max_length=50, default='Colombia')
    cityhasheado = models.CharField(max_length=50, default='Bogota')

    def __str__(self):
        return '{}'.format(self.name)

    def hashear(self, valor):
        hash = hashlib.md5((valor).encode()).hexdigest()
        return hash
    
    def save(self, *args, **kwargs):
        self.namehasheado = self.hashear(self.name)
        self.lastnamehasheado = self.hashear(self.lastname)
        self.countryhasheado = self.hashear(self.country)
        self.cityhasheado = self.hashear(self.city)
        super(Variable, self).save(*args, **kwargs)