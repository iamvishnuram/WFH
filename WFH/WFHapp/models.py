from django.db import models

class InterimFields(models.Model):
    WORK_FROM_HOME_CHOICES = (
    ('Business Travel', 'Business Travel'),
    ('Office Closure', 'Office Closure'),
    ('Others', 'Others'),
)
    
    STATUS_CHOICES = (
        ('Approved', 'True'),
        ('Rejected', 'False')
    )
    
    request_id = models.CharField(max_length=20)
    employee_name = models.CharField(max_length=100)
    employee_id = models.IntegerField()
    email = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    reporting_manager = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    num_of_days = models.IntegerField()
    reason = models.CharField(choices=WORK_FROM_HOME_CHOICES, max_length=50, default="Others")
    description = models.CharField(max_length=100, null=True)
    tenure = models.IntegerField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="Approved", max_length=50, null=True)
    
    
    def __str__(self):
        return self.employee_name

    
class Employee(models.Model):
    
    STATUS_CHOICES = (
        ('True', 'Active'),
    )
    
    Employee = models.IntegerField(null=True)
    FirstName = models.CharField(max_length=100, null=True)
    LastName = models.CharField(max_length=100, null=True)
    PreferredName = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=100, default='Active', null=True)
    JobLevel = models.CharField(max_length=100, null=True)
    EmploymentStatus = models.CharField(max_length=100, null=True)	
    Location = models.CharField(max_length=100, null=True)	
    Division = models.CharField(max_length=100, null=True)	
    Department = models.CharField(max_length=100, null=True)	
    JobLevel = models.CharField(max_length=100, null=True)	 
    ReportingTo	= models.CharField(max_length=100, null=True)
    WorkEmail = models.EmailField(max_length=254)
    JobInformation_Date = models.DateField(null=True)
    FirstNameLastName = models.CharField(max_length=100, null=True)
    SupervisorID = models.PositiveIntegerField(null=True)	
    Budgeter = models.CharField(max_length=100, null=True)	
    NetsuiteInternalID = models.IntegerField(null=True)		 
    EmploymentStatus_Date = models.DateField(null=True)	
    FTE = models.CharField(max_length=100, null=True)
    ResignationDate	= models.DateField(null=True)
    Product1 = models.CharField(max_length=100, null=True)
    Product2 = models.CharField(max_length=100, null=True)	
    Entity	= models.CharField(max_length=100, null=True)
    HireDate = models.DateField(null=True)	
    Tenure = models.CharField(max_length=100, null=True)
    TimeZone_Offset_Value = models.IntegerField(null=True)
    
    def __str__(self):
        return self.FirstNameLastName

