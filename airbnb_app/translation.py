from .models import Property, Rules, City
from modeltranslation.translator import register, TranslationOptions


@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Rules)
class RulesTranslationOptions(TranslationOptions):
    fields = ('rules_name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)




