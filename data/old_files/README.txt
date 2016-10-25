################################################################################################
MONOLINGUAL ALIGNMENT PROJECT
INSTRUCTIONS FOR GENERATING AND PROCESSING HITS FROM THE LCD DATASET

VICTORIA XIAO
SUMMER 2016
################################################################################################

All lines preceeded with "=>" should be executed as commands in terminal. Note that these are sample commands that demonstrate possible arguments for each python script; check out the .py files themselves for an explanation of what each argument represents.

Table of Contents [0000]
-----------------------------------------------------------------------------------------------
* [0001a] Generate machine-made alignments with Sultan's Monolingual Aligner
* [0001b] Generate machine-made alignments with the Berkeley Aligner
* [0002] Generate HIT templates for Mechanical Turk 
* [0003] Uploading HITs and qualifications 
* [0004] Processing training HITs 

Generate machine-made alignments with Sultan's Monolingual Aligner [0001]
-----------------------------------------------------------------------------------------------
* Run create_pairs_by_jaccard_distance.py to extract the top most interesting sentences pairs to generate hits for
	=> python create_pairs_by_jaccard_distance.py all.tsv pairs_output.csv 3 0 1 > pairs_output_print.txt

* Install Sultan's monolingual aligner by following the instructions at https://github.com/ma-sultan/monolingual-word-aligner

* Navigate to the stanford-corenlp-python folder and launch the Stanford CoreNLP server 
	=> python corenlp.py

* Place monolingual_align.py in the monolingual-word-aligner folder

* Navigate to the monolingual-word-aligner folder and run monolingual_aligner.py in order to generate alignments (this might take some time)
	=> python monolingual_align.py pairs_output.csv output.align 1 > align_output_print.txt

* Seperate pairs_output.csv into two seperate files (this is necessary to run create_aligned_HIT.py in the next step)
	=> cat pairs_output.csv | cut -f1 -s > output.e1
	=> cat pairs_output.csv | cut -f2 -s > output.e2

Generate machine-made alignments with the Berkeley Aligner [0001b] 
-----------------------------------------------------------------------------------------------
In addition to using Sultan's monolingual aligner, you can also generate alignments using the Berkeley Aligner, which is meant to be used to generate bilingual alignments. Note that future steps in the pipeline assume the usage of the Monolingual Aligner, so generating following the instructions in [0001] to align sentence pairs is recommended. These instructions are just here for informational purposes. 

* Run create_pairs_by_jaccard_distance.py to extract the top most interesting sentences pairs to generate hits for
	=> python create_pairs_by_jaccard_distance.py all.tsv pairs_output.csv 3 1 1 > pairs_output_print.txt

* Seperate pairs_output.csv into two training files for the Berkeley aligner
	=> cat pairs_output.csv | cut -f1 -s > output.e1
	=> cat pairs_output.csv | cut -f2 -s > output.e2
			- pairs_output.csv is the file that will be seperated (ie. the output of reate_pairs_by_jaccard_distance.py)
			- f1 refers to the column 1 in pairs_output.csv, f2 refers to column 2
			- output.e1 is the file that column 1 of pairs_output.csv will be printed to

* Download and unzip the Berkeley aligner from https://code.google.com/archive/p/berkeleyaligner/

* Place output.e1 and output.e2 in berkeleyaligner/new_dir

* Modify example.conf so that the trainSources value is new_dir

* Run the aligner
	=> java -server -mx200m -Xmx6g -jar berkeleyaligner.jar ++example.conf
			- see berkeley_aligner_instructions.txt for more detailed instructions
			- your alignments file is output/training.align, copy this to the folder where all your python files are and rename it "output.align"


Generate HIT templates for Mechanical Turk [0002]
------------------------------------------------------------------------------------------------
* Run create_aligned_HIT.py to generate the HIT template for output.align
	=> python create_aligned_HIT.py output.e1 output.e2 output.align all.tsv alignment_HIT_input.csv


(NEW CONTENT BELOW-----

* python convert_edinburgh_to_aligner_input.py generating_QA_HITs/train.json generating_QA_HITs/train_output_pairs.tsv 0

* Navigate to monolingual-word-aligner:
	=> python monolingual_align.py train_output_pairs.tsv train_output.align 1 > train_output_align_print.txt

------)

Uploading HITs and qualifications [0003]
------------------------------------------------------------------------------------------------
* Download the Mechanical Turk Command Line Tools API from https://requester.mturk.com/developer/tools/clt

* Move the passed_align_training_qual folder into the aws-mturk-clt-1.3.1/samples folder

* Navigate to aws-mturk-clt-1.3.1/sample/passed_align_training_qual and create the qualification by running the following in terminal:
	=> ./run.sh

* Create and upload the actual HITs on MT, using word-alignment-HIT-template.html as the HTML source code and alignment_HIT_input.csv as the batch file.

* Create and upload the training HITs on MT, using training_HIT.html as the HTML source code. Make sure to change the url in training_HIT.html to the url of the actual HITs before uploading. Upload using training_HIT_new.csv as the batch file.

* Navigate to aws-mturk-clt-1.3.1/sample/passed_align_training_qual and open qualification.question. Change the url in qualification.question to point to the training HITs url.

* Update your changes to the qualification by navigating to aws-mturk-clt-1.3.1/bin and running in terminal:
	=> ./updateQualificationType.sh -qualtypeid 3O6AFTPKRK6Y7QY6I9BNWPUILMJJC5 -question ../samples/passed_align_training_qual/qualification.question -properties ../samples/passed_align_training_qual/qualification.properties

Processing training HITs [0004]
------------------------------------------------------------------------------------------------
* Download the training batch results file from Mechanical Turk

* If necessary, open the batch results file in a text editor (ie. emacs, Sublime, etc.). Find and replace the following phrases:
	- 8/9/2016 -> 8 9
	- 1/2/2000 -> 0 1 2
	- 1/1/2016 -> 1-1

* If necessary, run fix_batch_answer_key.py to fix various errors in the answer key:
	=> python fix_batch_answer_key.py [batch-results-file].csv [batch-results-file]_correct.csv

* Create a new file in a text editor. Enter "{}" into the file (without the quotation marks) and save the file as workers_dict.json

* Run generate_worker_score.py to generate a list of workers, as well as stats on how accurate their submissions are:
	=> python generate_worker_score.py [batch-results-file]_correct.csv worker_dict.json worker_results.csv qualified_worker_results.csv non_qualified_worker_results.csv hits_result.csv > workers_score_print.txt

Uploading HITs onto Mechanical Turk (tentative)
------------------------------------------------------------------------------------------------
1. Upload qualification
2. Upload batch of qualified workers HITs with qualification
3. Upload batch of all workers HITs with link to qualification
4. Update qualification with link to all workers HITs
5. Grant qualification to appriopriate users
6. Send email to ppl 
