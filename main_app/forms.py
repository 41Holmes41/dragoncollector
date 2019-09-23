from django.forms import ModelForm
from .models import Burning

class BurningForm(ModelForm):
  class Meta:
    model = Burning
    fields = ['date', 'town']