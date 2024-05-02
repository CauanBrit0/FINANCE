from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from .models import Conta, Categoria
from .utils import calcula_total, calcula_equilibrio_financeiro
from extrato.models import Valores
from datetime import datetime

def home(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        valores = Valores.objects.filter(data__month = datetime.now().month)
        valores_entrada = valores.filter(tipo = 'E')
        valores_saida = valores.filter(tipo = 'S')
        total_entrada = calcula_total(valores_entrada, 'valor')
        total_saida = calcula_total(valores_saida, 'valor')
        contas = Conta.objects.all()
        valor_total = calcula_total(contas,'valor')
        total_saida_planejamento = calcula_total(valores,'valor')
        total_planejamento = calcula_total(categorias,'valor_planejamento')

        total_livre = int(total_planejamento - total_saida_planejamento)
        
        percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
        return render(request,'home/home.html',{'contas':contas
                                                ,'valor_total':valor_total,
                                                'total_saida':total_saida,
                                                'total_entrada':total_entrada,
                                                'total_saida_planejamento':total_saida_planejamento,
                                                'total_planejamento':total_planejamento,
                                                'total_livre':total_livre,
                                                'percentual_gastos_essenciais':int(percentual_gastos_essenciais),
                                                'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais)})
    
    if request.method =="POST":
        pass



def gerenciar(request):
    if request.method =="GET":
        contas = Conta.objects.all()
        categoria = Categoria.objects.all()
        valor_total = calcula_total(contas,'valor')
        
            
            
            

        return render(request, 'gerenciar/gerenciar.html',{'contas': contas,'valor_total': valor_total, 'categoria':categoria})

    if request.method =="POST":
        contas = Conta.objects.all()
        pass




def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if Conta.objects.filter(apelido = apelido) or  len(apelido.strip()) == 0:
        messages.add_message(request,constants.WARNING,'Nome da conta inválido.')
        return redirect('/perfil/gerenciar/')
    
    if len(valor.strip()) == 0:
        messages.add_message(request,constants.WARNING,'Preencha o campo Valor')
        return redirect('/perfil/gerenciar/')
    try:
        conta = Conta(apelido = apelido, banco = banco, tipo = tipo, valor = valor, icone = icone)
        conta.save()
        messages.add_message(request,constants.SUCCESS,'Conta cadastrada.')
        return redirect('/perfil/gerenciar/')
    
    except:
        messages.add_message(request,constants.WARNING,'Erro interno do sistema.')
        return redirect('/perfil/gerenciar/')
    


def deletar_banco(request, id):
    if request.method == "GET":
        conta = Conta.objects.get(id = id)
        conta.delete()
        messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso.')
        return redirect('/perfil/gerenciar/')
    



def cadastrar_categoria(request):
        nome = request.POST.get('categoria')
        essencial = bool(request.POST.get('essencial'))

        if len(nome.strip()) == 0:
            messages.add_message(request, constants.WARNING,"Preencha o nome da sua categoria")
            return redirect('/perfil/gerenciar/')
        try:
            categoria = Categoria(categoria = nome, essencial = essencial)
            categoria.save()
            messages.add_message(request, constants.SUCCESS,'Categoria cadastrada com sucesso.')
            return redirect('/perfil/gerenciar/')

        except:
            messages.add_message(request, constants.WARNING,'Erro interno do sistema.')
            return redirect('/perfil/gerenciar/')
        
    

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar')
