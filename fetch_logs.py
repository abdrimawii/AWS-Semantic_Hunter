import boto3
import os
import gzip
import shutil

BUCKET_NAME = 'threat-hunt-lab-rimawi'  
LOCAL_LOG_DIR = './raw_logs'

if not os.path.exists(LOCAL_LOG_DIR):
    os.makedirs(LOCAL_LOG_DIR)

s3 = boto3.client('s3', region_name='eu-north-1')

def download_recursive():
    print(f"Searching for logs in bucket: {BUCKET_NAME}...")
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_NAME)
    file_count = 0
    for page in pages:
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.json.gz'):
                file_name = key.split('/')[-1]
                local_path = os.path.join(LOCAL_LOG_DIR, file_name)
                
                print(f"Found log: {file_name}")
                s3.download_file(BUCKET_NAME, key, local_path)
                
                with gzip.open(local_path, 'rb') as f_in:
                    with open(local_path.replace('.gz', ''), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(local_path)
                file_count += 1
    if file_count == 0:
        print("Still no logs found. Try running 'aws s3 ls' in your cmd and wait 10 mins.")
    else:
        print(f"Success! Downloaded {file_count} log files.")
if __name__ == "__main__":
    download_recursive()