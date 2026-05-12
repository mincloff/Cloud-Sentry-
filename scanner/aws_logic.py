import boto3
from decouple import config
from .models import WasteReport

def run_aws_scan():
    session = boto3.Session(
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
        region_name=config('AWS_REGION')
    )
    
    
    WasteReport.objects.all().delete()

    
    ec2 = session.resource('ec2')
    volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
    for vol in volumes:
        WasteReport.objects.create(
            resource_id=vol.id,
            resource_type='EBS',
            monthly_loss=vol.size * 0.08 
        )

    
    ec2_client = session.client('ec2')
    ips = ec2_client.describe_addresses()
    for addr in ips['Addresses']:
        if 'AssociationId' not in addr:
            WasteReport.objects.create(
                resource_id=addr['PublicIp'],
                resource_type='EIP',
                monthly_loss=3.60 
            )

    
    rds_client = session.client('rds')    
    instances = rds_client.describe_db_instances()
    for db in instances['DBInstances']:
        if db['DBInstanceStatus'] == 'available':
            WasteReport.objects.create(
                resource_id=db['DBInstanceIdentifier'],
                resource_type='RDS',
                monthly_loss=50.00
            )
            
    
    snapshots = rds_client.describe_db_snapshots(SnapshotType='manual')
    for snap in snapshots['DBSnapshots']:
        size_gb = snap.get('AllocatedStorage', 0)
        WasteReport.objects.create(
            resource_id=snap['DBSnapshotIdentifier'],
            resource_type='SNAP',
            monthly_loss=size_gb * 0.095
        )

    elb_client=session.client('elbv2')
    load_balancers=elb_client.describe_load_balancers()
    for lb in load_balancers['LoadBalancers']:
        WasteReport.objects.create(
            resource_id=lb['LoadBalancerName'],
            resource_type='ELB',
            monthly_loss=16.00
        )     

    nat_gateways=ec2_client.describe_nat_gateways()
    for nat in nat_gateways['NatGateways']:
        if nat['State']=='available':
            WasteReport.objects.create(
                resource_id=nat['NatGatewayID'],
                resource_type='NAT',
                monthly_loss=32.00
            )   

    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    for instance in instances:
        WasteReport.objects.create(
            resource_id=instance.id,
            resource_type='EC2',
            monthly_loss=4.00 
        )         

    return "Scan Complete!"