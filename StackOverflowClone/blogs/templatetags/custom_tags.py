from django import template
import arrow

register = template.Library()

@register.filter
def human_time(date):
    local = arrow.get(date)
    response = local.humanize()
    return response