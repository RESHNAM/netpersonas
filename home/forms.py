from django.forms import ModelForm
from .models import Feedback
from django.template.defaultfilters import slugify


class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'