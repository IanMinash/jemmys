from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from jemmys.main.models import Product


class LoginForm(AuthenticationForm):
    """Form that allows managers & admin login."""

    username = forms.CharField(
        label=_("Username"),
        max_length=254,
        widget=forms.TextInput(attrs={}),)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={}),
    )


class NewProductForm(forms.ModelForm):
    """Form for creating a new product."""

    class Meta:
        """Meta definition for NewProductform."""

        model = Product
        fields = ('name', 'description', 'price',
                  'category', 'quantity', 'variant_info')
        widgets = {
            'category': forms.Select(attrs={'class': ''}),
        }


class NewVariantForm(forms.Form):
    """Form for adding a new variant."""

    name = forms.CharField(max_length=50)
    quantity = forms.IntegerField()
    variant_info = forms.CharField(max_length=50)
    variant_of = forms.IntegerField()

    def save(self, commit=True):
        form_fields = self.cleaned_data
        v_of = Product.objects.get(id=form_fields.get("variant_of"))
        instance = Product.objects.create(
            name=form_fields.get("name"), quantity=form_fields.get("quantity"), category=v_of.category, price=v_of.price, variant_of=v_of, variant_info=form_fields.get("variant_info"))
        return instance
