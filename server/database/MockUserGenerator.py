import uuid
import random


def _string_random(n):
    lst = []
    for i in range(n):
        lst.append(random.randint(0, 9))
    sent_str = ""
    for i in lst:
        sent_str += str(i)
    return sent_str


def generate_mock_users(num_of_users):
    mock_users = {}

    for i in range(num_of_users):
        phone_numbers = []
        number_of_phone_numbers = random.randint(1, 3)
        for j in range(number_of_phone_numbers):
            phone_numbers.append('+1' + '504' + str(_string_random(3)) + str(_string_random(4)))

        user_id = str(uuid.uuid4())

        user_dict = {
            'id': user_id,
            'address': "Random Street Address " + str(i),
            'lat': str(random.uniform(30.030049, 30.150631)),
            'long': str(random.uniform(-89.920564, -89.743159)),
            'phone_numbers': phone_numbers,
            'party_member': {
                'adults': str(random.randint(0, 3)),
                'children': str(random.randint(0, 3)),
                'infants': str(random.randint(0, 2)),
                'elderly': str(random.randint(0, 2)),
                'pets': str(random.randint(0, 2))
            },
            'supplies': {
                'water': str(random.randint(0, 10)),
                'food': str(random.randint(0, 45))
            }
        }

        mock_users[user_id] = user_dict

    return mock_users
