from django.contrib import admin
from django.contrib.auth.models import  Group,User
from django.dispatch import receiver
from .models import Profile,Meep
from django.db.models.signals import post_save

#Unregister Groups
admin.site.unregister(Group)

admin.site.register(Meep)

#Mixed Profile Info into User info
class ProfileInline(admin.StackedInline):
    model=Profile

#extend user model
class UserAdmin(admin.ModelAdmin):
    model=User
    #Just display username fields on admin page
    fields=["username"]
    inlines=[ProfileInline]
#unregister initial user
admin.site.unregister(User)

# Reregister user
admin.site.register(User,UserAdmin)
#admin.site.register(Profile)

#Create Profile When New User Signs Up
@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile=Profile.objects.create(user=instance)
        user_profile.save()
        #Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

#post_save.connect(create_profile,sender=User)
