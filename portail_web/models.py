from django.db import models
import uuid

class Postuler(models.Model):
    id=models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=40)
    compagny = models.CharField(max_length=50)
    cv = models.FileField(upload_to='curriculum_vitae')
    message = models.CharField(max_length=100)
    type_candidat =models.CharField(max_length=50)
    non_spontaner=models.BooleanField(null=True,default=False)

    class Meta:
        db_table = 'postuler'