import uuid
from django import forms
from .models import InterimFields

class InterimForm(forms.ModelForm):
    class Meta:
        model = InterimFields
        fields = ['employee_name', 'employee_id', 'email', 'location', 'department', 'designation', 'reporting_manager', 'start_date', 'end_date', 'num_of_days', 'reason', 'description', 'tenure']

    def __init__(self, *args, **kwargs):
        super(InterimForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != 'description':
                self.fields[field_name].widget.attrs['readonly'] = True
        
        self.fields['num_of_days'].required = True

    def save(self, commit=True):
        instance = super(InterimForm, self).save(commit=False)
        instance.request_id = f"{uuid.uuid4().hex[:20]}"  # Generating a unique request_id
        if commit:
            instance.save()
        return instance
    

        
       
        
    
    

