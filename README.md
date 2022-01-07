# wordle
Get Wordle word hints or simply reveal today's answer

Wordle is available here: https://www.powerlanguage.co.uk/wordle/

I extracted the word lists from Wordle's javascript files on January 5, 2022 and include them here as separate text files. If the Wordle developers change their wordlists or the underlying game logic then this script has a good chance of misleading you.... but until then it'll work!

# general usage
Modify the filtering list and regular expressions in lines 67, 71, and 74 to reflect your puzzle's progress in the form of grey (unused) letters, yellow (wrong position) letters, and green (correct position) letters. The script will output eligible words that meet those criteria.

# today's answer
To reveal today's answer (based on your system's local time), set the line 79 show_me_the_answer variable to True

# letter frequency
To display the word lists' letter frequencies and some suggested high scoring words, set the line 80 calc_freqs variable to True
