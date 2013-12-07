from django.contrib import admin
from django.db.models import get_models
from django.db.models import get_app

# register all models
app = get_app("schedulerapp")
for model in get_models(app):
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
