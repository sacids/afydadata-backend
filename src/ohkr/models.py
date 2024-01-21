from django.db import models

# Create your models here.
class Specie(models.Model):
    
    title = models.CharField(max_length = 150)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ohkr_specie'
        managed = True
        
class Disease(models.Model):
    
    title   = models.CharField(max_length = 150)
    specie  = models.ForeignKey(Specie, on_delete=models.CASCADE)
    
    #image
    #description    
    
    def __str__(self):
        return self.title+" : "+self.specie.title

    
    class Meta:
        db_table = 'ohkr_disease'
        managed = True


class Symptom(models.Model):
    
    title   = models.CharField(max_length = 150)
    code    = models.CharField(max_length = 15)
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ohkr_symtpom'
        managed = True

class SymptomToDisease(models.Model):
    
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    score   = models.IntegerField()    

    def __str__(self):
        return self.disease.title+' : '+self.symptom.title

    class Meta:
        db_table = 'ohkr_symtpom2disease'
        managed = True