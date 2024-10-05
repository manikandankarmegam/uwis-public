from django.contrib import admin
from Ad.models import *

# Register your models here.

admin.site.register(ad)
admin.site.register(Weld)
admin.site.register(project)
admin.site.register(WeldProcess)
admin.site.register(weld_location)

admin.site.register(materialsgrade)
admin.site.register(w_p_s)
admin.site.register(KVMaster)
admin.site.register(MaterialSizeThicknessMasterData)
admin.site.register(TFAUpload)
admin.site.register(TFAVerify)
admin.site.register(TFAPhotos)
admin.site.register(TFAHistory)
