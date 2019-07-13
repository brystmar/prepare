import json


class DatabaseDAO:

    def __init__(self, flat_file_path):
        # open flat file
        self.flat_file_path = flat_file_path
        with open(self.flat_file_path, 'r') as database_file:
            self.user_data_dict = json.load(database_file)

    def get_user(self, id):
        return self.user_data_dict[id]

    def put_user(self, id, user):
        self.user_data_dict[id] = user
        print(user)
        with open(self.flat_file_path, 'w') as database_file:
            json.dump(self.user_data_dict, database_file)
