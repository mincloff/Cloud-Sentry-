import boto3
from decouple import config

# 1. Pull keys from the .env file
ACCESS_KEY = config('AWS_ACCESS_KEY_ID')
SECRET_KEY = config('AWS_SECRET_ACCESS_KEY')
REGION = config('AWS_REGION')

# 2. Create a session (The "Handshake")
try:
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )
    
    # 3. Ask AWS for a list of S3 buckets (Standard "Is it working?" test)
    s3 = session.resource('s3')
    print("--- Connection Report ---")
    for bucket in s3.buckets.all():
        print(f"Found Bucket: {bucket.name}")
    
    print("\n✅ Success! Your local environment is connected to AWS.")

except Exception as e:
    print(f"❌ Connection Failed: {e}")