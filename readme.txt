README for OB_EPL model
Imam and Cleland 2020, Nature Machine Intelligence
Also:  https://arxiv.org/abs/1906.07067


1. System requirements
	a. Software dependencies 
		-- Python version 2.7 
		-- Python packages numpy and matplotlib
	b. Versions that the software has been tested on 
		-- Python version 2.7 running on Mac OS X 10.11 and Windows 10
	c. Non-standard hardware 
		None. The code provided here runs on a convetional desktop computer. For the full model, 
		this code runs three orders of magnitude slower than the model implemented in Intel's Loihi neuromorphic 
		system. 

2. Installation guide
	a. We recommend using the Anaconda Python Distribution. 
		-- Installation link: https://docs.anaconda.com/anaconda/install/
		-- Chooose your operating system and Python version 2.7
		-- Download and install
	b. Typical install time: Approximately 20 minutes

3. Demo
	a. Instructions to run on data
		-- Open the Anaconda Navigator
		-- Click "Launch" under "Spyder" (a Python development environment)    
		-- Click File->Open 
		-- Open the file "singleOdorTest.py"
		-- Click Run->Run
	b. Expected output
		-- Raster plots showing spiking activity for a test sample of Toluene. Autoassociative 
		   network dynamics across five gamma cycles can be observed across the five raster plots. 
		-- Bar plot showing the similarity between a test sample of Toluene and the learned representation 
		   of Toluene across five gamma cycles. 
	c. Expected run time on a conventional desktop computer: ~15 seconds. 

4. Instructions for use
	a. Files "singleOdorTest.py", "multiOdorTest.py", "plumeTest.py" can be run
	   through Spyder (see step 3a above). 
        b. Reproduction instructions 
		-- "singleOdorTest.py" generates main results of Figure 3. 
		-- "multiOdorTest.py" generates main results of Figure 4. 
		-- "plumeTest.py" generates main results of Figure 5. 
.