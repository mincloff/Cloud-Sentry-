import boto3
from decouple import config

# 1. Setup Connection
session = boto3.Session(
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
    region_name=config('AWS_REGION')
)
ec2 = session.resource('ec2')

def scan_elastic_ips():
    ec2_client = session.client('ec2') # We use the client here for addresses
    addresses = ec2_client.describe_addresses()
    
    print("\n--- 🌐 Checking Elastic IPs ---")
    unused_ips = 0
    for addr in addresses['Addresses']:
        if 'AssociationId' not in addr:
            # AWS typically charges ~$0.005 per hour for idle IPs (~$3.60/month)
            print(f"📍 Unused IP Found: {addr['PublicIp']} | Cost: ~$3.60/month")
            unused_ips += 1
            
    if unused_ips == 0:
        print("✅ No unused Elastic IPs found.")
    return unused_ips * 3.60

def scan_for_waste():
    print("--- 🛡️ Cloud Guardian: Scanning for Waste ---")
    
    # 2. Find volumes that are "available" (not in use)
    # RIGHT: Values=['available']
    volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
    
    total_waste = 0
    count = 0

    for vol in volumes:
        # Standard gp3 pricing is roughly $0.08 per GB per month
        monthly_cost = vol.size * 0.08 
        print(f"📍 Found Idle Volume: {vol.id} | Size: {vol.size}GB | Cost: ~${monthly_cost}/month")
        total_waste += monthly_cost
        count += 1

    print("------------------------------------------")
    print(f"Total Ghost Volumes Found: {count}")
    print(f"Potential Monthly Savings: ${round(total_waste, 2)}")

if __name__ == "__main__":
    scan_for_waste()