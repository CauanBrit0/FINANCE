from django.db import models
from datetime import datetime
from perfil.utils import calcula_total

class Categoria(models.Model):
    categoria = models.CharField(max_length= 50)
    essencial = models.BooleanField(default = False)
    valor_planejamento = models.FloatField(default = 0)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).filter(tipo = 'S')
        total_valor = 0
        for valor in valores:
            total_valor += valor.valor
        return total_valor
    
    def calcula_percentual_gasto_por_categoria(self):
        try:
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except:
            return 0

    



class Conta (models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE','Caixa Econômica'),

    )

    tipos_choices = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),

    )

    apelido = models.CharField(max_length = 50)
    banco = models.CharField(max_length = 2, choices = banco_choices)
    tipo = models.CharField(max_length= 2, choices = tipos_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to= 'icones')

    def __str__(self):
        return self.apelido
