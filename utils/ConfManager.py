import yaml
import os
import sys, getopt

class Configuration():
    # Load configuration
    def __init__(self, argv):
        self.conf = self.get_conf_file()
        self.get_conf_from_env()
        self.get_conf_from_params(argv)
        self.check_types()

    # Load static configuration from file
    def get_conf_file(self):
        with open('config.yaml') as json_data_file:
            conf = yaml.load(json_data_file)
            return conf 

    # Check if configuration is not override in env
    def get_conf_from_env(self):
        for key in self.conf.keys():
            try:
                self.conf[key] = os.environ[key.upper()]
            except:
                pass

    # Check if configuration is not override by the command line params
    def get_conf_from_params(self, argv):
        try:
            opts, args = getopt.getopt(argv, "o:f:t:a:l:b:p:d:")
        except getopt.GetoptError:
            print('export_dynamodb_to_s3 -o <outputfile> -f <format> -t <tablename> -a <aws_region> -l <limit> -b <bucket_name> -p <bucket_path> -d <delete>')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', "--help"):
                print('export_dynamodb_to_s3 -o <outputfile> -f <format> -t <tablename> -a <aws_region> -l <limit> -b <bucket_name> -p <bucket_path> -d <delete>')
                sys.exit()
            elif opt in ("-o", "--outputfile"):
                self.conf["filename"] = arg
            elif opt in ("-f", "--format"):
                self.conf["output_format"] = arg
            elif opt in ("-t", "--tablename"):
                self.conf["tablename"] = arg
            elif opt in ("-a", "--aws_region"):
                self.conf["aws_region"] = arg
            elif opt in ("-l", "--limit"):
                self.conf["limit_per_file"] = arg
            elif opt in ("-b", "--bucket_name"):
                self.conf["bucket_name"] = arg
            elif opt in ("-p", "--bucket_path"):
                self.conf["bucket_path"] = arg
            elif opt in ("-d", "--delete"):
                self.conf["delete_items"] = arg

    # Check type of config (delete_items must be a bool and limit an integer)
    def check_types(self):
        if str == type(self.conf["delete_items"]):
            if "true" == self.conf["delete_items"].lower():
                self.conf["delete_items"] = True
            elif "false" == self.conf["delete_items"].lower():
                self.conf["delete_items"] = False
            else:
                print("Param Error. delete_items must be a boolean")
                sys.exit(2)
        if str == type(self.conf["limit_per_file"]):
            try:
                self.conf["limit_per_file"] = int(self.conf["limit_per_file"])
            except:
                print("Param Error. limit_per_file must be an integer")
                sys.exit(2)