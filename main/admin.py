from django.contrib import admin
from .models import Team, LadderMatch, FakeMatch, PointSystem, Tournament, Result

# Register your models here.
admin.site.register(Team)
admin.site.register(LadderMatch)
admin.site.register(FakeMatch)
admin.site.register(PointSystem)
admin.site.register(Tournament)
admin.site.register(Result)
