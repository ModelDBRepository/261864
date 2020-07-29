import MCs
import GCs

class EPL():
    def __init__(self, nMCs = 10, nGCs = 20, GCsPerNeurogenesis=5, gamma_period = 40):
        self.timestamp = 0; 
        self.nMCs = nMCs
        self.nGCs = nGCs
        self.GCsPerNeurogenesis = nMCs*GCsPerNeurogenesis;       
        self.MClayer = MCs.MClayer(nMCs = nMCs, nGCs = nGCs, GCsPerNeurogenesis = self.GCsPerNeurogenesis)
        self.GClayer = GCs.GClayer(nGCs = nGCs, nMCs = nMCs, nNeurogenesis = self.GCsPerNeurogenesis)
        self.GClayer.connect_all(nMCs = nMCs)        #Connect MCs to GCs randomly
        self.MC_spike_delay = 1
        self.MC_delivery_time = {}    
        self.gp = gamma_period; 
        self.GC_go = {}; 
        self.GC_ids = {}        #stores spiking GCs of each gamma cycle
        self.gammaCode = []; 
        self.gammaSpikes = [];                            
        self.spikingGCs = []    #from previous timestep
        self.spikingMCs = []

    def reset(self):
        self.MClayer.reset();
        self.GClayer.reset();
        self.spikingGCs = []; 
        self.spikingMCs = []; 
 
    def update(self, sensorV, learn_flag, AChLevel=0):
        self.timestamp = self.timestamp + 1;
        #Recording spiking MCs
        for i in self.spikingMCs:     
            self.MC_delivery_time[i] = self.MC_spike_delay;         
        delayedMCspikes = [];         
        for i in self.MC_delivery_time.keys():
            if self.MC_delivery_time[i] > 1:
                self.MC_delivery_time[i] = self.MC_delivery_time[i] - 1; 
            else:
                del self.MC_delivery_time[i]; 
                delayedMCspikes.append(i); 
        #Recording spiking GCs
        for i in self.spikingGCs:    
            self.GC_go[i] = 1; 
        if self.timestamp%self.gp == self.gp-2:
            self.GC_ids[self.timestamp+2] = []
            for i in self.GC_go.keys():
                del self.GC_go[i]
                self.GC_ids[self.timestamp+2].append(i)
        #Gamma pulse
        if (self.timestamp-1)%(self.gp/2) == 0: 
            gammaPulse = 1;
        else:
            gammaPulse = 0; 
        #Store gamma code 
        if (self.timestamp-1)%(self.gp) == 0: 
            self.gammaCode.append([0]*self.nMCs);
            self.gammaSpikes.append([0]*self.nMCs);
        #Update MCs and GCs
        self.spikingMCs = self.MClayer.update(sensorV, self.spikingGCs, self.timestamp, learn_flag, gammaPulse);    
        self.spikingGCs = self.GClayer.update(delayedMCspikes, self.timestamp, learn_flag, AChLevel); 
        for i in self.spikingMCs:
            self.gammaCode[-1][i] = (self.gp/2) - self.timestamp%self.gp + 1;
            self.gammaSpikes[-1][i] = self.timestamp; 
        return self.spikingMCs, self.spikingGCs; 