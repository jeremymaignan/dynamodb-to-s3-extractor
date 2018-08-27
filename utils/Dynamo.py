from tqdm import tqdm
import boto3

class Dynamo():
    # Connect to the database
    def __init__(self, tablename, aws_region):
        dynamodb = boto3.resource('dynamodb', aws_region)
        self.table = dynamodb.Table(tablename)
        self.client = boto3.client('dynamodb', aws_region)
        self.tablename = tablename
        print("[INFO] Connected to {}".format(tablename))

    # Dynamicaly find the indexes of the DB
    # Needed to delete items
    def get_index(self):
        hash_ = ""
        range_ = ""
        indexes = self.client.describe_table(
            TableName=self.tablename
        )["Table"]["KeySchema"]
        for index in indexes:
            if "HASH" == index["KeyType"]:
                hash_ = index["AttributeName"]
            if "RANGE" == index["KeyType"]:
                range_ = index["AttributeName"]
        print("[INFO] Range: {} Hash: {}".format(hash_, range_))
        return hash_, range_
        
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
        hash_, range_ = self.get_index()
        for item in tqdm(items):
            key = {}
            if None != hash_:
                key[hash_] = item[hash_]
            if None != range_:
                key[range_] = item[range_]
            self.table.delete_item(Key=key)
        print("[INFO] {} Items deletes".format(len(items)))