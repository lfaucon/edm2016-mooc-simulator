# edm2016-mooc-simulator

This repository contains a custom implementation of the EM algorithm applied on a sample dataset in order to fit students behavior with semi-markov models

## Data format

The data should be in a json format as follow:
```
{
	"STUDENT_ID": [[timestamp,activityType,repetition],...],
	...
}
```
Each student must have a unique ID, and the json object contains the list of tuples describing the series of activity of a student.

## Format of the semi-markov model

The semi-markov model in our implementation is represented by a 5x5 matrix
- On cell (i,i) is the average number of repetition of activity i 
- Otherwise on cell (i,j) is the transition probability from i to j

