import random
import string
import re

def random_string(length = 10, patterns = [r'[A-Z]', r'[a-z]', r'[0-9]']):
    choices = string.ascii_letters + string.digits
    rnd_str = ''.join(random.choice(choices) for _ in range(length))

    while None in [re.search(p, rnd_str) for p in patterns]:
        rnd_str = ''.join(random.choice(choices) for _ in range(length))
    else:
        return rnd_str
        