import boto3
import os

s3_client = boto3.client("s3")

product_list = os.listdir("../raw_data")

print(product_list)
print(len(product_list))

for product_id in product_list:
    s3_client.upload_file(f"../raw_data/{product_id}/images/{product_id}.jpg", "aicore-box-datalake", f"{product_id}.jpg")
    # s3_client.upload_file(f"../raw_data/{product_id}/data.json", "aicore-box-datalake", f"{product_id}.json")