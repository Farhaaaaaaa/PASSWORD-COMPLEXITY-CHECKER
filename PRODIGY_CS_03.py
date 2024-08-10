import pyfiglet
import string
import math
import os

def display_fancy_text(text):
    fancy_text = pyfiglet.figlet_format(text)
    print(fancy_text)

def calculate_entropy(password):
    pool_size = 0
    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)
    
    return len(password) * math.log2(pool_size)

def estimate_crack_time(entropy):
    return 2**entropy / (10**10)  # Assuming 10 billion guesses per second

def check_common_password(password, common_password_file):
    try:
        with open(common_password_file, 'r') as f:
            common_passwords = f.read().splitlines()
        if password in common_passwords:
            return True
        return False
    except FileNotFoundError:
        print("Common password file not found. Skipping common password check.")
        return False

# Display the fancy software name
display_fancy_text("PASSWORD COMPLEXITY CHECKER")

# ANSI escape code for red text
red_text = "\033[91m"
reset_text = "\033[0m"

# Prompt the user for the operation
password = input(red_text+ "ENTER THE PASSWORD YOU WANT TO CHECK:"+ reset_text).upper()

# Check if the password is common
common_password_file = 'common_password'
is_common = check_common_password(password, common_password_file)

if is_common:
    print("Your password is too common and highly insecure. Consider changing it immediately.")
    score = 0
else:
    # Calculate entropy
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)


    print(f"Estimated Time to Crack: {crack_time:.2f} seconds")

    # Criteria-based scoring
    score = 0
    length = len(password)
    upper_case = any(c.isupper() for c in password)
    lower_case = any(c.islower() for c in password)
    special_character = any(c in string.punctuation for c in password)
    digits = any(c.isdigit() for c in password)
    criteria = [upper_case, lower_case, special_character, digits]

    # Length-based scoring
    if length > 8:
        score += 1
    if length > 12:
        score += 1
    if length > 16:
        score += 1
    if length > 20:
        score += 1


    # Criteria-based scoring
    score += sum(criteria)

    # Feedback based on the score
    if score < 4:
        print(f"Your password is weak! Your score is {score}/7")
    elif score == 4:
        print(f"Your password is okay! Your score is {score}/7")
    elif score < 6:
        print(f"Your password is pretty good! Your score is {score}/7")
    else:
        print(f"Your password is strong! Your score is {score}/7")
