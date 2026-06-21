from modeltranslation.translator import TranslationOptions, register

from .models import (
    Expedition,
    Fleet,
    Place,
    Restaurant,
    Souvenir,
    Stay,
    Stopover,
)


@register(Expedition)
class ExpeditionTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ("name", "description", "specialization", "mastery_text")


@register(Stay)
class StayTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ("name", "description", "category", "location_detail", "amenities")


@register(Fleet)
class FleetTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ("name", "description")


@register(Restaurant)
class RestaurantTranslationOptions(TranslationOptions):
    # Added 'name'
    fields = ("name", "description", "subtitle", "location")


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(Stopover)
class StopoverTranslationOptions(TranslationOptions):
    fields = ("name", "description", "transfer_details")
@register(Souvenir)
class SouvenirTranslationOptions(TranslationOptions):
    fields = ("name", "description", )


