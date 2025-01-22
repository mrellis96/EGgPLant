README
EGgPLant V1.0
            _______________________________
           /_______________________________\
          //                               \\
         //                         ▒▒      \\
        //                          ▒▒       \\
       //                         ▒▒          \\
      //                      ░░░░▒▒░░         \\
     //                     ░░░░░░░░░░          \\
    //                      ░░░░░░░░░░           \\
   //                       ▒▒░░░░░░░░░           \\
  //                      ▒▒▒▒▒▒▒▒░░▒▒░░           \\
 //                      ▒▒▒▒▒▒▒▒▒▒▒▒▒              \\
//                      ▒▒▒▒▒▒▒▒▒▒▒▒                 \\
\\                      ▒▒▒▒▒▒▒▒▒▒▒▒                 //
 \\                   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒                //
  \\                  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒               //
   \\               ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒              //
    \\            ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒               //
     \\           ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒              //
      \\          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒               //
       \\         ▒▒▒▒▒▒▒▒▒▒▒▒▒▒              //
        \\        ▒▒▒▒▒▒▒▒▒▒▒▒               //
         \\         ▒▒▒▒▒▒▒▒                //
          \\_______________________________//
           \_______________________________/

-------------------------------------------------------------------------------------------------------------------------------------------
EGgPLant has been developed by Morgan Ellis and Owen Holland
For any issues please contact either of the above.
Requirements:
Linux OS (including WSL on Windows) or Mac OS
IMPORTANT: If not using manual installation, EGgPLant will download and install the needed programs (Including R, cutadapt, vsearch, taxonkit, NCBI BLAST+, NCBI Entrez Direct, libxml2-dev, libssl-dev and coreutils) if they are not present. For Linux OS this will involve adding to and updating the apt list and then installing the programs so your password for sudo will be required. For Mac OS this will involve installing homebrewer if it is not already present and installing the programs through homebrewer. EGgPLant won't update these packages for you, so you may wish to update the packages from the list above in parentheses that haven't received a fresh install.

-------------------------------------------------------------------------------------------------------------------------------------------
Installation:
Download the tarball (`EGgPLant_VXX.tar.gz`) and the install script `install.eggplant.sh` 
run `bash install.eggplant.sh` in the same directory as the EGgPLant tarball. The install script will now install all the necessary programs and move the EGgPLant script to `/usr/bin/` (`/usr/local/bin/` on mac)

Manual install:
1) Extract files
2) Go to the folder containing the script file and run:
<export PATH=$PATH:~/Path/To/Scripts>

The manual install method is great when you have permissions limitations (say, on a university or institution issued machine without admin privileges). However, EGgPLant will still try to run dependencies (e.g. cutadapt, vsearch, taxonkit, etc.) and these will need to be installed. In such a case, it might be best to create a conda environment with all your dependencies installed, and then running EGgPLant within this environment.  

-------------------------------------------------------------------------------------------------------------------------------------------
`eggqual` - Quality Plot Generator:

1) Go to the directory where you would like to run the pipeline
2) Ensure your fastq.gz files are in a subdirectory within the current directory
3) run:
`eggqual -d [path/to/reads]`
-d: Directory, where the raw reads are stored - REQUIRED

NOTE: `eggqual -h` will display the help file

-------------------------------------------------------------------------------------------------------------------------------------------
`eggplant` - Main Pipeline:

1) Go to the directory where you would like to run the pipeline
2) run:
<eggplant -d [] -f [] -r [] -l [] -p [] -t [] -y [] -n [] -m [] -o []> # Replace [] with value eg: -t 120
-d: Directory, where the raw reads are stored - REQUIRED
-f: Forward primer, the sequence of the forward primer for cutadapt to remove (optional)
-r: Reverse primer, The sequence of the reverse primer for cutadapt to remove (NOT reverse complemented; paired reads only; optional)
-l: Minimum overlap, the minimum number of base pair overlap (alignment) between the primer and the returned sequence before cutadapt will recognise the primer (optional, but required if -f or -r are used)
-p: Poly tail, Removes poly tails of Base [] if there are more than >6 repeating bases in a row. (optional)
-t: Truncate, where you would like `filterAndTrim` to truncate the forward reads (default = no truncation; use eggqual to find suitable level of truncation)
-y: Reverse truncate, where you would like `filterAndTrim` to truncate the reverse reads (default = no truncation; use eggqual to find suitable level of truncation. Paired reads only)
-n: Remove reads with length less than [n] BP (default = 20; optional)
-m: Minimum number of reads per sample allowed after chimera removal (default = 10; optional)
-b: Blast database, database to BLAST output sequences against. Must be BLASTn formated database. You can use `eggdb` to create your own. (optional, but recommended)
-v: Taxonomic mapping file, path to taxmap file used to report corresponding taxonomic assignments based on blast outputs. Format: `header/accession taxid` (e.g. `DQ268529.1 9606`) (optional, but REQUIRED if -b is used)
-o: Cluster ASVs to OTUs. ASVs will be clustered in to OTUs based on the similarity value (float 0-1; default = no clustering; optional)

3) Check number of reads after each step in the terminal for optimising these variables.

NOTE: `eggplant -h` will display the help file
      `eggplant -c` will display the citation file	

-------------------------------------------------------------------------------------------------------------------------------------------
`eggdb` - Blast DB Creator:

1) Go to the directory where you would like to create your database. It is strongly recommended that you use the same directory where your raw sequence subdirectory is stored.
2) Run
<eggdb -q [] -d []>
-q: Query, Enter the desired query to search. To get the correct syntax for the query, go to the NCBI site and perform the desired search. Then copy the query from the "Search details" box. - It is recommended to search broadly for your gene region of your marker. The query must be enclosed with quotation marks. If you have double quotation marks WITHIN the query the query MUST be enclosed with SINGLE quotation marks - REQUIRED
-d: Database Name, The name for the database - NOTE: Spaces are not accepted. - REQUIRED

3) For blast to find the database the path must be exported (eg <export BLASTDB=/path/to/database/>). This can be added to your bashrc automatically by the script or run at the stat of each session.

NOTE: <eggdb -h> will display the help file

-------------------------------------------------------------------------------------------------------------------------------------------
Updates:
 
V0.1.1: Added cancel option to Paired End Question; Changed README to .txt file; Added disclaimer; Added EGPLQ to run qPlots before Main Pipeline; Script now checks for Forward Directory, if present will skip sorting step; Fixed loop to Paired End Question; Script will now check if needed programs are installed and if not, install them.  
V0.1.1.1: Bug Fixes, Script will check for reverse reads before making reverse/.  
V0.1.1.2: Set repository to https://cran.csiro.au/, Added text for transparancy and debugging.  
V0.1.2: Added support for Mac OS, Quality plots are now an aggregate of the whole data set rather than the first 9 sequences.  
V0.2.0: Added EGDB to create databases from queries, altered the way the script searches for packages so it is more reliable on both OS systems.  
V0.2.1: Added Help messages to EGPL, EGPLQ, EGDB. Added Install script to automatically install script.  
V0.2.2: Added -d option for EGPL and EGPLQ to specify the directory the raw reads are stored in, fixed various spelling and grammatical errors.  
V0.2.3: Added -o to EGPL to cluster ASVs into OTUs. Minor Fixes to install script.  
V0.2.3.1: Fixed errors in README. Change repository to ubuntu version used.  
V0.2.3.2: Moved ubuntu version check so it no longer interferes with the installation of R, Changed Vim script to awk script in EGDB, Added '--relabel OTU_' to EGPL, Moved updates to end of README, added '(Y/N/C)' to EGPL.Inst.sh.  
V0.2.3.3: Fixed errors with EGPL.inst.sh.  
V0.2.4: Fixed issues with R library paths, removed redundancies in EGPL, EGPLQ, EGDB created from EGPL.Inst.sh.  
V0.2.5 Added option [-n] to EGPL, Fixed bug that caused mac pipelines to error if option [-o] is added, Made 10 the default for option [-m].  
V0.3.0: EGPL now uses 'Cutadapt' to remove primers instead of dada2:filterAndTrim, ASV's now added to Pipeline_results.csv instead of sequences. ASV's automatically converted to OTU's and stored in OTU.csv.  
V0.3.1: Readded truncation to pipeline, added Poly tail remover, added vSearch citations.           
V0.3.1.1: Fixed numerous errors preventing r from running, added "then" to cutadapt script, fixed minor erros in cutadapt script, fixed errors in README.  
V0.4.0: Added Interactive Pipeline (EGIP).  
V0.4.0.1: Improved the way EGIP and EGPL pass options to RScript to simplify R code and reduce chance of errors.  
V0.4.1: Added EGDB and BlastN to EGIP, R now outputs fasta file as 'Results.fa'.  
V0.4.1.1: Name Changed to EGgPLant.  
V0.4.1.2: Bug Fixes.  
V0.4.2: Changed install script to install to a local dir. not /usr/bin, Added LCA script, renamed EGPL to eggplant.  
V0.5.0: Intergrated blast and LCA script in to main eggplant pipeline, depreciated EGIP, improved speed through awk handling.
V1.0: Set public release
-------------------------------------------------------------------------------------------------------------------------------------------
#DISCLAIMER: While all effort was taken to ensure this script is free from errors, Morgan Ellis, Owen Holland and the EcoGenetics Lab take no responsibility to any damage, corruption or issues that may arise from running this script or pipeline. Please use at your own risk.

