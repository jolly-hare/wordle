import datetime
import json
import re
import nltk
import time
import sys

# updated February 15, 2022:
#   * New Yorks Times purchased the game, now at: https://www.nytimes.com/games/wordle/index.html
#   * updated wordlists to reflect NYT's updates from https://www.nytimes.com/games/wordle/main.bd4cb59c.js
#   * added command line arguments to avoid needing to hand edit the script each new hint

# Initial script as of January 5, 2022....
#   * main puzzle at https://www.powerlanguage.co.uk/wordle/
#   * word lists extracted from https://www.powerlanguage.co.uk/wordle/main.db1931a8.js
#   * the puzzle word is always 5 characters in length, so too are these word lists


def load_wordlists(var):
    if var == "original":
        with open("wordle_answers.txt", "r") as f:
            answer_words = json.load(f)
        with open("wordle_valid.txt", "r") as f:
            valid_words = json.load(f)
    elif var == "nyt":
        with open("wordle_nyt_answers.txt", "r") as f:
            answer_words = json.load(f)
        with open("wordle_nyt_valid.txt", "r") as f:
            valid_words = json.load(f)

    return sorted(answer_words + valid_words), answer_words


def todays_answer(ans):
    # the game uses local system time to determine the answer
    delta = datetime.datetime.now() - datetime.datetime(2021, 6, 19)
    return ans[delta.days].upper()


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


def hints(wl, args):
    # find eligible words given grey, yellow, and green puzzle hints
    # grey = letter not in answer word
    # yellow = letter in answer word in a different position(s)
    # green = letter in word at this position; possibly in other positions (e.g. double letters)
    # a good start word is AROSE then UNTIL - naively using the top ten letters to get at least a couple yellows
    # with the defaults, it'll print all ~13k game-valid words
    yellow = ''
    for char in args[2]:
        if char != '.':
            yellow += f'(?=.*{char})'
    yellow += '.+'
    for word in wl:
        # skip words with grey letters
        if any(letter in args[3] for letter in word):
            continue
        # yellow letter(s), position invariant.
        # Default: r'.+' Example: r'(?=.*c)(?=.*d).+' means one or more "c" and one or more "d" in the word
        if re.search(fr'{yellow}', word) is not None:
            # green letters, in their position(s).
            # Default r'.....' Example: r'e.f..'
            if re.match(fr'{args[1]}', word) is not None:
                print(word)


def calc_edit_distance(wl, ans):
    distances = {}
    tic = time.perf_counter()
    for i in ans:
        for j in wl:
            dist = nltk.edit_distance(i, j)
            if dist in distances:
                distances[dist] += 1
            else:
                distances[dist] = 1
    toc = time.perf_counter()
    print(f'Calculated {sum(x for x in distances.values())} distances in {toc - tic:0.2f} seconds')
    # distances = {1: 46326, 2: 616059, 3: 5384578, 4: 26235133, 5: 51847810}  # wordlist x wordlist
    # distances = {0: 2315, 1: 13648, 2: 160098, 3: 1450456, 4: 8279588, 5: 20124075}  # answers x wordlist
    print('The number of words with a nltk.edit_distance(word1, word2):')
    print(sorted(distances.items(), key=lambda x: x[1]))


if __name__ == "__main__":
    show_me_the_answer = False  # do you want to see today's answer?
    calc_freqs = False  # do you want to calculate letter frequencies and word scores?
    calc_distances = False  # do you want to calculate edit distances between valid words?

    wordlist, answers = load_wordlists("nyt")  # "original" or "nyt"
    if show_me_the_answer:
        print(f"Today's answer is \"{todays_answer(answers)}\"")
    if calc_freqs:
        score_words(wordlist, get_letter_freq(wordlist))
    if calc_distances:
        calc_edit_distance(wordlist, answers)

    if len(sys.argv) != 4 or sys.argv[1] in ["/?", '--help'] or len(sys.argv[1]) != 5:
        print('\nReveal eligible words satisfying letter constraints\n')
        print('Usage: python wordle.py {green} {yellow} {grey}')
        print('  {green} is any green letters, with "." for spaces: \"a..s.\", or \".....\" for none')
        print('  {yellow} is any yellow letters: \"re\" or \".\" for none')
        print('  {grey} is any grey letters: \"xz\" or \".\" for none')
        print('\nExample (new puzzle): wordle.py ..... . .')
        print('Example (only grey): wordle.py ..... . untilxyz')
        print('Example (few yellow and grey): wordle.py ..... ar utlxyz')
        print('Example (few green and grey): wordle.py ar... . utlxyz')
    else:
        hints(wordlist, sys.argv)
