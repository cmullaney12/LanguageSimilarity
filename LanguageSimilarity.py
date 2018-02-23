import sys
import re
import math


def parseInputFile(filename):
    """This function takes the filename of the input file and parses it.

    Output is a tuple with two items:
        - A dictionary mapping unique language names to a list of filenames
          for that language
        - A list of the 'unknown' language file names
    """
    lang_dict = {}
    unknown_files = []
    f = open(filename)
    for line in f:
        lang, txt = line.split()
        if lang == 'Unknown':
            unknown_files.append(txt)
        else:
            lang_dict[lang] = lang_dict.get(lang, []) + [txt]
    f.close()
    return (lang_dict, unknown_files)

def readFile(filename):
    """Read a single language file"""
    f = open(filename)
    text = f.read()
    f.close()
    return text

def cleanText(text):
    """Clean some given text:
        - convert to lowercase
        - remove non-alpha characters
    """
    cleaned = text.lower()
    cleaned = re.sub('[^a-zA-Z]+', ' ', cleaned)

    return cleaned

def countTrigrams(text):
    """Generate trigram frequency counts for the given text.

    Output a dictionary mapping trigrams to frequency counts
    """
    tri_counts = {}
    if len(text) >= 3:
        for index in range(len(text)-2):
            tri = text[index:index+3]
            tri_counts[tri] = tri_counts.get(tri, 0) + 1
    
    return tri_counts

def combineTrigramCounts(list_of_counts):
    """Given a list of trigram counts (as dictionaries)
    combine them into one dictionary containing total counts for all trigrams
    """
    combined_counts = {}
    for d in list_of_counts:
        for key in d:
            combined_counts[key] = combined_counts.get(key, 0) + d[key]
    
    return combined_counts

def normalizeTrigramCounts(tri_counts):
    """Given a dictionary of trigram frequencies, normalize each
    value using the total count of all trigrams
    """
    totalFreq = float(sum(tri_counts.values()))
    normalized = {}
    for tri in tri_counts:
        normalized[tri] = tri_counts[tri] / totalFreq
    
    return normalized

def getLanguageCounts(list_of_files):
    """Given a list of filenames (for a certain language), do the following:
    - Read each language file
    - Clean the resulting text
    - Count trigram frequencies
    - Combine all trigram frequencies for this language
    - Output normalized trigram counts
    """
    text_list = [readFile(f) for f in list_of_files]
    cleaned_list = [cleanText(t) for t in text_list]
    tri_counts = [countTrigrams(c) for c in cleaned_list]
    lang_freq = combineTrigramCounts(tri_counts)

    return normalizeTrigramCounts(lang_freq)

def fileToTrigrams(filename):
    """Given a single file name, read it, clean it, 
    count trigrams and output the normalized frequencies
    """
    text = readFile(filename)
    cleaned = cleanText(text)
    tri_counts = countTrigrams(cleaned)
    
    return normalizeTrigramCounts(tri_counts)

def cosineSimilarity(langA, langB):
    """Given normalized trigram frequencies for language A
    and language B, calculate the overall cosine similarity
    using the formula: https://en.wikipedia.org/wiki/Cosine_similarity
    """
    sum_AxB = sum([langA[tri] * langB.get(tri, 0) for tri in langA])
    
    sum_square_A = sum([v**2 for v in langA.values()])
    sum_square_B = sum([v**2 for v in langB.values()])

    return sum_AxB / (math.sqrt(sum_square_A) * math.sqrt(sum_square_B))


def predictLanguages(lang_dict, unknown):
    """Given a dictionary of known languages and trigram frequencies,
    and the trigram frequencies for an unknown language:
    - Calculate the cosine similarity between each known language and the unknown language
    - Output a list of (known_language, similarity) tuples, sorted in descending order
    """
    predictions = []
    for lang in lang_dict:
        sim = cosineSimilarity(unknown, lang_dict[lang])
        predictions.append((lang, sim))
    
    return sorted(predictions, key= lambda pair: pair[1], reverse=True)

if __name__ == '__main__':

    ## Read the input and output text file names
    input_txt = sys.argv[1]
    output_txt = sys.argv[2]

    output_file = open(output_txt, 'w')

    ## Parse the input text and generate trigram counts for each language
    files, unknowns = parseInputFile(input_txt)
    lang_dict = {lang:getLanguageCounts(files[lang]) for lang in files}

    ## For each unknown file
    for u in unknowns:
        ## Generate trigram frequencies
        u_trigrams = fileToTrigrams(u)

        ## Make predictions for all known languages
        preds = predictLanguages(lang_dict, u_trigrams)

        ## Write out the similarities for this unknown language
        output_file.write(u+'\n')
        for p in preds:
            output_file.write('    {}:  {}\n'.format(p[0], p[1]))