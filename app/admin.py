from django.contrib import admin

from app.models import MyUser, Course, StudCour, TeachCour

admin.site.register(MyUser)
admin.site.register(Course)
admin.site.register(StudCour)
admin.site.register(TeachCour)