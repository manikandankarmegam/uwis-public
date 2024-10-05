from django.urls import path
from . import views
urlpatterns = [

      # Project
    path('', views.project_views , name = "project" ),
    path('umainproject/<int:id>/', views.mainproject , name = "mainproject" ),


    # Weldhistory
    path('uweldhistory/<str:drg>/<int:sh>/<str:rev>/', views.weldhistory , name = "weldhistory" ),
    path('updateweldhistory/<int:id>/', views.updateWeld , name = "updateweldhistory" ),
    path('unewweldhistory/', views.newweldhistory , name = "newweldhistory" ),
    path('usheetweldhistory/', views.sheetweldhistory , name = "sheetweldhistory" ),
    path('unewdrawing/', views.newdrawing , name = "newdrawing" ),
    path('uiso/', views.iso , name = "iso" ),
    path('unewiso/', views.newiso , name = "newiso" ),
    path('udetailiso/<int:proid>', views.detailiso , name = "detailiso" ),
    path('unew_isoedit/<int:id>/', views.isoedit, name = "unew_isoedit"),
    path('unew_isodel/',views.isodel, name = "unew_isodel" ),
    path('uview_record_list/', views.view_record_list , name = "view_record_list" ),
    path('uview_record_create/', views.view_record_create , name = "view_record_create" ),
    path('uview_record_detail/', views.view_record_detail , name = "view_record_detail" ),
    path('addtext/<str:drg>/<int:sheetno>/', views.addtext , name = "addtext" ),
    path('removetext/<str:drg>/<int:sheetno>/', views.removetext , name = "removetext" ),
    path('uweldhistory-form-download/', views.weldhistory_form_download , name = "weldhistory_form_download" ),
    path('uweldsummary-form-download/', views.weldsummary_form_download , name = "weldsummary_form_download" ),

    path('addsheet/<str:drg>/', views.addsheet , name = "addsheet" ),
    path('addnorec/<str:drg>/<int:sh>/<str:rev>/', views.addnorec , name = "addnorec" ),
    path('uaddrev/<str:drg>/<int:sheetno>/', views.addrev , name = "addrev" ),
    path('uremoverev/<str:drg>/<int:sheetno>/', views.removerev , name = "removerev" ),

   
   

    path('search/', views.search, name='search'),

    # Nde
    path('undemonitor/', views.ndemonitor , name = "ndemonitor" ),
    path('underequestno/', views.nderequestno , name = "nderequestno" ),
    path('underequestnoreq/', views.nderequestnoreq , name = "nderequestnoreq" ),
    path('undereportrequestnoreq/', views.ndereportrequestnoreq , name = "ndereportrequestnoreq" ),
    path('underequest/', views.nderequest , name = "nderequest" ),
    path('undereport/', views.ndereport , name = "ndereport" ),
    path('undestatus/', views.ndestatus , name = "ndestatus" ),
  

    # rfi
    path('urfirequest/', views.rfirequest , name = "rfirequest" ),
    path('urficreate/', views.rficreate , name = "rficreate" ),

    # iso
    path('uisosheet/', views.isosheet , name = "isosheet" ),
    path('uisosheet/form-download/', views.isosheet_form_download , name = "isosheet_form_download" ),
    path('uisospool/', views.isospool , name = "isospool" ),
    path('uisospool/form-download/', views.isospool_form_download , name = "isospool_form_download" ),

    # ncr/qr
    path('uncr/', views.ncr , name = "ncr" ),
    path('unewncr/', views.newncr , name = "newncr" ),
    path('uqr/', views.qr , name = "qr" ),
    path('unewqr/', views.newqr , name = "newqr" ),


    path('uwelderperformance/', views.welderperformance , name = "welderperformance" ),


    # spool
    path('uspool/', views.spool , name = "spool" ),

    # painting
    path('upainting/', views.painting , name = "painting" ),
    path('fetch-nde-details/',views.fetch_ndeGrade, name= "fetchndegrade"),
    path('fetch-weld-details/',views.fetch_weldGrade, name= "fetchweldgrade"),
    path('fetch-ndereq-details/',views.fetch_ndereqGrade, name= "fetchndereqgrade"),
    path('fetch-weld-grade/',views.fetch_weld_matGrade, name= "fetchweldgrade"),
    path('fetch-welder/',views.fetch_welder, name= "fetchwelder"),



    path('utfascanner_dashboard/', views.tfascanner_dashboard , name = "tfascanner_dashboard" ),

    path('utfascanner/', views.tfascanner , name = "tfascanner" ),
    path('utfaspec/<int:id>/', views.tfaspec , name = "tfaspec" ),
    path('utfa_break/', views.tfa_break , name = "tfa_break" ),
    path('utfa_specedit/<int:id>/', views.tfa_specedit , name = "tfa_specedit" ),
    path('utfa_overview/<int:id>/', views.tfa_overview , name = "tfa_overview" ),
    path('utfa_pass/<int:id>/', views.tfa_pass , name = "tfa_pass" ),
    path('utfa_pass_create/', views.tfa_pass_create , name = "tfa_pass_create" ),
    path('utfa_photos/<int:id>/', views.tfa_photos , name = "tfa_photos" ),
    path('utfa_photos_create/', views.tfa_photos_create , name = "tfa_photos_create" ),
    path('utfa_report/<int:id>/', views.tfa_report , name = "tfa_report" ),
    path('ufiter_list/', views.fiter_list , name = "fiter_list" ),
    path('ufiter_pass/<int:id>/', views.fiter_pass , name = "fiter_pass" ),
    path('ufitter_photos/<int:id>/', views.fitter_photos , name = "fitter_photos" ),
    path('ufitter_succ/<int:id>/', views.fitter_succ , name = "fitter_succ" ),
    path('uqc_list/', views.qc_list , name = "qc_list" ),
    path('uqc_overview/<int:id>/', views.qc_overview , name = "qc_overview" ),
    path('uqc_succ/<int:id>/', views.qc_succ , name = "qc_succ" ),
    path('uqc_verfication/<int:id>/', views.qc_verfication , name = "qc_verfication" ),







  
    



]