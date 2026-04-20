from django import forms
from django.contrib.auth import get_user_model
from .models import Category


User = get_user_model()


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "type", "is_active", "parent")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(),
            "parent": forms.Select(attrs={"class": "form-control"})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["parent"].queryset = Category.objects.filter(
                user=self.user,
                parent__isnull=True
            )


    def clean(self):
        cleaned_data = super().clean()
        if self.user:
            self.instance.user = self.user 
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance