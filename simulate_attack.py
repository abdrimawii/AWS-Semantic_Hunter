import boto3
import botocore

s3 = boto3.client('s3')
iam = boto3.client('iam')

print("Starting simulated reconnaissance...")

# Recon: Try to list all IAM users (often blocked for interns)
try:
    iam.list_users()
    print("[!] Logged: User enumeration attempt.")
except botocore.exceptions.ClientError:
    print("[!] Logged: Unauthorized user enumeration.")

# Recon: Try to list S3 buckets
try:
    s3.list_buckets()
    print("[!] Logged: Bucket discovery.")
except botocore.exceptions.ClientError:
    print("[!] Logged: Unauthorized bucket discovery.")

print("✅ Simulation complete. Wait 10-15 minutes for CloudTrail to update.")