from string import ascii_lowercase, ascii_uppercase, digits
from itertools import combinations

# Custom alphabet with lowercase letters, uppercase letters, numbers, and some punctuation symbols
alphabet = list(ascii_lowercase + ascii_uppercase + digits + "!@#$%^&*()")


def generate_combinations(word_length, print_each):
    for combination in combinations(alphabet, word_length):
        if print_each:
            print(combination)
        yield "".join(combination)


def save_combinations_to_file(word_length, print_each):
    file_name = f"words{word_length}.txt"
    with open(file_name, "w") as file:
        for word in generate_combinations(word_length, print_each):
            file.write(word + "\n")


if __name__ == "__main__":
    print_each = input("Print Each Password? y/n\n") == "y"
    word_length = int(input("Length: "))
    save_combinations_to_file(word_length, print_each)
