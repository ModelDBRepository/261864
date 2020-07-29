import neuron
import numpy as np

class MC():
    def __init__(self, ID):
        self.ID = ID; 
        self.AD = neuron.integrator();     
        self.gammaState = 0; 
        self.inhibitoryWeights = {};
        self.plasticSynapses = []; 
        self.spiketimes = [];         
        self.rperiod = 20; 
        self.rcounter = 0; 
        self.inhLearningRate = 1.0;      
        self.blockingInhibitions = {};   #keys are IDs of GC->MC synapses that are in their inhibitory states; values are counters
        self.reboundInhibitions = []; 
        self.ADspikeTime = 0; 
        self.inhReleaseTimes = {}; 
        self.ADtrigger = 0; 
        self.PSPsum = 0; 
        self.monitorFlag = 0; 
        self.wMonitor = []; 
        self.synMonitor = [0];
        self.inhMonitor = [0];
        self.stateMonitor = [0];
        self.stateMonitor2 = [0];
        
    def reset(self): 
        self.blockingInhibitions.clear(); 
        self.reboundInhibitions = []; 
        self.inhReleaseTimes.clear();
        self.PSPsum = 0;         
        
    def monitor(self):
        self.wMonitor.append(self.inhibitoryWeights.values());     
        
    def initSynapse(self, w_index):
        self.inhibitoryWeights[w_index] = 0;
        self.plasticSynapses.append(w_index); 
    
    def updateGammaState(self, learn_flag=0): 
        if self.gammaState == 1: 
            self.gammaState = 0; 
            self.AD.V = 0;
            self.ADtrigger  = 0; 
            if(learn_flag==1): 
                self.updateInhWeights();
            self.inhReleaseTimes.clear(); 
            if(learn_flag==1 and self.monitorFlag==1):
                self.monitor(); 
        else:   
            self.gammaState= 1;
            self.ADspikeTime = 0; 

    def updateInhibitoryStates(self, localGCspikes, timestamp):    
        self.reboundInhibitions = [];              
        for i in self.blockingInhibitions.keys():
            self.blockingInhibitions[i] = self.blockingInhibitions[i] - 1;
            if(self.blockingInhibitions[i]<=0):
                del self.blockingInhibitions[i];
                self.PSPsum = self.PSPsum + 1; 
                self.inhReleaseTimes[i] = timestamp;
                if(self.inhibitoryWeights[i] > 2):      #if sufficient inhibition
                    self.reboundInhibitions.append(i);
        for i in self.inhibitoryWeights.keys():
            if i in localGCspikes:
                self.blockingInhibitions[i] = self.inhibitoryWeights[i];
                self.PSPsum = self.PSPsum - 1; 
        
    def generateSpike(self, timestamp): 
        self.spiketimes.append(timestamp);  
        self.rcounter = self.rperiod; 
        return 1; 

    def update(self, sensorV, spiking_GCs, timestamp, learn_flag, gammaPulse):
        #spiking_GCs -- list of indices of GCs that spiked in the previous timestep
        if gammaPulse == 1:                                
            self.updateGammaState(learn_flag);             
        #Update GC inhibition states
        self.updateInhibitoryStates(spiking_GCs, timestamp);        
        #Update apical dendrite
        ADin = 0; 
        if self.gammaState==1: 
            ADin = sensorV;
        self.AD.update(timestamp, Vin=ADin);
        if (timestamp in self.AD.spiketimes):
            self.ADspikeTime = timestamp;
            self.ADtrigger = 1;
        #Update Soma
        spikeFlag = 0;
        if(learn_flag==0):
            sumV = self.ADtrigger + self.PSPsum + len(self.reboundInhibitions); 
        else:
            sumV = self.ADtrigger;              
        if(self.rcounter<=0):
            if(sumV>0 and self.gammaState==1):
                spikeFlag = self.generateSpike(timestamp);
        else:
            self.rcounter = self.rcounter - 1;         
        return spikeFlag; 

    def updateInhWeights(self):
        k = self.inhLearningRate; 
        for i in self.inhReleaseTimes.keys(): 
            if i in self.plasticSynapses:
                if(self.ADspikeTime!=0):     #if AD spike 
                    delw = k*(self.ADspikeTime - self.inhReleaseTimes[i]);
                else:
                    delw = 40;      
                self.inhibitoryWeights[i] = np.clip((self.inhibitoryWeights[i] + delw), 0, 40); 
            
class MClayer():
    def __init__(self, nMCs, nGCs, GCsPerNeurogenesis):
        self.MCs = [];
        GCs_per_Neurogenesis_per_MC = GCsPerNeurogenesis/nMCs;
        nNeurogenesis = nGCs/GCsPerNeurogenesis; 
        for i in range(0, nMCs):
            self.MCs.append(MC(ID=i))
            for j in range(0, nNeurogenesis):
                GCidStart = j*GCsPerNeurogenesis+i*GCs_per_Neurogenesis_per_MC; 
                GCidStop = GCidStart + GCs_per_Neurogenesis_per_MC;
                for k in range(GCidStart, GCidStop):
                    self.MCs[i].initSynapse(k);

    def reset(self):
        for i in range(0, len(self.MCs)):
            self.MCs[i].reset(); 

    def update(self, sensorV, spiking_GCs, timestamp, learn_flag, gammaPulse):
        #sensorV -- input to each MC
        #spiking_GCs -- list of spiking GCs in previous timestamp
        spikingMCs = []; 
        for i in range(0,len(self.MCs)):
            spikeFlag = self.MCs[i].update(sensorV[i], spiking_GCs, timestamp, learn_flag, gammaPulse)
            if spikeFlag == 1: 
                spikingMCs.append(i);
        return spikingMCs; 