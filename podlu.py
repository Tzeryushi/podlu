import itertools
from nltk.corpus import wordnet

#discover and populate 2d array with all possible synonyms
#run through first letters and see if any create real words
#attempt to suggest alternatives based on vowel structure?

#NEXT: work on increased word similarity net creation - does relatedwords have an api?

#grab phrases for acronym
print("Welcome to PODLU! Let's explore other options for your lacking acronyms.")
fullString = input("Enter your phrases, delineated by spaces: ")
wordArray = fullString.split()
wnLemmas = set(wordnet.all_lemma_names())
synList = []
failList = []
#for each word given, populate a list of homonyms and definitions, removing direct synonyms
for i, c in enumerate(wordArray):
    if not(c in wnLemmas):
        print("\"" + c + "\" not found in wordnet. No synonyms will be discovered.")
        failList.append(i)
        synList.append(c)
        continue
    tempSyns = wordnet.synsets(c)
    homonym = c
    tempSyns[:] = [h for h in tempSyns if h.name().split(".")[0] == homonym]
    if not tempSyns:
        print("Unfortunately, your word \"" + c + "\" exists but is not given a specified definition in Wordnet for whatever reason. I know, what the fuck.")
        failList.append(i)
        synList.append(c)
        continue
    synList.append(tempSyns)

#query the user for their preferred definition for each word
#populate 2d array (trueSyn) of synonyms of proper definition
trueSyn = []
for index, r in enumerate(synList):
    #print(r)
    if failList:
        if index == failList[0]:
            print(wordArray[index])
            trueSyn.append([wordArray[index]])
            failList.pop(0)
            continue
    print("Enter the index number of the definition you prefer for word " + str(index+1) + ", \"" + r[0].name().split(".")[0] + "\":")
    for i, c in enumerate(r):
        print("(" + str(i) + ") " + c.name().split(".")[1] + ". " + c.definition())
    word = int(input("Index: "))
    lemmas = r[word].lemma_names()
    similars = [h.name().split(".")[0] for h in r[word].similar_tos()]
    for h in similars:
        if not(h in lemmas):
            lemmas.append(h)
    trueSyn.append(lemmas)
    #trueSyn.append([h.name().split(".")[0] for h in r[word].similar_tos()])

#run through trueSyn to discover possible acronym combinations
print(trueSyn)
acroLength = len(trueSyn)
acroList = []
if acroLength <= 1:
    print("Not enough phrases for acronym. Program will close.")
    quit()
mixedSyns = list(itertools.product(*trueSyn))
for r in mixedSyns:
    testCase = ""
    for c in r:
        testCase += c[0]
    if not(testCase in wnLemmas):
        print(testCase + " not found in wordnet. Rejected!")
    else:
        print(testCase + " is a word. Approved!")
        acroList.append(r)
    
if not acroList:
    print("Whoops, nothing nice found. Bye.")
else:
    print("Woah, we got options!\nHow about...\n")
    for r in acroList:
        for c in r:
            print(c)
        print()
dang = input("End program...")