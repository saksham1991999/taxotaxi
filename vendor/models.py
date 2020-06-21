from django.db import models

# Create your models here.
vendor_status_choices = (
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Hold', 'Hold'),
    ('Pending', 'Pending'),
)
class vendorprofile(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    status = models.CharField(max_length=8 , choices=vendor_status_choices, default = "Pending")
    full_name = models.CharField(max_length=256)

    father_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField()
    dob = models.DateField()
    email = models.EmailField()
    contact1 = models.CharField(max_length=10)
    contact2 = models.CharField(max_length=10, blank=True, null=True)

    address = models.TextField()

    pancard = models.ImageField()
    aadharcard_front = models.ImageField()
    aadharcard_rear = models.ImageField()
    votercard_front = models.ImageField(blank=True, null=True)
    votercard_rear = models.ImageField(blank=True, null=True)
    driving_licence_front = models.ImageField(blank=True, null=True)
    driving_licence_rear = models.ImageField(blank=True, null=True)

    company_name = models.CharField(max_length=100, blank=True, null=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)

    verified = models.BooleanField(default=0)
    rejection_reason = models.TextField(blank=True, null=True)

    date_of_registration = models.DateField(auto_now_add=True)

    total_compact = models.PositiveSmallIntegerField()
    total_sedan = models.PositiveSmallIntegerField()
    total_suv = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.full_name)

    class Meta:
        verbose_name_plural = 'Vendor Details'

account_type_choices = (
    ('C', 'Current'),
    ('S', 'Saving'),
)
class bank_detail(models.Model):
    vendor = models.ForeignKey('vendor.vendorprofile', on_delete=models.PROTECT)
    account_holder_name = models.CharField(max_length=50)
    account_no = models.IntegerField()
    bank_name = models.CharField(max_length=50)
    account_type = models.CharField(max_length=1, choices=account_type_choices)
    ifsc = models.CharField(max_length=20)
    bank_address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.vendor) + str(self.account_holder_name)


driver_status_choices = (
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Hold', 'Hold'),
    ('Pending', 'Pending'),
)
fuel_type_choices = (
    ('P', 'Petrol'),
    ('D', 'Diesel'),
    ('C', 'CNG'),
)
class vendor_cars(models.Model):
    vendor = models.ForeignKey(vendorprofile, on_delete=models.DO_NOTHING)
    car_type = models.ForeignKey('core.car_types', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=8 , choices=driver_status_choices, default = "Pending")

    owner_name = models.CharField(max_length=256, blank=True, null=True)
    father_name = models.CharField(max_length=256, blank=True, null=True)

    registration_no = models.CharField(max_length=50,blank=True, null=True)
    dateofregistration = models.DateField(blank=True, null=True)

    image_front = models.ImageField()
    image_rear = models.ImageField()

    rc_front = models.ImageField()
    rc_rear = models.ImageField()
    rc_valid_upto = models.DateField()

    touristpermit_front = models.ImageField()
    touristpermit_rear = models.ImageField(blank=True, null=True)
    touristpermit_valid_upto = models.DateField()

    permita_front = models.ImageField()
    permita_rear = models.ImageField(blank=True, null=True)

    permitb_front = models.ImageField()
    permitb_rear = models.ImageField(blank=True, null=True)

    insurance_front = models.ImageField()
    insurance_rear = models.ImageField(blank=True, null=True)
    insurance_valid_upto = models.DateField()
    pollution_certificate = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + str(self.car_type)

    class Meta:
        verbose_name_plural = 'Vendor Cars'

driver_status_choices = (
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Hold', 'Hold'),
    ('Pending', 'Pending'),
)
class driver(models.Model):
    vendor = models.ForeignKey(vendorprofile, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=8 , choices=driver_status_choices, default = "Pending")
    full_name = models.CharField(max_length=256)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField()
    dob = models.DateField()

    email = models.EmailField()
    contact1 = models.CharField(max_length=10)
    contact2 = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField()

    pancard_front = models.ImageField()
    pancard_rear = models.ImageField()

    aadharcard_front = models.ImageField()
    aadharcard_rear = models.ImageField()
    votercard_front = models.ImageField(blank=True, null=True)
    votercard_rear = models.ImageField(blank=True, null=True)

    driving_licence_front = models.ImageField(blank=True, null=True)
    driving_licence_rear = models.ImageField(blank=True, null=True)
    driving_licence_no = models.CharField(max_length=50, blank=True, null=True)
    driving_licence_valid_from = models.DateField()
    driving_licence_valid_till = models.DateField()

    driving_experience = models.PositiveSmallIntegerField()
    hill_experience = models.PositiveSmallIntegerField()

    police_verification_front = models.ImageField(blank=True, null=True)
    police_verification_rear = models.ImageField(blank=True, null=True)

    legal_accidental_case = models.BooleanField(default=False)
    legal_accidental_case_details = models.TextField(blank=True, null=True)
    legal_accidental_case_document = models.ImageField(blank=True, null=True)
