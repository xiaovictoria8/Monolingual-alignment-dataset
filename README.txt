###########################################################################
MONOLINGUAL ALIGNMENT PROJECT
INSTRUCTIONS FOR GENERATING AND PROCESSING HITS FROM THE LCD DATASET

VICTORIA XIAO
SUMMER 2016
###########################################################################

All lines preceeded with "=>" should be executed as commands in terminal (in the src folder unless otherwise noted). Note that these are sample commands that demonstrate possible arguments for each python script; check out the .py files themselves for an explanation of what each argument represents.

Table of Contents [0000]
---------------------------------------------------------------------------
* [0001] Upload "Passed Training" qualification on Mechanical Turk
* [0002] Upload training HITs on Mechanical Turk
* [0003] Processing training HITs results
* [0004] Generate LDC HITs input
* [0005] Upload LDC HITs on Mechanical Turk
* [0006] Processing LDC HITs results

[0001] Upload "Passed Training" qualification on Mechanical Turk
---------------------------------------------------------------------------
* Download and install the Mechanical Turk Command Line Tools API from https://requester.mturk.com/developer/tools/clt

* Move the passed_align_training_qual folder into the aws-mturk-clt-1.3.1/samples folder

* Navigate to aws-mturk-clt-1.3.1/sample/passed_align_training_qual in terminal and upload the qualification to MT:
	=> ./run.sh

[0002] Upload training HITs on Mechanical Turk
---------------------------------------------------------------------------
* Log in to Mechanical Turk and create a new project. 

* Copy and paste the contents of training_HITs/training-HIT.html as the source code for the project.

* Create a new batch for the project by uploading training_HITs/training_HIT_input.csv as the CSV input for the batch.

* training_HIT_input_stats.csv has statistics about how accurate the Berkeley aligner-generated alignments are for the sentence pairs in the training HITs.

* Open aws-mturk-clt-1.3.1/sample/passed_align_training_qual/qualification.question. Change the link for "Click here to access tthe training HITs" with the URL for the newly uploaded batch of training HITs.

* Update the qualifications test by navigating to aws-mturk-clt-1.3.1/bin in terminal and running:
	=> ./updateQualificationType.sh -qualtypeid [qual-type-id] -question ../samples/passed_align_training_qual/qualification.question -properties ../samples/passed_align_training_qual/qualification.properties

[0003] Processing training HITs
---------------------------------------------------------------------------
* Download the training batch results file from Mechanical Turk

* Find all instances of "[]" and replace them with "{}"

* Create a new file in a text editor. Enter "{}" into the file (without the quotation marks) and save the file as workers_dict.json

* Run generate_worker_score.py to generate a list of workers, as well as stats on how accurate their submissions are:
	=> python generate_worker_score_training.py [batch-results-file].csv worker_dict.json worker_results.tsv qualified_worker_results.tsv non_qualified_worker_results.tsv hits_result.tsv 

* Move qualified_worker_results.tsv to aws-mturk-clt-1.3.1/bin. Navigate to aws-mturk-clt-1.3.1/bin in terminal and run:
	=> ./assignQualification.sh -scorefile qualified_worker_results.tsv -qualtypeid [qual-type-id]

[0004] Generate LDC HITs template on Mechanical Turk
---------------------------------------------------------------------------
* Obtain the LDC dataset from CCB. Move all.tsv from the LDC dataset into the src folder.

* Install Sultan's monolingual aligner by following the instructions at https://github.com/ma-sultan/monolingual-word-aligner

* Move the monolingual-word-aligner folder in the src folder. 

* Create a new file in the monolingual-word-aligner folder using a text editor. Enter "from . import *" in the file and save it with the filename "__init__.py".

* Download the Edinburgh++ corpus from http://www.coffeeblack.org/#software.

* Open the Edinburgh corpus folder. Combine train.json and test.json by opening train.json, copying everything in the "paraphrases" list and pasting it into test.json's "paraphrase" list. Rename this new JSON file all_pairs.json and move itto the src folder.

* Navigate to the stanford-corenlp-python folder and launch the Stanford CoreNLP server 
	=> python corenlp.py

* Create the HIT CSV input file for the Edinburgh HITs by running:
	=> python convert_edinburgh_to_HITs.py all_pairs.json qa_HITs_input.csv annotator_batch_results.csv > 

* Open create_ldc_HIT_input.py and change the n variable in the main() function to the number of LDC HITs that you wish to create.

* Create the LDC HIT input file by running:
	=> python create_ldc_HIT_input.py all.tsv qa_HITs_input.csv ldc_HITs_input.csv

[0005] Upload LDC HITs on Mechanical Turk
---------------------------------------------------------------------------
* Log in to Mechanical Turk and create a new project. 

* Copy and paste the contents of other-files/word-alignment-HIT-template.html as the source code for the project.

* Create a new batch for the project by uploading ldc_HITs_input.csv as the CSV input for the batch.

[0006] Processing LDC HITs results
---------------------------------------------------------------------------
* Download the LDC batch results file from Mechanical Turk

* Generate statistics about worker performance by running:
	=> python generate_worker_score_from_qa_HITs.py other-files/list_batches.csv worker_stats_ldc.csv average_stats_ldc.csv