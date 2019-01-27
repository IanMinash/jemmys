from .models import BuyerAddress
from django.forms import ModelForm

class AddressForm(ModelForm):
    """Form definition for Address."""

    class Meta:
        """Meta definition for Addressform."""

        model = BuyerAddress
        fields = '__all__'
