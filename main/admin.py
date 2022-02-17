from django.contrib import admin
from .models import Team, Match, FakeMatch

# Register your models here.
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(FakeMatch)
