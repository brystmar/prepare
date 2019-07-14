import json
import csv

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

    def export_to_csv(self, csv_filepath):
        with open(csv_filepath, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Write CSV header
            csv_writer.writerow(['id', 'lat', 'long', 'address', 'ph_1', 'ph_2', 'ph_3', 'ph_4', 'ph_5', 'su_water', 'su_food', 'pty_adu', 'pty_chi', 'pty_inf', 'pty_eld', 'pty_pet'])
            for user_id in self.user_data_dict:
                user = self.user_data_dict.get(user_id)

                user_phone_numbers = user.get('phone_numbers')

                csv_writer.writerow([
                    user.get('id'),
                    float(user.get('lat', 0)),
                    float(user.get('long', 0)),
                    user.get('address'),
                    user_phone_numbers[0] if 0 < len(user_phone_numbers) else "",
                    user_phone_numbers[1] if 1 < len(user_phone_numbers) else "",
                    user_phone_numbers[2] if 2 < len(user_phone_numbers) else "",
                    user_phone_numbers[3] if 3 < len(user_phone_numbers) else "",
                    user_phone_numbers[4] if 4 < len(user_phone_numbers) else "",
                    int(user.get("supplies").get("water")),
                    int(user.get("supplies").get("food")),
                    int(user.get("party_member").get("adults")),
                    int(user.get("party_member").get("children")),
                    int(user.get("party_member").get("infants")),
                    int(user.get("party_member").get("elderly")),
                    int(user.get("party_member").get("pets"))
                ])