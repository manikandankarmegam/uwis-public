from django.urls import path
from.import views
urlpatterns = [

    path('udashboard/', views.dashboard , name = "dashboard" ),
    path('udashboardtabel/', views.dashboardtabel , name = "dashboardtabel" ),
    path('uadmin/', views.admin , name = "admin" ),    
    path('uadd_contractor/', views.add_contractor , name = "add_contractor" ),
    path('uprojectlist/', views.projectlist , name = "uprojectlist" ),
    path('ustartproject/', views.startproject , name = "startproject" ),
    path('ucreateproject/', views.createproject , name = "createproject" ),
    path('unewproject/', views.newproject , name = "newproject" ),
    path('udetailproject/<int:pro_id>', views.detailproject , name = "detailproject" ),
    path('uproject_welder/<int:id>/', views.project_welder , name = "project_welder" ),
    path('uaddproject_welder/<int:id>/', views.addproject_welder , name = "addproject_welder" ),
    path('usetupoption/', views.setupoption , name = "setupoption" ),
    path('uaddweldoption/', views.addweldoption , name = "addweldoption" ),
    path('uweldmapoption/', views.weldmapoption , name = "weldmapoption" ),
    path('uuserprofile/', views.userprofile , name = "userprofile" ),
    path('unew_profile/', views.newprofile , name = "newprofile" ),
    path('unew_profileadedit/<int:id>/', views.newprofileadedit , name = "unew_profileadedit" ),
    path('unew_profileaddel/<int:id>/', views.newprofileaddel , name = "unew_profileaddel" ),
    path('unew_profileqcedit/<int:id>/', views.newprofileqcedit, name = "unew_profileqcedit"),
    path('unew_profileqcdel/<int:id>/', views.newprofileqcdel , name = "unew_profileqcdel" ),
    path('unew_profileclientedit/<int:id>/', views.newprofileclientedit, name = "unew_profileclientedit"),
    path('unew_profileclientdel/<int:id>/', views.newprofileclientdel , name = "unew_profileclientdel" ),
    path('unew_profilefitteredit/<int:id>/', views.newprofilefitteredit, name = "unew_profilefitteredit"),
    path('unew_profilefitterdel/<int:id>/', views.newprofilefitterdel , name = "unew_profilefitterdel" ),
    path('udetail_profileqc/<int:proid>/', views.detailprofileqc , name = "udetail_profileqc" ),
    path('udetail_profile_fitter/<int:id>/', views.detailprofilefitter , name = "udetail_profile_fitter" ),
    path('udetail_profilead/<int:proid>/', views.detailprofilead , name = "udetail_profilead" ),
    path('udetail_profileclient/<int:proid>/', views.detailprofileclient , name = "udetail_profileclient" ),
   
    path('uweldtypes/', views.weldtypes , name = "weldtypes" ),
    path('unewweldtype/', views.newweldtype , name = "newweldtype" ),
    path('uweldprocess/', views.weldprocess , name = "weldprocess" ),
    path('unewweldprocess/', views.newweldprocess , name = "newweldprocess" ),
    path('uweldlocation/', views.weldlocation , name = "weldlocation" ),
    path('unewweldlocation/', views.newweldlocation , name = "newweldlocation" ),
    path('uwelders/', views.welders , name = "welders" ),
    path('unewwelders/', views.newwelders , name = "newwelders" ),
    path('udetailwelders/<int:id>/', views.detailwelders , name = "detailwelders" ),
    path('umaterials/', views.materials , name = "materials" ),
    path('unewmaterials/', views.newmaterials , name = "newmaterials" ),
    path('udetailmaterials/<int:id>/', views.detailmaterials , name = "detailmaterials" ),
    path('umaterialsgrade/<int:id>/', views.materials_grade , name = "materialsgrade" ),
    path('uuploadmaterials/', views.uploadmaterials , name = "uploadmaterials" ),
    path('uuploadmaterialslist/<int:id>/', views.uploadmaterialslist , name = "uploadmaterialslist" ),
    path('material-grade-fetch/',views.material_grade_fetch, name= "material_grade_fetch"),
    path('material-schedule-fetch/',views.material_schedule_fetch, name= "material_schedule_fetch"),
    path('material-thickness-fetch/',views.material_thickness_fetch, name= "material_thickness_fetch"),
    path('part-number-detail-fetch/',views.part_number_detail_fetch, name= "part_number_detail_fetch"),


    path('uwps/', views.wps , name = "wps" ),
    path('uaddwps/', views.addwps , name = "addwps" ),
    path('udetailwps/<int:id>/', views.detailwps , name = "detailwps" ),

    path('uuploads/<int:id>/', views.uploads , name = "uploads" ),
    path('uupload_spoolgen/<int:id>/', views.upload_spoolgen , name = "upload_spoolgen" ),
    path('uuploads_material/<int:id>/', views.uploads_material , name = "uploads_material" ),

    path('unew_weldedit/<int:id>/', views.weld_edit , name = "unew_weldedit"),
    path('unew_welddel/<int:id>/', views.delete_weld , name = "unew_welddel" ),
    path('unew_weldeditprocess/<int:id>/', views.weld_process_edit , name = "unew_weldeditprocess"),
    path('unew_welddelprocess/<int:id>/',views.delete_weld_process, name = "unew_welddelprocess" ),
    path('unew_weldlocationedit/<int:id>/', views.weld_location_edit , name = "unew_weldlocationedit"),
    path('unew_weldlocationdel/<int:id>/',views.delete_weld_location, name = "unew_weldlocationdel" ),
    path('unew_proedit/<int:id>/', views.project_edit, name = "unew_proedit"),
    path('unew_projectdel/<int:id>/',views.projectdel, name = "unew_projectdel" ),
    path('unew_materialedit/<int:id>/', views.materialsedit, name = "unew_materialedit"),
    path('unew_materialdel/<int:id>/',views.materialsdel, name = "unew_materialdel" ),
    path('unew_wpsedit/<int:id>/', views.wpsedit, name = "unew_wpsedit"),
    path('unew_wpsdel/<int:id>/',views.wpsdel, name = "unew_wpsdel" ),
    path('unew_weldersedit/<int:id>/', views.weldersedit, name = "unew_weldersedit"),
    path('unew_weldersdel/<int:id>/',views.weldersdel, name = "unew_weldersdel" ),
   
    path('unew_materialgradeedit/<int:id>/', views.materialsgradeedit, name = "unew_materialgradeedit"),
    path('unew_materialgradedel/<int:id>/',views.materialgradesdel, name = "unew_materialgradedel" ),
    
    path('fetch-material-details/',views.fetch_weldGrade, name= "fetchweldgrade"),



    path('uqr_scanner/', views.qr_scanner , name = "qr_scanner" ),
    path('uqr_fitup/', views.qr_fitup , name = "qr_fitup" ),
    path('uqr_visual/', views.qr_visual , name = "qr_visual" ),

    path('utfa_upload/<int:id>/', views.tfa_upload , name = "tfa_upload" ),












    


    






]