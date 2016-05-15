import json
import random

config = {
	"testProportion":0.
}

# Reading the data from the file in ./data/data_sample.json
with open('data/data_sample.json','r') as data:
	events = json.loads(data.read().replace('\n',''))

# Splitting the data
testData={}
trainData={}
for key in events:
    if random.random() < config["testProportion"]:
        testData[key] = events[key]
    else:
        trainData[key] = events[key]

# Writting the data in files
test_data = open('data/test_data.json','w')
test_data.write(json.dumps(testData))
test_data.close()

train_data = open('data/train_data.json','w')
train_data.write(json.dumps(trainData))
train_data.close()
