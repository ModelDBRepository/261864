import matplotlib.pyplot as plt

def plotFigure3b(gammaCode): 
    plt.figure(1, figsize=(6, 20))
    nGamma = 5; 
    nMCs = 72; 
    for i in range(0, nGamma):
        s = int('51'+str(i+1))
        plt.subplot(s);
        if(i==0): 
            plt.title("Five gamma cycles of occluded toluene"); 
        for j in range(0, nMCs):
            #Learned Toluene
            gammaID = 1*nGamma + 9; 
            if gammaCode[gammaID][j] != 0:
                spikeTime = 20 - gammaCode[gammaID][j]; 
                plt.scatter(spikeTime, j, s= 8, marker = 'o', color = 'w', edgecolor='k')
            #Occluded Toluene
            testSample = 0; 
            gammaID = 10 + nGamma*testSample + i; 
            if gammaCode[gammaID][j] != 0:
                spikeTime = 20 - gammaCode[gammaID][j]; 
                plt.scatter(spikeTime, j, s= 2, marker = 'o', color = (0, 0, 1, 0.5)); 
            plt.ylim([-2,71])
            offset = 40*i; 
            plt.xticks([0, 4, 8, 12, 16, 20], [offset+0, offset+4, offset+8, offset+12, offset+16, offset+20]); 
            plt.yticks([15, 30, 45, 60]); 
    plt.xlabel('Timesteps');
    plt.ylabel('MC Index');
    plt.show(); 

def plotFigure3d(sMatrix): 
    bar1_x, bar2_x = [], [];      
    bar1_y, bar2_y = [], [];      
    nGamma = 5; 
    testOdorID = 0;              #sniff ID of test odor 
    for i in range(0, nGamma):
        bar1_y.append(sMatrix[nGamma*testOdorID][0]);
        bar2_y.append(sMatrix[nGamma*testOdorID+i][0]);
    w = 0.25        #width of bars
    fsize = 14;
    xticks = []
    xtick_labels = []
    for i in range(0, 5):    
        bar1_x.append(i-w/2);
        bar2_x.append(i+w/2);
        xticks.append(i)
        xtick_labels.append(str(i+1))
    plt.figure(figsize=(10, 6))
    fig = plt.subplot(111)
    bar1 = plt.bar(bar1_x, bar1_y, width = w, color = (0.75, 0.75, 0.75), align='center')
    bar2 = plt.bar(bar2_x, bar2_y, width = w, color = (0, 0, 0.75), align='center')
    plt.xlim(-1, len(bar1_x)+0.2)
    plt.ylim(0.2, 1.02)
    plt.xticks(xticks, xtick_labels, fontsize=fsize)
    plt.yticks(fontsize=fsize); 
    fig.legend( (bar1, bar2), ('Naive', 'Trained'), loc = 'upper left', fontsize=fsize)
    plt.ylabel('Similarity', fontsize=fsize); 
    plt.xlabel('Gamma Cycle', fontsize=fsize);
    plt.title("Similarity of occluded toluene to learned toluene", fontsize=fsize); 
    plt.show()

def plotFigure4a(gammaCode): 
    plt.figure(1, figsize=(6, 20))
    nGamma = 5; 
    nMCs = 72; 
    for i in range(0, nGamma):
        s = int('51'+str(i+1))
        plt.subplot(s);
        if(i==0):
            plt.title("Figure 4a"); 
        for j in range(0, nMCs):
            #Learned Toluene
            gammaID = 0*nGamma + 9; 
            if gammaCode[gammaID][j] != 0:
                spikeTime = 20 - gammaCode[gammaID][j]; 
                plt.scatter(spikeTime, j, s= 8, marker = 'o', color = 'w', edgecolor=(0, 0, 1, 0.5))
            #Learned Acetone
            gammaID = 5*5*2 + 9;       #Acetone is odor # 6
            if gammaCode[gammaID][j] != 0: 
                spikeTime = 20 - gammaCode[gammaID][j]; 
                plt.scatter(spikeTime, j, s= 8, marker = 'o', color = 'w', edgecolor=(1, 0, 0, 0.25))
            #Occluded Toluene
            gammaID = 100 + i; 
            if gammaCode[gammaID][j] != 0:
                spikeTime = 20 - gammaCode[gammaID][j]; 
                plt.scatter(spikeTime, j, s= 2, marker = 'o', color = 'k'); 
            plt.ylim([-2,71])
            offset = 40*i; 
            plt.xticks([0, 4, 8, 12, 16, 20], [offset+0, offset+4, offset+8, offset+12, offset+16, offset+20]); 
            plt.yticks([15, 30, 45, 60]); 
    plt.xlabel('Timesteps');
    plt.ylabel('MC Index');  
    plt.show(); 

def plotFigure4b(sMatrix): 
    bar1_x, bar2_x, bar3_x, bar4_x, bar5_x = [], [], [], [], [];      
    bar1_y, bar2_y, bar3_y, bar4_y, bar5_y = [], [], [], [], [];      
    nGamma = 5; 
    testOdorID = 0;              #sniff ID of test odor 
    for i in range(0, nGamma):
        bar1_y.append(sMatrix[testOdorID+i][0]);
        bar2_y.append(sMatrix[testOdorID+i][4]);
        bar3_y.append(sMatrix[testOdorID+i][5]);
        bar4_y.append(sMatrix[testOdorID+i][1]);
        bar5_y.append(sMatrix[testOdorID+i][2]);
    w = 0.15        #width of bars
    fsize = 14;
    xticks = []
    xtick_labels = []
    for i in range(0, 5):    
        bar1_x.append(i-2*w);
        bar2_x.append(i-w);
        bar3_x.append(i);
        bar4_x.append(i+w); 
        bar5_x.append(i+2*w);     
        xticks.append(i)
        xtick_labels.append(str(i+1))
    plt.figure(2, figsize=(10, 5))
    fig = plt.subplot(111)
    opacity = 0.5; 
    bar1 = plt.bar(bar1_x, bar1_y, width = w, color = 'blue', alpha = opacity, align='center')
    bar2 = plt.bar(bar2_x, bar2_y, width = w, color = 'violet', alpha = opacity, align='center')
    bar3 = plt.bar(bar3_x, bar3_y, width = w, color = 'red', alpha = opacity, align='center')
    bar4 = plt.bar(bar4_x, bar4_y, width = w, color = 'orange', alpha=opacity, align='center')
    bar5 = plt.bar(bar5_x, bar5_y, width = w, color = 'green', alpha=opacity, align='center')
    plt.xlim(-1, len(bar1_x)+0.2)
    plt.ylim(0, 1.02)
    plt.xticks(xticks, xtick_labels, fontsize=fsize)
    plt.yticks(fontsize=fsize); 
    fig.legend( (bar1, bar2, bar3, bar4, bar5), ('Toluene', 'Ammonia', 'Acetone', 'Benzene', 'Methane'), loc = 'upper left', fontsize=fsize)
    plt.ylabel('Similarity', fontsize=fsize); 
    plt.xlabel('Gamma Cycles', fontsize=fsize); 
    plt.title("Figure 4b")
    plt.show()

def plotFigure4d(gammaCode, sMatrix): 
    fig, axs = plt.subplots(figsize=(18,9));
    fig.suptitle("Figure 4d", fontsize=16); 
    sampleNumbers = [0, 0, 0, 0, 0, 9, 0, 0, 0, 1]; 
    fsize=12;
    fsize2=16;  
    plt.subplots_adjust(hspace=0.45, wspace=0.25);
    plotTitles = ['Acetaldehyde', 'Acetone', 'Ammonia', 'Benzene', 'Butanol', 'Carbon Monoxide', 'Ethylene', 'Methane', 'Methanol', 'Toluene'];
    #Order of stim presentation in simulation: 
    #Toluene, Benzene, Methane, Carbon Monoxide, Ammonia, Acetone, Acetaldehyde, Methanol, Butanol, Ethylene
    rasterOrderOdors = [6, 5, 4, 1, 8, 3, 9, 2, 7, 0];         #alphabetical ordering for plots
    nMCs = len(gammaCode[0]); 
    nOdors = 10; 
    nGamma = 5; 
    nTestPerOdor = len(sMatrix)/(nOdors*nGamma);            
    for i in range(0,10):
        #Raster plot
        plt.subplot(5, 4, 2*i+1);
        odorID = rasterOrderOdors[i];  
        sniffID = nOdors*2 + nTestPerOdor*odorID + sampleNumbers[odorID];
        for j in range(0, nGamma): 
            gammaID = nGamma*sniffID + j; 
            for k in range(0, nMCs):
                if(gammaCode[gammaID][k] != 0): 
                    spikeTime = 20 - gammaCode[gammaID][k] + 40*j;
                    plt.scatter(spikeTime, k, color='k', s=2); 
        plt.title(plotTitles[i], fontsize=fsize2); 
        plt.yticks([0, 20, 40, 60], fontsize=fsize);
        if(i>=8): 
            plt.xticks([0, 40, 80, 120, 160, 200], fontsize=fsize);
            plt.xlabel('Timesteps', fontsize=fsize2);
            plt.ylabel('MC Index', fontsize=fsize2); 
        else:
            plt.xticks([]);
        #Similarity plot
        plt.subplot(5, 4, 2*i+2);
        bar_y = []; 
        gammaID = odorID*nTestPerOdor*nGamma + sampleNumbers[odorID]*nGamma; 
        for j in range(0, 5): 
            bar_y.append(sMatrix[gammaID+j][odorID]); 
        plt.bar([40, 80, 120, 160, 200], bar_y, color='black', width=10.0);
        plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], fontsize=fsize);
        plt.ylim([0.0, 1.02])
        plt.xlim([0, 240])
        if(i>=8): 
            plt.xticks([40, 80, 120, 160, 200], [1, 2, 3, 4, 5], fontsize=fsize);
            plt.xlabel('Gamma Cycles', fontsize=fsize2);
            plt.ylabel('Similarity', fontsize=fsize2); 
        else:
            plt.xticks([]);
    plt.show() 

def findRasterDataPlume(gammaSpikes, sniffIDs):
    MCidList = [];
    spikeTimes = []; 
    for i in range(0, len(sniffIDs)):
        sniffID = sniffIDs[i]; 
        offset = sniffID*200;                     #for intersniff interval
        for j in range(0, 5):
            gammaID = sniffID*5 + j;
            MCid = 0;
            for k in gammaSpikes[gammaID]:
                if (k!=0): 
                    MCidList.append(MCid);
                    spikeTimes.append(k+offset); 
                MCid+=1;
    return MCidList, spikeTimes; 

def findSimilarityForRasterPlume(SImatrix_gamma, plumeThetaCycles, odorID): 
    sdata = []; 
    k = 0; 
    for i in range(0, plumeThetaCycles): 
        sdata.append([]); 
        for j in range(0, 5):
            #sdata[k].append(SImatrix_gamma[i*5*2+j][odorID]);
            sdata[k].append(SImatrix_gamma[i*5+j][odorID]);
        k+=1; 
    return sdata; 

def plotFigure5def(gammaSpikes, sMatrix, plumeThetaCycles): 
    sniffIDs = range(2, 12);        #first two sniffs are for training and labeling
    #sniffIDs = range(20, 30);       
    MCidsRaster, spikeTimesRaster = findRasterDataPlume(gammaSpikes, sniffIDs=sniffIDs);
    fig = plt.figure(figsize=(10, 4))

    #Figure 5f
    zoomIDs = [0, 3, 6, 9];
    sData = findSimilarityForRasterPlume(sMatrix, plumeThetaCycles, odorID=0);
    for i in range(0, 4):
        #plotID = '34' + str(8+i+1); 
        #plt.subplot(plotID);
        fig.add_subplot(3, 4, 8+i+1)
        plt.bar(range(0, 5), sData[zoomIDs[i]], color='k', width=0.4);
        plt.xticks([]);
        plt.yticks([]);
        if(i==0):
            plt.yticks([0.0, 0.5, 1.0]);
        plt.xlim([-1, 5]);
        plt.ylim([0.0, 1.02])

    #Figure 5e    
    #offset = 800*10;           #training and labeling
    offset = 800; 
    for i in range(0, 4):
        plotID = '34' + str(4+i+1); 
        plt.subplot(plotID);
        plt.scatter(spikeTimesRaster, MCidsRaster, color='k', s=2);
        plt.xlim([offset+zoomIDs[i]*400, offset+zoomIDs[i]*400+200]);
        plt.xticks([]);
        plt.yticks([]);
        
    #Figure 5d
    plt.subplot(311); 
    plt.scatter(spikeTimesRaster, MCidsRaster, color='k', s=2);
    plt.ylim([-1, 72])
    plt.xticks([]);
    plt.yticks([]);
    plt.title("Figure 5d-f");
    #plt.gcf().subplots_adjust(top=0.15)

def plotFigure5g(gammaCode, sMatrix): 
    plt.figure(3); 
    sampleNumbers = [0, 0, 0, 0, 9, 9, 0, 0, 0, 9]; 
    fsize=12;
    fsize2=16;  
    plt.subplots_adjust(hspace=0.45, wspace=0.25);
    plotTitles = ['Acetaldehyde', 'Acetone', 'Ammonia', 'Benzene', 'Butanol', 'Carbon Monoxide', 'Ethylene', 'Methane', 'Methanol', 'Toluene'];
    #Order of stim presentation in simulation: 
    #Toluene, Benzene, Methane, Carbon Monoxide, Ammonia, Acetone, Acetaldehyde, Methanol, Butanol, Ethylene
    rasterOrderOdors = [6, 5, 4, 1, 8, 3, 9, 2, 7, 0];         #alphabetical ordering for plots
    nMCs = len(gammaCode[0]); 
    nOdors = 10; 
    nGamma = 5; 
    nTestPerOdor = len(sMatrix)/(nOdors*nGamma);            
    for i in range(0,10):
        #Raster plot
        plt.subplot(5, 4, 2*i+1);
        odorID = rasterOrderOdors[i];  
        sniffID = nOdors*2 + nTestPerOdor*odorID + sampleNumbers[odorID];
        for j in range(0, nGamma): 
            gammaID = nGamma*sniffID + j; 
            for k in range(0, nMCs):
                if(gammaCode[gammaID][k] != 0): 
                    spikeTime = 20 - gammaCode[gammaID][k] + 40*j;
                    plt.scatter(spikeTime, k, color='k', s=2); 
        plt.title(plotTitles[i], fontsize=fsize2); 
        plt.yticks([0, 20, 40, 60], fontsize=fsize);
        if(i>=8): 
            plt.xticks([0, 40, 80, 120, 160, 200], fontsize=fsize);
            plt.xlabel('Timesteps', fontsize=fsize2);
            plt.ylabel('MC Index', fontsize=fsize2); 
        else:
            plt.xticks([]);
        #Similarity plot
        plt.subplot(5, 4, 2*i+2);
        bar_y = []; 
        gammaID = odorID*nTestPerOdor*nGamma + sampleNumbers[odorID]*nGamma; 
        for j in range(0, 5): 
            bar_y.append(sMatrix[gammaID+j][odorID]); 
        plt.bar([40, 80, 120, 160, 200], bar_y, color='black', width=10.0);
        plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], fontsize=fsize);
        plt.ylim([0.0, 1.02])
        plt.xlim([0, 240])
        if(i>=8): 
            plt.xticks([40, 80, 120, 160, 200], [1, 2, 3, 4, 5], fontsize=fsize);
            plt.xlabel('Gamma Cycles', fontsize=fsize2);
            plt.ylabel('Similarity', fontsize=fsize2); 
        else:
            plt.xticks([]);
    plt.show() 

