from lib import epl 
from lib import OSN
from lib import readout
from lib import plots
import numpy as np
import pickle 

#Load Data
rf = open('./data/plumePlusImpulseNoiseData.pi', 'r');
trainingOdors = np.array(pickle.load(rf));
testOdors = np.array(pickle.load(rf));
testOdorLabels = pickle.load(rf); 
nNoise = pickle.load(rf); 
nSniffsPerPlume = pickle.load(rf);
rf.close();
trainingOdors = trainingOdors;
testOdors = testOdors; 
nTrainSamplesPerOdor = 1; 
nOdors = len(trainingOdors); 

#Network initialization
nMCs = len(trainingOdors[0]); 
GCsPerNeurogenesis = 5; 
nGCs = nMCs*GCsPerNeurogenesis*nOdors;     #every MC has 5 GCs per odor  
epl = epl.EPL(nMCs, nGCs, GCsPerNeurogenesis); 

#Sniff
def sniff(odor, learn_flag=0, nGammaPerOdor=5, gPeriod=40):
    sensorInput = OSN.OSN_encoding(odor); 
    for j in range(0, nGammaPerOdor):
        for k in range(0, gPeriod): 
            epl.update(sensorInput, learn_flag=learn_flag);
            pass; 
    epl.reset();

#Training
for i in range(0, len(trainingOdors)):
    sniff(trainingOdors[i], learn_flag=1);
    epl.GClayer.invokeNeurogenesis();
    sniff(trainingOdors[i], learn_flag=0);

#Testing
for i in range(0, len(testOdors)):
    sniff(testOdors[i], learn_flag=0); 

#Readout
sMatrix = readout.readoutPlume(epl.gammaCode, nOdors, testOdorLabels, nSniffsPerPlume)    

#Plot
plots.plotFigure5def(epl.gammaSpikes, sMatrix, nSniffsPerPlume); 

