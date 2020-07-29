import csv
import pickle
import random
import os

def loadFile(fileName, sampleTimes):
    lines = []; 
    rf = open(fileName, 'r');
    data = csv.reader(rf, delimiter='\t'); 
    for i in data:
        lines.append(i)
    odor_raw = []; 
    sampleID = 0; 
    nSamples = len(sampleTimes); 
    for i in range(0, len(lines)):
        #print lines[i][0]; 
        time = int(lines[i][0])/1000.0;
        if time > sampleTimes[sampleID]:           
            odor_raw.append([]);
            for j in range(12, 92):         #gas sensor data is stored at these locations
                if lines[i][j]!='1':
                    odor_raw[sampleID].append(int(lines[i][j]));
            sampleID+=1;
            if(sampleID==nSamples): 
                break
    rf.close(); 
    return odor_raw; 

def loadTestData(filename, dataList, labelList, labelID):
    #testSampleTimes = [100]; 
    #testSampleTimes = range(50, 200, 5)
    testSampleTimes = range(50, 100, 5)
    testSampleTimes.sort(); 
    data = loadFile(filename, testSampleTimes);
    for dataID in data: 
        dataList.append(dataID); 
        labelList.append(labelID);
    #return dataList, labelList

trainingFiles = ["201106050941_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Toluene_200ppm_p7",
                 "201105101707_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Benzene_200ppm_p7",
                 "201102200930_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Methane_1000ppm_p7",
                 "201012081822_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_CO_1000ppm_p7",
                 "201106080842_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Ammonia_10000ppm_p7",
                 "201107161019_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Acetone_2500ppm_p7", 
                 "201107172155_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Acetaldehyde_500ppm_p7", 
                 "201109060942_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Methanol_200ppm_p7", 
                 "201109071738_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Butanol_100ppm_p7", 
                 "201109142039_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Ethylene_500ppm_p7"]

raw_data = {}; 
plumeData = []; 
plumeDataLabels = []; 

currentOdorID = -1;
path = './'; 
for filename in trainingFiles[0:1]:
    currentOdorID += 1;
    loadTestData(path+filename, plumeData, plumeDataLabels, currentOdorID);
                     
outputFile = 'plumeData.pi'; 
pickleOut = open(outputFile, 'w'); 
pickle.dump(plumeData, pickleOut);
pickle.dump(plumeDataLabels, pickleOut);
pickleOut.close(); 