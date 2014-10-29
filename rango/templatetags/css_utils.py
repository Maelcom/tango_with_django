from django import template

register = template.Library()

# http://vanderwijk.info/blog/adding-css-classes-formfields-in-django-templates/
@register.filter()
def add_css(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v
    return field.as_widget(attrs=attrs)
