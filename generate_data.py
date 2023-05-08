import json
import logging
import time
from dataclasses import dataclass

from faker import Faker

# Initialize the Faker library
fake = Faker()

# Generate fake data for users


def generate_person() -> dict:
    created_at = fake.date_between(start_date='-5y', end_date='today')
    updated_at = fake.date_between(start_date=created_at, end_date='today')

    user = {
        "name": fake.name(),
        "email": fake.email(),
        "date_of_birth": fake.date_of_birth().strftime('%Y-%m-%d'),
        "created_at": created_at.strftime('%Y-%m-%d'),
        "updated_at": updated_at.strftime('%Y-%m-%d')
    }
    return user


@dataclass
class DataGenerator:
    person_num: int = 10
    user_data = []

    def start(self):
        # Load existing data from the JSON file
        try:
            with open('fake_users.json', 'r') as f:
                self.user_data = json.load(f)
        except FileNotFoundError:
            pass

        for _ in range(self.person_num):
            self.user_data.append(generate_person())

    def dump(self):
        # Save the data to a JSON file
        with open('fake_users.json', 'w') as f:
            json.dump(self.user_data, f)

        print("Fake data generated and added to fake_users.json")


while True:
    dg = DataGenerator()
    dg.start()
    dg.dump()
    logging.info("Added new {} persons".format(dg.person_num))
    time.sleep(1)
