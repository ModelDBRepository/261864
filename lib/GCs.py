import neuron
import numpy as np
np.random.seed(1); 

class GC():
    def __init__(self, nMCs, idx):   
        self.id = idx;
        self.GC = neuron.iaf();
        self.GCselectivity = 4;
        self.learningRate = 0.005;
        self.MC_GC_wInit = 0.2;     #for one-shot
        self.GC.wmax = 0.25; 
        self.GC.theta = self.MC_GC_wInit*self.GCselectivity + 0.1;
        self.MC_delw_pot = self.learningRate*self.MC_GC_wInit;      #increment of MC->GC weight
        self.MC_delw_dep = self.MC_delw_pot                         #decrement of MC->GC weight
        self.GC.w = {}                                              #weight of MC on GC
        self.nSisterMCs = 4; 
        self.plastic = 0; 
        self.MC_delay = {}
        self.MC_delivery_time = {}

    def reset(self):
        for i in self.MC_delivery_time.keys():
            del self.MC_delivery_time[i];
            
    def differentiate(self): 
        self.plastic = 0;  
        for i in self.GC.w.keys():
            if self.GC.w[i] <= self.MC_GC_wInit: 
                del self.GC.w[i];
        
    def update(self, spiking_MCs, timestamp, learnFlag, AChState):
        presynaptic_spikes = self.update_MC_spike_delivery(spiking_MCs);     
        #Effects of acetylcholine
        self.GC.theta = self.GC.theta - (AChState*6)
        #Update voltage
        if(learnFlag==0): 
            spikeFlag = self.GC.update(presynaptic_spikes, timestamp); 
        else:
            if(self.plastic==1):
                spikeFlag = self.GC.update(presynaptic_spikes, timestamp); 
            else:
                spikeFlag = self.GC.update([], timestamp);
        #Plasticity
        if learnFlag == 1 and self.plastic==1: 
            if spikeFlag==1: self.update_weights(presynaptic_spikes);
        return spikeFlag; 
        
    def update_MC_spike_delivery(self, spiking_MCs):
        out = []
        for i in self.MC_delivery_time.keys():
            if self.MC_delivery_time[i] == 0:
                out.append(i)
                del self.MC_delivery_time[i]
            else:
                self.MC_delivery_time[i] = self.MC_delivery_time[i] - 1
        for i in spiking_MCs:
            if i in self.MC_delay.keys():
                self.MC_delivery_time[i] = self.MC_delay[i];
        return out

    def update_weights(self, presynapticSpikes): 
        for i in self.GC.w.keys():
            if i in presynapticSpikes:
                self.GC.learn(i, self.MC_delw_pot);
            else:
                self.GC.learn(i, -self.MC_delw_dep);
                
class GClayer():
    def __init__(self, nGCs, nMCs, nNeurogenesis):
        self.GCs = []
        self.nCols = nMCs
        self.MC_GC_w_init = 0.2; 
        self.nSisterMCs = 4;
        self.matureGCcnt = 0;
        self.nNeurogenesis = nNeurogenesis; 
        self.plasticGCids = range(0, self.nNeurogenesis);
        self.nActiveGCs = len(self.plasticGCids); 
        for i in range(0, nGCs):        
            self.GCs.append(GC(nMCs, idx=i)); 
        for i in self.plasticGCids:
            self.GCs[i].plastic = 1;
    
    def reset(self):
        for i in range(0, len(self.GCs)):
            self.GCs[i].reset(); 
                 
    def invokeNeurogenesis(self):
        #Differentiate older GCs
        for i in self.plasticGCids:
            self.GCs[i].differentiate();
            self.matureGCcnt += 1; 
        self.plasticGCids = []; 
        #Introduce new naive GCs
        if(self.matureGCcnt < len(self.GCs)):
            for i in range(self.matureGCcnt, self.matureGCcnt+self.nNeurogenesis):
                self.GCs[i].plastic = 1;
                self.nActiveGCs += 1; 
                self.plasticGCids.append(i);
        
    def del_GC_conns(self, GC_index):
        self.GCs[GC_index].GC.w.clear()
        self.GCs[GC_index].MC_delay.clear()

    def connect_GC(self, GC_index, nMCs, GC_type=1): 
        MC_GC_connP = 0.2;
        delays = [16, 17, 18, 19];
        self.nSisterMCs = len(delays); 
        for i in range(0, nMCs):
            for j in range(0, self.nSisterMCs): 
                #if(random.random()<MC_GC_connP):
                if(np.random.random()<MC_GC_connP):
                    self.GCs[GC_index].GC.w[(i, j)] = self.GCs[GC_index].MC_GC_wInit;  
                    self.GCs[GC_index].MC_delay[(i, j)] = delays[j]; 
                                   
    def connect_all(self, nMCs):
        for i in range(0, len(self.GCs)):
            self.connect_GC(i, nMCs);

    def update(self, spiking_MCs, timestamp, learnFlag, AChLevel=0):
        spikingGCs = [];
        spikingSisterMCs = []; 
        for i in spiking_MCs:
            for j in range(0, self.nSisterMCs):
                spikingSisterMCs.append((i, j)); 
        for i in range(0, self.nActiveGCs): 
            s=0; 
            spikeFlag = self.GCs[i].update \
            (spikingSisterMCs, timestamp, learnFlag, AChState=s); 
            if spikeFlag == 1: 
                spikingGCs.append(i);
        return spikingGCs;     