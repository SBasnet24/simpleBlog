from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .utilities import unique_slug_generator
from django.urls import reverse


def upload_location(instance, filename):
    return "{}/{}".format(instance.id,filename)


class UserBlog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    image = models.ImageField(null=True, blank=True,
                              height_field="height_field",
                              width_field="width_field",
                              upload_to=upload_location)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)


    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        ordering = ['-updated', '-timestamp']

    def __str__(self):
        return self.title + " , by: " + str(self.user)

    def get_absolute_url(self):
        return reverse("blogapp:blog_detail")


@receiver(pre_save, sender=UserBlog)
def userblog_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
