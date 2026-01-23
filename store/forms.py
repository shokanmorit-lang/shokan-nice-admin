from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import StoreModel, Product


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class StoreForm(forms.ModelForm):
    class Meta:
        model = StoreModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            if f.widget.__class__.__name__ in ["CheckboxInput"]:
                continue
            f.widget.attrs.update({"class": "form-control"})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})


    # Validation آمن: ما يسبب خطأ لو الحقل غير موجود
    def clean(self):
        cleaned = super().clean()
        if "price" in cleaned and cleaned["price"] is not None:
            try:
                if cleaned["price"] <= 0:
                    self.add_error("price", "السعر يجب أن يكون أكبر من صفر.")
            except TypeError:
                pass
        return cleaned









