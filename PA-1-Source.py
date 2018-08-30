import sys
import os
import random
import time
import csv

def main(resultDir='results'):
##  Put all output files in resultDir so the user doesn't have to hunt
##  for them. If none is given, use a folder called "results" in the
##  current working directory. If resultDir doesn't exist, create it.
##  If it exists but isn't empty, do a sanity check.
    if not os.path.exists(resultDir):
        os.mkdir(resultDir)
    elif not os.path.isdir(resultDir):
        print('Error: "{}" is not a directory.'.format(resultDir), file=sys.stderr)
        sys.exit(1)
    elif os.listdir(resultDir):
        print('Warning: "{}" is not empty.'.format(resultDir))
        response = input("Continue? (y/n) ").strip().lower()
        if response != 'y':
            sys.exit()
    ##  As long as paths are RELATIVE, all files wind up in resultDir.
    os.chdir(resultDir)

    ## Random integer pairs are in a 2D array ([numOne, numTwo])
    pairs = generatePairs(-10000, 10000)
    
    #gcdsBF, timesBF = calculateBruteForce(pairs)
    #generateResults('Brute_Force_Results.csv', pairs, gcdsBF, timesBF, 
    #    ('Number One', 'Number Two', 'Their GCD', 'Time Spent (Milliseconds)'))
    #generateStatistics(gcdsBF, timesBF)
    
    gcdsEuclid, timesEuclid = calculateEuclid(pairs)
    generateResults('Original_Euclid_Results.csv', pairs, gcdsEuclid, timesEuclid,
        ('Number One', 'Number Two', 'Their GCD', 'Time Spent (Milliseconds)'))
    #generateStatistics(gcdsEuclid, timesEuclid)
    
    #gcdsImproved, timesImproved = calculateImproved(pairs)
    #generateResults('Improved_Euclid_Results.csv', pairs, gcdsImproved, timesImproved,
    #    ('Number One', 'Number Two', 'Their GCD', 'Time Spent (Milliseconds)'))
    #generateStatistics(gcdsImproved, timesImproved)

    #generateConclusion(timesBF, timesEuclid, timesImproved)
    
## Generate 100 pairs of random integers
def generatePairs(rangeMin, rangeMax):
    numOne = random.sample(range(rangeMin, rangeMax), 100)
    numTwo = random.sample(range(rangeMin, rangeMax), 100)
    return [numOne, numTwo]

## Calculate the GCD of all pairs using the Brute Force Algorithm
#def calculateBruteForce(pairs):

## Calculate the GCD of all pairs using Euclid's Algorithm
def calculateEuclid(pairs):
    gcds = []
    times = []
    
    for x in range(100):
        a = abs(pairs[0][x])
        b = abs(pairs[1][x])
        startTime = time.time()
        
        if a == 0:
            gcds.append(b)
            print("The GCD of ", pairs[0][x], " and ", pairs[1][x],  "is ",  b)
        elif b == 0:
            gcds.append(a)
            print("The GCD of ", pairs[0][x], " and ", pairs[1][x],  "is ",  a)
        elif a == 1:
            gcds.append(a)
            print("The GCD of ", pairs[0][x], " and ", pairs[1][x],  "is ",  a)
        elif b == 1:
            gcds.append(b)
            print("The GCD of ", pairs[0][x], " and ", pairs[1][x],  "is ",  b)
        else:
            y = max(a, b)
            z = min(a, b)
            remainder = None
            
            while remainder != 0:
                remainder = y % z
                y = z
                z = remainder
                
            gcds.append(y)
            print("The GCD of ", pairs[0][x], " and ", pairs[1][x],  "is ",  y)

        elapsedTime = (time.time() - startTime) * 1000
        times.append(elapsedTime)

    return gcds, times

## Calculate the GCD of all pairs using Euclid's Algorithm (Improved)
#def calculateImproved(pairs):

## Generate an Excel spreadsheet for each algorithm with the following information:
## Number One, Number Two, Their GCD, Time Spent (Milliseconds)
def generateResults(outpath, pairs, gcds, times, headers=()):
    with open(outpath, mode="wt", encoding="utf-8", newline='') as outfile:
        writer = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if headers:
            writer.writerow(headers)

        index = 0
        for a, b, gcd, time in zip(pairs[0], pairs[1], gcds, times):
            writer.writerow((a, b, gcd, time))
            index += 1

## Generate an Excel spreadsheet for each algorithm with the following information:
## Maximum Time, Minimum Time, Average Time, Median Time
#def generateStatistics(gcds, times):

## Determine how the algorithms performed against each other and save results to Conclusions.txt
def generateConclusion(timesBF, timesEuclid, timesImproved):
    output = ""
    
    ## Compare Euclid's Algorithm with the Brute Force Algorithm
    count = 0
    savedTime = 0
    
    for x in range(100):
        if timesEuclid[x] < timesBF[x]:
            savedTime += (timesBF[x] - timesEuclid[x])
            count += 1

    avgSavedTime = savedTime/count
    output += "Out of 100 pairs of integers, the original version of Euclid "
    output += "outperformed brute-force in %s pairs; and the average " % count
    output += "saved time for these %s pairs of integers was %s " % (count,avgSavedTime)
    output += "milliseconds.\n"
        
    
    ## Compare Euclid's Algorithm (Improved) with the Brute Force Algorithm
    count = 0
    savedTime = 0

    for x in range(100):
        if timesImproved[x] < timesBF[x]:
            savedTime += (timesBF[x] - timesImproved[x])
            count += 1

    avgSavedTime = savedTime/count
    output += "Out of 100 pairs of integers, the second version of Euclid "
    output += "outperformed brute-force in %s pairs; and the average " % count
    output += "saved time for these %s pairs of integers was %s " % (count,avgSavedTime)
    output += "milliseconds.\n"

    ## Compare Euclid's Algorithm (Improved) with Euclid's Algorithm
    count = 0
    savedTime = 0

    for x in range(100):
        if timesImproved[x] < timesEuclid[x]:
            savedTime += (timesEuclid[x] - timesImproved[x])
            count += 1

    avgSavedTime = savedTime/count
    output += "Out of 100 pairs of integers, the second version of Euclid "
    output += "outperformed the original one in %s pairs; and the average " % count
    output += "saved time for these %s pairs of integers was %s " % (count,avgSavedTime)
    output += "milliseconds."

    ## Write results to file
    with open("Conclusions.txt", mode="wt", encoding="utf-8") as outfile:
        outfile.write(output)
        print("Conclusions.txt successfully created.")

if __name__ == "__main__":
##  Treat the first command-line argument as the destination for generated files.
    try:
        resultDir = sys.argv[1]
        main(resultDir)
    except IndexError:
        main()
