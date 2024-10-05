from django.contrib import admin
from Qc.models import Qc
from django.apps import apps
# Register your models here.

# admin.site.register(Qc)

# Get the app configurations for the current app
app_config = apps.get_app_config('Qc')  # Replace 'your_app_name' with your app's name

# Loop through all models in the app
for model_name, model in app_config.models.items():
    # Dynamically create a ModelAdmin class
    class ModelAdmin(admin.ModelAdmin):
        pass

    # Register the model with the admin site
    admin.site.register(model, ModelAdmin)