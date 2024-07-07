from django.db import models

class CSVFile(models.Model):
    file_name = models.CharField(max_length=500,blank=True)
    file_path = models.CharField(max_length=500,blank=True)
    
    class Meta:
        db_table='csv_file'