from django.db import models

# Create your models here.

class vendorprofile(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    full_name = models.CharField(max_length=256)

    father_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField()
    dob = models.DateField()
    email = models.EmailField()
    contact1 = models.CharField(max_length=10)
    contact2 = models.CharField(max_length=10, blank=True, null=True)

    address = models.TextField()

    pancard = models.FileField()
    aadharcard_front = models.FileField()
    aadharcard_rear = models.FileField()
    votercard_front = models.FileField(blank=True, null=True)
    votercard_rear = models.FileField(blank=True, null=True)
    driving_licence_front = models.FileField(blank=True, null=True)
    driving_licence_rear = models.FileField(blank=True, null=True)

    company_name = models.CharField(max_length=100, blank=True, null=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)

    verified = models.BooleanField(default=0)
    rejection_reason = models.TextField()

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

fuel_type_choices = (
    ('P', 'Petrol'),
    ('D', 'Diesel'),
    ('C', 'CNG'),
)
class vendor_cars(models.Model):
    vendor = models.ForeignKey(vendorprofile, on_delete=models.DO_NOTHING)
    car_type = models.ForeignKey('core.car_types', on_delete=models.DO_NOTHING)

    owner_name = models.CharField(max_length=256, blank=True, null=True)
    father_name = models.CharField(max_length=256, blank=True, null=True)

    registration_no = models.CharField(max_length=50,blank=True, null=True)
    dateofregistration = models.DateField(blank=True, null=True)

    image_front = models.ImageField()
    image_rear = models.ImageField()

    rc_front = models.FileField()
    rc_rear = models.FileField()
    rc_valid_upto = models.DateField()

    touristpermit_front = models.FileField()
    touristpermit_rear = models.FileField(blank=True, null=True)
    touristpermit_valid_upto = models.DateField()

    permita_front = models.FileField()
    permita_rear = models.FileField(blank=True, null=True)

    permitb_front = models.FileField()
    permitb_rear = models.FileField(blank=True, null=True)

    insurance_front = models.FileField()
    insurance_rear = models.FileField(blank=True, null=True)
    insurance_valid_upto = models.DateField()
    pollution_certificate = models.FileField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + str(self.car_type)

    class Meta:
        verbose_name_plural = 'Vendor Cars'

class driver(models.Model):
    vendor = models.ForeignKey(vendorprofile, on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=256)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField()
    dob = models.DateField()

    email = models.EmailField()
    contact1 = models.CharField(max_length=10)
    contact2 = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField()

    pancard_front = models.FileField()
    pancard_rear = models.FileField()

    aadharcard_front = models.FileField()
    aadharcard_rear = models.FileField()
    votercard_front = models.FileField(blank=True, null=True)
    votercard_rear = models.FileField(blank=True, null=True)

    driving_licence_front = models.FileField(blank=True, null=True)
    driving_licence_rear = models.FileField(blank=True, null=True)
    driving_licence_no = models.CharField(max_length=50, blank=True, null=True)
    driving_licence_valid_from = models.DateField()
    driving_licence_valid_till = models.DateField()

    driving_experience = models.PositiveSmallIntegerField()
    hill_experience = models.PositiveSmallIntegerField()

    police_verification_front = models.FileField(blank=True, null=True)
    police_verification_rear = models.FileField(blank=True, null=True)

    legal_accidental_case = models.BooleanField(default=False)
    legal_accidental_case_details = models.TextField(blank=True, null=True)
    legal_accidental_case_document = models.FileField(blank=True, null=True)
