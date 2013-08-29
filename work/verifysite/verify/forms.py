#-*-coding:utf-8
from django.forms import ModelForm
from verify.models import Case
from django.forms import TextInput
class CaseForm(ModelForm):
	class Meta:
		model=Case
		widgets = {
            'requesturl':TextInput(attrs={"size":"120"}),
        }

