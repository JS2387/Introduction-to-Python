import sys
import string
import re
from collections import defaultdict, Counter
import argparse

def read_file(filename, encoding = 'utf-8'):
    """Reads a text file and returns its content as a string."""
    try:
        with open(filename, "rt", encoding = encoding) as f:
            return f.read()
    except FileNotFoundError:
        print("The file does not exist!")
        sys.exit()

def clean_text(text):
    """Cleans a string of text and returns a list of words."""
    text = text.lower() # Convert to lowercase
    text = text.replace('’',' ').replace('—',' ').replace('‘',' ').replace('“',' ').replace('”',' ')
    text = text.translate(str.maketrans('', '', string.punctuation + string.digits)) # Remove punctuation and digits
    words = text.split() # Split into words
    return words

# Define the frequency_table function to count the frequency of each letter in the text
def frequency_table_letters(words):
    freq = defaultdict(int)
    for word in words:
        for letter in word:
            freq[letter] += 1
    freq = dict(Counter(freq).most_common())
    return freq

# Define the frequency_table function to count the frequency of each word in the text
def frequency_table_words(words):
    freq = defaultdict(int)
    for word in words:
        freq[word] += 1
    freq = dict(Counter(freq).most_common())
    return freq

# Define the count_words function to count the number of words in the text
def count_words(words):
    return len(words)

# Define the count_unique_words function to count the number of unique words in the text
def count_unique_words(words):
    return len(set(words))

# Define the successor_table function to create a table of successors for each word
def successor_table(words):
    bigrams = defaultdict(Counter) # create a defaultdict to store the frequency counts for each bigram
    for i, word in enumerate(words[:-1]):
        bigrams[word][words[i+1]] += 1 # increment the frequency count for the current bigram
    
    successors = {} # create an empty dictionary to store the top 3 successors for each word
    for word, counts in bigrams.items():
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True) # sort the successor counts in descending order
        successors[word] = dict(sorted_counts[:3]) # keep only the top 3 successors for the current word
    
    return successors

def print_results(results, outfile=None):
    output = f"Number of words: {results['num_words']} \n" \
             f"Number of unique words: {results['num_unique_words']} \n" \
             f"Top 5 most common words: \n"
    for word, frequency in results['top_words']:
        output += f"{word}: {frequency} \n"
        if word in results['successors_table']:
            output += f"    Top 3 successors: \n"
            for successor, frequency in list(results['successors_table'][word].items())[:3]:
                output += f"    {successor}: {frequency}\n"

    output += f"Frequency table of letters: \n"
    for letter, count in results['letters_table'].items():
        output += f"{letter}: {count} \n"
        
    if outfile:
        outfile.write(output)
    else:
        print(output)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Text file to analyze")
    parser.add_argument("--output", help="output file name", default=None)
    args = parser.parse_args()
    
    # Read the text file
    text = read_file(args.filename)

    # Clean the text
    words = clean_text(text)
    
    # Create a frequency table of words
    freq_table_words = frequency_table_words(words)
    
    # Create a frequency table of letters
    freq_table_letters = frequency_table_letters(words)
    
    results = {
        "num_words": count_words(words),
        "num_unique_words": count_unique_words(words),
        "top_words": list(freq_table_words.items())[:5],
        "letters_table": freq_table_letters,
        "successors_table": successor_table(words),
    }
    
    if args.output:
        with open(args.output, 'w', encoding = 'utf-8') as outfile:
            print_results(results, outfile)
    else:
        print_results(results)

                 

if __name__ == '__main__':
    main()