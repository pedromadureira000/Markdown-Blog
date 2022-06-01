from django.db import models
from django.db.models.constraints import UniqueConstraint
from django_resized import ResizedImageField

class Menu(models.Model):
    class Meta:
        default_permissions = []
    slug = models.SlugField("Slug", max_length=25, primary_key=True)
    default_submenu = models.ForeignKey('SubMenu', blank=True, null=True, on_delete=models.PROTECT, related_name='default_submenu_option')
    title = models.CharField("Title", max_length=30)
    icon = models.CharField("Icon", max_length=15)


class SubMenu(models.Model):
    class Meta:
        default_permissions = []
        constraints = [UniqueConstraint(fields=['slug', 'menu',], name='Submenu compound id')]
    submenu_id = models.CharField("Submenu compound id", max_length=50, primary_key=True)
    slug = models.SlugField("Slug", max_length=25)
    menu = models.ForeignKey('Menu', on_delete=models.PROTECT)
    title = models.CharField("Title", max_length=30)
    icon = models.CharField("Icon", max_length=15)

class Page(models.Model):
    class Meta:
        default_permissions = []
        #  verbose_name = _('order')
        #  verbose_name_plural = _('orders')
        constraints = [UniqueConstraint(fields=['slug', 'submenu'], name='Page compound id')]
    page_id = models.CharField("Page compound id", max_length=75, primary_key=True)
    slug = models.SlugField("Slug", max_length=25)
    submenu = models.ForeignKey('SubMenu', on_delete=models.PROTECT)
    title = models.CharField("Title", max_length=30)
    description = models.CharField(max_length=200)
    image = ResizedImageField(size=[345, 261], quality=90, upload_to='images/page/', blank=True, null=True)
    markdown_text = models.TextField("Markdown text")
