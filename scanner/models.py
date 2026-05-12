from django.db import models

class WasteReport(models.Model):
    RESOURCE_TYPES = [
        ('EBS', 'Idle Volume'),
        ('EIP', 'Unused Elastic IP'),
        ('RDS', 'Idle Database'),
        ('SNAP', 'Old DB Snapshot'),
        ('ELB','Idle Load Balancer'),
        ('NAT','Active NAT Gateway'),
        ('EC2','Stopped EC2(Storage)'),
    ]
    
    resource_id = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    monthly_loss = models.DecimalField(max_digits=10, decimal_places=2)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource_type}: {self.resource_id} (${self.monthly_loss})"
# Create your models here.
