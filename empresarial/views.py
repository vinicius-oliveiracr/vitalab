from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.admin.views.decorators import staff_member_required
from exames.models import SolicitacaoExame
from django.http import HttpResponse, FileResponse
from .utils import gerar_pdf_exames, gerar_senha_aleatória

# Create your views here.

@staff_member_required
def gerenciar_clientes(request):
    clientes = User.objects.filter(is_staff = False)

    nome_completo = request.GET.get('nome')
    email = request.GET.get('email')

    if email:
        clientes = clientes.filter(email__contains = email)

    if nome_completo:
        clientes = clientes.annotate(
            full_name = Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__contains=nome_completo)

    return render (request, 'gerenciar_clientes.html', {'clientes': clientes})


@staff_member_required 
def cliente(request, cliente_id):
    cliente = User.objects.get(id=cliente_id)
    exames = SolicitacaoExame.objects.filter(usuario=cliente)
    return render(request, 'cliente.html', {'cliente': cliente, 'exames': exames})

@staff_member_required 
def exame_cliente(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    return render (request, 'exame_cliente.html', {'exame':exame})


def proxy_pdf(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    response = exame.resultado.open()

    return HttpResponse(response)


def gerar_senha(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)

    if exame.senha:
        return FileResponse(gerar_pdf_exames(exame.exame.nome, exame.usuario.first_name, exame.senha), filename="token.pdf")

    exame.senha = gerar_senha_aleatória(9)
    exame.save()
    return FileResponse(gerar_pdf_exames(exame.exame.nome, exame.usuario.first_name, exame.senha), filename="token.pdf")


