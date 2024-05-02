from django.shortcuts import render, redirect
from perfil.models import Conta,Categoria
from django.http import FileResponse
from django.contrib.messages import constants
from django.contrib import messages
from .models import Valores
from datetime import datetime
from django.template.loader import render_to_string
from django.conf import settings
import os
from weasyprint import HTML
from io import BytesIO

def novo_valor(request):
    if request.method =="GET":
        categorias = Categoria.objects.all()
        conta = Conta.objects.all()
        return render(request,'novo_valor.html',{'categoria':categorias,'conta':conta})
    
    if request.method == "POST":
        valor = request.POST.get('valor')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')
        if len(valor) == 0 or len(data) == 0:
            messages.add_message(request,constants.WARNING,'Preencha os Campos em Branco')
            return redirect('/extrato/novo_valor')
            
        valores= Valores(valor = valor, descricao = descricao, categoria_id = categoria, data = data, conta_id = conta, tipo = tipo)
        valores.save()
        
        conta = Conta.objects.get(id=conta)

        if tipo == "E":
            messages.add_message(request, constants.SUCCESS, 'Entrada realizada com sucesso')
            conta.valor += int(valor)
        
        elif tipo =="S":
            messages.add_message(request, constants.SUCCESS, 'Saída realizada com sucesso')
            conta.valor -= int(valor)
        
        conta.save()


        return redirect('/extrato/novo_valor')

    
        
def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    valores = Valores.objects.filter(data__month=datetime.now().month)
    periodo_get = request.GET.get('periodo')
    if conta_get:
        valores = valores.filter(conta__id = conta_get)

    if categoria_get:
        valores = valores.filter(categoria__id = categoria_get)
    
    if periodo_get:
        valores = valores.filter(data = datetime.now())
    return render(request, 'view_extrato.html', {'valores': valores, 'contas': contas, 'categorias': categorias})



def exportar_pdf(request):
    valores = Valores.objects.all()

    path_template = os.path.join(settings.BASE_DIR,'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores': valores})

    path_output = BytesIO()
    HTML(string= template_render).write_pdf(path_output)
    path_output.seek(0)

    return FileResponse(path_output, filename="extrato.pdf")