from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash  # Импорт функции для обновления сессии
from .forms import LoginForm, RegisterForm, EditProfileForm
from dogs.models import Dog


@login_required
def user_profile(request):
    """
    Представление для просмотра профиля пользователя,
    включая информацию об аккаунте и список любимых собак.
    """
    title = 'Профиль пользователя'
    user = request.user  # Получаем текущего пользователя
    dogs = Dog.objects.filter(owner=request.user)

    context = {
        'title': title,
        'user': user,  # Передаем информацию о пользователе в контекст
        'dogs': dogs,
    }
    return render(request, 'users/user_profile.html', context)


@login_required
def edit_profile(request):
    """
    Представление для редактирования профиля пользователя.
    """
    title = 'Редактировать профиль'
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:user_profile')  # Перенаправляем на страницу профиля
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = EditProfileForm(instance=request.user)
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'users/edit_profile.html', context)

def user_login(request):
    """
    Представление для входа пользователя.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dogs:index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
                return render(request, 'users/login.html', {'form': form})
        else:
            return render(request, 'users/login.html', {'form': form, 'error': 'Неверные данные'})
    else:
        form = LoginForm(request)
    return render(request, 'users/login.html', {'form': form})


def register(request):
    """
    Представление для регистрации нового пользователя.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('dogs:index')
            except Exception as e:
                messages.error(request, f"Ошибка при регистрации: {e}")
                return render(request, 'users/register.html', {'form': form})
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
            return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def logout(request):
    """
    Представление для выхода пользователя.
    """
    django_logout(request)
    return redirect('dogs:index')