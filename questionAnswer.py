# This is a Question answer system

# read the input file
import nltk
#nltk.data.path.append("/home/alangar/nltk_data")
from sys import argv
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import operator
import os

from nltk.stem.lancaster import LancasterStemmer
import nltk

confident = 6
clue = 3
good_clue = 4
slam_dunk = 20

# Read file and make a list
def readFile(path):
    st = open(path)
    lines = st.read().splitlines()
    return lines

def contains(a, b):
  return len(set(a).intersection(b))

def listToLower(list):
    listToLower =[ x.lower() for x in list]
    return listToLower

def pronounRule(question,stsent,stpre):
    Score = 0
    if contains(PRONOUN,stsent) and not contains(stsent,HUMAN):
        #print "he"
        if (contains(stpre,HUMAN) and contains(stpre,question) and contains(question,HUMAN)):
            Score = Score + 2 + WordMatch(question,stsent)
            print "scored"
    return Score


def whoRules(question,stsent):
    Score = 0
    flag = 1
    name = ["name", "named"]

    if contains(stsent,ORG) or contains(stsent, PERREP):
        Score = Score + confident
        print(stsent)
        print(question)
    if not contains(question,HUMAN) and contains(stsent,HUMAN):
        Score = Score + confident + WordMatch(question,stsent)

    if not contains(question, OCC) and contains(stsent, OCC):
        Score = Score + confident
    if not contains(question,HUMAN) and contains(stsent,name):
        Score = Score + good_clue
    if contains(stsent, listToLower(OCC)):
        Score = Score + good_clue
    if contains(stsent,HUMAN) and contains(stsent,listToLower(OCC)):
        Score = Score + slam_dunk

    return Score

def whatRules(question,stsent):
    Score = 0
    flag = 1
    tlist = ["today","yesterday","tomorrow","last night"]
    #timelist = ["a.m.","a.m","AM","A.M","p.m.","p.m","PM","P.M",]
    nPP = []

    for w in PP:
        nPP.append("name " + w)
    if contains(question,["time"]) and contains(stsent,timelist):
        Score = Score +15
    if contains(question,MONTH) and contains(stsent, tlist):
        Score = Score + min(contains(question,MONTH),contains(stsent, tlist))*clue

    if "kind" in question and contains(stsent, ["call","from"]):
        Score = Score + good_clue

    if "name" in question and contains(stsent,["name","call","known"]):
        Score = Score + slam_dunk

    if contains(question,nPP) and contains(stsent,HUMAN + OCC) and contains(HUMAN+OCC , PP):
        Score = Score + slam_dunk

    return Score

def whenRules(question,stsent):
    Score = 0
    flag = 1
    list = ["first","last","since","ago"]
    list2 = ["start", "begin"]
    list3 = ["start", "begin", "since", "year"]

    if contains(stsent,TIME):
        Score = Score + confident

        Score = Score + WordMatch(question,stsent)

    if contains(question,["the last"]) and contains(stsent,list):
        Score = Score + slam_dunk

    if contains(question,list2) and contains(stsent,list3):
        Score = Score + slam_dunk

    return Score

def whereRules(question,stsent):
    Score = 0
    flag = 1
    if contains(stsent, LOCPREP) and contains(stsent, LOC):
        Score = Score + good_clue + WordMatch(question,stsent)

    elif contains(stsent, LOC):
        Score = Score + 6 + WordMatch(question,stsent)

    return Score

def datelineRule(question):
    Score = 0

    if contains(question, "happens"):
        Score = Score + good_clue
    if contains(question, "take") and contains(question, "place"):
        Score = Score + good_clue
    if contains(question, "this"):
        Score = Score + slam_dunk
    if contains(question, "story"):
        Score = Score + slam_dunk

    return Score

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def howRules(question, stsent):
    Score = 0
    flag = 1
    number = hasNumbers(' '.join(stsent))
    cost = ["much", "cost", "paid", "earn"]
    currency = ["$", "euro", "euros","USD", "EUR", "pound","dollar","dollars","not paid", "salary", "money", "cent","cents","penny","pennies","dime","dimes","quarter","quarters"]
    siz = ["foot","square-foot","feet","meters","meter","inches","inch"]
    age = ["old", "age","young","years"]
    if contains(question, cost):

        if contains(stsent, currency):
            Score = Score + 10
            if(number):
                Score = Score + 6
    elif "how many" in " ".join(question).lower():

        if hasNumbers(stsent):
            Score = Score + 6
    elif "how big" in " ".join(question).lower() or "how tall" in " ".join(question).lower():

        if (number):
            Score = Score + 6
            if any(x in " ".join(stsent).lower() for x in siz):
                Score = Score + 20

    elif "how old" in " ".join(question).lower():
        if contains(stsent, age):
            Score = Score + 10
            if(number):
                Score = Score + 20


    return Score


def getVerbRoot(word):
    for i in range(len(VERBS)):
        if(word in VERBS[i]):
            return i

def WordMatch(question,stsent):
    Score = 0
    st = LancasterStemmer()
    qtag = nltk.pos_tag(question)
    stag = nltk.pos_tag(stsent)
    flag = 0
    #count = 0
    for i in range(0,len(question)):
        for j in range(0,len(stsent)):
            if('V' in qtag[i][1][0] and 'V' in stag[j][1][0]):
                flag =0
                '''
                Score = Score + count*0.1
                count =0
                '''
                verbQ = getVerbRoot(question[i])
                if verbQ is not None:
                    verbS = getVerbRoot(stsent[j])
                    if( verbQ==verbS ):
                        Score = Score + 12
    #
                elif(st.stem(question[i]) == st.stem(stsent[j])):
                    Score = Score + 12
            if(question[i].lower() == stsent[j].lower() and flag == 0):
                #flag = 1 #removed counting consecutive word block
                Score = Score + 4

            '''
            if(flag == 1):
                count = count + 1
            '''

    return Score




#script, filename = argv
filename = "C:/Users/harshitha/Desktop/NLP/Project/input"
#filename = "C:/Users/Varsha/PycharmProjects/NLP/nlp_daringduck/testset1"
txt = open(filename)
data = txt.readlines()
#print len(data)
path = data[0].strip("\n")
#print path

#SEMANTIC CLASSIFICATION:
HUMAN = []
LOC = []
TIME = []
OCC = []
PP = []
NAME = []
LOCPREP = []
VERBS = []
ORG = []
PERREP = []
PRONOUN = []

timelist = ["a.m.","a.m","AM","A.M","p.m.","p.m","PM","P.M",]
# Reading verbForms
lines = readFile('verbForms.txt')
lines = readFile('verbForms.txt')

for i in range(0,len(lines)):
    VERBS.append(lines[i].split("\t"))


PP = readFile('PP.txt')

ORG = readFile('org.txt')

PERREP = readFile('personRep.txt')

PRONOUN = readFile('pronouns')

humanFile = open("yob2000.txt")
humanFile = humanFile.readlines()
for i in range(1,len(humanFile)):
    name = humanFile[i].split(",")
    HUMAN.append(name[0])


MONTH = ["January", "February", "March","April","May","June","July","August","September","October","November","December"]

LOC = readFile("location.txt")
#print(LOC)

TIME = readFile("time.txt")
#print(TIME)

OCC = readFile("occupation1.txt")


LOCPREP = readFile("locationPrep.txt")

out = open("response_file.txt",'w')
for i in range(1,len(data)):
    sent = []
    #print i
    #story.append(data[i]+".story")
    #questions.append(data[i]+".questions")
    storytxt = open(os.path.join(path,data[i].strip("\n").strip(".story")+".story"))
    #storytxt = open(path + "/"+data[i].strip("\n")+".story")
    questionstxt = open(os.path.join(path,data[i].strip("\n").strip(".story")+".questions"))
    #storytxt = open(path + "/"+data[i].strip("\n")+".story")
    #questionstxt = open(path + "/"+data[i].strip("\n")+".questions")
    qt =  questionstxt.readlines()
    st = storytxt.readlines()

    # populate the story dictionary

    story = {
        "HEADLINE" : None,
        "DATE" : None,
        "STORYID" : None,
        "TEXT" : None
    }
    flag = 1
    para = ""
    for line in st:
        if(flag ==1 and "HEADLINE" in line) :
            hd = line.split(":")[1]
            story["HEADLINE"]  = hd.strip("\n")
            flag = 1
        elif(flag == 1 and "DATE" in line) :
            dt = line.split(":")[1]
            story["DATE"] = dt.strip("\n")
        elif(flag == 1 and "STORYID" in line) :
            stid = line.split(":")[1]
            story["STORYID"] = stid.strip("\n")
            flag = 0
        elif(flag == 0 and "TEXT" in line):
            flag = 2

        elif(flag == 2):
            para = para+ line.replace("\n"," ")


    sent = sent_tokenize(para)
    story["TEXT"] = sent


    flag = 1;
    for line in qt:
        if("QuestionID" in line):
            qid = line.split(":")[1].strip("\n")
            flag =1
        elif("Question" in line):
            qs = line.split(":")[1].strip("\n")
        elif("Difficulty") in line:
            df = line.split(":")[1].strip("\n")
            flag = 0;
        if flag ==0:
            # populate the question dictionary
            question = {
                "QuestionID" : qid,
                "Question" : qs,
                "Difficulty" : df
            }
            flag = 1

            qSent = question["Question"]
            stop = stopwords.words('english')
            qSentSplit = word_tokenize(qSent)
            punct = list(string.punctuation) + ["''","...","``",'""']
            punct.remove("$")
            qNoStop = []
            for i in range(len(qSentSplit)):
               # if qSentSplit[i] not in stop:
                 if qSentSplit[i] not in punct:
                    qNoStop.append(qSentSplit[i])
            Score = []
            dateLineScore = 0
            #print range(len(sent))
            for i in range(len(sent)):
                #print(sent)
                sentSplit = word_tokenize(sent[i])
                sentNoStop = []
                for j in range(len(sentSplit)):
                    if sentSplit[j] not in stop:
                        if sentSplit[j] not in punct:
                            sentNoStop.append(sentSplit[j])

                score = WordMatch(qNoStop, sentNoStop)
                sc = pronounRule(qSentSplit,sentSplit,word_tokenize(sent[i-1]))
                score = score + sc
                who = ["who", "whom","whose"]
                if(contains(who,qSent.lower())):
                    # Do who rules
                    #print "who"
                    sc = whoRules(qSentSplit, sentSplit)
                    score = score + sc

                elif("how" in qSent.lower()):
                    #How
                    sc = howRules(qSentSplit, sentSplit)
                    score = score + sc

                elif("what" in qSent.lower()):
                    # Do what rules
                    #print "what"
                    sc = whatRules(qSentSplit, sentSplit)
                    score = score + sc

                elif("when" in qSent.lower()):
                    # Do when rules
                    #print "when"
                    sc = whenRules(qSentSplit, sentSplit)
                    score = sc
                    sc2 = datelineRule(qSentSplit)
                    dateLineScore = dateLineScore + sc2

                elif("where" in qSent.lower()):
                    # Do where rules
                    sc = whereRules(qSentSplit, sentSplit)
                    score = score + sc

                    sc2 = datelineRule(qSentSplit)
                    dateLineScore = dateLineScore + sc2

                    #print "where"


                Score.append(score)
            if("why" in qSent.lower()):
                m = max(Score)
                best = [i for i,j in enumerate(Score) if j == m]
                sc = 0
                for k in range(0,len(sent)):
                    if k in best:
                        sc = sc + clue
                    if k+1 in best:
                        sc = sc + clue
                    if k-1 in best:
                        sc = sc + good_clue
                    if contains(sent[k].split(),["want"]):
                        sc = sc + good_clue
                    if contains(sent[k].split(),["because", "due to"]):
                        sc = sc + 10
                        #print sent[k]
                        #print qSent
                    Score[k] = Score[k] + sc

            #index, value = max(enumerate(Score), key=operator.itemgetter(1))

            m = max(Score)
            best = [i for i,j in enumerate(Score) if j == m]
            #print("QuestionID: " + question["QuestionID"])
            out.write("QuestionID: " + question["QuestionID"]+"\n")
            #print("Question: " + question["Question"])
            #print("Answer: " + sent[best[0]])

            sentSplit = word_tokenize(sent[best[0]])
            sentWithoutStop = []
            for i in range(len(sentSplit)):
                #if sentSplit[i].lower() not in stop:
                #    if sentSplit[i] not in punct:
                if sentSplit[i] not in qSentSplit:
                    sentWithoutStop.append(sentSplit[i])

            abc = []
            list1 = ["first","last","since","ago"]
            list2 = ["start", "begin"]
            list3 = ["start", "begin", "since", "year"]
            abc = sentWithoutStop
            sentWithoutStop = []
            if ("what time" in qSent.lower()):
                if contains(abc,timelist):
                    sentWithoutStop = set(abc).intersection(timelist)
                else:
                    sentWithoutStop =abc
            if "when" in qSent.lower():
                if contains(abc,TIME):
                    sentWithoutStop = set(abc).intersection(TIME)
                    print(sentWithoutStop)
                if contains(qSentSplit,["the last"]) and contains(abc,list1):
                    sentWithoutStop = set(abc).intersection(list1)
                if contains(qSentSplit,list2) and contains(abc,list3):
                    sentWithoutStop = set(abc).intersection(list3)
                else:
                    sentWithoutStop =abc
            elif "where" in qSent.lower():
                if contains(abc, LOCPREP) and contains(abc, LOC):
                    sentWithoutStop = abc
                    if set(abc).intersection(LOC) != None:
                        sentWithoutStop = set(abc).intersection(LOC)
                elif contains(abc, LOC):
                    sentWithoutStop = abc
                    if set(abc).intersection(LOC) != None:
                        sentWithoutStop = set(abc).intersection(LOC)
                else:
                    sentWithoutStop =abc
            else:
                sentWithoutStop = abc


            #print("Answer: " + ' '.join(sentWithoutStop) )
            #out.write("Answer: " + ' '.join(sentWithoutStop)+"\n")
            out.write("Answer: " + ' '.join(sentWithoutStop)+"\n")
            print()
            out.write("\n")
            #print(Score)

out.close()