from django.db import models
from login.models import User
from Ad.models import project,materialsgrade, w_p_s, welder

# Create your models here.

class Qc(models.Model):

    #id = models.AutoField

    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank= True)
    userid=models.CharField(max_length=10,null = True, blank = True)
    name = models.CharField(max_length= 20)
    number = models.IntegerField()
    email = models.EmailField(max_length = 20, unique = True, null = True)
    DOB = models.DateField(null = True, blank = True)
    gender=models.CharField(max_length=10,null = True, blank = True)
    pro = models.ManyToManyField(project, related_name='Qc')

    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        # Delete the associated user when deleting the customer
        self.user.delete()
        # Call the superclass method to perform the actual deletion
        super().delete(*args, **kwargs)


class Fitter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank= True)
    name = models.CharField(max_length= 20)
    userid=models.CharField(max_length=10,null = True, blank = True)
    number = models.CharField(max_length= 10)
    email = models.EmailField(max_length = 50, unique = True, null = True)
    DOB = models.DateField(null = True, blank = True)
    gender=models.CharField(max_length=10,null = True, blank = True)
    pro = models.ManyToManyField(project, related_name='Fitter')


    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        # Delete the associated user when deleting the customer
        self.user.delete()
        # Call the superclass method to perform the actual deletion
        super().delete(*args, **kwargs)


class projectuploadss(models.Model):
    certificateno=models.IntegerField(null=True)
    heatno=models.CharField(max_length=100,blank=True,null=True)
    calculative=models.IntegerField(null=True)
    receiveddate=models.CharField(max_length=100,blank=True,null=True)
    unit=models.CharField(max_length=100,blank=True,null=True)
    srnno=models.CharField(max_length=100,blank=True,null=True)
    itemcode=models.CharField(max_length=500,blank=True,null=True)
    size1=models.CharField(max_length=100,blank=True,null=True)
    foruwis=models.CharField(max_length=100,blank=True,null=True)
    sch1=models.CharField(max_length=100,blank=True,null=True)
    wt1=models.CharField(max_length=100,blank=True,null=True)
    size2=models.CharField(max_length=100,blank=True,null=True)
    sch2=models.CharField(max_length=100,blank=True,null=True)
    wt2=models.CharField(max_length=100,blank=True,null=True)
    description=models.CharField(max_length=100,blank=True,null=True)
    matl=models.CharField(max_length=100,blank=True,null=True)
    matlgrade=models.CharField(max_length=100,blank=True,null=True)
    qty=models.CharField(max_length=100,blank=True,null=True)
    issuedqty=models.CharField(max_length=100,blank=True,null=True)
    mfrorigin=models.CharField(max_length=100,blank=True,null=True)
    shortdescription=models.CharField(max_length=100,blank=True,null=True)
    actualqty=models.CharField(max_length=100,blank=True,null=True)
    ProId = models.ForeignKey(project, on_delete=models.CASCADE, null = True, blank= True)



class spoolgenmaterialsuploadss(models.Model):
    partrid=models.CharField(max_length=100,blank=True,null=True)
    pwht=models.CharField(max_length=100,blank=True,null=True)
    rt=models.CharField(max_length=100,blank=True,null=True)
    material=models.CharField(max_length=100,blank=True,null=True)
    piping=models.CharField(max_length=100,blank=True,null=True)
    service=models.CharField(max_length=100,blank=True,null=True) 
    acceptance=models.CharField(max_length=100,blank=True,null=True)
    lineno=models.CharField(max_length=100,blank=True,null=True)
    drgno=models.CharField(max_length=500,blank=True,null=True)
    rev=models.CharField(max_length=100,blank=True,null=True)
    sheetno=models.CharField(max_length=100,blank=True,null=True)
    spoolno=models.CharField(max_length=100,blank=True,null=True)
    weldno=models.CharField(max_length=100,blank=True,null=True)
    type=models.CharField(max_length=100,blank=True,null=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    size=models.CharField(max_length=100,blank=True,null=True)
    thk=models.CharField(max_length=100,blank=True,null=True)
    batch=models.CharField(max_length=100,blank=True,null=True)
    unit=models.CharField(max_length=100,blank=True,null=True)
    area=models.CharField(max_length=100,blank=True,null=True)
    insulation=models.CharField(max_length=100,blank=True,null=True)
    paint=models.CharField(max_length=100,blank=True,null=True)
    pidno=models.CharField(max_length=100,blank=True,null=True)
    tpress=models.CharField(max_length=100,blank=True,null=True)
    tmedia=models.CharField(max_length=100,blank=True,null=True)
    mom=models.CharField(max_length=100,blank=True,null=True)
    bhn=models.CharField(max_length=100,blank=True,null=True)
    ferraite=models.CharField(max_length=100,blank=True,null=True)
    mtpt=models.CharField(max_length=100,blank=True,null=True)
    pmi=models.CharField(max_length=100,blank=True,null=True)
    tiein=models.CharField(max_length=100,blank=True,null=True)
    opttemp=models.CharField(max_length=100,blank=True,null=True)
    subproject=models.CharField(max_length=100,blank=True,null=True)
    pcno=models.CharField(max_length=100,blank=True,null=True)
    ProId = models.ForeignKey(project, on_delete=models.CASCADE, null = True, blank= True)
    start=models.DateField(null=True,blank=True)
    end=models.DateField(null=True,blank=True)
    fitupdate= models.DateField(null=True,blank=True)
    grade=models.ForeignKey(materialsgrade, on_delete=models.CASCADE, null = True, blank= True)
    wpsnum=models.ForeignKey(w_p_s, on_delete=models.CASCADE, null = True, blank= True)
    welder1=models.ForeignKey(welder, on_delete=models.CASCADE, null = True, blank= True,related_name='spoolgenmaterialsuploads_as_welder1')
    welder2=models.ForeignKey(welder, on_delete=models.CASCADE, null = True, blank= True,related_name='spoolgenmaterialsuploads_as_welder2')
    rtrepair=models.CharField(max_length=100,blank=True,null=True)
    drgprefix=models.CharField(max_length=100,blank=True,null=True)
    hold=models.CharField(max_length=100,blank=True,null=True)
    itemno=models.CharField(max_length=100,blank=True,null=True)
    contractno=models.CharField(max_length=100,blank=True,null=True)
    nde=models.CharField(max_length=100,blank=True,null=True)
    is_nde_request_raised=models.BooleanField(default=False)
    partnoA=models.CharField(max_length=100,blank=True,null=True)
    mat_A=models.CharField(max_length=100,blank=True,null=True)
    heat_A=models.CharField(max_length=100,blank=True,null=True)
    cert_A=models.CharField(max_length=100,blank=True,null=True)
    partnoB=models.CharField(max_length=100,blank=True,null=True)
    mat_B=models.CharField(max_length=100,blank=True,null=True)
    heat_B=models.CharField(max_length=100,blank=True,null=True)
    cert_B=models.CharField(max_length=100,blank=True,null=True)
    
    def save(self, *args, **kwargs):
        if self.rev and self.rev[0].isalpha():
            self.drgprefix = self.rev[0]
        super(spoolgenmaterialsuploadss, self).save(*args, **kwargs)
            

class isomodel(models.Model):
    isonumber=models.CharField(max_length=100,blank=True,null=True)
    drgprefixno=models.CharField(max_length=100,blank=True,null=True)
    hold=models.CharField(max_length=100,blank=True,null=True)
    subproject=models.CharField(max_length=100,blank=True,null=True)
    pcno=models.CharField(max_length=100,blank=True,null=True)
    pipeclass=models.CharField(max_length=100,blank=True,null=True)
    area=models.CharField(max_length=100,blank=True,null=True)
    lineno=models.CharField(max_length=100,blank=True,null=True)
    service=models.CharField(max_length=100,blank=True,null=True)
    pidno=models.CharField(max_length=100,blank=True,null=True)
    tpress=models.CharField(max_length=100,blank=True,null=True)
    tmedia=models.CharField(max_length=100,blank=True,null=True)
    mom=models.CharField(max_length=100,blank=True,null=True)
    acceptstd=models.CharField(max_length=100,blank=True,null=True)
    matl=models.CharField(max_length=100,blank=True,null=True)
    ndereq=models.CharField(max_length=100,blank=True,null=True)
    pwhtreqt=models.CharField(max_length=100,blank=True,null=True)
    bhnreqt=models.CharField(max_length=100,blank=True,null=True)
    ferrite=models.CharField(max_length=100,blank=True,null=True)
    mtpt=models.CharField(max_length=100,blank=True,null=True)
    pmi=models.CharField(max_length=100,blank=True,null=True)
    insulation=models.CharField(max_length=100,blank=True,null=True)
    paintsys=models.CharField(max_length=100,blank=True,null=True)
    opttemp=models.CharField(max_length=100,blank=True,null=True)
    itemno=models.CharField(max_length=100,blank=True,null=True)
    contractno=models.CharField(max_length=100,blank=True,null=True)
    unitno=models.CharField(max_length=100,blank=True,null=True)
    plate=models.CharField(max_length=100,blank=True,null=True)
    length=models.CharField(max_length=100,blank=True,null=True)
    thk=models.CharField(max_length=100,blank=True,null=True)
    weldcondition=models.CharField(max_length=100,blank=True,null=True)
    ground=models.CharField(max_length=100,blank=True,null=True)
    welded=models.CharField(max_length=100,blank=True,null=True)
    treatment=models.CharField(max_length=100,blank=True,null=True)
    pre=models.CharField(max_length=100,blank=True,null=True)
    post=models.CharField(max_length=100,blank=True,null=True)
    rule=models.CharField(max_length=100,blank=True,null=True)
    welding=models.CharField(max_length=100,blank=True,null=True)
    magnifying=models.CharField(max_length=100,blank=True,null=True)
    others=models.CharField(max_length=100,blank=True,null=True)
    finalsurface=models.CharField(max_length=100,blank=True,null=True)
    sheetno=models.CharField(max_length=100,blank=True,null=True)
    currentrev=models.CharField(max_length=100,blank=True,null=True)
    revtest=models.CharField(max_length=100,blank=True,null=True)


class nderequestprocess(models.Model):
    ndttypes=models.CharField(max_length=100,blank=True,null=True)
    requestno=models.CharField(max_length=100,blank=True,null=True)
    date=models.DateField(null=True,blank=True)
    searchprocess=models.ForeignKey(spoolgenmaterialsuploadss, on_delete=models.CASCADE, null = True, blank= True)

class ndereportrequestprocess(models.Model):
    category=models.CharField(max_length=100,blank=True,null=True)
    reportno=models.CharField(max_length=100,blank=True,null=True)
    date=models.DateField(null=True,blank=True)
    flim_accept=models.CharField(max_length=100,blank=True,null=True)
    flim_reject=models.CharField(max_length=100,blank=True,null=True)
    ndereqprocess=models.ForeignKey(nderequestprocess, on_delete=models.CASCADE, null = True, blank= True)

class spoolmanagementprocess(models.Model):
    relesedate=models.DateField(null = True, blank = True)
    spoolreleseno=models.CharField(max_length=100,blank=True,null=True)
    comments=models.CharField(max_length=100,blank=True,null=True)
    drgno=models.CharField(max_length=100,blank=True,null=True)
    spoolno=models.CharField(max_length=100,blank=True,null=True)

class spoolpaintingprocess(models.Model):  
    drgno=models.CharField(max_length=100,blank=True,null=True)
    spoolno=models.CharField(max_length=100,blank=True,null=True)
    insulation_release=models.CharField(max_length=100,blank=True,null=True)
    ral_number=models.CharField(max_length=100,blank=True,null=True)
    do_number=models.CharField(max_length=100,blank=True,null=True)
    do_date=models.DateField(null=True,blank=True)
    blasting_date=models.DateField(null=True,blank=True)
    primer_inspection_date=models.DateField(null=True,blank=True)
    midcoat_inspection_date=models.DateField(null=True,blank=True)
    finalcoat_inspection_date=models.DateField(null=True,blank=True)
    ic_report_number=models.CharField(max_length=100,blank=True,null=True)
    m_run=models.CharField(max_length=100,blank=True,null=True)
    test_condition=models.CharField(max_length=100,blank=True,null=True)
    report_number=models.CharField(max_length=100,blank=True,null=True)
    painting_date=models.DateField(null=True,blank=True)
    ProId = models.ForeignKey(project, on_delete=models.CASCADE, null = True, blank= True)

class rficrteate(models.Model):
    location =models.CharField(max_length=100,blank=True,null=True)
    rfino =models.CharField(max_length=100,blank=True,null=True)
    rfidate =models.DateField(null = True, blank = True)
    discipline =models.CharField(max_length=100,blank=True,null=True)
    inspectorname =models.CharField(max_length=100,blank=True,null=True)
    inspect_item =models.CharField(max_length=100,blank=True,null=True)
    hold =models.CharField(max_length=100,blank=True,null=True)
    witness =models.CharField(max_length=100,blank=True,null=True)
    inspection =models.CharField(max_length=100,blank=True,null=True)
    review =models.CharField(max_length=100,blank=True,null=True)
    ProId = models.ForeignKey(project, on_delete=models.CASCADE, null = True, blank= True)


class IsoSheet(models.Model):
    relesedate=models.DateField(null = True, blank = True)
    isopackno=models.CharField(max_length=100,blank=True,null=True)
    drgno=models.CharField(max_length=100,blank=True,null=True)
    sheetno=models.CharField(max_length=100,blank=True,null=True)    


class IsoSpool(models.Model):
    relesdate=models.DateField(null = True, blank = True)
    isopacno=models.CharField(max_length=100,blank=True,null=True)
    drgno=models.CharField(max_length=100,blank=True,null=True)
    spoolno=models.CharField(max_length=100,blank=True,null=True)   


class NCRInfo(models.Model):
    ncr_no=models.CharField(max_length=100,null = True,blank = True)
    initiator=models.CharField(max_length=200,blank=True,null=True)
    discipline=models.CharField(max_length=100,blank=True,null=True)
    contractor=models.CharField(max_length=100,blank=True,null=True)   
    contractor_no=models.CharField(max_length=100,blank=True,null=True)   
    project=models.ForeignKey(project, on_delete=models.CASCADE, null = True, blank= True)
    project_no=models.CharField(max_length=200,blank=True,null=True)   
    date=models.DateField(null=True, blank=True)
    non_conformity=models.TextField()
    major=models.CharField(max_length=100,blank=True,null=True)
    minor=models.CharField(max_length=100,blank=True,null=True)
    observation=models.CharField(max_length=100,blank=True,null=True)
    type=models.CharField(max_length=100,blank=True,null=True)


class MIRUpload(models.Model):
    location=models.CharField(max_length=100,null = True,blank = True)
    category=models.CharField(max_length=100,null = True,blank = True)
    mir_no=models.CharField(max_length=100,null = True,blank = True)
    start_date=models.DateField(null=True, blank=True)
    part_id=models.CharField(max_length=100,null = True,blank = True)
    mir_item=models.CharField(max_length=100,null = True,blank = True)
    material=models.CharField(max_length=100,null = True,blank = True)
    grade=models.CharField(max_length=200,blank=True,null=True)
    weld_type=models.CharField(max_length=100,blank=True,null=True)
    size_1=models.CharField(max_length=100,blank=True,null=True)   
    sch_1=models.CharField(max_length=100,blank=True,null=True)   
    thk_1=models.CharField(max_length=100,blank=True,null=True)
    size_2=models.CharField(max_length=100,blank=True,null=True)   
    sch_2=models.CharField(max_length=100,blank=True,null=True)   
    thk_2=models.CharField(max_length=100,blank=True,null=True)
    qty=models.CharField(max_length=100,blank=True,null=True)   
    length=models.CharField(max_length=200,blank=True,null=True)   
    heat_no=models.CharField(max_length=100,blank=True,null=True)
    certificate_no=models.CharField(max_length=100,blank=True,null=True)
    mfr=models.CharField(max_length=100,blank=True,null=True)
    cal_qty=models.CharField(max_length=100,blank=True,null=True)
    project=models.ForeignKey(project, on_delete=models.CASCADE, null = True, blank= True)
