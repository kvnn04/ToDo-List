from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


# @login_required
# def task_list(request):
#     try:
#         tasks = Task.objects.filter(user=request.user)
#     except Exception as e:
#         messages.error(request, 'Error al obtener las tareas.')
#         tasks = []
#     return render(request, 'app_to_do/task_list.html', {'tasks': tasks})

# @login_required
# def task_list(request):
#     tasks_todo = Task.objects.filter(user=request.user, status='todo')
#     tasks_in_progress = Task.objects.filter(user=request.user, status='in_progress')
#     tasks_done = Task.objects.filter(user=request.user, status='done')

#     context = {
#         'tasks_todo': tasks_todo,
#         'tasks_in_progress': tasks_in_progress,
#         'tasks_done': tasks_done,
#     }
#     return render(request, 'app_to_do/task_list.html', context)
@login_required
def task_list(request):
    try:
        # tasks = Task.objects.filter(user=request.user)
        tasks = Task.objects.filter(user=request.user)
    except Exception as e:
        messages.error(request, 'Error al obtener las tareas.')
        tasks = []
    
    return render(request, 'app_to_do/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                messages.success(request, 'Tarea creada correctamente.')
                return redirect('task-list')
            except Exception as e:
                messages.error(request, f'Error al crear la tarea: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TaskForm()
    return render(request, 'app_to_do/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Tarea actualizada correctamente.')
                return redirect('task-list')
            except Exception as e:
                messages.error(request, f'Error al actualizar la tarea: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'app_to_do/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            task.delete()
            messages.success(request, 'Tarea eliminada correctamente.')
            return redirect('task-list')
        except Exception as e:
            messages.error(request, f'Error al eliminar la tarea: {str(e)}')
            return redirect('task-list')
    return render(request, 'app_to_do/task_confirm_delete.html', {'task': task})
