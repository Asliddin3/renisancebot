from django.db import models
from django.contrib.postgres.fields import ArrayField



# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(verbose_name="Telegramdagi Ismi", max_length=100)
    # real_name=models.CharField(verbose_name="Toliq ism sharifi",max_length=150,default="",null=True)
    username = models.CharField(verbose_name="Telegram username", max_length=100, null=True)
    state=models.CharField(verbose_name="User state",max_length=150,null=False,default="menu::::")
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', unique=True, default=1)
    # phone=models.CharField(verbose_name="Telefon raqam",null=True,max_length=100)
    # passport=models.CharField(verbose_name="Passport id si",null=True,max_length=20)
    # extra_phone=models.CharField(verbose_name="Qoshicha telefon raqam",null=True,max_length=100)
    # jshshir=models.CharField(verbose_name="JSHSHIR",null=True,max_length=30)
    # address=models.CharField(verbose_name="Address",null=True,max_length=1000)
    # photo_id=models.CharField(verbose_name="Passport Photo ID",null=True,max_length=1500)
    # result=models.IntegerField(verbose_name="Togri javoblar soni",default=0)
    def __str__(self):
        return f"{self.id} - {self.telegram_id} - {self.full_name}"

Times = (
        ('daytime', 'Kunduzgi',),
        ('evening', 'Kechki',),
        ("distance","Sirtqi")
    )


Lang = (
        # ('en', 'English',),
        ('ru', 'Russian',),
        ("uz","Uzbek")
    )

class Test(models.Model):
    number=models.IntegerField(verbose_name="Savol raqami")
    question=models.TextField(verbose_name="Savol",max_length=1000)
    answer=models.CharField(verbose_name="JAVOBI",max_length=1)
    def __str__(self):
        return f"{self.number} - {self.question}"

class Fakultet(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(verbose_name="Fakultet nomi",max_length=150)
    lang=models.CharField(verbose_name="Fakultet tili",max_length=12,default="uz",choices=Lang)
    time=models.CharField(verbose_name="Talim shakli",max_length=100,choices=Times)
    summa=models.IntegerField(verbose_name="Contract summasi")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.lang} - {self.time} - {self.summa}"


ContractState = (
    # ('en', 'English',),
    ("new", "Toldirilmagan shartnoma"),
    ("registered", "Registraciyadan o'tdi"),
    ("archive", "Arhivlandi"),
    ("accepted","Qabul qilindi")
)

class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    telegram_id=models.BigIntegerField(verbose_name="Telegram id si",null=True)
    fakultet_id=models.IntegerField(verbose_name="fakultet idsi",default=0,null=False)
    message_id=models.CharField(verbose_name="Contractni habar id si",max_length=1000,null=True)
    full_name=models.CharField(verbose_name="Toliq ismi sharifi",default="",max_length=200,null=True)
    phone=models.CharField(verbose_name="Telefon raqam",max_length=100,default="",unique=True,null=True)
    extra_phone=models.CharField(verbose_name="Qoshimcha raqam",max_length=100,default="",null=True)
    state=models.CharField(verbose_name="Contract holati",max_length=100,default="registered",choices=ContractState,null=True)
    result=models.IntegerField(verbose_name="Togri topilgan javoblar soni",default=0,null=True)
    dtm=models.DecimalField(verbose_name="DTM test natijasi",default=0,null=True)
    address=models.CharField(verbose_name="Propiska joyi",max_length=1000,null=True)
    passport = models.CharField(verbose_name="Passport raqami", max_length=100,unique=True,null=True)
    passport_photo=models.CharField(verbose_name="Passoprt rasmini idsi",max_length=1000,null=True)
    jshshir=models.CharField(verbose_name="JSHSHIR",null=True,max_length=30)

    def __str__(self):
        return f"{self.id} - {self.full_name} - {self.phone} - {self.result}"

# class Cart(models.Model):
#     id = models.AutoField(primary_key=True)
#     buyer = models.ForeignKey(User)
#     item_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=20, verbose_name="Telefon")
