def OSN_encoding(odor=[]): 
    OSN = [];
    encoding = {0: 0, 1: 1.0, 2: 1.06, 3: 1.12, 4: 1.18, 5:1.25, 6:1.34, 7:1.43, 8:1.54, 9:1.67, 10:1.82, 11:2.0, 12:2.3, 13:2.5, 14:2.86, 15:3.34};    
    for i in range(0, len(odor)):
        OSN.append(encoding[odor[i]]); 
    return OSN; 