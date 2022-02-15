# wordle
Get Wordle word hints or simply reveal today's answer

Wordle is available here: https://www.nytimes.com/games/wordle/index.html

I extracted the word lists from Wordle's javascript files on February 15, 2022 and include them here as separate text files. If the New York Times changes their wordlists or the underlying game logic then this script has a good chance of misleading you.... but until then it'll work!

The New York Times also removed a number of words from the original valid words and answer words lists that are offensive or racial slurs. I'm leaving those orignal word lists intact in this repo, but I do not condone the use of that offensive or derogatory language.

# general usage
python wordle.py {green} {yellow} {grey}

{green} is any green letters, with "." for spaces: \"a..s.\", or \".....\" for none

{yellow} is any yellow letters: \"re\" or \".\" for none

{grey} is any grey letters: \"xz\" or \".\" for none


Example (new puzzle): wordle.py ..... . .

Example (only grey): wordle.py ..... . untilxyz

Example (few yellow and grey): wordle.py ..... ar utlxyz

Example (few green and grey): wordle.py ar... . utlxyz

        
Reflect your puzzle's progress in the form of grey (unused) letters, yellow (wrong position) letters, and green (correct position) letters. The script will output eligible words that meet those criteria.

# today's answer
To reveal today's answer (based on your system's local time), set the line 115 show_me_the_answer variable to True

# letter frequency
To display the word lists' letter frequencies and some suggested high scoring words, set the line 116 calc_freqs variable to True

# edit_distance
Calculate the Levenshtein edit-distance between two words: the answers and the wordlist
