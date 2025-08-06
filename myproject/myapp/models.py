from django.db import models

# Create your models here.
class Student(models.Model):
    firstname=models.CharField(max_length=50)
    email=models.EmailField()
    contact=models.IntegerField()
    image=models.ImageField(upload_to='image/')
    document=models.FileField(upload_to='file/')
    password=models.CharField(max_length=16)

    def __str__(self):
        return self.firstname + " "+ self.email + " " + str(self.contact) + " " + str(self.image) + " " + str(self.document)+ " " + str(self.password)
    
class queryy(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    query=models.CharField(max_length=300)


    def __str__(self):
        return self.name + " " + self.email + " " + self.query