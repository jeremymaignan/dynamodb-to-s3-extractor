from tqdm import tqdm
import boto3

class Dynamo():
    # Connect to the database
    def __init__(self, tablename, aws_region):
        dynamodb = boto3.resource('dynamodb', aws_region)
        self.table = dynamodb.Table(tablename)
        print("[INFO] Connected to {}".format(tablename))

    # Fetch $limit items from db
    # Loop and use an offset to fetch enough items
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

    # Delete items one by one
    def delete_items(self, items):
        print("[INFO] Deleting items")
        for item in tqdm(items):
            self.table.delete_item(Key={
                 "email": item["email"],
                 "id": item["id"]
            })
        print("[INFO] {} Items deletes".format(len(items)))