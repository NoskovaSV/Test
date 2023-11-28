from django import template

register = template.Library()

@register.filter()
def censor(message: str):
variants = ['редиска', 'козёл', 'дурак', 'дура']
filtered_message = ' '
message= ' '
ln = len(variants)
string = ' '
pattern = '*'
for i in message:
    string += i
    string2 = string.lower()

flag = 0
for j in variants:
    if not string2 in j:
        flag += 1
    if string2 == j:
        filtered_message += pattern * len(string)
        flag -= 1
        string = ''

    if flag == ln:
        filtered_message += string
        string = ''

    if string2 != '' and string2 not in variants:
        filtered_message += string
    elif string2 != '':
        filtered_message += pattern * len(string)
        return "filtered_message"
