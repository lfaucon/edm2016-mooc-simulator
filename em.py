import json
import random
import math

# configuration of the algorithm
config = {
    "numberOfClasses": 2,
    "numberOfEventTypes": 5,
    "numberOfIterations": 10,
    "maxNumberOfRepetition": 1000
}

# Reading the data
with open('data/train_data.json','r') as data:
    events = json.loads(data.read().replace('\n',''))

# precompute the table of log(k!) for the poisson probability distribution
logTable = [0 for k in range(config["maxNumberOfRepetition"])]
for k in range(1,len(logTable)):
    logTable[k] = logTable[k-1] + math.log(k)

# For one student, computes the repartition probability in the different classes
def getRepartition(eventList, models):
    logProbability = [0. for _ in range(len(models))]
    for i in range(len(models)):
        for e in range(1,len(eventList)):
            cur = eventList[e]
            prev = eventList[e-1] 
            logProbability[i] += math.log(models[i][prev[1]-1][cur[1]-1]+1e-10)
            lamb = 1e-10 + models[i][cur[1]-1][cur[1]-1]
            logProbability[i] += (cur[2]-1) * math.log(lamb-1) - lamb+1 - logTable[cur[2]-1];
    # computes probabilities from the log_probabilities
    m = max(logProbability)
    p = [math.exp(p-m) for p in logProbability]
    s = sum(p)
    return [x/s for x in p]

# From the repartition of the students, computes the model of index i
# a model is a 5x5 matrix:
# - on the diagonal is the average number of repetition of each activity
# - on cell i,j is the probability of doing activity j after activity i
def getModel(events,students,i):
    model = [[0. for _ in range(config["numberOfEventTypes"])] for _ in range(config["numberOfEventTypes"])]
    for key in events.keys():
        ski = students[key][i]
        eventList=events[key]
        for e in range(1,len(eventList)):
            cur = eventList[e]
            prev = eventList[e-1] 
            model[prev[1]-1][cur[1]-1] += ski
            model[cur[1]-1][cur[1]-1] += (cur[2]-1)*ski
    s = [sum(line) for line in model]
    out = [
        [count/(s[eventType]-model[eventType][eventType] + 1e-10) for count in model[eventType]] 
        for eventType in range(config["numberOfEventTypes"])
    ]
    for eventType in range(config["numberOfEventTypes"]):
        out[eventType][eventType] = (s[eventType]+1e-10)/(s[eventType]-model[eventType][eventType]+1e-10)
    return out

# Randomly initialise models
models=[[
    [random.random() for _ in range(config["numberOfEventTypes"])] 
    for _ in range(config["numberOfEventTypes"])
] for _ in range(config['numberOfClasses']) ]

for model in range(config['numberOfClasses']):
    for eventType in range(config["numberOfEventTypes"]):
        models[model][eventType][eventType] += 1.

# Initialise the students repartition
studentsRepartition = {}

# Core of the algorithm
print "Running iterations. . ."
for iteration in range(config['numberOfIterations']):
    for key in events.keys():
        studentsRepartition[key] = getRepartition(events[key],models)
    models = [[] for _ in range(config['numberOfClasses'])]
    for i in range(len(models)):
        models[i] = getModel(events,studentsRepartition,i)

# Prints the student repartition
for student in studentsRepartition.keys():
    print student,studentsRepartition[student]

# Prints the computed models
for model in models:
    print "========================"
    for line in model:
        print line

output = open('data/em_markov_models_'+str(config['numberOfClasses'])+'.json','w')
output.write(json.dumps(models))
output.close()

print 'Job done !'
