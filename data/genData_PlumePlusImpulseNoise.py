#use python3 to run below

import pickle
import numpy as np
import random
import copy
import csv

random.seed(10); 

def loadFile(fileName):
    lines = []
    data = csv.reader(open("./" + fileName, 'r'), delimiter='\t')
    for i in data:
        lines.append(i)
    odor_raw = []; 
    for i in range(0, len(lines)): 
        time = int(lines[i][0])/1000.0;
        if time > 100:          #load the data recorded at time 100s 
            #odor_raw.append(time);
            for j in range(12, 92):         #gas sensor data is stored at these locations
                if lines[i][j]!='1':
                    odor_raw.append(int(lines[i][j]));
            break
            #odor_raw[k].append( round( float(lines[i][j]) *2, 6)/2 )		
    return odor_raw, time; 

def loadTrainingData(): 
    CO_filename = "201012081822_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_CO_1000ppm_p7"; 
    CO_raw, CO_time = loadFile(CO_filename);

    Methane_filename = "201102200930_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Methane_1000ppm_p7"; 
    Methane_raw, Methane_time = loadFile(Methane_filename); 
    
    Benzene_filename = "201105101707_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Benzene_200ppm_p7"; 
    Benzene_raw, Benzene_time = loadFile(Benzene_filename); 
                          
    Toluene_filename = "201106050941_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Toluene_200ppm_p7"; 
    Toluene_raw, Toluene_time = loadFile(Toluene_filename); 

    Ammonia_filename = "201106080842_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Ammonia_10000ppm_p7";
    Ammonia_raw, Ammonia_time = loadFile(Ammonia_filename); 
                          
    Acetone_filename = "201107161019_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Acetone_2500ppm_p7"; 
    Acetone_raw, Acetone_time = loadFile(Acetone_filename); 
                          
    Acetaldehyde_filename = "201107172155_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Acetaldehyde_500ppm_p7"; 
    Acetaldehyde_raw, Acetaldehyde_time = loadFile(Acetaldehyde_filename); 

    Methanol_filename = "201109060942_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Methanol_200ppm_p7"; 
    Methanol_raw, Methanol_time = loadFile(Methanol_filename); 
                        
    Butanol_filename = "201109071738_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Butanol_100ppm_p7"; 
    Butanol_raw, Butanol_time = loadFile(Butanol_filename); 

    Ethylene_filename = "201109142039_board_setPoint_500V_fan_setPoint_060_mfc_setPoint_Ethylene_500ppm_p7";
    Ethylene_raw, Ethylene_time = loadFile(Ethylene_filename); 

    odors_raw = [Toluene_raw, Benzene_raw, Methane_raw, CO_raw, Ammonia_raw, Acetone_raw, Acetaldehyde_raw, Methanol_raw, Butanol_raw, Ethylene_raw]; 
                
    return odors_raw; 

def findDynamicRange(odors_raw):
    nSensors = len(odors_raw[0]);
    dRange = [[0,0]]*nSensors;          #(min, max) for each sensor
    for i in range(0, len(odors_raw)):
        for j in range(0, nSensors):  #+1 because 0 is timestamp 
            if(i==0):
                dRange[j] = [odors_raw[i][j], odors_raw[i][j]];
            elif odors_raw[i][j] < dRange[j][0]:     #new < min
                dRange[j][0] = odors_raw[i][j]; 
            elif odors_raw[i][j] > dRange[j][1]:     #new > max
                dRange[j][1] = odors_raw[i][j]; 
    return dRange; 

def findBinSpacing(odors_raw, nBins):
    dRange = findDynamicRange(odors_raw);
    binSpacing = [];
    for i in dRange:
        interval = i[1]-i[0]; 
        binSpacing.append(round(interval/float(nBins-1), 4));
    return dRange, binSpacing; 

def binData(odorMainUnbinned, binSpacing, dRange, nBins):
    odorMain = []; 
    for i in range(0, len(odorMainUnbinned)):
        odorMain.append([]); 
        for j in range(0, len(dRange)):
            temp = (odorMainUnbinned[i][j] - dRange[j][0])/binSpacing[j]; 
            #temp = np.clip(int(round(temp)), 0, nBins-1)
            temp = np.clip(int(round(temp)), 1, nBins-1)
            if nBins == 32: 
                temp = np.clip(temp-16, 0, 15);
                pass;
            if nBins == 20: 
                temp = np.clip(temp-4, 0, 15);
                pass;
            odorMain[i].append(temp); 
    return odorMain; 

def sparsifySingle(odorDense):
    top = [0]*72;           #list of most active sensors
    odorTemp = copy.deepcopy(odorDense); 
    cutoff = 36;        #number of sensors that make the top list
    for i in range(0, cutoff):
        m = max(odorTemp);
        index1 = odorTemp.index(m); 
        odorTemp[index1] = 0;
        top[index1] = m; 
    return top; 

def sparsifyOdors(odorsDense):
    odorsSparsified = []; 
    for i in odorsDense:
        s = sparsifySingle(i); 
        odorsSparsified.append(s);
    return odorsSparsified

def AddOcclusion(
data = [[]],
odorLabels = [],   
pList = [0.5]    #mean of bernoulli process 
):
    noisy_data = []; 
    l=-1;
    noisy_data_labels = []; 
    for noiseLevel in pList: 
        for i in range(0, len(data)):
            ndim = len(data[i]); 
            noisy_data.append([]);
            noisy_data_labels.append(odorLabels[i]); 
            l+=1;
            affected_ids = random.sample(range(ndim), int(noiseLevel*ndim))
            for k in range(0, ndim):
                if k in affected_ids:
                    noise_act = random.randint(0, 15);       #random destructive interference
                    noisy_data[l].append(noise_act)
                else:
                    noisy_data[l].append(data[i][k])
    return noisy_data, noisy_data_labels
 
#%%
    
rf = open('./plumeData.pi', 'r')
plumeDataRaw = pickle.load(rf); 
plumeDataLabelsRaw = pickle.load(rf);
rf.close();
trainingDataRaw = loadTrainingData();  

nBins = 16; 
dRange, binSpacing = findBinSpacing(trainingDataRaw, nBins); 
trainingOdorsDense = binData(trainingDataRaw, binSpacing, dRange, nBins); 
trainingOdors = sparsifyOdors(trainingOdorsDense);

plumeSamplesDense = binData(plumeDataRaw, binSpacing, dRange, nBins); 
plumeSamplesLabels = plumeDataLabelsRaw;  
plumeSamples = sparsifyOdors(plumeSamplesDense);

noiseLevels = [0.4];
nNoise = len(noiseLevels); 
testOdorsImpulseNoise, testOdorsImpulseNoiseLabels = AddOcclusion(plumeSamples, plumeSamplesLabels, pList=noiseLevels);

#%%
nsensors = len(trainingOdors[0]); 
nOdors = len(trainingOdors);          
#trainingOdors = trainingOdors[0:10]; 
trainingOdors = trainingOdors[0:1]; 
nSniffsPerPlume = len(plumeSamples)/len(trainingOdors);        

wf = open("./plumePlusImpulseNoiseData.pi", 'wb')
pickle.dump(trainingOdors, wf); 
pickle.dump(testOdorsImpulseNoise, wf);
pickle.dump(testOdorsImpulseNoiseLabels, wf); 
pickle.dump(nNoise, wf); 
pickle.dump(nSniffsPerPlume, wf);
wf.close()               
