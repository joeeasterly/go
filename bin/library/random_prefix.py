import random
def random_prefix():
    initials = '123456789abcdefghjkmnopqrstuvwxyz'
    prefix = random.choice(initials) + random.choice(initials)
    return prefix
print(random_prefix())