from .models import EmailUserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada con éxito. Ahora podés iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Hubo un error al crear la cuenta. Revisá los campos.')
    else:
        form = EmailUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})