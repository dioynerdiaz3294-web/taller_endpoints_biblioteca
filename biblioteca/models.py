from django.db import models


class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    anio = models.PositiveIntegerField(null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"