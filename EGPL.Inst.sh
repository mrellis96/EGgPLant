#!/bin/bash
#EcoGenetics Pipeline install Scrip V4.0.1
echo "Thank you for choosing EcoGeneticsPipeline"
echo "The pipeline will now be installed including all programs such as R, Vim, NCBI-Blast etc."
read -p "Do you want to continue? (Y/N/C) "
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]] || exit -1
then
echo "Unzipping"
tar -xf EcoGeneticsPipelineV*.tar.xz
if [[ "$(uname)" == "Linux" ]];
	then
	echo "Installing scripts (Linux OS)"
	if [ -f "/usr/bin/EGPL" ]
		then
		sudo rm /usr/bin/EGIP /usr/bin/EGPL /usr/bin/EGPLQ /usr/bin/EGDB /usr/bin/EGPEP /usr/bin/EGSEP /usr/bin/EGPEPQ /usr/bin/EGSEPQ 
		sudo rm /usr/bin/.EGS -f
	fi
	cd EcoGeneticsPipeline/
	chmod 777 EGPL EGPLQ EGDB EGPEP EGSEP EGSEPQ EGPEPQ EGIP .EGS
	sudo mv EGPL EGPLQ EGDB EGPEP EGSEP EGSEPQ EGPEPQ EGIP .EGS /usr/bin
	sudo mv EGPL_README.txt ../
	cd $cwd
	sudo rm -r EcoGeneticsPipeline/
	fi
	
	echo "Checking packages"
	#Check if packages are installed
 	echo "r-base"
     	which R &> /dev/null
     	

    	if [ $? -ne 0 ]

        	then
        	. /etc/lsb-release
     		dcn=$DISTRIB_CODENAME  

            	echo "Not installed"  
            	echo "setting repostiories"
		
		sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $dcn-cran40/"
		sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
            	sudo apt-get update
            	
            	echo "installing packages"
            	sudo apt-get install r-base r-base-core r-recommended r-base-dev 
        else
        echo    "Installed"
        echo
        
	fi
    	echo "libcurl4-openssl-dev"
    	which curl-config &> /dev/null
    	if [ $? -ne 0 ]
    		then
    		echo "Not installed"
    		sudo apt-get install libcurl4-openssl-dev
    	else
    	echo "Installed"
    	echo
 	fi   		
    	echo "libxml2-dev"
    	which xml2-config &> /dev/null
    	if [ $? -ne 0 ]
    		then
		echo "Not installed"
    		sudo apt-get install libxml2-dev
    		else
    		echo "Installed"
    	echo
 	fi   	
 	echo "libssl-dev"
 	dpkg -s libssl-dev &> /dev/null
 	if [ $? -ne 0 ]
 		then
 		echo "Not installed"
 		sudo apt-get install libssl-dev
 	else
 	echo "Installed"
 	echo
 	fi
 	
 	echo "Blast+"
     	which blastn &> /dev/null  
    	if [ $? -ne 0 ]
        	then
            	echo "Not installed"  
           	sudo apt-get install ncbi-blast+
        else
        echo    "Installed"
        echo
	fi
	
	echo "Entrez Direct"
	which esearch &> /dev/null 
    	if [ $? -ne 0 ]
        	then
            	echo "Not installed"  
            	sudo apt-get install ncbi-entrez-direct   	
        else
        echo    "Installed"
        echo
	fi
	
	echo "vsearch"
	which vsearch &> /dev/null 
    	if [ $? -ne 0 ]
        	then
            	echo "Not installed"  
            	sudo apt-get install vsearch    	
         	else
        	echo    "Installed"
        	echo
	fi
	
	echo "Cutadapt"
	which cutadapt &> /dev/null
	if [ $? -ne 0 ]
		then
		echo "Not installed"
		sudo apt install python3-pip
		pip install --upgrade --user pip
		python3 -m pip install --user --upgrade cutadapt
		echo "Adding cutadapt to PATH"
		export PATH=$PATH:$HOME/.local/bin
		echo "export PATH=$PATH:$HOME/.local/bin" >> $HOME/.bashrc
		else
		echo "Installed"
		echo
	fi
	
	echo "R Personal lib"
	plib="~/R/x86_64-pc-linux-gnu-library/4.0"
	if [ ! -d "$HOME/R/x86_64-pc-linux-gnu-library/4.0" ]
		then
		echo "Personal Library not found"
		read -p "Would you like to create a personal library
‘~/R/x86_64-pc-linux-gnu-library/4.0’ to install R Packages? (Y/N) "
		echo    # (optional) move to a new line
		if [[ $REPLY =~ ^[Yy]$ ]]
			then
			mkdir -p ~/R/x86_64-pc-linux-gnu-library/4.0
			else
			echo "Please ensure a writable library is available for R to install packages"
		fi
		else echo "Personal Lib Found"
		echo
	fi
	
elif [[ "$(uname)" == "Darwin" ]];
	then
	echo "Installing scripts (Mac OS)"
	if [ -f "/usr/local/bin/EGPL" ]
		then
		sudo rm /usr/local/bin/EGIP /usr/local/bin/EGPL /usr/bin/local/EGPLQ /usr/local/bin/EGDB /usr/local/bin/EGPEPM /usr/local/bin/EGSEPM /usr/local/bin/EGPEPQM /usr/local/bin/EGSEPQM
		sudo rm /usr/local/bin/.EGS -f
	fi
	cd EcoGeneticsPipeline/
	chmod 777 EGPL EGPLQ EGDB EGPEPM GSEPM EGPEPQM EGSEPQM EGIP .EGS
	sudo mv EGPL EGPLQ EGDB EGPEPM EGSEPM EGSEPQM EGPEPQM EGIP .EGS /usr/local/bin
	sudo mv EGPL_README.txt ../
	cd $cwd
	sudo rm -r EcoGeneticsPipeline/
	
	
	echo "Checking packages"
	echo "r-base"
     	which R &> /dev/null  
    	if [ $? -ne 0 ]
        	then
            	echo "Not installed"  
           	which brew &> /dev/null 
           	if [ $? -ne 0 ]
           		then
			echo "Installing Homebrew (Required to install packages)"
			-c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
		fi              
		brew install r         	
           	else
        	echo    "Installed"
	fi
	echo "Blast+"
     	which blastn &> /dev/null  
    	if [ $? -ne 0 ]
        	then
            	echo "Not installed"  
           	which brew &> /dev/null 
           	if [ $? -ne 0 ]
           		then
			echo "Installing Homebrew (Required to install packages)"
			-c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
           	fi
           	brew install blast          	
           	else
        	echo    "Installed"
	fi
	
	echo "Entrez Direct"
     	which esearch &> /dev/null  
    	if [ $? -ne 0 ]
        	then
            	echo "Not installed" 
            	cwd=$(pwd)
            	cd ~
		/bin/bash
		perl -MNet::FTP -e \
		    '$ftp = new Net::FTP("ftp.ncbi.nlm.nih.gov", Passive => 1);
		    $ftp->login; $ftp->binary;
		    $ftp->get("/entrez/entrezdirect/edirect.tar.gz");'
		gunzip -c edirect.tar.gz | tar xf -
		rm edirect.tar.gz
		builtin exit
		export PATH=$PATH:$HOME/edirect >& /dev/null || setenv PATH "${PATH}:$HOME/edirect"
		./edirect/setup.sh
		echo "export PATH=\$PATH:\$HOME/edirect" >> $HOME/.bash_profile
		cd $cwd
         	else
        	echo    "Installed"
	fi
	echo "Cutadapt"
	which cutadatp &> /dev/null
	if [ $? -ne 0 ]
		then
		echo "Not installed"
		pip install --upgrade --user pip
		python3 -m pip install --user --upgrade cutadapt
		else
		echo "Installed"
		echo
	fi
	echo "vsearch"
     	which vsearch &> /dev/null  
    	if [ $? -ne 0 ]
        	then
            	echo "Not installed"  
           	which brew &> /dev/null 
           	if [ $? -ne 0 ]
           		then
			echo "Installing Homebrew (Required to install packages)"
			-c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
           	fi
           	brew install vsearch          	
           	else
        	echo    "Installed"
	fi
fi
echo "The pipeline and all dependacies are now installed"
echo "Please read the readme (EGPL_README.txt) found in the found in "$cwd" before use"
