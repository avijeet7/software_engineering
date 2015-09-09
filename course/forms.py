from django.forms import ModelForm
from course.models import Catalog

class courseform(ModelForm):
    class Meta:
        model = Catalog
        fields = ['code', 'name', 'credits']