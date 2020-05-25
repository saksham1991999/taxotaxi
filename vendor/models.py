from django.db import models

# Create your models here.
account_type_choices = (
    ('C', 'Current'),
    ('S', 'Saving'),
)
class vendorprofile(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    father_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField()
    dob = models.DateField()
    email = models.EmailField()
    contact1 = models.CharField(max_length=10)
    contact2 = models.CharField(max_length=10, blank=True, null=True)


    street_1 = models.CharField(max_length=100)
    street_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    pancard = models.FileField()
    aadharcard_front = models.FileField()
    aadharcard_rear = models.FileField()
    votercard = models.FileField(blank=True, null=True)
    driving_licence_front = models.FileField(blank=True, null=True)
    driving_licence_rear = models.FileField(blank=True, null=True)

    company_name = models.CharField(max_length=100)
    gst_no = models.CharField(max_length=15)

    account_name = models.CharField(max_length=50)
    account_no = models.IntegerField()
    bank_name = models.CharField(max_length=50)
    account_type = models.CharField(max_length=1, choices=account_type_choices)
    ifsc = models.CharField(max_length=20)
    bank_address = models.CharField(max_length=200)

    verified = models.BooleanField(default=0)

    def __str__(self):
        return str(self.first_name)

    class Meta:
        verbose_name_plural = 'Vendor Details'

fuel_type_choices = (
    ('P', 'Petrol'),
    ('D', 'Diesel'),
    ('C', 'CNG'),
)
class vendor_cars(models.Model):
    vendor = models.ForeignKey(vendorprofile, on_delete=models.DO_NOTHING)
    car_type = models.ForeignKey('core.car_types', on_delete=models.DO_NOTHING)
    registration_no = models.CharField(max_length=50,blank=True, null=True)
    dateofregistration = models.DateField(blank=True, null=True)
    image_front = models.ImageField()
    image_rear = models.ImageField()

    rc_front = models.FileField()
    rc_rear = models.FileField()
    touristpermit_front = models.FileField()
    touristpermit_rear = models.FileField(blank=True, null=True)
    permita_front = models.FileField()
    permita_rear = models.FileField(blank=True, null=True)
    permitb_front = models.FileField()
    permitb_rear = models.FileField(blank=True, null=True)

    insurance_front = models.FileField()
    insurance_rear = models.FileField(blank=True, null=True)
    pollution_certificate = models.FileField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + str(self.car_type)

    class Meta:
        verbose_name_plural = 'Vendor Cars'

class driver(models.Model):
    vendor = models.ForeignKey(vendorprofile, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField()
    dob = models.DateField()

    driving_licence_no = models.CharField(max_length=50)
    driving_licence_valid_from = models.DateField()
    driving_licence_valid_till = models.DateField()

    driving_experience = models.SmallIntegerField()
    hill_experience = models.SmallIntegerField()


    email = models.EmailField()
    contact1 = models.CharField(max_length=10)
    contact2 = models.CharField(max_length=10, blank=True, null=True)

    street_1 = models.CharField(max_length=100)
    street_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    pancard = models.FileField()
    aadharcard_front = models.FileField()
    aadharcard_rear = models.FileField()
    votercard = models.FileField(blank=True, null=True)
    driving_licence_front = models.FileField(blank=True, null=True)
    driving_licence_rear = models.FileField(blank=True, null=True)
    police_verification_front = models.FileField(blank=True, null=True)
    police_verification_rear = models.FileField(blank=True, null=True)

    legal_accidental_case = models.BooleanField()
    legal_accidental_case_details = models.TextField(blank=True, null=True)