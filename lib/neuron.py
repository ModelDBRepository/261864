import numpy as np

class iaf:
    def __init__(self):
        self.theta = 1.01;        
        self.rcounter = 0; 
        self.rperiod = 20; 
        self.w = {}; 
        self.spiketimes= [];        
        self.wmax = 0.25;     
        self.wmin = 0.0;
                
    def learn(self, w_index, w_inc):
        if w_index in self.w.keys():
            self.w[w_index] = np.clip(self.w[w_index] + w_inc, self.wmin, self.wmax)

    def findPSPsum(self, preSpikes):
        pspSum = 0; 
        for i in preSpikes:
            if i in self.w.keys():
                pspSum += self.w[i]; 
        return pspSum
        
    def update(self, ax, timestamp):
        V = 0; 
        if self.rcounter == 0: 
            V = self.findPSPsum(preSpikes=ax); 
        else: self.rcounter = self.rcounter - 1; 
        if V >= self.theta:
            self.spiketimes.append(timestamp)
            self.rcounter = self.rperiod
            return 1; 
        else:
            return 0; 
        
class integrator:
    def __init__(self):
        self.V = 0;        
        self.spikeTheta = 20     
        self.w = {}             
        self.spiketimes = []                
        self.monitorFlag = 0;
        self.vMonitor = [0];
        self.rperiod = 20; 
        self.rcounter = 0; 

    def update(self, timestamp, Vin = 0):
        if self.rcounter == 0: 
            self.V = self.V + Vin; 
            if self.monitorFlag == 1: 
                self.vMonitor.append(self.V);
            if self.V >= self.spikeTheta:
                self.spiketimes.append(timestamp);
                self.V = 0; 
                self.rcounter = self.rperiod; 
        else: 
            self.rcounter = self.rcounter - 1; 