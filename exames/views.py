from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import TiposExames, PedidosExames, SolicitacaoExame
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET":
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    
    elif request.method == "POST":
        exames_id = request.POST.getlist('exames')
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        preco_total = 0
        for i in solicitacao_exames:
            if i.disponivel:
                preco_total += i.preco
            
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames,
                                                         'solicitacao_exames': solicitacao_exames,
                                                         'preco_total': preco_total})
    

def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exame = TiposExames.objects.filter(id__in=exames_id)

    pedido_exame = PedidosExames(
        usuario = request.user,
        data= datetime.now()
    )
    pedido_exame.save()
    for exame in solicitacao_exame:
        solicitacao_exame_temp = SolicitacaoExame(
            usuario = request.user,
            exame = exame,
            status = "E"
        )
        solicitacao_exame_temp.save()
        pedido_exame.exames.add(solicitacao_exame_temp)

    pedido_exame.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido de exame realizado com sucesso!')

    return redirect('/exames/ver_pedidos/')