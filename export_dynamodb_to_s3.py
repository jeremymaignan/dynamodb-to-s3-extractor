from utils.ConfManager import get_conf
from utils.Dynamo import Dynamo
from utils.FileManager import FileManager
from utils.S3 import S3

from datetime import datetime
from time import strftime
from tqdm import tqdm
import os

if __name__ == '__main__':
    os.system("mkdir -p tmp")

    # Get Items from DB
    db = Dynamo(get_conf("tablename"), get_conf("aws_region"))
    items = db.fetch_all_items(get_conf("limit_per_file"))
    print("[INFO] {} items found".format(len(items)))
                                                                                                                                    
    # Write file
    fm = FileManager()
    filename =  "{}_{}.{}".format(get_conf("filename"), datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), get_conf("output_format"))
    if "json" == get_conf("output_format"):
        fm.write_json(items, filename)
    else:
        fm.write_csv(items, filename)

    # Upload file on S3
    s3 = S3()
    if s3.upload_s3(get_conf("bucket_name"), get_conf("bucket_path"), filename):
        # Delete items in Dynamo
        db.delete_items(items)
