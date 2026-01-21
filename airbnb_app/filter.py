from django_filters import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'price':['gt', 'lt'],
            'property_type':['exact'],
            'max_guests':['gt', 'lt'],
        }