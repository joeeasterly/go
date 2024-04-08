#!/usr/local/gh/go/.venv/bin/python3
# Your base-32 numbering system
BASE32_CHARS = "123456789abcdefghjkmnpqrstuvwxyz"

# Encoding function
def encode_base32(number):
    if number == 0:
        return BASE32_CHARS[0]
    
    encoding = ''
    while number > 0:
        remainder = number % 32
        encoding = BASE32_CHARS[remainder] + encoding
        number //= 32
    return encoding

# Calculate the number of 4-digit numbers in your base-32 system (32^4)
total_numbers = 32 ** 4

# Generate the four-digit numbers in your custom base-32 system
numbers_base32 = [encode_base32(i).zfill(4) for i in range(total_numbers)]

# Write these numbers to a file
with open('new_identifiers.txt', 'w') as f:
    for num in numbers_base32:
        f.write(f"{num}\n")

print(f"Written {total_numbers} four-digit numbers to new_identifiers.txt")
