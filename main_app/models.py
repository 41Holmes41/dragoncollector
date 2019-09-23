from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


# Create your models here.

class Player(models.Model):
  api_id=models.IntegerField()
  first_name=models.CharField(max_length=50)
  last_name=models.CharField(max_length=50)

class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('toys_detail', kwargs={'pk': self.id})

class Dragon(models.Model):
  name = models.CharField(max_length=100)
  breed = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  toys = models.ManyToManyField(Toy)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'dragon_id': self.id} )

TOWNS = (
  ('B', 'Bangladesh'),
  ('L', 'London'),
  ('D', 'Denmark'),
)

class Burning(models.Model):
  date = models.DateField()
  town= models.CharField(
    max_length=1,
    choices=TOWNS,
    default = TOWNS[0][0]
  )
  dragon = models.ForeignKey(Dragon, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_town_display()} on {self.date}"
    
  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=200)
  dragon = models.ForeignKey(Dragon, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for dragon_id: {self.dragon_id} @{self.url}"