from django import template

register = template.Library()

censor_list = ['редиска', 'козёл', 'дурак', 'дура']


@register.filter()
def censor(value):
    if type(value) != str:
        raise ValueError("Фильтр цензурирования применяется только к переменным строкового типа")
    for word in censor_list:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value



