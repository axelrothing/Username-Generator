from fastapi import FastAPI, Path
import random
import string

app = FastAPI()

numbers_used = None

@app.get("/generate-username/{first}/{last}/{numbers}/{unique}")
def generate(first: str = Path(None, description="The last name of the name to create a username"), last: str = Path(None, description="The last name of the name to create a username"), numbers: int = Path(None, description="Choose if the username should have numbers, 1 for yes and 0 for no", ge=0, le=1), unique: int = Path(None, description="Choose if the username should have a last letter that is not in the first or last name, 1 for yes and 0 for no", ge=0, le=1)):
    return {
        "username": generate_username(first, last, numbers, unique),
        "numbers": numbers_used
    }

def generate_username(first_name: str, last_name: str, numbers: int, unique: int):
    global numbers_used

    first_name = first_name.lower()
    last_name = last_name.lower()
    username_string = ""
    username_string += first_name[:2]
    username_string += last_name[:2]
    if unique == 1:
        letter_list = string.ascii_lowercase
        while True:
            last_letter = random.choice(letter_list)
            if letter_list not in username_string:
                break
        username_string += last_letter
    else:
        username_string += random.choice(first_name)

    def generate_numbers():
        while True:
            random_numbers_list = [random.randint(0, 9) for _ in range(2)]
            if (random_numbers_list[0] != random_numbers_list[1]) and (random_numbers_list[1] not in [0, 9]):
                random_numbers_list = [str(num) for num in random_numbers_list]
                break
        random_numbers_string = "".join(random_numbers_list)
        random_numbers_string += random_numbers_list[1]
        return random_numbers_string

    if numbers == 1:
        no_numbers = [911, 112, 113, 110, 199]
        while True:
            random_numbers = generate_numbers()
            if no_numbers != int(random_numbers):
                break
        numbers_used = random_numbers
        username_string += random_numbers

    return username_string

