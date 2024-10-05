from django.db import models
from login.models import User
from django.utils import timezone

# Create your models here.

class StartProject(models.Model):
    Description = models.CharField(max_length = 400, null= True, blank = True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    

class Weld(models.Model): #class Table_name(models.Model)

    weldType = models.CharField(max_length = 400, null= True, blank = True)
    weldDesc = models.CharField(max_length = 70, blank = True ,null = True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

class WeldProcess(models.Model):
    weldProcess = models.CharField(max_length = 100, blank = True, null = True)
    weldProcessDesc = models.CharField(max_length = 250, null = True, blank = True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)



class weld_location(models.Model):
    weldlocation =models.CharField(max_length=1000,blank =True,null=True)
    weldlocationdesc =models.CharField(max_length=1000,blank =True,null=True)
    role =models.CharField(max_length=10,null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)






class project(models.Model):
    projectno =models.CharField(max_length=100,null=True,blank=True)
    projectname =models.CharField(max_length=100,null=True,blank=True)
    customer =models.CharField(max_length=100,null=True,blank=True)
    role =models.CharField(max_length=100,null=True,blank=True)
    maincont =models.CharField(max_length=100,null=True,blank=True)
    subcontractor=models.CharField(max_length=200,null=True,blank=True)
    client =models.CharField(max_length=100,null=True,blank=True)
    startdate =models.DateField(null = True, blank = True)
    enddate =models.DateField(null = True, blank = True)
    fabcont=models.CharField(max_length=100,null=True,blank=True)
    fabcli=models.CharField(max_length=100,null=True,blank=True)
    finalaccon =models.CharField(max_length=100,null=True,blank=True)
    finalaccus=models.CharField(max_length=100,null=True,blank=True)
    finalac= models.CharField(max_length=100,null=True,blank=True)
    drarev =models.CharField(max_length=100,null=True,blank=True)
    weldsum =models.CharField(max_length=100,null=True,blank=True)
    dailyrec=models.CharField(max_length=100,null=True,blank=True)
    indrec =models.CharField(max_length=100,null=True,blank=True)
    spoolre =models.CharField(max_length=100,null=True,blank=True)
    rtform =models.CharField(max_length=100,null=True,blank=True)
    ndereq =models.CharField(max_length=100,null=True,blank=True)
    ptform =models.CharField(max_length=100,null=True,blank=True)
    pmiform =models.CharField(max_length=100,null=True,blank=True)
    pwhtform =models.CharField(max_length=100,null=True,blank=True)
    mtform =models.CharField(max_length=100,null=True,blank=True)
    bhnform =models.CharField(max_length=100,null=True,blank=True)
    ferrite =models.CharField(max_length=100,null=True,blank=True)
    pautform =models.CharField(max_length=100,null=True,blank=True)
    prhtform =models.CharField(max_length=100,null=True,blank=True)
    utform =models.CharField(max_length=100,null=True,blank=True)
    utgform =models.CharField(max_length=100,null=True,blank=True)
    shopadd =models.CharField(max_length=200,null=True,blank=True)
    fieldadd =models.CharField(max_length=200,null=True,blank=True)
    cliconno =models.CharField(max_length=200,null=True,blank=True)
    utocjobno =models.CharField(max_length=200,null=True,blank=True)
    weldid=models.CharField(max_length=200,null=True,blank=True)
    Projectclosed=models.CharField(max_length=200,null=True,blank=True)
    welders= models.ManyToManyField('welder', related_name='project')
    owner_logo = models.ImageField(upload_to='images/owner/',null=True,blank=True)  # Uploads to media/images/
    client_logo = models.ImageField(upload_to='images/client/',null=True,blank=True)  # Uploads to media/images/
    utoc_logo = models.ImageField(upload_to='images/utoc/',null=True,blank=True)  # Uploads to media/images/

    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.projectname
    

class ad(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank= True)
    userid=models.CharField(max_length=10,null = True, blank = True)
    name = models.CharField(max_length= 20)
    number = models.CharField(max_length=10,null = True, blank = True)
    email = models.EmailField(max_length = 20, unique = True) 
    DOB = models.DateField(null = True, blank = True)
    gender=models.CharField(max_length=10,null = True, blank = True)
    pro = models.ManyToManyField('project', related_name='ad')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Delete the associated user when deleting the customer
        self.user.delete()
        # Call the superclass method to perform the actual deletion
        super().delete(*args, **kwargs)
    
class mat(models.Model):
    materials =models.CharField(max_length=100,null=True,blank=True)
    materialsdesc =models.CharField(max_length=100,null=True,blank=True)
    materialsdescription=models.CharField(max_length=100,null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
class materialsgrade(models.Model):
    materialgrade=models.CharField(max_length=100,null=True,blank=True)
    materialdesc=models.CharField(max_length=100,null=True,blank=True)
    mat = models.ForeignKey(mat, on_delete=models.CASCADE, null = True, blank= True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

class w_p_s(models.Model):
    pipesize1=models.IntegerField(null=True)
    pipesize2=models.IntegerField(null=True)
    pipethickness1 =models.IntegerField(null=True)
    pipethickness2=models.IntegerField(null=True)
    material=models.ForeignKey(mat, on_delete=models.CASCADE, null = True, blank= True)
    grade =models.ForeignKey(materialsgrade, on_delete=models.CASCADE, null = True, blank= True)
    wpsno =models.CharField(max_length=200,null=True,blank=True)
    classid=models.CharField(max_length=100,null=True,blank=True)
    weldingprocess=models.CharField(max_length=100,null=True,blank=True)
    description=models.CharField(max_length=100,null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)    


class contract(models.Model):
    contractor=models.CharField(max_length=100,blank=True,null=True)
    contractortype=models.CharField(max_length=100,blank=True,null=True)
class welder(models.Model):

    weldname =models.CharField(max_length=100,blank=True,null=True)
    welderid=models.CharField(max_length=100,blank=True,null=True)
    finno =models.CharField(max_length=200,null=True,blank=True)
    primosno =models.CharField(max_length=200,null=True,blank=True)
    primosexpdate =models.DateField()
    weldwps = models.ManyToManyField('w_p_s', related_name='welder')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    contrac=models.ForeignKey(contract, on_delete=models.CASCADE, null = True, blank= True)


class KVMaster(models.Model):
    CATEGORY_CHOICES = [
        ('material_item', 'Material Item'),
        ('material_grade', 'Material Grade')
    ]
    category=models.CharField(max_length=100, choices=CATEGORY_CHOICES, null = True,blank = True)
    key=models.CharField(max_length=100,blank=True,null=True)
    value=models.CharField(max_length=100,blank=True,null=True)
    description=models.CharField(max_length=100,blank=True,null=True)


class MaterialSizeThicknessMasterData(models.Model):
    size=models.CharField(max_length=100,null = True,blank = True)
    schedule=models.CharField(max_length=100,blank=True,null=True)
    thickness=models.CharField(max_length=100,blank=True,null=True)

STATUS_CHOICES = [
        ('untouched', 'Untouched'),
        ('tightened', 'Tightened'),
        ('qcpass', 'QcPass'),
        ('completed', 'Completed')
    ]

class TFAUpload(models.Model): 
    permanent_joint_id=models.CharField(max_length=100,null = True,blank = True)
    plant_name=models.CharField(max_length=100,blank=True,null=True)
    area=models.CharField(max_length=100,blank=True,null=True)
    process_unit=models.CharField(max_length=100,blank=True,null=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    flange_description=models.CharField(max_length=100,blank=True,null=True)
    drawing_name_A=models.CharField(max_length=100,blank=True,null=True)
    sheet_no=models.CharField(max_length=100,blank=True,null=True)
    fluid=models.CharField(max_length=100,blank=True,null=True)
    pipe_specification=models.CharField(max_length=100,blank=True,null=True)
    flange_size=models.CharField(max_length=100,blank=True,null=True)
    standard=models.CharField(max_length=100,blank=True,null=True)
    critical_service=models.CharField(max_length=100,blank=True,null=True)
    reference_no=models.CharField(max_length=100,blank=True,null=True)
    flange_rating=models.CharField(max_length=100,blank=True,null=True)
    flange_material=models.CharField(max_length=100,blank=True,null=True)
    gasket_material=models.CharField(max_length=100,blank=True,null=True)
    bolt_material=models.CharField(max_length=100,blank=True,null=True)
    nut_material=models.CharField(max_length=100,blank=True,null=True)
    no_of_bolts=models.CharField(max_length=100,blank=True,null=True)
    bolt_diameter=models.CharField(max_length=100,blank=True,null=True)
    lubricant=models.CharField(max_length=100,blank=True,null=True)
    bolt_length=models.CharField(max_length=100,blank=True,null=True)
    tightening_method=models.CharField(max_length=100,blank=True,null=True)
    qc_scope=models.CharField(max_length=100,blank=True,null=True)
    required_torque=models.CharField(max_length=100,blank=True,null=True)
    contracting_company=models.CharField(max_length=100,blank=True,null=True)
    sub_contracting_company=models.CharField(max_length=100,blank=True,null=True)
    test_pack_no=models.CharField(max_length=100,blank=True,null=True)
    test_requirement=models.CharField(max_length=100,blank=True,null=True)
    test_completion_date=models.DateField(null=True,blank=True)
    reinstatement_completion_date=models.DateField(null=True,blank=True)
    project_name=models.CharField(max_length=100,blank=True,null=True)
    client_name=models.CharField(max_length=100,blank=True,null=True)
    temp_joint_id=models.CharField(max_length=100,blank=True,null=True)
    work_order_no=models.CharField(max_length=100,blank=True,null=True)
    stud_and_nut_coating=models.CharField(max_length=100,blank=True,null=True)
    system_number=models.CharField(max_length=100,blank=True,null=True)
    vessel_id=models.CharField(max_length=100,blank=True,null=True)
    pass_one=models.CharField(max_length=100,blank=True,null=True)
    pass_two=models.CharField(max_length=100,blank=True,null=True)
    pass_three=models.CharField(max_length=100,blank=True,null=True)
    pass_four=models.CharField(max_length=100,blank=True,null=True)
    is_flange_satisfactory=models.CharField(max_length=100,blank=True,null=True)
    admin_comments=models.TextField(blank=True)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES,default="Untouched")
    project=models.ForeignKey(project, on_delete=models.CASCADE, null = True, blank= True)


class TFAPhotos(models.Model):
    tfa_upload = models.ForeignKey(TFAUpload, on_delete=models.CASCADE, null = True, blank= True)
    flange_face_image = models.ImageField(upload_to='images/flanges/',null=True,blank=True)
    gasket_image = models.ImageField(upload_to='images/flanges/',null=True,blank=True)
    assembled_image = models.ImageField(upload_to='images/flanges/',null=True,blank=True)
    check_image = models.ImageField(upload_to='images/flanges/',null=True,blank=True)
    any_flange_damage=models.CharField(max_length=100,blank=True,null=True)


class TFAVerify(models.Model):
    tfa_upload = models.ForeignKey(TFAUpload, on_delete=models.CASCADE, null = True, blank= True)
    is_gasket_type_correct=models.CharField(max_length=100,blank=True,null=True)
    are_bolts_lubricated=models.CharField(max_length=100,blank=True,null=True)
    is_flange_gap_within_tolerance=models.CharField(max_length=100,blank=True,null=True)
    are_flanges_aligned=models.CharField(max_length=100,blank=True,null=True)
    is_sign_of_corrosion=models.CharField(max_length=100,blank=True,null=True)
    final_qc_image = models.ImageField(upload_to='images/flanges/',null=True,blank=True)


class TFAHistory(models.Model):
    tfa_upload = models.ForeignKey(TFAUpload, on_delete=models.CASCADE, null = True, blank= True)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES,default="Untouched")
    operator=models.CharField(max_length=100,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
