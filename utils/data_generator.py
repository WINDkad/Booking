import random
import string
from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        return faker.email()

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        uppercase = random.choice(string.ascii_uppercase)

        lowercase = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special_char = random.choice("?@#$%^&*|:")

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(uppercase + lowercase + digit + special_char + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_random_asc_or_desc():
        return random.choice(['asc', 'desc'])

    @staticmethod
    def generate_random_int(min, max):
        return faker.random_int(min=min, max=max)

    @staticmethod
    def generate_random_sentence(count):
        return faker.sentence(nb_words=count)

    @staticmethod
    def generate_random_boolean():
        return faker.boolean()