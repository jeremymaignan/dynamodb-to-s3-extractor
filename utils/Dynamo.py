from tqdm import tqdm
import boto3

class Dynamo():
    def __init__(self, tablename, aws_region):
        dynamodb = boto3.resource('dynamodb', aws_region)
        self.table = dynamodb.Table(tablename)
        print("[INFO] Connected to {}".format(tablename))

    def fetch_all_items(self, limit=0):
        response = self.table.scan()
        items = response["Items"]
        while 'LastEvaluatedKey' in response:
            if 0 != limit and limit < len(items):
                break
            response = self.table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items += response["Items"]
        return items if 0 == limit else items[:limit]

    def delete_items(self, items):
        print("[INFO] Delete items")
        for item in tqdm(items):
            self.table.delete_item(Key={
                 "email": item["email"],
                 "id": item["id"]
            })