from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import uuid
import boto3
from .models import Dragon, Toy, Photo
from .forms import BurningForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'dragoncollector'


# Create your views here.
#define the home view

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_burning(request, dragon_id):
    # create the ModelForm using the data in request.POST
  form = BurningForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the dragon_id assigned
    new_burning = form.save(commit=False)
    new_burning.dragon_id = dragon_id
    new_burning.save()
  return redirect('detail', dragon_id=dragon_id)

def home(request):
    return HttpResponse('<h1> yo </h1>')

def about(request):
    return render(request, 'about.html')

@login_required
def dragons_index(request):
    dragons = Dragon.objects.filter(user=request.user)
    return render(request, 'dragons/index.html', { 'dragons': dragons })

@login_required
def dragons_detail(request, dragon_id):
    dragon = Dragon.objects.get(id=dragon_id)
    toys_dragon_doesnt_have = Toy.objects.exclude(id__in = dragon.toys.all().values_list('id'))

    burning_form = BurningForm()
    return render(request, 'dragons/detail.html', { 
      'dragon': dragon, 
      'burning_form' : burning_form,
      'toys': toys_dragon_doesnt_have 
    })

class DragonCreate(LoginRequiredMixin, CreateView):
    model = Dragon
    fields = '__all__'

    def form_valid(self, form):
      # Assign the logged in user (self.request.user)
      form.instance.user = self.request.user
      # Let the CreateView do its job as usual
      return super().form_valid(form)

class DragonUpdate(LoginRequiredMixin, UpdateView):
    model= Dragon
    fields=['breed', 'description', 'age']

class DragonDelete(LoginRequiredMixin, DeleteView):
    model=Dragon
    success_url= '/dragons/'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, dragon_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dragon.objects.get(id=dragon_id).toys.add(toy_id)
  return redirect('detail', dragon_id=dragon_id)

@login_required
def add_photo(request, dragon_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to dragon_id or dragon (if you have a dragon object)
      photo = Photo(url=url, dragon_id=dragon_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', dragon_id=dragon_id)