from django.shortcuts import render, redirect, get_object_or_404
from .models import Breed, Dog
from .forms import DogForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
@login_required
def add_dog_to_profile(request, dog_id):
    dog = get_object_or_404(Dog, pk=dog_id)
    dog.owner = request.user
    dog.save()
    return redirect(request.META.get('HTTP_REFERER', reverse('dogs:dogs_list')))

@require_http_methods(["DELETE"])
@login_required
def remove_dog_from_profile(request, dog_id):
   dog = get_object_or_404(Dog, pk=dog_id, owner=request.user)
   dog.owner = None
   dog.save()
   return JsonResponse({'message': 'Собака успешно удалена из профиля.'})

@login_required
def index(request):
    title = 'Главная страница'
    context = {'title': title}
    return render(request, 'dogs/index.html', context)

@login_required
def breeds(request):
    title = 'Породы собак'
    breeds = Breed.objects.all()  # Получаем все породы
    breeds_with_dogs = {breed: Dog.objects.filter(breed=breed) for breed in breeds}  # Получаем собак по породам
    context = {'title': title, 'breeds_with_dogs': breeds_with_dogs}
    return render(request, 'dogs/breeds.html', context)


@login_required
def dogs_list(request):
    title = 'Список всех собак'
    dogs = Dog.objects.all()  # Получаем всех собак
    context = {'title': title, 'dogs': dogs}
    return render(request, 'dogs/dogs_list.html', context)

@login_required
def dog_create(request):
    title = 'Добавить собаку'
    form = DogForm()  # Инициализация формы
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save()
            return redirect('dogs:dogs_list')
    context = {'title': title, 'form': form}
    return render(request, 'dogs/dog_create.html', context)

@login_required
def dog_update(request, pk):
    title = 'Редактировать информацию о собаке'
    dog = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('dogs:dog_read', pk=dog.pk)
    else:
        form = DogForm(instance=dog)
    context = {'title': title, 'form': form, 'dog': dog}
    return render(request, 'dogs/dog_update.html', context)

@login_required
def dog_delete(request, pk):
    title = 'Удалить собаку'
    dog = get_object_or_404(Dog, pk=pk)
    dog.delete()  # Удаляем собаку
    return redirect(reverse('dogs:dogs_list'))  # Перенаправляем на список собак

@login_required
def dog_read(request, pk):
    title = 'Информация о собаке'
    dog = get_object_or_404(Dog, pk=pk)
    context = {'title': title, 'dog': dog}
    return render(request, 'dogs/dog_read.html', context)  # Исправлен путь к шаблону

@login_required
def all_dogs(request):
    title = 'Все собаки'
    dogs = Dog.objects.all()  # Получаем всех собак
    context = {'title': title, 'dogs': dogs}
    return render(request, 'dogs/all_dogs.html', context)

