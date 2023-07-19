import sys
import random
from text_stats import clean_text, successor_table


def generate_text(filename, starting_word, max_words):
    with open(filename, 'r', encoding='utf8') as file:
        text = file.read()
    words = clean_text(text)
    table = successor_table(words)
    
    cur_word = starting_word
    msg = cur_word
    i = 0
    while i < max_words and cur_word in table:
        successors = table[cur_word]
        total_freq = sum(successors.values())
        weighted_successors = [(k, v / total_freq) for k, v in successors.items()]
        cur_word = random.choices([k for k, v in weighted_successors], [v for k, v in weighted_successors])[0]
        msg += " " + cur_word
        i += 1
    
    print(msg)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python generate_text.py <filename> <starting_word> <max_words>')
    else:
        generate_text(sys.argv[1], sys.argv[2], int(sys.argv[3]))