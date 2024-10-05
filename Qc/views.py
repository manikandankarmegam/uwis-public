from django.shortcuts import render
from Ad.models import * 
from Qc.models import *
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.db import transaction
from datetime import datetime
from django.db.models import Count, Max, Min
import json
import math
# project
def project_views(request):
    return render(request,'project.html')

def mainproject(request, id):
    
    pro = project.objects.get(id=id)
    print(pro)
    return render(request,'mainproject.html',{'project':pro})

# weldhistory
def weldhistory(request,drg,sh,rev):
    try:
        if request.method == "GET":
            active_project = request.COOKIES.get('active_project')
            if active_project and project.objects.filter(projectno=active_project).exists():
                active_project_obj = project.objects.filter(projectno=active_project).first()
                spool = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno = drg , sheetno = sh)
                
                weldnum= spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('weldno').distinct()
                spoolnum= spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('spoolno').distinct()
                locations=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('location').distinct()
                pipesizes=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('size').distinct()
                pipethickness=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('thk').distinct()
                weldtype=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('type').distinct()
                mtpt=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('mtpt').distinct()
                wpsnum=w_p_s.objects.values('id','wpsno').distinct()
                welder_list = []
                for welder_obj in active_project_obj.welders.all():
                    welder_list.append({
                        "id": welder_obj.id,
                        "weldname": welder_obj.weldname,
                        "welderid": welder_obj.welderid,
                        "wps": list(welder_obj.weldwps.all().values_list("wpsno", flat=True))
                    })
                
                part_no_list = MIRUpload.objects.filter(project=active_project_obj).values('part_id')
            else:
                spool = spoolgenmaterialsuploadss.objects.filter(drgno = drg , sheetno = sh)

                weldnum= spoolgenmaterialsuploadss.objects.values('weldno').distinct()
                spoolnum= spoolgenmaterialsuploadss.objects.values('spoolno').distinct()
                locations=spoolgenmaterialsuploadss.objects.values('location').distinct()
                pipesizes=spoolgenmaterialsuploadss.objects.values('size').distinct()
                pipethickness=spoolgenmaterialsuploadss.objects.values('thk').distinct()
                weldtype=spoolgenmaterialsuploadss.objects.values('type').distinct()
                mtpt=spoolgenmaterialsuploadss.objects.values('mtpt').distinct()
                wpsnum=w_p_s.objects.values('id','wpsno').distinct()
                welder_list = []
                for welder_obj in welder.objects.all():
                    welder_list.append({
                        "id": welder_obj.id,
                        "weldname": welder_obj.weldname,
                        "welderid": welder_obj.welderid,
                        "wps": list(welder_obj.weldwps.all().values_list("wpsno", flat=True))
                    })
                materials = mat.objects.all()
                grade_choices = {}
                for spool_data in spool:
                    if spool_data.material.isdigit():
                        product = materialsgrade.objects.filter(mat__id=spool_data.material)
                    else:
                        product = materialsgrade.objects.filter(mat__materials=spool_data.material)
                    choices = []
                    for product_instance in product:
                        choices.append({
                            'id': product_instance.id,
                            'GradeNmae': product_instance.materialgrade,
                        })
                    grade_choices[spool_data.id] = choices
                part_no_list = MIRUpload.objects.all().values('part_id')
            materials = mat.objects.all()
            grade_choices = {}
            for spool_data in spool:
                if spool_data.material.isdigit():
                    product = materialsgrade.objects.filter(mat__id=spool_data.material)
                else:
                    product = materialsgrade.objects.filter(mat__materials=spool_data.material)
                choices = []
                for product_instance in product:
                    choices.append({
                        'id': product_instance.id,
                        'GradeNmae': product_instance.materialgrade,
                    })
                grade_choices[spool_data.id] = choices
            return render(request,'weldhistory.html',{'data':spool,'drg':drg,'sh':sh,'rev':rev,'weldno':weldnum,
                                                    'spoolno':spoolnum,'location':locations,'pipesise':pipesizes,
                                                    'pipethicknes':pipethickness,'weldtypes':weldtype,
                                                    'mtpts':mtpt,'wpsno':wpsnum, 'part_no_list':part_no_list,
                                                    'welder_list':welder_list, 'mat':materials, 'grade_choices':grade_choices
                                                    })
    except Exception as exc:
        print(exc)


def weldhistory_form_download(request):
    try:
        drg= request.GET.get("drgno")
        sh = request.GET.get("sheetno")
        rev = request.GET.get("rev")
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            spool = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg,sheetno=sh)
        else:
            spool = spoolgenmaterialsuploadss.objects.filter(drgno=drg,sheetno=sh)
        if request.GET.get("fitup_type"):
            spool = spool.filter(location=request.GET.get("fit_type"))
        return render(request,'weldhistory_form_download.html',{'data':spool,'drg':drg,'sh':sh,'rev':rev})
    except Exception as exc:
        print(exc)


def weldsummary_form_download(request):
    try:
        drg= request.GET.get("drgno")
        sh = request.GET.get("sheetno")
        rev = request.GET.get("rev")
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            spool = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg,sheetno=sh)
        else:
            spool = spoolgenmaterialsuploadss.objects.filter(drgno=drg,sheetno=sh)
        if request.GET.get("fitup_type"):
            spool = spool.filter(location=request.GET.get("fit_type"))
        return render(request,'weldsummary_form_download.html',{'data':spool,'drg':drg,'sh':sh,'rev':rev})
    except Exception as exc:
        print(exc)


def updateWeld(request,id):
    try:
        if request.method == "POST":

            spool = spoolgenmaterialsuploadss.objects.get(id=id)
            drg = spool.drgno
            sh = spool.sheetno
            rev = spool.rev

            weldnum = request.POST.get('weldnum')
            pipesize = request.POST.get('pipesize')
            thickness=request.POST.get('thickness')
            spoolno = request.POST.get('spoolno')
            Parta = request.POST.get('parta')
            material =request.POST.get('material')
            location =request.POST.get('location')
            grade =request.POST.get('grade')
            weldtype =request.POST.get('weldtype')
            ndereqt =request.POST.get('ndereqt')
            mtpt =request.POST.get('mtpt')
            grade = request.POST.get('grade')
            rtrepair=request.POST.get('rtrepair')
            start=request.POST.get('start',"")
            end=request.POST.get('end',"")
            fitup=request.POST.get('fitup',"")
            wpsnum=request.POST.get('wpsnum')
            welder1=request.POST.get('welder1')
            welder2=request.POST.get('welder2')
            partnoA=request.POST.get('partnoA')
            mat_A=request.POST.get('mat_A')
            heat_A=request.POST.get('heat_A')
            cert_A=request.POST.get('cert_A')
            partnoB=request.POST.get('partnoB')
            mat_B=request.POST.get('mat_B')
            heat_B=request.POST.get('heat_B')
            cert_B=request.POST.get('cert_B')
            if fitup == '':
                fitup = None
            if start == '':
                start = None
            if end == '':
                end = None
            try:
                # spoolgenmaterialsuploadss.objects.filter(id=id).update(welder1=welder.objects.get(id=int(welder1)),welder2=welder.objects.get(id=int(welder2)),grade=materialsgrade.objects.get(id=int(grade)),wpsnum=w_p_s.objects.get(id=wpsnum),fitupdate=fitup,size=pipesize,thk=thickness,weldno=weldnum,spoolno=spoolno,
                #                                                     location= location,rtrepair=rtrepair,material=material,type=weldtype,rt=ndereqt,mtpt=mtpt,start=start,end=end)
                
                spool.welder1=welder.objects.get(id=int(welder1))
                spool.welder2=welder.objects.get(id=int(welder2))
                spool.grade=materialsgrade.objects.get(id=int(grade))
                spool.wpsnum=w_p_s.objects.get(id=wpsnum)
                spool.fitupdate=fitup
                spool.size=pipesize
                spool.thk=thickness
                spool.weldno=weldnum
                spool.spoolno=spoolno
                spool.location= location
                spool.rtrepair=rtrepair
                spool.material=material
                spool.type=weldtype
                spool.rt=ndereqt
                spool.mtpt=mtpt
                spool.start=start
                spool.end=end
                spool.partnoA=partnoA
                spool.mat_A=mat_A
                spool.heat_A=heat_A
                spool.cert_A=cert_A
                spool.partnoB=partnoB
                spool.mat_B=mat_B
                spool.heat_B=heat_B
                spool.cert_B=cert_B
            except Exception as exc:
                print(exc)
            if spool.fitupdate and spool.welder1 and spool.welder2 and spool.start and spool.end:
                spool.is_nde_request_raised = True
            spool.save()                                                  

            return redirect(reverse('weldhistory', args=(drg, sh,rev)))

    except Exception as exc:
        print(exc)

def newweldhistory(request):
    return render(request,'newweldhistory.html')

def sheetweldhistory(request):
    # if request.method == 'GET'and 'search_term' in request.GET:
    #     search_term = request.GET.get('search_term', None)
        
    #     filtered_rows = spoolgenmaterialsuploadss.objects.filter(drgno__icontains=search_term).distinct('drgno')
            
    #     # Extracting unique values from the filtered records
    #     unique_values = filtered_rows.values_list('drgno', flat=True).distinct()
    #     print(search_term) 
    #     print(unique_values)

    #     filtered_rows = spoolgenmaterialsuploadss.objects.filter(drgno__icontains=search_term)
    
    #     # Grouping by 'drgno' and 'sheet_number' and annotating the count
    #     drgno_counts = filtered_rows.values('drgno', 'sheetno').annotate(drgno_count=Count('drgno'))
    #     print(drgno_counts)

    #     return render(request, 'sheetweldhistory.html', {'data': unique_values, 'search_term': search_term})

    # return render(request, 'sheetweldhistory.html')
    try:
        if request.method == 'GET' and 'search_term' in request.GET:
            search_term = request.GET.get('search_term', None)
            
            # Filtering records based on search_term
            # Filter the records based on the search term
            
            active_project = request.COOKIES.get('active_project')
            if active_project and project.objects.filter(projectno=active_project).exists():
                active_project_obj = project.objects.filter(projectno=active_project).first()
                print(11)
                filtered_rows = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno__icontains=search_term)
                print(3222)
            else:
                filtered_rows = spoolgenmaterialsuploadss.objects.filter(drgno__icontains=search_term)
            drg_id = ""
            locations = filtered_rows.values('location').distinct().exclude(location__isnull=True)
            if filtered_rows.last():drg_id = filtered_rows.last().id
            # Group the records by 'drgno', 'sheetno', and 'rev' and count them
            drgno_counts = filtered_rows.values('drgno', 'sheetno', 'rev').annotate(record_count=Count('id'))

            # Constructing a list to organize data for the template
            organized_data = []
            for item in drgno_counts:
                drgno = item['drgno']
                sheetno = item['sheetno']
                rev = item['rev']
                record_count = item['record_count']
                organized_data.append({'drgno': drgno, 'sheetno': sheetno, 'rev': rev, 'record_count': record_count})
            return render(request, 'sheetweldhistory.html', {'search_term': search_term, 'drgno_counts': organized_data, "drg_id":drg_id, 'location':locations})
        else:
            return render(request, 'sheetweldhistory.html', {})
    except Exception as exc:
        print(exc)

def newdrawing(request):
    return render(request,'newdrawing.html')

def iso(request):
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        latest_ids = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).exclude(drgno__isnull=True).values('drgno').annotate(
            latest_id=Max('id')
        ).values('latest_id')
    else:
        latest_ids = spoolgenmaterialsuploadss.objects.exclude(drgno__isnull=True).values('drgno').annotate(
            latest_id=Max('id')
        ).values('latest_id')

    distinct_queryset = spoolgenmaterialsuploadss.objects.filter(id__in=latest_ids)

    return render(request,'iso.html',{'data': distinct_queryset})

def newiso(request):
     if request.method =='POST':
        isonumber =request.POST.get('isonumber')
        drgprefix =request.POST.get('drg')
        hold=request.POST.get('hold')
        subproject=request.POST.get('subproject')
        pcno=request.POST.get('pcnop')
        pipeclss=request.POST.get('pipeclass')
        area=request.POST.get('area')
        lineno=request.POST.get('lineno')
        service=request.POST.get('service')
        pidno=request.POST.get('pidno')
        tpress=request.POST.get('tpress')
        tmedia=request.POST.get('tmedia')
        mom=request.POST.get('mom')
        accept=request.POST.get('accept')
        matl=request.POST.get('matl')
        rt=request.POST.get('rt')
        pwht=request.POST.get('pwht')
        bhn=request.POST.get('bhn')
        ferraite=request.POST.get('ferraite')
        mtpt=request.POST.get('mtpt')
        pmi=request.POST.get('pmi')
        insulation=request.POST.get('insulation')
        paint=request.POST.get('paint')
        opttemp=request.POST.get('opttemp')
        itemno=request.POST.get('itemno')
        contractno=request.POST.get('contractno')
        unitno=request.POST.get('unitno')
        plate=request.POST.get('plate')
        length=request.POST.get('length')
        thk=request.POST.get('thk')
        weldcondition=request.POST.get('weldcondition')
        ground=request.POST.get('ground')
        welded=request.POST.get('welded')
        treatment=request.POST.get('treatment')
        pre=request.POST.get('pre')
        post=request.POST.get('post')
        rule=request.POST.get('rule')
        weldinggauge=request.POST.get('weldgauge')
        magnify=request.POST.get('magnify')
        others=request.POST.get('others')
        finalsurface=request.POST.get('finalsurface')
        sheetno=request.POST.get('sheetno')
        revno=request.POST.get('revno')
        currentrev=request.POST.get('currentrev')
        revision=request.POST.get('revision')
        spool_obj = spoolgenmaterialsuploadss.objects.create(drgno=isonumber,subproject=subproject,pcno=pcno,piping=pipeclss,
                       area=area,lineno=lineno,service=service,pidno=pidno,tpress=tpress,tmedia=tmedia,mom=mom,
                       acceptance=accept,material=matl,pwht=pwht,bhn=bhn,ferraite=ferraite,mtpt=mtpt,pmi=pmi,
                       insulation=insulation,paint=paint,opttemp=opttemp,unit=unitno,
                       thk=thk, drgprefix=drgprefix, hold=hold, itemno=itemno, contractno=contractno,
                       sheetno=sheetno, rt=rt,rev=revno)
        print(spool_obj,"spool_obj")
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project = project.objects.filter(projectno=active_project).first()
            spool_obj.ProId = active_project
            spool_obj.save()
        return redirect ("iso")
     else:
        return render(request,'newiso.html')


def detailiso(request,proid):
    qc_detail=spoolgenmaterialsuploadss.objects.get(id=proid)
    return render(request,'detailiso.html',{'data':qc_detail})


def isoedit(request,id):
    data = spoolgenmaterialsuploadss.objects.filter(id=id).first()
    if request.method =='POST':
        isonumber =request.POST.get('isonumber')
        drgprefix =request.POST.get('drg')
        hold=request.POST.get('hold')
        subproject=request.POST.get('subproject')
        pcno=request.POST.get('pcnop')
        pipeclss=request.POST.get('pipeclass')
        area=request.POST.get('area')
        lineno=request.POST.get('lineno')
        service=request.POST.get('service')
        pidno=request.POST.get('pidno')
        tpress=request.POST.get('tpress')
        tmedia=request.POST.get('tmedia')
        mom=request.POST.get('mom')
        accept=request.POST.get('accept')
        matl=request.POST.get('matl')
        rt=request.POST.get('rt')
        pwht=request.POST.get('pwht')
        bhn=request.POST.get('bhn')
        ferraite=request.POST.get('ferraite')
        mtpt=request.POST.get('mtpt')
        pmi=request.POST.get('pmi')
        insulation=request.POST.get('insulation')
        paint=request.POST.get('paint')
        opttemp=request.POST.get('opttemp')
        itemno=request.POST.get('itemno')
        contractno=request.POST.get('contractno')
        unitno=request.POST.get('unitno')
        plate=request.POST.get('plate')
        length=request.POST.get('length')
        thk=request.POST.get('thk')
        weldcondition=request.POST.get('weldcondition')
        ground=request.POST.get('ground')
        welded=request.POST.get('welded')
        treatment=request.POST.get('treatment')
        pre=request.POST.get('pre')
        post=request.POST.get('post')
        rule=request.POST.get('rule')
        weldinggauge=request.POST.get('weldgauge')
        magnify=request.POST.get('magnify')
        others=request.POST.get('others')
        finalsurface=request.POST.get('finalsurface')
        sheetno=request.POST.get('sheetno')
        currentrev=request.POST.get('currentrev')
        revision=request.POST.get('revision')
        revno=request.POST.get('revno')
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project = project.objects.filter(projectno=active_project).first()
            spoolgenmaterialsuploadss.objects.filter(id=id).update(drgno=isonumber,subproject=subproject,pcno=pcno,piping=pipeclss,
                       area=area,lineno=lineno,service=service,pidno=pidno,tpress=tpress,tmedia=tmedia,mom=mom,
                       acceptance=accept,material=matl,pwht=pwht,bhn=bhn,ferraite=ferraite,mtpt=mtpt,pmi=pmi,
                       insulation=insulation,paint=paint,opttemp=opttemp,unit=unitno,
                       thk=thk, drgprefix=drgprefix, hold=hold, itemno=itemno, contractno=contractno,rev=revno,
                       sheetno=sheetno, rt=rt, ProId=active_project)
        else:
            spoolgenmaterialsuploadss.objects.filter(id=id).update(drgno=isonumber,subproject=subproject,pcno=pcno,piping=pipeclss,
                       area=area,lineno=lineno,service=service,pidno=pidno,tpress=tpress,tmedia=tmedia,mom=mom,
                       acceptance=accept,material=matl,pwht=pwht,bhn=bhn,ferraite=ferraite,mtpt=mtpt,pmi=pmi,
                       insulation=insulation,paint=paint,opttemp=opttemp,unit=unitno,
                       thk=thk, drgprefix=drgprefix, hold=hold, itemno=itemno, contractno=contractno,rev=revno,
                       sheetno=sheetno, rt=rt)
        return redirect ("iso")
    else:
        return render(request,'newiso.html' ,{'data': data} )

        
    

def isodel(request):
    if request.method =='POST':
        if request.POST.get('delete_type') == "iso_sheet":
            print(request.POST)
            active_project = request.COOKIES.get('active_project')
            if active_project and project.objects.filter(projectno=active_project).exists():
                active_project_obj = project.objects.filter(projectno=active_project).first()
                isodel=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=request.POST.get('drgno'),sheetno=request.POST.get('sheet_no'),rev=request.POST.get('rev')).delete()
            else:   
                active_project = request.COOKIES.get('active_project')
                if active_project and project.objects.filter(projectno=active_project).exists():
                    active_project_obj = project.objects.filter(projectno=active_project).first() 
                    isodel=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=request.POST.get('drgno'),sheetno=request.POST.get('sheet_no'),rev=request.POST.get('rev')).delete()
                else:
                    isodel=spoolgenmaterialsuploadss.objects.filter(drgno=request.POST.get('drgno'),sheetno=request.POST.get('sheet_no'),rev=request.POST.get('rev')).delete()
            url = f"{reverse('sheetweldhistory')}?search_term={request.POST.get('drgno')}"
            return redirect(url)
        elif request.POST.get('delete_type') == "iso":
            spoolgenmaterialsuploadss.objects.filter(drgno=request.POST.get('drgno')).delete()
            return redirect('iso')
    

def search(request):
    query = request.GET.get('query')
    if query:
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            results = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno__icontains=query).values('drgno').distinct()
        else:
            results = spoolgenmaterialsuploadss.objects.filter(drgno__icontains=query).values('drgno').distinct()

        results = list(results)
    else:
        results = []

    print(query)
    print(results)

    return JsonResponse({'results': results})



# def addsheet(request,drg):
#     print(drg)
#     drgs = spoolgenmaterialsuploadss.objects.filter(drgno = drg)

#      # Check if there are any rows with the specified drgno
#     if drgs.exists():
#         # Get the maximum sheet number among the filtered rows
#         max_sheet_number = drgs.aggregate(max_sheet_number=models.Max('sheetno'))['max_sheet_number']
        
#         # Increment the maximum sheet number by 1 to get the next sheet number
#         next_sheet_number = int(max_sheet_number) + 1
        
#         # Create a new row with the next sheet number
#         new_row = spoolgenmaterialsuploadss(drgno=drg, sheetno=next_sheet_number)
#         new_row.save()

#     # Construct the URL with query parameters
    
#     url = f"{reverse('sheetweldhistory')}?search_term={drg}"
    
#     # Redirect to the constructed URL
#     return redirect(url)

# def addrev(request, drg, sheetno):

#     print(drg,"45454545454")

#     print(sheetno)
#     # Filter rows with the specified 'drgno', 'sheetno', and 'rev' number
#     drgs = spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno)
    
#     # Check if there are any rows with the specified drgno and sheetno
#     if drgs.exists():
#         # Get the latest rev number for the specified 'drgno' and 'sheetno'
#         latest_rev = drgs.latest('id').rev

#         if latest_rev is None:
#         # If there are no existing rows, set the rev to 1
#             latest_rev = 1
#         else:
#             # Convert latest_rev to an integer and increment it
#             latest_rev = int(latest_rev) + 1
        
#         # Create a new row with the same 'drgno', 'sheetno', and 'rev' number
#         new_row = spoolgenmaterialsuploadss(drgno=drg, sheetno=sheetno, rev=latest_rev)
#         new_row.save()

#     url = f"{reverse('sheetweldhistory')}?search_term={drg}"
    
#     # Redirect to the constructed URL
#     return redirect(url)



def addtext(request,drg,sheetno):
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        drgs = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg, sheetno=sheetno)
    else:    
        drgs = spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno)

    # Check if there are any rows with the specified drgno and sheetno
    if drgs.exists():
        # Get the latest rev number for the specified 'drgno' and 'sheetno'
        latest_rev = drgs.latest('id').rev
        
        try:
            if latest_rev[-1].isdigit():
                next_rev = latest_rev + "A"
            elif latest_rev[-1].upper() < 'Z':
                next_rev = latest_rev[:-1] + chr(ord(latest_rev[-1].upper()) + 1)
            else:
                next_rev = latest_rev
            # Calculate the next rev value
            # next_rev = get_next_rev(latest_rev)
        except ValueError as e:
            # Handle the error (e.g., log it, display a message to the user)
            return str(e)  # Return error message for simplicity

        # Update the 'rev' field for all matching rows
        with transaction.atomic():
            active_project = request.COOKIES.get('active_project')
            if active_project and project.objects.filter(projectno=active_project).exists():
                active_project_obj = project.objects.filter(projectno=active_project).first()
                spoolgenmaterialsuploadss.objects.filter(ProdId=active_project_obj,drgno=drg, sheetno=sheetno).update(rev=next_rev)
            else:    
                spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno).update(rev=next_rev)

        url = f"{reverse('sheetweldhistory')}?search_term={drg}"
        # Redirect to the constructed URL
        return redirect(url)

def removetext(request,drg,sheetno):
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        drgs = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg, sheetno=sheetno)
    else:
        drgs = spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno)

    # Check if there are any rows with the specified drgno and sheetno
    if drgs.exists():
        # Get the latest rev number for the specified 'drgno' and 'sheetno'
        latest_rev = drgs.latest('id').rev
        
        try:
            if latest_rev[-1].isdigit():
                next_rev = latest_rev
            elif latest_rev[-1].upper()=='A':
                next_rev = latest_rev[:-1]
            else:
                next_rev = latest_rev[:-1] + chr(ord(latest_rev[-1].upper()) - 1)
            # Calculate the next rev value
            # next_rev = get_prev_rev(latest_rev)
        except ValueError as e:
            # Handle the error (e.g., log it, display a message to the user)
            return str(e)  # Return error message for simplicity

        # Update the 'rev' field for all matching rows
        with transaction.atomic():
            active_project = request.COOKIES.get('active_project')
            if active_project and project.objects.filter(projectno=active_project).exists():
                active_project_obj = project.objects.filter(projectno=active_project).first()
                spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg, sheetno=sheetno).update(rev=next_rev)
            else:
                spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno).update(rev=next_rev)

        url = f"{reverse('sheetweldhistory')}?search_term={drg}"
        # Redirect to the constructed URL
        return redirect(url)


def addrecord(request):
    return render(request,'addrecord.html')
def view_record_list(request):
    return render(request,'view_record_list.html')

def view_record_create(request):
    return render(request,'view_record_create.html')

def view_record_detail(request):
    return render(request,'view_record_detail.html')


# nde
# def ndemonitor(request):
#     if request.method == 'GET' :
        
#         location = request.GET.get('location', '')
#         nde_type = request.GET.get('nde_type', '')
#         nde_percentage = request.GET.get('nde_percentage', '')
#         pipe_class = request.GET.get('pipe_class', '')
#         Welder = request.GET.get('welder', '')
#         weld_type = request.GET.get('weld_type', '')

#         start_date_str = request.GET.get('start_date', '')
#         end_date_str = request.GET.get('end_date', '')


#         loc = spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('location').distinct().exclude(location__isnull=True)
#         bhn = spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('bhn').distinct()
#         rt=spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('rt').distinct()
#         ferraite=spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('ferraite').distinct()
#         mtpt=spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('mtpt').distinct()
#         pmi=spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('pmi').distinct()
#         piping_list=spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('piping').distinct().exclude(piping__isnull=True)
#         weld_type_list=spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True).values('type').distinct().exclude(type__isnull=True)

#         cust_list = spoolgenmaterialsuploadss.objects.filter(is_nde_request_raised=True)
#         print(cust_list)
#         request_no_dct = {} 
#         for nde_process in nderequestprocess.objects.all():
#             request_no_dct[nde_process.searchprocess.id] = nde_process
#         welder_list = []
#         for welder_obj in welder.objects.all():
#             welder_list.append({
#                 "id": welder_obj.id,
#                 "weldname": welder_obj.weldname,
#                 "welderid": welder_obj.welderid
#             })

#         valid_fields = [
#         'ProId', 'ProId_id', 'acceptance', 'area', 'batch', 'bhn', 'drgno', 
#         'ferraite', 'id', 'insulation', 'lineno', 'location', 'material', 
#         'mom', 'mtpt', 'opttemp', 'paint', 'partrid', 'pcno', 'pidno', 
#         'piping', 'pmi', 'pwht', 'rev', 'rt', 'service', 'sheetno', 'size', 
#         'spoolno', 'subproject', 'thk', 'tiein', 'tmedia', 'tpress', 'type', 
#         'unit', 'weldno'
#         ]

#         if location:
#             cust_list = cust_list.filter(location=location)

#         if nde_percentage:
#             if nde_type in valid_fields:
#                 filter_kwargs = {nde_type: nde_percentage}

#                 cust_list = cust_list.filter(**filter_kwargs)

#         if pipe_class:
#             cust_list = cust_list.filter(piping=pipe_class)

#         if Welder:
#             cust_list = cust_list.filter(Q(welder1__id=Welder)|Q(welder2__id=Welder))

#         if weld_type:
#             cust_list = cust_list.filter(type=weld_type)

#         if start_date_str:
#                 try:
#                     cust_list = cust_list.filter(start__gte=start_date_str)
#                 except ValueError:
#                     pass 

#         if end_date_str:
#             try:
#                 cust_list = cust_list.filter(end__lte=end_date_str)
#             except ValueError:
#                 pass  
#         print(cust_list)
#         data = {
#             'locations':loc,
#             'bhns' : bhn,
#             'rts'  :rt,
#             'ferraites':ferraite,
#             'mtpts':mtpt,
#             'pmis':pmi,
#             'list':cust_list,
#             'welder_list': welder_list,
#             'piping_list': piping_list,
#             'weld_type_list': weld_type_list,
#             'request_no_dct': request_no_dct
#         }
#         return render(request,'ndemonitor.html',data)


def ndemonitor(request):
    if request.method == 'GET':
        
        location = request.GET.get('location', '')
        nde_type = request.GET.get('nde_type', '')
        nde_percentage = request.GET.get('nde_percentage', '')
        pipe_class = request.GET.get('pipe_class', '')
        Welder = request.GET.get('welder', '')
        weld_type = request.GET.get('weld_type', '')

        start_date_str = request.GET.get('start_date', '')
        end_date_str = request.GET.get('end_date', '')
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            proj_nos = [active_project]
        else:
            active_project_obj = None
            proj_nos = list(project.objects.all().values_list('projectno', flat=True))
        loc = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('location').distinct().exclude(location__isnull=True)
        bhn = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('bhn').distinct()
        rt = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('rt').distinct()
        ferraite = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('ferraite').distinct()
        mtpt = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('mtpt').distinct()
        pmi = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('pmi').distinct()
        piping_list = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('piping').distinct().exclude(piping__isnull=True)
        weld_type_list = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('type').distinct().exclude(type__isnull=True)

        cust_list = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True)
        
        request_no_dct = {}
        for nde_process in nderequestprocess.objects.filter(searchprocess__ProId__projectno__in=proj_nos):
            request_no_dct[nde_process.searchprocess.id] = nde_process

        
        welder_list = []
        if active_project_obj:
            for welder_obj in active_project_obj.welders.all():
                welder_list.append({
                    "id": welder_obj.id,
                    "weldname": welder_obj.weldname,
                    "welderid": welder_obj.welderid
                })
        else:
            for welder_obj in welder.objects.all():
                welder_list.append({
                    "id": welder_obj.id,
                    "weldname": welder_obj.weldname,
                    "welderid": welder_obj.welderid
                })

        valid_fields = [
            'ProId', 'ProId_id', 'acceptance', 'area', 'batch', 'bhn', 'drgno', 
            'ferraite', 'id', 'insulation', 'lineno', 'location', 'material', 
            'mom', 'mtpt', 'opttemp', 'paint', 'partrid', 'pcno', 'pidno', 
            'piping', 'pmi', 'pwht', 'rev', 'rt', 'service', 'sheetno', 'size', 
            'spoolno', 'subproject', 'thk', 'tiein', 'tmedia', 'tpress', 'type', 
            'unit', 'weldno'
        ]

        # Applying filters based on user input
        if location:
            cust_list = cust_list.filter(location=location)

        if nde_percentage:
            if nde_type in valid_fields:
                filter_kwargs = {nde_type: nde_percentage}
                cust_list = cust_list.filter(**filter_kwargs)

        if pipe_class:
            cust_list = cust_list.filter(piping=pipe_class)

        if Welder:
            cust_list = cust_list.filter(Q(welder1__id=Welder) | Q(welder2__id=Welder))

        if weld_type:
            cust_list = cust_list.filter(type=weld_type)

        if start_date_str:
            try:
                cust_list = cust_list.filter(start__gte=start_date_str)
            except ValueError:
                pass  # Handle invalid date format or other errors here

        if end_date_str:
            try:
                cust_list = cust_list.filter(end__lte=end_date_str)
            except ValueError:
                pass  # Handle invalid date format or other errors here

        # Map the request_no and date fields from request_no_dct to each nde entry
        for nde in cust_list:
            nde.requestno = "-"
            nde.date = "-"
            if nde.id in request_no_dct:
                nde.requestno = request_no_dct[nde.id].requestno
                nde.date = request_no_dct[nde.id].date

        # Pass all context data
        data = {
            'locations': loc,
            'bhns': bhn,
            'rts': rt,
            'ferraites': ferraite,
            'mtpts': mtpt,
            'pmis': pmi,
            'list': cust_list,
            'welder_list': welder_list,
            'piping_list': piping_list,
            'weld_type_list': weld_type_list,
            'request_no_dct': request_no_dct
        }
        return render(request, 'ndemonitor.html', data)

    
def nderequestno(request):

            return render(request,'ndemonitor.html')

def nderequestnoreq(request):
            
            if request.method == 'POST':
                # Parse the JSON data
                data = json.loads(request.body)

                ndt = data.get('date')
                rqs = data.get('req')
                material = data.get('cate')
                selected_spools = data.get('selected_spools', [])
                
                # Process the selected spool IDs as needed

                for i in selected_spools:
                    if nderequestprocess.objects.filter(searchprocess__id=i).exists():
                        nderequestprocess.objects.filter(searchprocess__id=i).update(ndttypes=material,requestno=rqs,date=ndt)
                    else:
                        nderequestprocess.objects.create(ndttypes=material,requestno=rqs,searchprocess_id=i,date=ndt)

                # Return a JSON response
                return JsonResponse({'status': 'success', 'data': selected_spools})
            
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def ndereportrequestnoreq(request):
            
            if request.method == 'POST':
                # Parse the JSON data
                data = json.loads(request.body)
                category = data.get('category')
                reportno = data.get('reportno')
                date = data.get('date')
                flim_accept = data.get('flim_accept')
                flim_reject = data.get('flim_reject')
                selected_spools = data.get('selected_spools', [])
                
                # Process the selected spool IDs as needed

                for i in selected_spools:
                    ndereportrequestprocess.objects.create(category=category,reportno=reportno,ndereqprocess_id=i,date=date,flim_accept=flim_accept,flim_reject=flim_reject)

                # Return a JSON response
                return JsonResponse({'status': 'success', 'data': selected_spools})
            
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def fetch_ndeGrade(request):

    material = request.GET.get('material')
    print(material, "scad barcode ----------------")
    
    try:
        product_data = []
        active_project = request.COOKIES.get('active_project')
        active_project_obj = None
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
        if material == "RT":
            if active_project_obj:
                product = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('rt').distinct().exclude(rt__isnull=True).exclude(rt__exact='')
            else:
                product = spoolgenmaterialsuploadss.objects.values('rt').distinct().exclude(rt__isnull=True).exclude(rt__exact='')

            for product_instance in product:
                product_data.append({
                    
                    'GradeNmae': product_instance['rt'],
                    # Include other product details as needed
                })
                print(product_data)
        elif material == "MTPT":
            if active_project_obj:
                product = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('mtpt').distinct().exclude(mtpt__isnull=True).exclude(mtpt__exact='')
            else:
                product = spoolgenmaterialsuploadss.objects.values('mtpt').distinct().exclude(mtpt__isnull=True).exclude(mtpt__exact='')
            

            for product_instance in product:
                product_data.append({
                    
                    'GradeNmae': product_instance['mtpt']
                    # Include other product details as needed
                })
                print(product_data)
        elif material == "PMI":
            if active_project_obj:
                product = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('pmi').distinct().exclude(pmi__isnull=True).exclude(pmi__exact='')
            else:
                product = spoolgenmaterialsuploadss.objects.values('pmi').distinct().exclude(pmi__isnull=True).exclude(pmi__exact='')
            

            for product_instance in product:
                product_data.append({
                    
                    'GradeNmae': product_instance['pmi'],
                    # Include other product details as needed
                })


        # product_data = []

        # for product_instance in product:
        #     product_data.append({
                
        #         'GradeNmae': product_instance.,
        #         # Include other product details as needed
        #     })
        #     print(product_data)
        return JsonResponse({'products': product_data})

    except materialsgrade.DoesNotExist:
        data = {'error': 'not found'}
        return JsonResponse(data, status=404)
    

def fetch_welder(request):

    wpsId = request.GET.get('wpsId')
    
    try:
        welder_list = []
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            for welder_obj in active_project_obj.welders.filter(weldwps__id=wpsId):
                welder_list.append({
                    "id": welder_obj.id,
                    "weldname": welder_obj.weldname,
                    "welderid": welder_obj.welderid
                })
        else:
            for welder_obj in welder.objects.filter(weldwps__id=wpsId):
                welder_list.append({
                    "id": welder_obj.id,
                    "weldname": welder_obj.weldname,
                    "welderid": welder_obj.welderid,
                    "wps": list(welder_obj.weldwps.all().values_list("wpsno", flat=True))
                })

        
        return JsonResponse({'welders': welder_list})

    
    except Exception as e:
        data = {'error': 'not found'}
        return JsonResponse(data, status=404)
    
def fetch_weld_matGrade(request):

    material = request.GET.get('material')
    print(material, "scad barcode ----------------")
    
    try:
        product_data = []
        
        product = materialsgrade.objects.filter(mat_id=material)
        print(product)

        for product_instance in product:
            product_data.append({
                
                'id': product_instance.id,
                'GradeNmae': product_instance.materialgrade,
                # Include other product details as needed
            })
            print(product_data)

        # product_data = []

        # for product_instance in product:
        #     product_data.append({
                
        #         'GradeNmae': product_instance.,
        #         # Include other product details as needed
        #     })
        #     print(product_data)
        return JsonResponse({'products': product_data})

    
    except materialsgrade.DoesNotExist:
        data = {'error': 'not found'}
        return JsonResponse(data, status=404)
    
def fetch_ndereqGrade(request):

    material = request.GET.get('material')
    
    try:
        product_data = []
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            product = nderequestprocess.objects.filter(searchprocess__ProId=active_project_obj,ndttypes=material).values('requestno').distinct().exclude(requestno__isnull=True).exclude(requestno__exact='')
        else:  
            product = nderequestprocess.objects.filter(ndttypes=material).values('requestno').distinct().exclude(requestno__isnull=True).exclude(requestno__exact='')
        

        for product_instance in product:
            product_data.append({
                
                'GradeNmae': product_instance['requestno'],
                # Include other product details as needed
            })
    
        return JsonResponse({'products': product_data})
    except materialsgrade.DoesNotExist:
        data = {'error': 'not found'}
        return JsonResponse(data, status=404)

def fetch_weldGrade(request):

    material = request.GET.get('cate')
    print(material, "scad barcode ----------------")
    
    try:
        product_data = []
        
        active_project = request.COOKIES.get('active_project')
        active_project_obj = None
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
        if material == "material":
            if active_project_obj:
                product = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('type').distinct().exclude(rt__isnull=True).exclude(rt__exact='')
            else:
                product = spoolgenmaterialsuploadss.objects.values('type').distinct().exclude(rt__isnull=True).exclude(rt__exact='')
            

            for product_instance in product:
                product_data.append({
                    
                    'GradeNmae': product_instance['type'],
                    # Include other product details as needed
                })
                print(product_data)
        elif material == "piping":
            if active_project_obj:
                product = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('type').distinct().exclude(mtpt__isnull=True).exclude(mtpt__exact='')
            else:
                product = spoolgenmaterialsuploadss.objects.values('type').distinct().exclude(mtpt__isnull=True).exclude(mtpt__exact='')
            

            for product_instance in product:
                product_data.append({
                    
                    'GradeNmae': product_instance['type']
                    # Include other product details as needed
                })
                print(product_data)
        elif material == "service":
            if active_project_obj:
                product = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('type').distinct().exclude(pmi__isnull=True).exclude(pmi__exact='')
            else:
                product = spoolgenmaterialsuploadss.objects.values('type').distinct().exclude(pmi__isnull=True).exclude(pmi__exact='')
            

            for product_instance in product:
                product_data.append({
                    
                    'GradeNmae': product_instance['type'],
                    # Include other product details as needed
                })
                print(product_data)



        # product_data = []

        # for product_instance in product:
        #     product_data.append({
                
        #         'GradeNmae': product_instance.,
        #         # Include other product details as needed
        #     })
        #     print(product_data)
        return JsonResponse({'products': product_data})

    
    except materialsgrade.DoesNotExist:
        data = {'error': 'not found'}
        return JsonResponse(data, status=404)


def nderequest(request):
    ndt = request.GET.get('ndt', '')
    rqs = request.GET.get('rqs', '')
    print(ndt)
    print(rqs)
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        cust_list = nderequestprocess.objects.filter(searchprocess__ProId=active_project_obj)
    else:   
        cust_list=nderequestprocess.objects.all()

    if ndt:
        cust_list = cust_list.filter(ndttypes=ndt)
    
    if rqs:
        cust_list = cust_list.filter(requestno=rqs)

    data={'list':cust_list}
    print(cust_list)


    return render(request,'nderequest.html',data)

# def ndereport(request):
#         ndt = request.GET.get('ndt', '')
#         rqs = request.GET.get('rqs', '')
#         print(ndt)
#         print(rqs)

#         cust_list=nderequestprocess.objects.all()

#         if ndt:
#                 cust_list = cust_list.filter(ndttypes=ndt)
        
#         if rqs:
#                 cust_list = cust_list.filter(requestno=rqs)

        
#         request_no_dct = {} 
#         for nde_report_process in ndereportrequestprocess.objects.all():
#             request_no_dct[nde_report_process.ndereqprocess.id] = nde_report_process
#         data={'list':cust_list, 'request_no_dct':request_no_dct}
#         print(cust_list)

#         return render(request,'ndereport.html',data)

def ndereport(request):
    ndt = request.GET.get('ndt', '')
    rqs = request.GET.get('rqs', '')
    
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        cust_list = nderequestprocess.objects.filter(searchprocess__ProId=active_project_obj)
    else:   
        cust_list=nderequestprocess.objects.all()

    if ndt:
        cust_list = cust_list.filter(ndttypes=ndt)
    
    if rqs:
        cust_list = cust_list.filter(requestno=rqs)

    # Create a dictionary where the key is the `ndereqprocess.id` and the value is the entire `ndereportrequestprocess` object
    # request_no_dct = {nde_report_process.ndereqprocess.id: nde_report_process for nde_report_process in ndereportrequestprocess.objects.all()}
    nde_req_list = []
    for nde_req in cust_list:
        nde_req_list.append({"nde_req":nde_req, "request_no_dct": ndereportrequestprocess.objects.filter(ndereqprocess=nde_req).first()})
    # Pass both the customer list and the dictionary to the template
    data = {'list': nde_req_list}

    return render(request, 'ndereport.html', data)


def ndestatus(request):
     if request.method == 'GET' :
        
        location = request.GET.get('location', '')
        nde_type = request.GET.get('nde_type', '')
        category = request.GET.get('category', '')
        nde_value = request.GET.get('nde_value', '')
        weld_type = request.GET.get('weld_type', '')
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            proj_nos = [active_project]
        else:
            active_project_obj = None
            proj_nos = list(project.objects.all().values_list('projectno', flat=True))
        loc = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('location').distinct().exclude(location__isnull=True)
        bhn = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('bhn').distinct()
        rt=spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('rt').distinct()
        ferraite=spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('ferraite').distinct()
        mtpt=spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('mtpt').distinct()
        pmi=spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('pmi').distinct()
        weld_type_list=spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos,is_nde_request_raised=True).values('type').distinct().exclude(type__isnull=True)

        report_list = []
        if request.GET:
            cust_list = spoolgenmaterialsuploadss.objects.filter(ProId__projectno__in=proj_nos)
            valid_fields = [
            'ProId', 'ProId_id', 'acceptance', 'area', 'batch', 'bhn', 'drgno', 
            'ferraite', 'id', 'insulation', 'lineno', 'location', 'material', 
            'mom', 'mtpt', 'opttemp', 'paint', 'partrid', 'pcno', 'pidno', 
            'piping', 'pmi', 'pwht', 'rev', 'rt', 'service', 'sheetno', 'size', 
            'spoolno', 'subproject', 'thk', 'tiein', 'tmedia', 'tpress', 'type', 
            'unit', 'weldno'
            ]
            print(cust_list.count(),"A")
            if location:
                cust_list = cust_list.filter(location=location)

            print(cust_list.count(),"B")

            if nde_type:
                if nde_type in valid_fields:
                    filter_kwargs = {nde_type: nde_value}

                    cust_list = cust_list.filter(**filter_kwargs)
            
            print(cust_list.count(),"C")
            
            if weld_type:
                cust_list = cust_list.filter(type=weld_type)

            print(cust_list.count(),"D")

            if category == 'Welder':
                cust_list.values('welder1__id').distinct().exclude(piping__isnull=True)
                welders_from_welder1 = cust_list.exclude(welder1__isnull=True).values_list('welder1__id', flat=True)

                welders_from_welder2 = cust_list.exclude(welder2__isnull=True).values_list('welder2__id', flat=True)
                for Welder in set(welders_from_welder1).union(set(welders_from_welder2)):
                    print(Welder)
                    total_joints = cust_list.filter(Q(welder1__id=Welder)|Q(welder2__id=Welder)).count()
                    req_joints = math.ceil(total_joints/100)*int(nde_value)
                    total_welded_joints = cust_list.filter(Q(welder1__id=Welder)|Q(welder2__id=Welder)).exclude(start__isnull=True).count()
                    req_weld_joints = math.ceil((total_welded_joints/100)*int(nde_value))
                    rt_taken = ndereportrequestprocess.objects.filter(ndereqprocess__searchprocess__id__in=list(cust_list.filter(Q(welder1__id=Welder)|Q(welder2__id=Welder)).exclude(start__isnull=True).values_list('id', flat=True))).count()
                    balance_rt = req_weld_joints - rt_taken
                    report_list.append({
                        "welder": welder.objects.filter(id=Welder).first(),
                        "total_joints": total_joints,
                        "req_joints": req_joints,
                        "total_welded_joints": total_welded_joints,
                        "req_weld_joints": req_weld_joints,
                        "rt_taken": rt_taken,
                        "balance_rt": balance_rt
                    })
            else:
                print(cust_list.count(),"E")
                for pipe_class in set(list(cust_list.exclude(piping__isnull=True).values_list('piping',flat=True))):
                    print(pipe_class)
                    total_joints = cust_list.filter(piping=pipe_class).count()
                    req_joints = math.ceil((total_joints/100)*int(nde_value))
                    total_welded_joints = cust_list.filter(piping=pipe_class).exclude(start__isnull=True).count()
                    req_weld_joints = math.ceil((total_welded_joints/100)*int(nde_value))
                    rt_taken = ndereportrequestprocess.objects.filter(ndereqprocess__searchprocess__id__in=list(cust_list.filter(piping=pipe_class).exclude(start__isnull=True).values_list('id', flat=True))).count()
                    balance_rt = req_weld_joints - rt_taken
                    report_list.append({
                        "piping_class": pipe_class,
                        "total_joints": total_joints,
                        "req_joints": req_joints,
                        "total_welded_joints": total_welded_joints,
                        "req_weld_joints": req_weld_joints,
                        "rt_taken": rt_taken,
                        "balance_rt": balance_rt
                    })
                print(report_list)
                



        data = {
            'locations':loc,
            'bhns' : bhn,
            'rts'  :rt,
            'ferraites':ferraite,
            'mtpts':mtpt,
            'pmis':pmi,
            'weld_type_list': weld_type_list,
            'report': report_list

        }  
        print(data)
        return render(request,'ndestatus.html',data)


# rfi
def rfirequest(request):
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        data=rficrteate.objects.filter(ProId=active_project_obj)
    else:
        data=rficrteate.objects.all()
    return render(request,'rfirequest.html',{'data':data})
    
def rficreate(request):
    if request.method =='POST':
        print(request.POST.copy())
        location=request.POST.get('location')
        rfino=request.POST.get('rfino')
        date=request.POST.get('date')
        discipline=request.POST.get('discipline')
        insname=request.POST.get('insname')
        inspect_item=request.POST.get('inspecItem')

        hold = request.POST.get('hold', 'off')
        wit = request.POST.get('wit', 'off')
        ins = request.POST.get('ins', 'off')
        rev = request.POST.get('rev', 'off')



        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            newrficreate=rficrteate(location=location,rfino=rfino,rfidate=date,discipline=discipline,inspectorname=insname,hold=hold,
                                    witness=wit,inspection=ins,review=rev, inspect_item=inspect_item,ProId=active_project_obj)
        else:
            newrficreate=rficrteate(location=location,rfino=rfino,rfidate=date,discipline=discipline,inspectorname=insname,hold=hold,
                                    witness=wit,inspection=ins,review=rev, inspect_item=inspect_item)

        
        newrficreate.save()
        return redirect('rfirequest')
    else:
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            data=rficrteate.objects.filter(ProId=active_project_obj)
        else:
            data=rficrteate.objects.all()
        data_dict = {
        'admin_data': ad.objects.all(),
        'qc_data': Qc.objects.all(),
        'rfi_list': data
        }
        return render(request,'rficreate.html',data_dict)

def isosheet(request):
    if request.method == 'POST':
        print(request.POST.copy())
        data = json.loads(request.body)
        date = data.get('date') 
        isoeno = data.get('isono')
        selected_spools = data.get('selected_spools', [])
        print(selected_spools)
        for spool in selected_spools:
            drgno = spool.get('drgno')
            sheetno = spool.get('sheetno')
            if IsoSheet.objects.filter(drgno=drgno, sheetno=sheetno).exists():
                IsoSheet.objects.filter(drgno=drgno, sheetno=sheetno).update(relesedate=date,isopackno=isoeno)
            else:
                IsoSheet.objects.create(relesedate=date,isopackno=isoeno,sheetno=sheetno,drgno=drgno)
        return JsonResponse({'status': 'success'})
    else:
        sheet_list = []
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            spool_queryset = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).exclude(sheetno__isnull=True)
        else:
            spool_queryset = spoolgenmaterialsuploadss.objects.exclude(sheetno__isnull=True)
        if request.GET.get('location', ''):
            spool_queryset = spool_queryset.filter(location=request.GET.get('location', ''))
        for sheet_data in spool_queryset.values('sheetno', 'drgno').distinct():
            print(sheet_data)
            sheet_fil = spool_queryset.filter(sheetno=sheet_data['sheetno'],drgno=sheet_data['drgno'])
            spool_count = sheet_fil.values('spoolno').distinct().count()
            print(spool_count)
            completed_spool_count = 0
            for spool_data in sheet_fil.values('spoolno').distinct():
                if sheet_fil.filter(spoolno=spool_data["spoolno"]).count() == sheet_fil.filter(spoolno=spool_data["spoolno"],is_nde_request_raised=True).count():
                    completed_spool_count += 1

            status = int((completed_spool_count/spool_count)*100)
            sheet_list.append({
                "drgno": sheet_data['drgno'],
                "sheetno": sheet_data['sheetno'],
                "spool_count": spool_count ,
                "rev": sheet_fil.first().rev,
                "status": str(status)+" %",
                "isosheet": IsoSheet.objects.filter(sheetno=sheet_data['sheetno'], drgno=sheet_data['drgno']).first()
            })
        print(sheet_list)
        return render(request,'isosheet.html',{"data":sheet_list,"locations":spoolgenmaterialsuploadss.objects.exclude(spoolno__isnull=True).values('location').distinct().exclude(location__isnull=True)})

def isosheet_form_download(request):

    drgno = request.GET.get('drgno')
    sheetno = request.GET.get('sheetno')
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        spool_queryset = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj, drgno=drgno, sheetno=sheetno)
    else:
        spool_queryset = spoolgenmaterialsuploadss.objects.filter(drgno=drgno, sheetno=sheetno)
    spool_list = []
    spool_no_list = []
    for spool_data in spool_queryset:
        if spool_data.spoolno not in spool_no_list:
            spool_list.append(spool_data)
            spool_no_list.append(spool_data.spoolno)
    data_dict = {
            "spool": spool_queryset.first(),
            "spool_queryset": spool_list,
            "isosheet": IsoSheet.objects.filter(sheetno=sheetno, drgno=drgno).first()
        }
    return render(request,'isosheet_form_download.html',data_dict)

def isospool(request):
    if request.method == 'POST':
        print(request.POST.copy(),"requ")
        data = json.loads(request.body)
        print(data)
        date = data.get('date') 
        isoeno = data.get('isono')
        selected_spools = data.get('selected_spools', [])
        print(selected_spools, "selected_spools")
        for spool in selected_spools:
            drgno = spool.get('drgno')
            spoolno = spool.get('spoolno')
            if IsoSpool.objects.filter(drgno=drgno,spoolno=spoolno).exists():
                IsoSpool.objects.filter(drgno=drgno,spoolno=spoolno).update(relesdate=date,isopacno=isoeno)
            else:  
                IsoSpool.objects.create(relesdate=date,isopacno=isoeno,spoolno=spoolno,drgno=drgno)
        return JsonResponse({'status': 'success'})
        # return redirect("isospool")
    else:
        spool_list = []
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            spool_queryset = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).exclude(Q(sheetno__isnull=True)| Q(spoolno__isnull=True))
        else:
            spool_queryset = spoolgenmaterialsuploadss.objects.exclude(Q(sheetno__isnull=True)| Q(spoolno__isnull=True))
        if request.GET.get('location', ''):
            spool_queryset = spool_queryset.filter(location=request.GET.get('location', ''))
        for spool_data in spool_queryset.values('spoolno', 'drgno').distinct():
            print(spool_data)
            spool_fil = spool_queryset.filter(spoolno=spool_data['spoolno'],drgno=spool_data['drgno'])
            date_range = spool_fil.aggregate(
                max_date=Max('start'),
                min_date=Min('start')
            )
            status = int((spool_fil.exclude(start__isnull=True).count()/spool_fil.count())*100)
            spool_list.append({
                "drgno": spool_data['drgno'],
                "spoolno": spool_data['spoolno'],
                "rev": spool_fil.first().rev,
                "sheetno": spool_fil.first().sheetno,
                "start_date":  date_range['max_date'],
                "end_date":  date_range['min_date'],
                "status": str(status)+" %",
                "isospool": IsoSpool.objects.filter(spoolno=spool_data['spoolno'], drgno=spool_data['drgno']).first()
            })
        print(spool_list)
        return render(request,'isospool.html',{"data":spool_list,"locations":spoolgenmaterialsuploadss.objects.exclude(spoolno__isnull=True).values('location').distinct().exclude(location__isnull=True)})


def isospool_form_download(request):
    
    drgno = request.GET.get('drgno')
    sheetno = request.GET.get('sheetno')
    spoolno = request.GET.get('spoolno')
    spool_list = []
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        spool_queryset = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj, drgno=drgno, sheetno=sheetno, spoolno=spoolno)
    else:
        spool_queryset = spoolgenmaterialsuploadss.objects.filter(drgno=drgno, sheetno=sheetno, spoolno=spoolno)
    isospool = IsoSpool.objects.filter(spoolno=spoolno, drgno=drgno).first()
    spool_list = []
    for iso_spool in IsoSpool.objects.filter(isopacno=isospool.isopacno, drgno=drgno):
        spool_list.append(spoolgenmaterialsuploadss.objects.filter(drgno=drgno, spoolno=iso_spool.spoolno).first())
        
    data_dict = {
            "spool": spool_queryset.first(),
            "isospool": isospool,
            "spool_queryset": spool_list
        }
    return render(request,'isospool_form_download.html',data_dict)


# ncr/qr
def ncr(request):
    queryset = NCRInfo.objects.all()
    return render(request,'ncr.html',{'data': queryset})

def newncr(request):
    if request.method =='POST':
        ncr_info = NCRInfo()
        ncr_info.ncr_no=request.POST.get("ncr_no")
        ncr_info.initiator=request.POST.get("initiator")
        ncr_info.discipline=request.POST.get("discipline")
        ncr_info.contractor=request.POST.get("contractor")
        ncr_info.project=project.objects.get(id=request.POST.get("project"))
        ncr_info.date=request.POST.get("date")
        ncr_info.non_conformity=request.POST.get("non_conformity")
        ncr_info.type=request.POST.get("type")
        ncr_info.major=request.POST.get('major', 'off')
        ncr_info.minor=request.POST.get('minor', 'off')
        ncr_info.observation=request.POST.get('observation', 'off')
        ncr_info.save()
        return redirect('ncr')

    data = {
        "project": project.objects.all(),
        "contractor": contract.objects.all(),
        'admin_data': ad.objects.all(),
        'qc_data': Qc.objects.all()
    }
    return render(request,'newncr.html',data)

def qr(request):
    return render(request,'qr.html')

def newqr(request):
    return render(request,'newqr.html')

def welderperformance(request):
    welder_list = []
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        locations=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('location').distinct()
        weldtype=spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('type').distinct()
        for welder_obj in active_project_obj.welders.all():
            welder_list.append({
                "id": welder_obj.id,
                "weldname": welder_obj.weldname,
                "welderid": welder_obj.welderid,
                "wps": list(welder_obj.weldwps.all().values_list("wpsno", flat=True))
            })
    else:
        locations=spoolgenmaterialsuploadss.objects.values('location').distinct()
        weldtype=spoolgenmaterialsuploadss.objects.values('type').distinct()
        for welder_obj in welder.objects.all():
            welder_list.append({
                "id": welder_obj.id,
                "weldname": welder_obj.weldname,
                "welderid": welder_obj.welderid,
                "wps": list(welder_obj.weldwps.all().values_list("wpsno", flat=True))
            })
    materials = mat.objects.all()
    data_dict = {
        "locations": locations,
        "weldtype": weldtype,
        "welder_list": welder_list,
        "materials": materials
    }
    return render(request,'welderperformance.html', data_dict)


# spool
def spool(request):
    data = spoolgenmaterialsuploadss.objects.all()
    if request.method == 'POST':
        print(request.POST.copy())
        date = request.POST.get('date') 
        spoolreleseno = request.POST.get('spoolreleseno')
        comments = request.POST.get('comments')
        drgno = request.POST.get('drgno')
        spoolno = request.POST.get('spoolno')
        if spoolmanagementprocess.objects.filter(drgno=drgno, spoolno=spoolno).exists():
            spoolmanagementprocess.objects.filter(drgno=drgno, spoolno=spoolno).update(relesedate=date, spoolreleseno=spoolreleseno,comments=comments)
        else:  
            spoolmanagementprocess.objects.create(drgno=drgno, spoolno=spoolno, relesedate=date, spoolreleseno=spoolreleseno,comments=comments)
        return redirect( 'spool' )
    else:
        spool_list = []
        active_project = request.COOKIES.get('active_project')
        active_project_obj = None
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            spool_gen_comb = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('spoolno', 'drgno').distinct()
        else:
            spool_gen_comb = spoolgenmaterialsuploadss.objects.values('spoolno', 'drgno').distinct()
        for spool_data in spool_gen_comb:
            print(spool_data)
            if active_project_obj:
                spool_fil = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,spoolno=spool_data['spoolno'],drgno=spool_data['drgno'])
            else:
                spool_fil = spoolgenmaterialsuploadss.objects.filter(spoolno=spool_data['spoolno'],drgno=spool_data['drgno'])
            date_range = spool_fil.aggregate(
                max_date=Max('start'),
                min_date=Min('start')
            )
            status = int((spool_fil.exclude(start__isnull=True).count()/spool_fil.count())*100)
            spool_list.append({
                "drgno": spool_data['drgno'],
                "spoolno": spool_data['spoolno'],
                "rev": spool_fil.first().rev,
                "start_date":  date_range['max_date'],
                "end_date":  date_range['min_date'],
                "status": str(status)+" %",
                "spoolmanagementprocess": spoolmanagementprocess.objects.filter(spoolno=spool_data['spoolno'], drgno=spool_data['drgno']).first()
            })

        print(spool_list)

        return render(request,'spool.html',{"data":spool_list})


# painting
def painting(request):
    if request.method == 'POST':
        print(request.POST.copy())
        insulation_release = request.POST.get('insulation_release') 
        ral_number = request.POST.get('ral_number')
        do_number = request.POST.get('do_number')
        do_date = request.POST.get('do_date')
        blasting_date = request.POST.get('blasting_date')
        primer_inspection_date = request.POST.get('primer_inspection_date')
        midcoat_inspection_date = request.POST.get('midcoat_inspection_date')
        finalcoat_inspection_date = request.POST.get('finalcoat_inspection_date')
        ic_report_number = request.POST.get('ic_report_number')
        m_run = request.POST.get('m_run')
        test_condition = request.POST.get('test_condition')
        painting_date = request.POST.get('painting_date')
        report_number = request.POST.get('report_number')
        drgno = request.POST.get('drgno')
        spoolno = request.POST.get('spoolno')
        active_project = request.COOKIES.get('active_project')
        active_project_obj = None
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
        if spoolpaintingprocess.objects.filter(drgno=drgno, spoolno=spoolno).exists():
            spoolpaintingprocess.objects.filter(drgno=drgno, spoolno=spoolno).update(insulation_release=insulation_release, ral_number=ral_number,do_number=do_number
                ,do_date=do_date,blasting_date=blasting_date,primer_inspection_date=primer_inspection_date,midcoat_inspection_date=midcoat_inspection_date,finalcoat_inspection_date=finalcoat_inspection_date,
                ic_report_number=ic_report_number,m_run=m_run,test_condition=test_condition,painting_date=painting_date, report_number=report_number, ProId=active_project_obj)
        else:  
            spoolpaintingprocess.objects.create(drgno=drgno, spoolno=spoolno,insulation_release=insulation_release, ral_number=ral_number,do_number=do_number
                ,do_date=do_date,blasting_date=blasting_date,primer_inspection_date=primer_inspection_date,midcoat_inspection_date=midcoat_inspection_date,finalcoat_inspection_date=finalcoat_inspection_date,
                ic_report_number=ic_report_number,m_run=m_run,test_condition=test_condition,painting_date=painting_date, report_number=report_number, ProId=active_project_obj)
        return redirect('painting')
    else:
        spool_list = []
        active_project = request.COOKIES.get('active_project')
        active_project_obj = None
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            spool_gen_comb = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj).values('spoolno', 'drgno').distinct()
            proj_nos = [active_project]
        else:
            proj_nos = list(project.objects.all().values_list('projectno', flat=True))
            spool_gen_comb = spoolgenmaterialsuploadss.objects.values('spoolno', 'drgno').distinct()
        for spool_data in spool_gen_comb:
            print(spool_data)
            if active_project_obj:
                spool_fil = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,spoolno=spool_data['spoolno'],drgno=spool_data['drgno'])
            else:
                spool_fil = spoolgenmaterialsuploadss.objects.filter(spoolno=spool_data['spoolno'],drgno=spool_data['drgno'])
            date_range = spool_fil.aggregate(
                max_date=Max('start'),
                min_date=Min('start')
            )
            status = int((spool_fil.exclude(start__isnull=True).count()/spool_fil.count())*100)
            spool_list.append({
                "drgno": spool_data['drgno'],
                "spoolno": spool_data['spoolno'],
                "rev": spool_fil.first().rev,
                "spoolpaintingprocess": spoolpaintingprocess.objects.filter(ProId__projectno__in=proj_nos,spoolno=spool_data['spoolno'], drgno=spool_data['drgno']).first()
            })

        return render(request,'painting.html',{"data":spool_list})


def addsheet(request,drg):
    try:
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            drgs = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg)
        else:
            drgs = spoolgenmaterialsuploadss.objects.filter(drgno = drg)

        # Check if there are any rows with the specified drgno
        if drgs.exists():
            # Get the maximum sheet number among the filtered rows
            max_sheet_number = drgs.aggregate(max_sheet_number=models.Max('sheetno'))['max_sheet_number']

            # Increment the maximum sheet number by 1 to get the next sheet number
            next_sheet_number = int(max_sheet_number) + 1
            drgprefix = ''
            drg_obj=drgs.first()
            if drg_obj.drgprefix: drgprefix = drg_obj.drgprefix
            # Create a new row with the next sheet number
            
            new_row = spoolgenmaterialsuploadss(drgno=drg, sheetno=next_sheet_number, rev=drgprefix+"0",subproject=drg_obj.subproject,pcno=drg_obj.pcno,piping=drg_obj.piping,
                        area=drg_obj.area,lineno=drg_obj.lineno,service=drg_obj.service,pidno=drg_obj.pidno,tpress=drg_obj.tpress,tmedia=drg_obj.tmedia,mom=drg_obj.mom,
                        acceptance=drg_obj.acceptance,material=drg_obj.material,pwht=drg_obj.pwht,bhn=drg_obj.bhn,ferraite=drg_obj.ferraite,mtpt=drg_obj.mtpt,pmi=drg_obj.pmi,
                        insulation=drg_obj.insulation,paint=drg_obj.paint,opttemp=drg_obj.opttemp,unit=drg_obj.unit,
                        thk=drg_obj.thk, hold=drg_obj.hold, itemno=drg_obj.itemno, contractno=drg_obj.contractno,
                        rt=drg_obj.rt,ProId=drg_obj.ProId)
            new_row.save()
        # Construct the URL with query parameters
    except Exception as exc:
        print(exc)
    url = f"{reverse('sheetweldhistory')}?search_term={drg}"

    # Redirect to the constructed URL
    return redirect(url)

def addnorec(request,drg,sh,rev):
    try:
        nu = request.POST.get("addsheet")
        nu = int(nu)
        active_project = request.COOKIES.get('active_project')
        if active_project and project.objects.filter(projectno=active_project).exists():
            active_project_obj = project.objects.filter(projectno=active_project).first()
            drg_obj = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg).first()
        else:
            drg_obj = spoolgenmaterialsuploadss.objects.filter(drgno = drg).first()
        for _ in range(nu):
            new_row = spoolgenmaterialsuploadss(drgno=drg, sheetno=sh, rev=rev,subproject=drg_obj.subproject,pcno=drg_obj.pcno,piping=drg_obj.piping,
                        area=drg_obj.area,lineno=drg_obj.lineno,service=drg_obj.service,pidno=drg_obj.pidno,tpress=drg_obj.tpress,tmedia=drg_obj.tmedia,mom=drg_obj.mom,
                        acceptance=drg_obj.acceptance,material=drg_obj.material,pwht=drg_obj.pwht,bhn=drg_obj.bhn,ferraite=drg_obj.ferraite,mtpt=drg_obj.mtpt,pmi=drg_obj.pmi,
                        insulation=drg_obj.insulation,paint=drg_obj.paint,opttemp=drg_obj.opttemp,unit=drg_obj.unit,
                         hold=drg_obj.hold, itemno=drg_obj.itemno, contractno=drg_obj.contractno,
                        rt=drg_obj.rt,ProId=drg_obj.ProId)
            new_row.save()
        # url = f"{reverse('weldhistory')}/{drg}/{int(sh)}/{rev}"

        # Redirect to the constructed URL
        return redirect(reverse('weldhistory', args=(drg, sh,rev)))
    except Exception as exc:
        print(exc)



def addrev(request, drg, sheetno):
    # Filter rows with the specified 'drgno', 'sheetno', and 'rev' number
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        drgs = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg, sheetno=sheetno)
    else:
        active_project_obj = None
        drgs = spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno)

    # Check if there are any rows with the specified drgno and sheetno
    if drgs.exists():
        # Get the latest rev number for the specified 'drgno' and 'sheetno'
        latest_rev = drgs.latest('id').rev
        if len(latest_rev) == 1:
            next_rev = str(int(latest_rev[0]) + 1)
        elif latest_rev[-1].isdigit():
            next_rev = latest_rev[0] + str(int(latest_rev[1:]) + 1)
        else:
            next_rev = latest_rev[0] + str(int(latest_rev[1:-1]) + 1) 

        # Filter the rows with the specified 'drgno' and 'sheetno'
        if active_project_obj:
            rows_to_update = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg, sheetno=sheetno)
        else:
            rows_to_update = spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno)

        # Update the 'rev' field for all matching rows
        rows_to_update.update(rev=next_rev)

    url = f"{reverse('sheetweldhistory')}?search_term={drg}"

    # Redirect to the constructed URL
    return redirect(url)

def removerev(request, drg, sheetno):

    print(drg,"45454545454")

    print(sheetno)
    # Filter rows with the specified 'drgno', 'sheetno', and 'rev' number
    active_project = request.COOKIES.get('active_project')
    if active_project and project.objects.filter(projectno=active_project).exists():
        active_project_obj = project.objects.filter(projectno=active_project).first()
        drgs = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg, sheetno=sheetno)
    else:
        active_project_obj = None
        drgs = spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno)

    # Check if there are any rows with the specified drgno and sheetno
    if drgs.exists():
        # Get the latest rev number for the specified 'drgno' and 'sheetno'
        latest_rev = drgs.latest('id').rev
        
        if len(latest_rev) == 1 and str(latest_rev[-1]) != "0":
            next_rev = str(int(latest_rev[0]) - 1)
        elif latest_rev[-1].isdigit():
            if str(latest_rev[-1]) == "0":
                next_rev = latest_rev
            else:
                next_rev = latest_rev[0] + str(int(latest_rev[1:]) - 1)
        else:
            next_rev = latest_rev[0] + str(int(latest_rev[1:-1]) - 1) + latest_rev[-1]


        # Filter the rows with the specified 'drgno' and 'sheetno'
        if active_project_obj:
            rows_to_update = spoolgenmaterialsuploadss.objects.filter(ProId=active_project_obj,drgno=drg, sheetno=sheetno)
        else:
            rows_to_update = spoolgenmaterialsuploadss.objects.filter(drgno=drg, sheetno=sheetno)

        
        # Update the 'rev' field for all matching rows
        rows_to_update.update(rev=next_rev)
 
    url = f"{reverse('sheetweldhistory')}?search_term={drg}"

    # Redirect to the constructed URL
    return redirect(url)

def get_next_rev(latest_rev):
    import re

    # Regular expression to find the numerical part and the suffix
    match = re.match(r'(\d+)([a-zA-Z]?)', latest_rev[1:])
    
    if match:
        number_part = match.group(1)
        suffix_part = match.group(2)
        print(number_part)
        print(suffix_part)
        
        if suffix_part == '':
            # No suffix yet, start with 'a'
            return number_part + 'A'
        elif suffix_part.upper() < 'Z':
            # Increment the suffix
            next_suffix = chr(ord(suffix_part.upper()) + 1)
            return number_part + next_suffix
        else:
            # Handle the case where the suffix is 'z'
            raise ValueError("Suffix has reached its maximum value.")
    else:
        # If rev is not matching the expected pattern
        raise ValueError("Unexpected rev format.")
    
def get_prev_rev(latest_rev):
    import re
    
    match = re.match(r'(\d+)([a-zA-Z]?)', latest_rev)
    
    if match:
        number_part = match.group(1)
        suffix_part = match.group(2)
        
        if suffix_part == '':
            return latest_rev  # No suffix to decrement
        elif suffix_part.upper() > 'A':
            prev_suffix = chr(ord(suffix_part.upper()) - 1)
            if prev_suffix == '@':  # Character before 'A' in ASCII
                return number_part
            return number_part + prev_suffix
        elif suffix_part.upper() == 'A':
            return number_part  # Remove suffix if it's 'A'
        else:
            raise ValueError("Unexpected suffix value.")
    else:
        raise ValueError("Unexpected rev format.")
    


def tfascanner_dashboard(request):
    report = (
        TFAUpload.objects
        .values('status')  # Group by the status field
        .annotate(count=Count('id'))  # Count occurrences
        .order_by('status')  # Optional: order by status
    )
    status_report = {entry['status']: entry['count'] for entry in report}

    data ={
        "status_report" : status_report
    }
    return render(request,'tfascanner_dashboard.html',data)
    
def tfascanner(request):
    tfa_list = []
    for tfa_obj in TFAUpload.objects.all():
        tfa_list.append(get_TFA_detail(tfa_obj))
    return render(request,'tfascanner.html',{"tfa_list":tfa_list})

def tfaspec(request,id):
    tfa_obj = TFAUpload.objects.filter(id=id).first()
    return render(request,'tfaspec.html',get_TFA_detail(tfa_obj))

def tfa_break(request):
    return render(request,'tfa_break.html')

def tfa_specedit(request,id):
    tfa = TFAUpload.objects.filter(id=id).first()
    if request.method =='POST':
        tfa.permanent_joint_id = request.POST.get("permanent_joint_id")
        tfa.flange_size = request.POST.get("flange_size")
        tfa.tightening_method = request.POST.get("tightening_method")
        tfa.flange_description = request.POST.get("flange_description")
        tfa.standard = request.POST.get("standard")
        tfa.flange_material = request.POST.get("flange_material")
        tfa.pipe_specification = request.POST.get("pipe_specification")
        tfa.flange_rating = request.POST.get("flange_rating")
        tfa.fluid = request.POST.get("fluid")
        tfa.critical_service = request.POST.get("critical_service")
        tfa.no_of_bolts = request.POST.get("no_of_bolts")
        tfa.bolt_diameter = request.POST.get("bolt_diameter")
        tfa.bolt_material = request.POST.get("bolt_material")
        tfa.nut_material = request.POST.get("nut_material")
        tfa.required_torque = request.POST.get("required_torque")
        tfa.bolt_length = request.POST.get("bolt_length")
        tfa.gasket_material = request.POST.get("gasket_material")
        tfa.lubricant = request.POST.get("lubricant")
        tfa.location = request.POST.get("location")
        tfa.area = request.POST.get("area")
        tfa.save()
        return redirect(reverse('tfaspec', args=(tfa.id,)))

    return render(request,'tfa_specedit.html',get_TFA_detail(tfa))


def tfa_overview(request,id):
    tfa_obj = TFAUpload.objects.filter(id=id).first()

    return render(request,'tfa_overview.html',get_TFA_detail(tfa_obj))

def tfa_pass(request,id):
    tfa_obj = TFAUpload.objects.filter(id=id).first()
    return render(request,'tfa_pass.html',get_TFA_detail(tfa_obj))

def tfa_pass_create(request):
    return render(request,'tfa_pass_create.html')

def tfa_photos(request,id):
    tfa_obj = TFAUpload.objects.filter(id=id).first()
    return render(request,'tfa_photos.html',get_TFA_detail(tfa_obj))

def tfa_photos_create(request):
    return render(request,'tfa_photos_create.html')

def tfa_report(request,id):
    tfa_obj = TFAUpload.objects.filter(id=id).first()
    if request.method =='POST':
        print(request.POST)
        tfa_obj.is_flange_satisfactory = request.POST.get("is_flange_satisfactory")
        tfa_obj.admin_comments = request.POST.get("admin_comments")
        tfa_obj.status = "completed"
        tfa_obj.save()
        
        operator = "-"
        if request.user and request.user.is_authenticated:
            operator = request.user.first_name

        TFAHistory.objects.create(tfa_upload=tfa_obj,status="completed",operator=operator)

        return redirect(reverse('tfa_overview', args=(tfa_obj.id,)))
    return render(request,'tfa_report.html',get_TFA_detail(tfa_obj))

def get_TFA_detail(tfa_obj):
    return {
        "tfa":tfa_obj,
        "tfa_photos":TFAPhotos.objects.filter(tfa_upload=tfa_obj).first(),
        "tfa_verify":TFAVerify.objects.filter(tfa_upload=tfa_obj).first(),
        "tfa_history":TFAHistory.objects.filter(tfa_upload=tfa_obj)
    }

def fiter_list(request):
    tfa_list = []
    if request.GET and request.GET.get("search"):
        qs = TFAUpload.objects.filter(permanent_joint_id=request.GET.get("search"),status="untouched")
    else:
        qs = TFAUpload.objects.filter(status="untouched")
    for tfa_obj in qs:
        tfa_list.append(get_TFA_detail(tfa_obj))
    return render(request,'fiter_list.html',{"tfa_list":tfa_list})

def fiter_pass(request, id):
    if request.method =='POST':
        print(request.POST)
        tfa_obj = TFAUpload.objects.filter(id=id).first()
        print(tfa_obj)
        if tfa_obj:
            tfa_obj.pass_one = request.POST.get("pass_one")
            tfa_obj.pass_two = request.POST.get("pass_two")
            tfa_obj.pass_three = request.POST.get("pass_three")
            tfa_obj.pass_four = request.POST.get("pass_four")
            tfa_obj.status = "tightened"
            tfa_obj.save()
            operator = "-"
            if request.user and request.user.is_authenticated:
                operator = request.user.first_name

            TFAHistory.objects.create(tfa_upload=tfa_obj,status="tightened",operator=operator)

            return redirect(reverse('fitter_succ', args=(tfa_obj.id,)))
        
    return render(request,'fiter_pass.html')

def fitter_photos(request, id):
    if request.method =='POST':
        print(request.POST)
        print(request.FILES)
        tfa_obj = TFAUpload.objects.filter(id=id).first()
        if TFAPhotos.objects.filter(tfa_upload=tfa_obj).exists():
            tfa_photo = TFAPhotos.objects.filter(tfa_upload=tfa_obj).first()
        else:
            tfa_photo = TFAPhotos()
            tfa_photo.tfa_upload = tfa_obj
        tfa_photo.flange_face_image = request.FILES.get("flange_face_image")
        tfa_photo.gasket_image = request.FILES.get("gasket_image")
        tfa_photo.assembled_image = request.FILES.get("assembled_image")
        tfa_photo.check_image = request.FILES.get("check_image")
        tfa_photo.any_flange_damage = request.POST.get("any_flange_damage")
        tfa_photo.save()
        return redirect(reverse('fiter_pass', args=(tfa_obj.id,)))

    return render(request,'fitter_photos.html')

def fitter_succ(request, id):
    return render(request,'fitter_succ.html',{
        "tfa_obj": TFAUpload.objects.filter(id=id).first()
    })

def qc_list(request):
    tfa_list = []
    if request.GET and request.GET.get("search"):
        qs = TFAUpload.objects.filter(permanent_joint_id=request.GET.get("search"),status="tightened")
    else:
        qs = TFAUpload.objects.filter(status="tightened")
    for tfa_obj in qs:
        tfa_list.append(get_TFA_detail(tfa_obj))
    return render(request,'qc_list.html',{"tfa_list":tfa_list})

def qc_overview(request, id):
    tfa_obj = TFAUpload.objects.filter(id=id).first()
    return render(request,'qc_overview.html',get_TFA_detail(tfa_obj))

def qc_succ(request, id):
    return render(request,'qc_succ.html',{
        "tfa_obj": TFAUpload.objects.filter(id=id).first()
    })

def qc_verfication(request, id):
    if request.method =='POST':
        tfa_obj = TFAUpload.objects.filter(id=id).first()
        if TFAVerify.objects.filter(tfa_upload=tfa_obj).exists():
            tfa_verify = TFAVerify.objects.filter(tfa_upload=tfa_obj).first()
        else:
            tfa_verify = TFAVerify()
            tfa_verify.tfa_upload = tfa_obj
        tfa_verify.is_gasket_type_correct = request.POST.get("is_gasket_type_correct")
        tfa_verify.are_bolts_lubricated = request.POST.get("are_bolts_lubricated")
        tfa_verify.is_flange_gap_within_tolerance = request.POST.get("is_flange_gap_within_tolerance")
        tfa_verify.are_flanges_aligned = request.POST.get("are_flanges_aligned")
        tfa_verify.is_sign_of_corrosion = request.POST.get("is_sign_of_corrosion")
        tfa_verify.final_qc_image = request.FILES.get("final_qc_image")
        tfa_obj.status = "qcpass"
        tfa_obj.save()
        tfa_verify.save()
        operator = "-"
        if request.user and request.user.is_authenticated:
            operator = request.user.first_name
            
        TFAHistory.objects.create(tfa_upload=tfa_obj,status="qcpass", operator=operator)
        return redirect(reverse('qc_succ', args=(tfa_obj.id,)))
    return render(request,'qc_verfication.html')

