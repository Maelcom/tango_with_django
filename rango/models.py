from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from utils.queryset import GetOrNoneManager
from django.db.models.signals import post_save


class BaseModel(models.Model):
    objects = GetOrNoneManager()

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.views < 0:
            self.views = 0
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Page(BaseModel):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class UserProfile(BaseModel):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

    @staticmethod
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile(user=instance).save()
# Hook to create UserProfile when new User is created
post_save.connect(UserProfile.create_profile, sender=User, weak=False)
