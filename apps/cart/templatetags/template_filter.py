from django.template.defaultfilters import register

@register.filter(is_safe=True)
def get_dict(value,name):
    return value.get(name)


