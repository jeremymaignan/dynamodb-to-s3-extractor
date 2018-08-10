from tqdm import tqdm
import decimal
import csv
import json

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

class FileManager():
    def get_keys(self, items):
        keys = []
        for item in items:
            for key in item.keys():
                if key not in keys:
                    keys.append(key)
        print("[INFO] Header {}".format(keys))
        return keys

    def write_csv(self, items, filename):
        keys = self.get_keys(items)
        file = csv.writer(open("tmp/{}".format(filename), "w"), delimiter=';')
        file.writerow(keys)
        print("[INFO] Write csv")
        for item in tqdm(items):
            tmp = []
            for key in keys:
                if key in item.keys():
                    tmp.append(item[key])
                else:
                    tmp.append("")
            file.writerow(tmp)

    def write_json(self, items, filename):
        with open("tmp/{}".format(filename), 'w+') as f:
            f.write(json.dumps(items, cls=DecimalEncoder))
