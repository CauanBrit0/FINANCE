from django.shortcuts import render, redirect
from perfil.models import Categoria
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages
from .models import ContaPaga, ContaPagar
from datetime import datetime
from extrato.models import Valores
def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento =  request.POST.get('dia_pagamento')

        if len(titulo.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(request, constants.WARNING, 'Preencha os campos em branco.')
            return redirect('/contas/definir_contas')
    
        try:
            conta = ContaPagar(titulo = titulo, categoria_id = categoria, descricao = descricao, valor = valor, dia_pagamento = dia_pagamento)
            conta.save()
            messages.add_message(request, constants.SUCCESS,'Conta Adicionada com Sucesso')
            return redirect('/contas/definir_contas')


        except:
            messages.add_message(request, constants.WARNING,'Erro interno do sistema')
            return redirect('/contas/definir_contas')
        
    

def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month = MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt = DIA_ATUAL).exclude(id__in = contas_pagas)
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gt = DIA_ATUAL).exclude(id__in = contas_pagas)
    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in = contas_pagas).exclude(id__in = contas_proximas_vencimento)
    return render(request,'ver_contas.html', {'contas_vencidas':contas_vencidas,
                                              'contas_proximas_vencimento':contas_proximas_vencimento,
                                              'restantes':restantes})



def dashboard(request):

    dados = {}

    categorias = Categoria.objects.all()
    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria = categoria)
        for v in valores:
            total += v.valor
        dados[categoria.categoria] = total
    return render(request,'dashboard.html',{'labels': list(dados.keys()),
                                            'values':list(dados.values())})