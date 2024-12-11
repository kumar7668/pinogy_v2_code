import datetime
import calendar

from django import template
from djangocms_blog.models import Post
from django.db.models import Q, Count

register = template.Library()


@register.simple_tag(takes_context=True)
def get_publish_blogs(context):
    posts = Post.objects.filter(
        publish=True, date_published__lte=datetime.datetime.now()
    ).order_by().values('date_published__year', 'date_published__month').annotate(Count('pk')
    ).order_by('-date_published__year', '-date_published__month')

    context['archives'] = posts
    return context


@register.filter(name='get_month_name')
def get_month_name(month):
    return calendar.month_name[month]
