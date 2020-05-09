from django.db import models

# Create your models here.
from django.db import models

class customerprofile(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    document = models.FileField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Customer Details'

class customer_promotional(models.Model):
    customer = models.ForeignKey(customerprofile, on_delete=models.CASCADE, verbose_name='Customer to assign the referral code to')
    promotional_code = models.CharField(max_length=10)
    referralbenefit = models.IntegerField(verbose_name='Amount to be credited to the person using it')
    customerbenefit = models.IntegerField(verbose_name='Amount to be credited to the customer referring')
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.promotional_code

    class Meta:
        verbose_name_plural = 'Customer Promotional Codes'


class referrals(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.DO_NOTHING)
    promocode = models.ForeignKey(customer_promotional, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return self.promocode

    class Meta:
        verbose_name_plural = 'Customer Promotional Code Used'

