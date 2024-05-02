from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from perfil.models import Categoria, Conta
import json
from django.views.decorators.csrf import csrf_exempt
from extrato.models import Valores
from perfil.utils import calcula_total
def definir_planejamento(request):
    categorias = Categoria.objects.all()
    conta = Conta.objects.all()
    return render(request,'definir_planejamento.html',{'categorias':categorias, 'conta':conta})

@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    conta = Conta.objects.all()
    valores = Valores.objects.all()
    total_saida = calcula_total(valores,'valor')
    total_planejamento = calcula_total(categorias,'valor_planejamento')

    percentual_total = int((total_saida * 100) / total_planejamento)

    return render(request,'ver_planejamento.html', {'categorias':categorias, 'conta':conta, 'total_planejamento':total_planejamento, 'total_saida':total_saida, 'percentual_total':percentual_total })


    