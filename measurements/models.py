from django.db import models
import hashlib

class Measurement(models.Model):
    trabajo = models.CharField(max_length=255, default='')
    ingresos = models.CharField(max_length=200, default='')
    deudas = models.CharField(max_length=200, default='')
    creditos = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return '{}'.format(self.trabajo)

    def hashear(self, valor):
        hash = hashlib.md5((valor).encode()).hexdigest()
        return hash

    def save(self, *args, **kwargs):
        self.trabajo = self.hashear(self.trabajo)
        self.ingresos = self.hashear(self.ingresos)
        self.deudas = self.hashear(self.deudas)
        self.creditos = self.hashear(self.creditos)
        super(Measurement, self).save(*args, **kwargs)
