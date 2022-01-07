import datetime
import json
import re


# as of January 5, 2022....
# main puzzle at https://www.powerlanguage.co.uk/wordle/
# word lists extracted from https://www.powerlanguage.co.uk/wordle/main.db1931a8.js
# the puzzle word is always 5 characters in length, so too are these word lists


def load_wordlists():
    with open("wordle_answers.txt", "r") as f:
        answer_words = json.load(f)
    with open("wordle_valid.txt", "r") as f:
        valid_words = json.load(f)
    return sorted(answer_words + valid_words), answer_words


def todays_answer(ans):
    # the game uses local system time to determine the answer
    delta = datetime.datetime.now() - datetime.datetime(2021, 6, 19)
    print(f"Today's answer is \"{ans[delta.days].upper()}\"")


def get_letter_freq(wl):
    # count all the letters and determine their frequency
    letter_counts = {}
    for word in wl:
        for letter in word:
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1
    letter_freq = {}
    for k, v in letter_counts.items():
        letter_freq[k] = round(v / (len(wl) * 5) * 100, 2)
    result = sorted(letter_freq.items(), key=lambda x: x[1], reverse=True)
    print(f"Wordlists' letter frequencies:\n{result}\n")
    return letter_freq


def score_words(wl, f):
    # top scoring words without duplicate letters
    scored_words = {}
    for word in wl:
        if len(word) == len(set(word)):
            score = 0
            for letter in word:
                score += f[letter]
            scored_words[word.upper()] = round(score, 2)
    scored_words_sorted = sorted(scored_words.items(), key=lambda x: x[1], reverse=True)
    print(f"Using the above frequencies on the {len(scored_words)} wordlist words with no letter duplication, "
          f"these are among the \"best\" starts:\n{scored_words_sorted[:30]}")


def hints(wl):
    # find eligible words given grey, yellow, and green puzzle hints
    # grey = letter not in answer word
    # yellow = letter in answer word in a different position(s)
    # green = letter in word at this position; possibly in other positions (e.g. double letters)
    # a good start word is AROSE then UNTIL - naively using the top ten letters to get at least a couple yellows
    # with the defaults, it'll print all ~13k game-valid words
    for word in wl:
        # skip words with grey letters
        # Default: ['.'] Example: ['a', 'b']
        if any(letter in ['.'] for letter in word):
            continue
        # yellow letter(s), position invariant.
        # Default: r'.+' Example: r'(?=.*c)(?=.*d).+' means one or more "c" and one or more "d" in the word
        elif re.search(r'.+', word) is not None:
            # green letters, in their position(s).
            # Default r'.....' Example: r'e.f..'
            if re.match(r'e.f..', word) is not None:
                print(word)


if __name__ == "__main__":
    show_me_the_answer = False  # do you want to see today's answer?
    calc_freqs = False  # do you want to calculate letter frequencies and word scores?

    wordlist, answers = load_wordlists()
    if show_me_the_answer:
        todays_answer(answers)
    if calc_freqs:
        score_words(wordlist, get_letter_freq(wordlist))
    hints(wordlist)  # to list eligible words, update these regexp each round (as desired) of your puzzle
