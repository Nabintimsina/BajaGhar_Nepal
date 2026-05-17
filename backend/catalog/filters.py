import django_filters
from .models import Instrument


class InstrumentFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    region = django_filters.CharFilter(field_name='region', lookup_expr='iexact')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')

    class Meta:
        model = Instrument
        fields = ['category', 'region', 'is_featured']
