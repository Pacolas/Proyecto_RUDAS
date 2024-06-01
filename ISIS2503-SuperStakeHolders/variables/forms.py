from django import forms
from .models import Variable


#TODO: llenar valores formulario
class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = [
            'name',
            'lastname',
            'country',
            'city',
            'phone',
            'mail'
        ]
        labels = {
            'name': 'Name',
            'lastname': 'Lastname',
            'country': 'Country',
            'city': 'City',
            'phone': 'Phone',
            'mail': 'Mail'
        }

    def save(self):
        variable = super(VariableForm, self).save(commit=False)
        #variable.name = variable.hashear(self.cleaned_data['name'])
        #variable.lastname = variable.hashear(self.cleaned_data['lastname'])
        #variable.country = variable.hashear(self.cleaned_data['country'])
        #variable.city = variable.hashear(self.cleaned_data['city'])

        #variable.save()
        return variable