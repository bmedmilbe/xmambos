# filters.py
import django_filters

from .models import Post, Expedition, Stay


class ExpeditionFilter(django_filters.FilterSet):
    specialization = django_filters.CharFilter(
        field_name="specialization",
        lookup_expr="iexact"
    )

    class Meta:
        model = Expedition
        fields = ["specialization"]

class StayFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category",
        lookup_expr="iexact"
    )

    class Meta:
        model = Stay
        fields = ["category"]
class CMSPostShadowFilter(django_filters.FilterSet):
    language = django_filters.CharFilter(
        field_name="language",
        lookup_expr="iexact"
    )

    class Meta:
        model = Post
        fields = ["language"]
