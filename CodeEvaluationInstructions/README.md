
# Epilepsyecosystem.org instruction for seizure prediction code evaluation (Dated 16/06/2020)

This document is a guide on how to prepare the input and output of your algorithm along with their associated folders to run your code for convenient independent evaluation on both the contest data and on the full trial dataset. For the full trial dataset, we will use a train, validation and test set from the long-term continuous data for each patient in the trial. The validation set will be used to compare algorithms and choose the best one for a given patient. The test set will then allow us to statistically compare the best method with a single benchmark algorithm and avoid issues with multiple comparisons. We will use the tool Singularity so we can run your code on our supercomputer and avoid any issues with dependencies of your code. Instructions and examples on creating a Singularity image for running your code on our system are provided in the attached document titled “Singularity Tutorial”. You can also watch this tutorial video [![Watch the video]](https://www.youtube.com/watch?v=RvpdwQ2aPog&t=853s) on code evaluation instructions and Singularity. 

You should **provide a readme file** that describes your algorithm (about ½ a page) and provides basic usage instructions for your code.

We require you to **provide a uri to your Singularity image**, that we can run your code in, **and your code separate from the Singularity image**. It is important for you to provide your code separate from the Singularity image in case we need to modify your code. 

Your **Python 3 (Anaconda)** code should:

<!---1. **have control 5 variables** called ‘run_on_contest_data’, ‘mode’, ‘patient_index’, ‘segment_length_minutes’, ‘subtract_mean’ and **four directory path string variables** called ‘model’, ‘feat’, ‘CSV’ and ‘solutions’ that are set by reading in the attached ![“SETTINGS.json”](SETTINGS.json) file, and described below. We can modify these variables in the ![“SETTINGS.json”](SETTINGS.json) file in order to run different jobs with your code.--->

1. **have control 4 variables** called ‘run_on_contest_data’, ‘mode’, ‘patient_index’, ‘subtract_mean’ and **four directory path string variables** called ‘model’, ‘feat’, ‘CSV’ and ‘solutions’ that are set by reading in the attached ![“SETTINGS.json”](SETTINGS.json) file, and described below. We can modify these variables in the ![“SETTINGS.json”](SETTINGS.json) file in order to run different jobs with your code. 

<!---2. **have the option to run the code on the contest data or the continuous long-term data** by specifying ‘run_on_contest_data’ to be 1 to run on the contest data or 0 to run on the continuous data. When running on the contest data (‘run_on_contest_data’=1) your code will read in the files you have been given previously when you first started working on the data and process all three contest data patients at the same time to generate the required solution file in the form given previously, and the only other control variable used will be ‘mode’. Providing this option will enable us to double check we are running your code correctly on our system. This means that ‘patient_index’, ‘segment_length_minutes’, and ‘subtract_mean’ in the ![“SETTINGS.json”](SETTINGS.json) file should be ignored in this case. Only ‘mode’ will be used.--->

2. **have the option to run the code on the contest data or the continuous long-term data** by specifying ‘run_on_contest_data’ to be 1 to run on the contest data or 0 to run on the continuous data. When running on the contest data (‘run_on_contest_data’=1) your code will read in the files you have been given previously when you first started working on the data and process all three contest data patients at the same time to generate the required solution file in the form given previously, and the only other control variable used will be ‘mode’. Providing this option will enable us to double check we are running your code correctly on our system. This means that ‘patient_index’, and ‘subtract_mean’ in the ![“SETTINGS.json”](SETTINGS.json) file should be ignored in this case. Only ‘mode’ will be used.

<!---When running on the full continuous data (‘run_on_contest_data’=0) there is much more data and so individual patients will be processed separately and all control variables will be used: ‘mode’, ‘patient_index’, ‘segment_length_minutes’, ‘subtract_mean’.--->

When running on the full continuous data (‘run_on_contest_data’=0) there is much more data and so individual patients will be processed separately and all control variables will be used: ‘mode’, ‘patient_index’, ‘subtract_mean’.  

3. **have three data set modes,** specified by the variable called ‘mode’, that we can switch between easily. For the contest data (‘run_on_contest_data’=1) the options will be: 

     mode=1: Train and output train solution file (one file for all 3 patients).
     mode=3: Output test solution file (one file for all 3 patients). 
     
For the continuous data (‘run_on_contest_data’=0) the options will be: 

     mode=1: Train and output train solution file (for individual patients).
     mode=2: Output validation solution file (for individual patients).
     mode=3: Output test solution file (for individual patients).
     
4. **be able to read the data in as .mat Matlab files of version 5.0.** See items 10/11 below for data filename information.

<!---**Note**: A 10 min segment of the **continuous** data set is of shape (239770,16) and in the **contest** data it is (240000,16), where actual sampling rate is around 399.6098 for each patient.--->

**Note**: A 10 min segment of the contest data has shape (240000,16) and to simplify things people were told the sampling rate was 400 Hz. The actual sampling rate is approximately 399.6098 Hz. This non-integer sampling rate means that for the continuous data the number of samples in a 10 minute segment can vary slightly.


<!---5. **be efficient such that the time taken to classify a 10 minute data segment is at most 30 seconds.** This duration needs to include all feature calculation and classification steps of a pretrained algorithm. [[[[You are allowed to use GPUs for training (when mode=1) if needed but then your code needs to switch to single thread for the validation and test modes (mode=2 or 3).]]]] We will use the ‘sacct’ command on our Slurm job queue system to determine the total run time for your job and divide by the total number of files processed to obtain estimates of time taken to classify.--->

5. **be efficient such that the time taken to classify a 10 minute data segment is at most 30 seconds.** This duration needs to include all feature calculation and classification steps of a pretrained algorithm. We will use the ‘sacct’ command on our Slurm job queue system to determine the total run time for your job and divide by the total number of files processed to obtain estimates of time taken to classify. 

6. **utilise at most 100 MB of RAM when classifying a 10 minute data segment.** We need to know the max RAM used during each mode (mode = 1, 2 or 3). We will use the ‘sacct’ command on our Slurm job queue system to determine the max RAM usage during your jobs.

**The next two items refer ONLY to the continuous data case (‘run_on_contest_data’=0)**

7. **if ‘run_on_contest_data’=0, train, validate or test on one patient at a time** and should include the control variable called ‘patient_index’ we can modify that selects the index of the patient to be analysed. The patient indices range from 1 to 15.

<!---8. **if ‘run_on_contest_data’=0, be able to read in file segments of different sizes** by changing the control variable called ‘segment_length_minutes’ which takes different values. You should set the default to 10 minutes to be consistent with the contest data. We will explore the effect of 1 vs 10 minute window sizes on only the best algorithm for each patient as determined from the validation set.--->


8. **if ‘run_on_contest_data’=0, be able to switch ON or OFF subtraction of the mean from each channel within each data segment** by changing the control variable called ‘subtract_mean’ which takes on values 0 (OFF) or 1 (ON). To avoid reverse engineering the contest data during the Kaggle contest, the contest data had the mean of each channel within a file segment subtracted from each corresponding channel. This is not the case with the original continuous data. We want to see what effect subtracting the mean will have on the continuous data so want to be able to switch it ON or OFF.

**The remaining items refer to both the contest data (‘run_on_contest_data’=1) and continuous data (‘run_on_contest_data’=0) cases**

9. **be able to train on a set of file segments.**

**If ‘run_on_contest_data’=1,** we want your code to load in the file  
http://www.epilepsyecosystem.org/s/contest_train_data_labels.csv as you can find it here!["here"](CSV)
as input and use it to read in the training files. This csv file should be stored in the folder path pointed to by ‘CSV’ in the ![“SETTINGS.json”](SETTINGS.json) file. Note we will be using a modified version of this .csv file where in each row we include the ‘PATH’ on our supercomputer to the files so that in our file each row will look as follows: 
‘[PATH]/PatITrain_J_K.mat’
You do not need to work with the modified .csv file, you only need to make sure your code reads in ‘contest_train_data_labels.csv’ so that it knows how to load in the files for training. Note your code should process all patients in the contest data at once so a single solution file can be generated for all patients.  

<!---**If ‘run_on_contest_data’=0,** we want your code to be able to train on a set of file segments of length ‘segment_length_minutes’ for each patient specified by a list of filenames using the similar list structure as given in the contest data. However, the csv file containing the list of **training** set filenames will have the following filename structure:---> 

**If ‘run_on_contest_data’=0,** we want your code to be able to train on a set of file segments of length 10 minute for each patient specified by a list of filenames using the similar list structure as given in the contest data. However, the csv file containing the list of **training** set filenames will have the following filename structure: 

<!---‘train_filenames_labels_patient[patient_index] _segment_length_ [segment_length_minutes].csv’ as you can find them !["here"](CSVfiles)--->

‘train_filenames_labels_patient[patient_index]_segment_length_10.csv’ as you can find them !["here"](CSV)

<!---where ‘patient_index’ and ‘segment_length_minutes’ are defined above. These csv files !["CSVfiles"](CSVfiles) should be stored in the folder path pointed to by ‘CSV’ in the ![“SETTINGS.json”](SETTINGS.json) file.--->

where ‘patient_index’ is defined above. These csv files !["CSV"](CSV) should be stored in the folder path pointed to by ‘CSV’ in the ![“SETTINGS.json”](SETTINGS.json) file. 

<!---In each row of each ‘train_filenames_labels_patient[patient_index]_segment_length_ [segment_length_minutes].csv’ file the first column called ‘image’ will contain the segment filename:--->

In each row of each ‘train_filenames_labels_patient[patient_index]_segment_length_10.csv’ file the first column called ‘image’ will contain the segment filename: 

‘[PATH]/UTC_AB_CD_EF.mat’ (as you can find here examples of .mat files for testing your code !["here"](CSV/matfiles) which have been used in CSV)

where ‘PATH’ points to where we have stored the file and “AB_CD_EF” corresponds to the hours, minutes and seconds of the start of the segment relative to the start of the recording in UTC time. Moreover, the second column called ‘class’ will contain the class label: 0 for interictal, 1 for preictal.

<!---**Note:** This means you cannot get the class label from a training file segment’s filename like you can with the contest training data. The class label will be available in the second column of the ‘train_filenames_labels_patient[patient_index]_segment_length_[segment_length_minutes].csv’ files availabe !["here"](CSVfiles).--->

**Note:** This means you cannot get the class label from a training file segment’s filename like you can with the contest training data. The class label will be available in the second column of the ‘train_filenames_labels_patient[patient_index]_segment_length_10.csv’ files availabe !["here"](CSV).

10. **Generate solution files for the train, validation and test sets** where the solution files are to be stored in a folder pointed to by the variable ‘solutions’ in the ![“SETTINGS.json”](SETTINGS.json) file. To avoid evaluation errors, the number of the rows and order of filenames listed in the solution files should precisely match the number of the rows and order of filenames provided in the corresponding lists of filenames for the train, validation or test sets that are used to read data segments into your code.

**If ‘run_on_contest_data’=1, we want**

a.	the solution files to be given the following filename structure: 

‘contest_data_solution_[Seer_Username]_mode[mode].csv’  

where ‘Seer_Username’ is the username you used to access the Seer platform and download the contest data and ‘mode’ has been defined above.

b.	the code to separately read in the train (mode=1) or test (mode=3) sets depending on the ‘mode’ and for testing your code should read in the file
https://www.epilepsyecosystem.org/s/contest_test_data_labels_public.csv (find it here ["here"](CSV))
as input so that it knows which test files to read in. This csv file should be stored in the folder path pointed to by ‘CSV’ in the ![“SETTINGS.json”](SETTINGS.json) file. Note, similar to the training data we will be using a modified version of this .csv file where in each row we include the ‘PATH’ on our supercomputer to the files so that in our file each row will look as follows: 

‘[PATH]/PatITest_J_0.mat’

Again, you do not need to work with the modified .csv file, you only need to make sure your code reads in ‘contest_test_data_labels_public.csv’ so that it knows how to load in the files for testing. Note your code should process all patients in the contest data at once so a single solution file can be generated for all patients.

c.	The solution file should have the same internal structure to the contest solution file provided at: http://www.epilepsyecosystem.org/s/contest_solution_file.csv 
Where the first column is called ‘image’ and the second column is called ‘class’. In the second column you should provide the preictal probability for the file segment in the corresponding row. The probability should be a value between 0 and 1, 0 indicating interictal and 1 preictal. If you don’t want to provide a preictal probability for a row leave this empty or enter a ‘None’ or ‘NaN’.

<!---**If ‘run_on_contest_data’=0,** we want your code to generate solution files for the train, validation and test sets for given ‘patient_index’ and ‘segment_length_minutes’ values where:--->

**If ‘run_on_contest_data’=0,** we want your code to generate solution files for the train, validation and test sets for given ‘patient_index’ values where:

a. the solution files are given the following filename structure: 

<!---‘solution_[Seer_Username]_pat[patient_index]_seg[segment_length_minutes]_mode[mode]_subtract[subtract_mean].csv’--->

‘solution_[Seer_Username]_pat[patient_index]_mode[mode]_subtract[subtract_mean].csv’ 

where ‘Seer_Username’ is the username you used to access the Seer platform and other variables have been defined above.

b. the code separately reads in the train (mode=1), validation (mode=2) or test (mode=3) sets depending on the ‘mode’ and the validation and test segment filenames are provided in a similar fashion to the training set filenames. The csv file containing the list of **validation** set filenames will have the following filename structure:  

<!---‘validation_filenames_patient[patient_index]_segment_length_[segment_length_minutes].csv’ availabe !["here"](CSVfiles)--->

‘validation_filenames_patient[patient_index]_segment_length_10.csv’ availabe !["here"](CSV)

and the csv file containing the list of **test** set filenames will have the following filename structure: 

<!---‘test_filenames_patient[patient_index]_segment_length_[segment_length_minutes].csv’ availabe !["here"](CSVfiles)--->

‘test_filenames_patient[patient_index]_segment_length_10.csv’ availabe !["here"](CSV)

These csv files should be stored in the folder path pointed to by ‘CSV’ in the ![“SETTINGS.json”](SETTINGS.json) file. Similar to the case for training, in each row of each of these validation and test filename list csv files the first column called ‘image’ will contain the segment filename: 
‘[PATH]/UTC_AB_CD_EF.mat’

c.	The solution files have a similar internal structure to the contest solution file provided at: http://www.epilepsyecosystem.org/s/contest_solution_file.csv 
Where the first column is called ‘image’ and the second column is called ‘class’. In each row the first column should contain the filename of a segment: 
‘[PATH]/UTC_AB_CD_EF.mat’
And the second column should contain the preictal probability for the file segment in the corresponding row. The probability should be a value between 0 and 1, 0 indicating interictal and 1 preictal. If you don’t want to provide a preictal probability for a row leave this empty or enter a ‘None’ or ‘NaN’.

11. **store the trained models in a folder** pointed to by the string variable ‘model’ defined in ![“SETTINGS.json”](SETTINGS.json) and saved with the filenames: 

<!---‘model_dataset[run_on_contest_data]_pat[patient_index]_seg[segment_length_minutes]_subtract[subtract_mean]’--->

‘model_dataset[run_on_contest_data]_pat[patient_index]_subtract[subtract_mean]’

12. **(if necessary) store intermediate features in a folder** path defined by the concatenation of the string variable ‘feat’ defined in ![“SETTINGS.json”](SETTINGS.json) and sub-folders called: 
<!---‘feat_dataset[run_on_contest_data]_pat[patient_index]_seg[segment_length_minutes]_subtract[subtract_mean]’--->

‘feat_dataset[run_on_contest_data]_pat[patient_index]_subtract[subtract_mean]’

It is up to you if you store files directly in these sub-folders or in sub-folders within these sub-folders.

**Additional note:** we will provide you with sample versions of the required files for testing your code.










