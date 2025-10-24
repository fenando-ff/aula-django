from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from . import models

# Create your views here.
def list_aluno(request):
    alunos = models.Aluno.objects.all()
    
    context = {
        'alunos': alunos
    }
    return render(request, 'aluno_list/aluno_list.html', context)

def aluno_create(request):
    # Carrega todas as turmas disponíveis
    try:
        turmas = models.Turma.objects.all()
    except models.Turma.DoesNotExist:
        turmas = []
        messages.error(request, 'Nenhuma turma encontrada. Por favor, crie uma turma antes de adicionar alunos.')
        return render(request, 'aluno_create/aluno_create.html', {'turmas': turmas})

    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.POST.get('nome_aluno')
        data_nascimento = request.POST.get('nascimento_aluno')  # Nome ajustado para corresponder ao formulário HTML
        cpf_aluno = request.POST.get('cpf_aluno').replace('.', '').replace('-', '')
        observacao_aluno = request.POST.get('observacao_aluno')  # Nome ajustado para corresponder ao formulário HTML
        turma = request.POST.get('turma')  # Nome ajustado para corresponder ao formulário HTML

        # Valida se todos os campos obrigatórios foram preenchidos
        if not all([nome, data_nascimento, cpf_aluno, turma]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('aluno_create')

        # Valida se a turma existe
        try:
            turma_instance = models.Turma.objects.get(id_turma=turma)
        except models.Turma.DoesNotExist:
            messages.error(request, 'Turma selecionada não existe.')
            return redirect('aluno_create')

        try:
            # Usa a conexão com o banco para chamar a stored procedure
            with connection.cursor() as cursor:
                cursor.callproc('insert_aluno', [
                    nome,
                    data_nascimento,
                    cpf_aluno,
                    observacao_aluno if observacao_aluno else None,
                    turma_instance.id_turma # Usa diretamente, pois id_turma já é um inteiro
                ])
            messages.success(request, 'Aluno cadastrado com sucesso.')
            return redirect('aluno_list')

        except Exception as e:
            messages.error(request, f'{str(e)}')
            return redirect('aluno_create')

    # Contexto para renderizar o formulário em GET
    context = {
        'turmas': turmas
    }
    return render(request, 'aluno_create/aluno_create.html', context)

def aluno_update(request, aluno_id):
    # Tenta carregar o aluno pelo ID
    try:
        aluno = models.Aluno.objects.get(id_aluno=aluno_id)
    except models.Aluno.DoesNotExist:
        messages.error(request, 'Aluno não encontrado.')
        return redirect('aluno_list')

    # Carrega todas as turmas disponíveis
    try:
        turmas = models.Turma.objects.all()
    except models.Turma.DoesNotExist:
        turmas = []
        messages.error(request, 'Nenhuma turma encontrada. Por favor, crie uma turma antes de atualizar alunos.')

    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.POST.get('nome_aluno')
        data_nascimento = request.POST.get('dataNasc_aluno')
        cpf_aluno = request.POST.get('cpf_aluno').replace('.', '').replace('-', '')
        observacao_aluno = request.POST.get('observacao_aluno')
        turma = request.POST.get('turma')

        # Valida se a turma existe
        try:
            turma_instance = models.Turma.objects.get(id_turma=turma)
        except models.Turma.DoesNotExist:
            messages.error(request, 'Turma selecionada não existe.')
            return redirect('aluno_update', aluno_id=aluno_id)

        try:
            # Chama a stored procedure para atualizar o aluno
            with connection.cursor() as cursor:
                cursor.callproc('update_aluno', [
                    aluno_id,
                    nome,
                    data_nascimento,
                    cpf_aluno,
                    observacao_aluno if observacao_aluno else None,  # Passa NULL se observação estiver vazia
                    turma_instance.id_turma
                ])
            messages.success(request, 'Aluno atualizado com sucesso.')
            return redirect('aluno_list')

        except Exception as e:
            messages.error(request, f'{str(e)}')
            return redirect('aluno_update', aluno_id=aluno_id)

    # Contexto para renderizar o formulário em GET
    context = {
        'aluno': aluno,
        'turmas': turmas
    }
    return render(request, 'aluno_update/aluno_update.html', context)

def aluno_delete(request, aluno_id):
    try:
        aluno = models.Aluno.objects.get(id_aluno=aluno_id)
    except models.Aluno.DoesNotExist:
        messages.error(request, 'Aluno não encontrado.')
        return redirect('aluno_list')
    
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso.')
        return redirect('aluno_list')
    
    context = {
        'aluno': aluno
    }
    return render(request, 'aluno_delete/aluno_delete.html', context)