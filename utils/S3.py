from boto3.s3.transfer import S3Transfer
import boto3

class S3():
    def upload_s3(self, bucket_name, path, filename):
        try:
            transfer = S3Transfer(boto3.client('s3'))
            transfer.upload_file("tmp/{}".format(filename), bucket_name, path + "/" + filename)
            print("[INFO] {}/{}/{} file uploaded on S3.".format(bucket_name, path, filename))
            return True
        except Exception as err:
            print("[ERROR] Cannot upload file. Error: {}".format(err))
            return False