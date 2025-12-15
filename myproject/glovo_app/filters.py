from .models import Store, Product
from django_filters import FilterSet


class StoreFilterSet(FilterSet):
    class Meta:
        model = Store
        fields = {
            'category': ['exact'],
        }