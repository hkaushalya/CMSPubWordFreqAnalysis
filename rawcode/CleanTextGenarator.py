__author__ = 'samantha'

#!/usr/bin/python

import sys
import string
from collections import Counter
import re

words_dic = {}
exclude = set(string.punctuation)
exclude.add('\xef')
exclude.add('\xbb')
# print('exclude=', exclude)
# should keep of the prepositions as they can carry valuable insight
ex_words = []   # any words
studylist = set(['the', 'of', 'and', 'to', 'is', 'are', 'to', 'for', 'with', 'from', 'as', 'by', 'on', 'this', 'we',
                'be', 'that', 'an', 'or', 'which', 'these', 'has', 'have', 'all', 'between', 'can', 'both', 'also', 'not'])
outfilename = 'wordcounts.txt'
discardfilename = 'discarded.txt'
outfilename2 = 'allwordcounts.txt'
outfilename3 = 'allwords.txt'
cleanwordsfilename = 'cleanWords.txt'

def results(filecount):
    global words_dic
    global studylist
    new_dic = {}

    for k, v in words_dic.items():
        if not k.isalpha():
            continue
        match = re.search(r"\\", k)
        if match:
            #print('found match {0}', match.group())
            continue

        if k not in ex_words:
            new_dic[k] = v

    cnt = Counter(new_dic)

    #print(cnt.most_common())
    fp = open(outfilename, 'w')
    fp2 = open(outfilename2, 'w')
    allwords_dic = dict(cnt.most_common())  # convert the paired list to dict

    fp.write('{0},{1}\n'.format('word', 'norm_count'))
    fp2.write('{0},{1}\n'.format('word', 'norm_count'))
    for wd in sorted(studylist):
        n = 0
        if wd in allwords_dic.keys():
            n = allwords_dic[wd]

        print('{0},{1},{2}'.format(wd, n, round(float(n)/filecount), 2))
        fp.write('{0},{1}\n'.format(wd, round(float(n)/filecount), 2))
        fp2.write('{0},{1}\n'.format(wd, round(float(n)/filecount), 2))


    #for tup in cnt.most_common():
    #    if tup[0] in studylist:
    #        print('{0},{1},{2}'.format(tup[0], tup[1], float(tup[1])/filecount))
    #        fp.write('{0},{1},{2}\n'.format(tup[0], tup[1], float(tup[1])/filecount))

    fp.close()
    print('Total words count =', sum([t[1] for t in cnt.most_common()]))


def process(argv):
    global words_dic

    f_disc = open(discardfilename, 'w')
    f_clean = open(cleanwordsfilename, 'w')

    for file in argv[1:]:
        # ignore previous outputs of this from processing (if case wild cards were used)
        if file.find(outfilename) >= 0 or \
            file.find(discardfilename) >= 0:
            print('Skipping possible previous output file ', file)
            continue

        print('Processing file ', file)
        fp = open(file)
        lineno = 0
        linesproc = []

        for line in fp.readlines():
            # do not read below Acknowledgment (avoid names/references)
            # One special case when the line contains only the word 'Acknowledgements'
            #print('found#', line.lower().find('acknowled')) # there can be spelling errors, so minimize requirement
            line = line.lower()
            lineno += 1
            #print('processing line:', line.lower())

            if line.find('acknowled') >= 0:
                print('\t Found a break point. Moving to next file!')
                break

            cleanWords = []
            for wd in line.split():
                #this may need word needs a bit of cleaning
                if len(wd) > 1:
                    if wd[-1] in string.punctuation.replace('-', ''):
                        #print(wd)
                        wd = wd.rstrip(string.punctuation.replace('-', ''))
                        #print('new wd=', wd)

                if len(wd) > 0:
                    if wd[0] in string.punctuation:
                        wd = wd.lstrip(string.punctuation.replace('-', ''))

                #if the wd len ==0 after striping
                if len(wd) < 2:
                    continue

                #this will be most expensive, cpu wise
                discard = False
                for c in string.punctuation.replace('-', ''):
                    if c in wd:
                        discard = True
                        break
                else:
                    if lineno not in linesproc:
                        linesproc.append(lineno)

                    if wd in words_dic.keys():
                        words_dic[wd] += 1
                    else:
                        words_dic[wd] = 1

                if not wd.isalpha():
                    discard = True

                if discard:
                    #print('Discarded=', wd)
                    f_disc.write(wd+'\n')
                else:
                    cleanWords.append(wd)

            #write this cleaned line to file
            cleanWords.append('\n')
            f_clean.write(' '.join(cleanWords))

        fp.close()


    f_clean.close()
    f_disc.close()
    f_clean.close()
    results(len(argv[1:]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need input file name")
    else:
        process(sys.argv)