import django_filters

from .models import *

class UnitFilter(django_filters.FilterSet):
    class Meta:
        model = unit
        fields = ['unitcode','unitname','date_created']