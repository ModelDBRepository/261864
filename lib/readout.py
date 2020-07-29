import numpy as np

def jaccardSimilarity(l1 = [], l2 =[]):
    list1 = [];
    list2 = [];
    for i in range(0, len(l1)):
        list1.append((i, l1[i]));
        list2.append((i, l2[i]));
    set1 = set(list1);
    set2 = set(list2);
    intersectionSize = len(set.intersection(set1, set2));
    unionSize = len(set.union(set1, set2));
    return intersectionSize/float(unionSize);

def computeSimilarity(l1, l2):
    return jaccardSimilarity(l1, l2);

def findLearnedGammaCode(gammaCode, nOdors, nGammaPerLearning):
    learnedGammaCode = [];  
    for i in range(1, nOdors+1):
        labelGammaID = i*nGammaPerLearning + 5*i - 1; 
        learnedGammaCode.append(gammaCode[labelGammaID]); 
    return learnedGammaCode; 

def findSImatrixGamma(gammaCode, learnedGammaCode, nOdors, testStartID):
    SImatrixGamma = []; 
    k = 0; 
    for i in range(testStartID, len(gammaCode)):
        SImatrixGamma.append([]); 
        for j in range(0, nOdors): 
            similarity = computeSimilarity(gammaCode[i], learnedGammaCode[j]);
            SImatrixGamma[k].append(round(similarity, 2));
        #print(SImatrixGamma[k]); 
        k+=1; 
    return SImatrixGamma; 
        
def findPrediction(SImatrixGamma, nTotalTests, nGammaPerOdor=5): 
    pValues = []; 
    pThreshold = 0.8;
    #pThreshold = 0.1; 
    for i in range(0, nTotalTests):
        gammaID = (i+1)*nGammaPerOdor - 1; 
        lastGamma = SImatrixGamma[gammaID]; 
        maxSI = max(lastGamma);
        predictedOdor = lastGamma.index(maxSI); 
        if(maxSI >= pThreshold):
            pValues.append(predictedOdor);
        else:
            pValues.append('x'); 
    return pValues

def findPredictionPlume(pValues, nOdors, odorLabels, nSniffsPerPlume=10):
    predictionCnt = [0]*nOdors;
    currentPlumeID = 0;
    pValuesPlume = []; 
    odorLabelsPlume = []; 
    for i in range(0, len(pValues)):
        odorID = odorLabels[i]; 
        if(pValues[i]==odorID):
            predictionCnt[odorID] = predictionCnt[odorID] + 1;
        if((i+1)%nSniffsPerPlume==0): 
            currentPlumeID += 1;
            odorLabelsPlume.append(odorID); 
            if(sum(predictionCnt)!=0):
                prediction = predictionCnt.index(max(predictionCnt)); 
                pValuesPlume.append(prediction);
                predictionCnt = [0]*nOdors;
            else:
                pValuesPlume.append('x');
                predictionCnt = [0]*nOdors;
    return pValuesPlume, odorLabelsPlume; 

def computeClassification(predictions, nOdors, nTestPerOdor): 
    currentOdorID = 0; 
    odorPscore = [0]*nOdors;
    testID = 0; 
    for i in range(0, len(predictions)): 
        if(predictions[i]==currentOdorID): 
            odorPscore[currentOdorID] = odorPscore[currentOdorID] + 1; 
        testID += 1; 
        if(testID==nTestPerOdor):
            currentOdorID += 1; 
            testID = 0;
    #print(odorPscore); 
    for i in range(0, len(odorPscore)):
        odorPscore[i] = odorPscore[i]/float(nTestPerOdor);
    netP = sum(odorPscore)/float(nOdors); 
    return odorPscore, netP; 

def computeClassificationPlume(predictions, nOdors, odorLabels):  
    odorPscore = [0]*nOdors;
    odorTestCnt = [0]*nOdors; 
    correctCnt = 0;
    #Find number of correct classifications for each odor
    for i in range(0, len(predictions)): 
        odorTestCnt[odorLabels[i]] += 1; 
        if(predictions[i]==odorLabels[i]): 
            odorPscore[odorLabels[i]] = odorPscore[odorLabels[i]] + 1;
            correctCnt+=1; 
    #Find %correct for each odor
    for i in range(0, len(odorPscore)):
        odorPscore[i] = odorPscore[i]/float(odorTestCnt[i]);
    #Find net classification performance
    nTestOdors = len(odorLabels); 
    #print(correctCnt);
    #print(nTestOdors); 
    netP = correctCnt/float(nTestOdors); 
    return odorPscore, netP; 
                
def readout(gammaCode, nOdors, nTestPerOdor):
    nTrainSamplesPerOdor = 1; 
    nGammaPerLearning = nTrainSamplesPerOdor*5;
    learnedGammaCode = findLearnedGammaCode(gammaCode, nOdors, nGammaPerLearning);
    testStartID = nOdors*nGammaPerLearning + nOdors*5;     #learning + labeling 
    SImatrix = findSImatrixGamma(gammaCode, learnedGammaCode, nOdors, testStartID);
    nTotalTests = nOdors*nTestPerOdor;
    #nTotalTests = len(SImatrix)/5; 
    pValues = findPrediction(SImatrix, nTotalTests, nGammaPerOdor=5); 
    odorClassification, netClassification = computeClassification(pValues, nOdors, nTestPerOdor)
    #return learnedGammaCode, SImatrix, pValues, odorClassification, netClassification;        
    return SImatrix

def readoutPlume(gammaCode, nOdors, odorLabels, nSniffsPerPlume=10):
    nTrainSamplesPerOdor = 1; 
    nGammaPerLearning = nTrainSamplesPerOdor*5;
    learnedGammaCode = findLearnedGammaCode(gammaCode, nOdors, nGammaPerLearning);
    testStartID = nOdors*nGammaPerLearning + nOdors*5;     #learning + labeling 
    SImatrix = findSImatrixGamma(gammaCode, learnedGammaCode, nOdors, testStartID);
    nTotalTests = len(SImatrix)/5; 
    pValues = findPrediction(SImatrix, nTotalTests, nGammaPerOdor=5); 
    pValuesPlume, odorLabelsPlume = findPredictionPlume(pValues, nOdors, odorLabels, nSniffsPerPlume); 
    odorClassification, netClassification = computeClassificationPlume(pValues, nOdors, odorLabels);
    odorClassificationPlume, netClassificationPlume = computeClassificationPlume(pValuesPlume, nOdors, odorLabelsPlume);
    #return learnedGammaCode, SImatrix, pValues, pValuesPlume, odorClassification, netClassification, odorClassificationPlume, netClassificationPlume;        
    return SImatrix

def readoutNoiseScan(pValues, nOdors, nTestPerNoise, nNoise): 
    cValues = [];
    for i in range(0, nNoise):
        indexStart = i*nTestPerNoise*nOdors; 
        indexEnd = indexStart + nTestPerNoise*nOdors;
        pValuesTemp = pValues[indexStart:indexEnd];
        odorClassification, netClassification = computeClassification(pValuesTemp, nOdors, nTestPerNoise)
        cValues.append(netClassification); 
    return cValues
        
        