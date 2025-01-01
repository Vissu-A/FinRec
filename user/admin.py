'''
Registering models on admin site.
'''

from django.contrib import admin

from .models import FinRecUser

admin.site.register(FinRecUser)
