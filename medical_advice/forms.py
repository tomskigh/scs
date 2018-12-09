# django library
from django import forms

# my models
from medical_advice.models import MedicalAdviceDescription


DISCOUNT = [('B', 'B'), ('R-30%', 'R-30%'), ('R-50%', 'R-50%'), ('100%', '100%')]

class MedicalAdviceDescriptionForm(forms.ModelForm):
    discount = forms.ChoiceField(widget=forms.RadioSelect, choices=DISCOUNT, label='Select the discount value:')

    class Meta:
        model = MedicalAdviceDescription
        fields = ('symptoms', 'recommendations', 'prescribed_medicines', 'discount')
        widgets = {'symptoms': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
                   'recommendations': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
                   'prescribed_medicines': forms.Textarea(attrs={'cols': 40, 'rows': 3}),}