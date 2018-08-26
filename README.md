# Data extractor from DynamoDB to S3

### Purpose:
Useful tool allowing to extract data from dynamoDB, create files (json or csv), upload them on S3 and delete (or not) the items on S3.

### Configuration:

```yaml
filename: users_extract
output_format: json
tablename: users
aws_region: eu-west-1
limit_per_file: 1000
bucket_name: users
bucket_path: database_backup
delete_items: False
```

### Usage:

```sh
pip3 install -r requirements.txt
export_dynamodb_to_s3.py -o <outputfile> -f <format> -t <tablename> -a <aws_region> -l <limit> -b <bucket_name> -p <bucket_path> -d <delete>
```
