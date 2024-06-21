from django.db import models
class UserRegistration(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.first_name + " " + self.last_name
class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=100)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    def __str__(self):
        return self.name
class Family(models.Model):
    father = models.ForeignKey(Person, related_name='father_of', on_delete=models.CASCADE, null= True, blank=True)
    mother = models.ForeignKey(Person, related_name='mother_of', on_delete=models.CASCADE, null=True, blank=True)
    children = models.ManyToManyField(Person, related_name='children')
    def __str__(self):
        return 'Family of ' + self.father.name + ' and ' + self.mother.name
    
class SpouseInfo(models.Model):
    person = models.ForeignKey(Person, related_name='spouses', on_delete=models.CASCADE)
    spouse_name = models.CharField(max_length=100, null=True, blank=True)
    spouse_fathername = models.CharField(max_length=100,null=True, blank=True)
    spouse_village = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return "Spouse Information of " + ' ' +self.person.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"
