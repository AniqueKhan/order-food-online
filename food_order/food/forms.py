from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Sales

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        selected_dishes = cleaned_data.get('dishes')
        selected_restaurant = cleaned_data.get('restaurant')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Check if start date is earlier than end date
        if start_date and end_date and start_date >= end_date:
            self.add_error('start_date', "Start date must be earlier than end date.")

        # Check if end date is in the past
        today = timezone.now().date()
        if end_date and end_date < today:
            self.add_error('end_date', "End date cannot be in the past.")

        if selected_dishes.exists():
            for dish in selected_dishes.all():
                if dish.restaurant != selected_restaurant:
                    raise ValidationError(
                        "The dish '{}' does not belong to the selected restaurant."
                        .format(dish.name)
                    )

        return cleaned_data
