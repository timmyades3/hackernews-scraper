from django.db import models
from django.utils.translation import gettext_lazy as _

class News(models.Model):
    item_id = models.PositiveIntegerField(null=True)
    type = models.CharField(_('Item Type'), max_length=255)
    author = models.CharField(_('Item Author'), max_length=255)
    date_created = models.DateTimeField(_('Creation Time'), null=True)
    is_posted = models.BooleanField(_('Is Item Posted?'), default=False)
    kids = models.JSONField(_('Kids'), blank=True, null=True) 
    text = models.TextField(_('Item Text'), blank=True, null=True)
    descendants = models.IntegerField(_('Comment count'), blank=True, null=True)
    score = models.IntegerField(_('Item Score'), blank=True, null=True)
    url = models.CharField(_('Item url'), max_length=255, null=True, blank=True)
    title = models.CharField(_('Item Title'), blank=True, max_length=255)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    comment_id = models.PositiveIntegerField(null=True)
    parent = models.IntegerField(_('Comment Parent'), blank=True, null=True)
    text = models.TextField(_('Item Text'), max_length=255, blank=True, null=True)
    date_posted = models.DateTimeField(_('Creation Time'), null=True)
    kids = models.JSONField(_('Kids'), blank=True, null=True)  
    type = models.CharField(_('Item Type'), max_length=255)
    author = models.CharField(_('Item Author'), max_length=255, null=True, blank=True)

