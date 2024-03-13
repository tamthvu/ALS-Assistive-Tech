# Find the word that starts with substring and has highest usage
# Returns word and count
def find_word_with_highest_count(substring):
    highest_count = 0
    matching_word = ""

    with open("words.txt", "r") as file:
        for line in file:
            word, count_str = line.strip().split()
            count = int(count_str)

            if word.startswith(substring) and count > highest_count:
                highest_count = count
                matching_word = word

    return matching_word, highest_count


substring = "ki"
result_word, result_count = find_word_with_highest_count(substring)

if result_word:
    print(f"The word starting with '{substring}' and having the highest count is '{result_word}' with count {result_count}.")
else:
    print(f"No matching word found for the given substring.")