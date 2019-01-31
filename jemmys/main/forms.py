from .models import BuyerAddress, UserIssue
from django.forms import ModelForm

class AddressForm(ModelForm):

    class Meta:
        """Meta definition for Addressform."""

        model = BuyerAddress
        fields = '__all__'


class UserIssueForm(ModelForm):

    class Meta:
        """Meta definition for UserIssueform."""

        model = UserIssue
        fields = '__all__'
