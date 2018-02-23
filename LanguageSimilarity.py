import sys
import re
import math


def parseInputFile(filename):
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
    f = open(filename)
    text = f.read()
    f.close()
    return text

def cleanText(text):
    cleaned = text.lower()
    cleaned = re.sub('[^a-zA-Z]+', ' ', cleaned)

    return cleaned

def countTrigrams(text):
    tri_counts = {}
    if len(text) >= 3:
        for index in range(len(text)-2):
            tri = text[index:index+3]
            tri_counts[tri] = tri_counts.get(tri, 0) + 1
    
    return tri_counts

def combineTrigramCounts(list_of_counts):
    combined_counts = {}
    for d in list_of_counts:
        for key in d:
            combined_counts[key] = combined_counts.get(key, 0) + d[key]
    
    return combined_counts

def normalizeTrigramCounts(tri_counts):
    totalFreq = float(sum(tri_counts.values()))
    normalized = {}
    for tri in tri_counts:
        normalized[tri] = tri_counts[tri] / totalFreq
    
    return normalized

def getLanguageCounts(list_of_files):
    text_list = [readFile(f) for f in list_of_files]
    cleaned_list = [cleanText(t) for t in text_list]
    tri_counts = [countTrigrams(c) for c in cleaned_list]
    lang_freq = combineTrigramCounts(tri_counts)

    return normalizeTrigramCounts(lang_freq)

def fileToTrigrams(filename):
    text = readFile(filename)
    cleaned = cleanText(text)
    tri_counts = countTrigrams(cleaned)
    
    return normalizeTrigramCounts(tri_counts)

def cosineSimilarity(langA, langB):
    sum_square_A = math.sqrt(sum([v**2 for v in langA.values()]))
    sum_square_B = math.sqrt(sum([v**2 for v in langB.values()]))
    sum_AxB = sum([langA[tri] * langB.get(tri, 0) for tri in langA])

    return sum_AxB / (sum_square_A * sum_square_B)


def predictLanguages(lang_dict, unknown):
    predictions = []
    for lang in lang_dict:
        sim = cosineSimilarity(unknown, lang_dict[lang])
        predictions.append((lang, sim))
    
    return sorted(predictions, key= lambda pair: pair[1], reverse=True)

if __name__ == '__main__':
    input_txt = sys.argv[1]
    output_txt = sys.argv[2]

    output_file = open(output_txt, 'w')

    files, unknowns = parseInputFile(input_txt)
    lang_dict = {lang:getLanguageCounts(files[lang]) for lang in files}

    for u in unknowns:
        u_trigrams = fileToTrigrams(u)
        preds = predictLanguages(lang_dict, u_trigrams)
        output_file.write(u+'\n')
        for p in preds:
            output_file.write('    {}:  {}\n'.format(p[0], p[1]))