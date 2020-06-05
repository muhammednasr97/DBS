from django import forms
from .models import Equipment, Technical_Report, Technical_Specs, General_Specs


class AddEquipment(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ('code', 'equipment_name', 'purpose', 'speciality', 'picture', 'general_specs', 'technical_specs')
        """
        labels = {
            'fullname':'Full Name',
            'emp_code':'EMP. Code'
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = "Select"
        self.fields['emp_code'].required = False
        """


class AddReport(forms.ModelForm):
    class Meta:
        model = Technical_Report
        fields = ('report_id', 'equipment_name', 'modification_date', 'addition_date', 'technology_level', 'facility_level')


class AddGeneralSpecs(forms.ModelForm):
    class Meta:
        model = General_Specs
        fields = ('name', 'value')

class AddTechSpecs(forms.ModelForm):
    class Meta:
        model = Technical_Specs
        fields = ('name', 'value')

