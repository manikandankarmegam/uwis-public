from django.db import models
from login.models import User
from Ad.models import project

class client(models.Model):

    #id = models.AutoField

    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank= True)
    name = models.CharField(max_length= 20)
    number = models.CharField(max_length=10,null = True, blank = True)
    email = models.EmailField(max_length = 20, unique = True) 
    DOB = models.DateField(null = True, blank = True)
    gender=models.CharField(max_length=10,null = True, blank = True)
    pro = models.ManyToManyField(project, related_name='Client')
    
 
    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        # Delete the associated user when deleting the customer
        self.user.delete()
        # Call the superclass method to perform the actual deletion
        super().delete(*args, **kwargs)