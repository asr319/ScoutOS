import boto3
import os

AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_QUOTA_BYTES = int(os.getenv("AWS_S3_QUOTA_BYTES", "0"))

s3 = boto3.client("s3")

def get_s3_bucket_size():
    paginator = s3.get_paginator('list_objects_v2')
    total_size = 0
    for page in paginator.paginate(Bucket=AWS_S3_BUCKET):
        for obj in page.get('Contents', []):
            total_size += obj['Size']
    return total_size

def update_storage_metrics(storage_used_gauge, storage_total_gauge):
    used_bytes = get_s3_bucket_size()
    storage_used_gauge.set(used_bytes)
    storage_total_gauge.set(AWS_S3_QUOTA_BYTES)
