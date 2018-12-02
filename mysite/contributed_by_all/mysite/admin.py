#from django.contrib import admin
#from .models import Profile
#admin.site.register(Profile)
# Register your models here.

#start

"""from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
    list_select_related = ('profile', )

    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
"""


#end

from django.contrib import admin
from .models import UserProfileModel, ResponseTable, QuestionTable


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender','age']

admin.site.register(UserProfileModel ,UserProfileAdmin)

class responseinline(admin.TabularInline):
    model = ResponseTable
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Detail', {'fields':['yes_vote','no_vote','confused_vote','dontcare_vote','category','gender','dead_line']})

    ]
    inlines = [responseinline]
    admin.site.register(ResponseTable)

admin.site.register(QuestionTable, QuestionAdmin)

