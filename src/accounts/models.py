
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from hashlib import md5
from src.surveys.utils import calculate_digest

from projects.models import Project, ProjectGroup, ProjectMember



class Profile(models.Model):
    MALE       = 'M'
    FEMALE     = 'F'

    SEX = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    digest      = models.CharField(max_length=200,null=True)
    gender      = models.CharField(choices=SEX,default=MALE,max_length=1)
    pic         = models.ImageField(upload_to="img/")
    location    = models.CharField(max_length=30, blank=True)

    def save(self, *args, **kwargs):
        self.digest         = calculate_digest(self.user.username, self.user.password)
        super(Profile, self).save(*args, **kwargs)
    class Meta:
        db_table = 'ad_profile'
        managed = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # create profile
        Profile.objects.create(user=instance)
        # attach to Project general
        #ProjectGroup    = ProjectGroup.objects.get(pk=1)
        #ProjectMember.objects.create(project=ProjectGroup,member=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
