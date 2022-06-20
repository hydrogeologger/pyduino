Guidelines:

Step 1: Download Data from Thingsboard:
	-prepare schedule.json and tb_ch.json (These 2 files contain credential info and hence not included in this folder)
	-execute get_data_py3.py and generate the CSV file contains all the data for balances and sensors

Step 2: Prepare photos:
 	-create a folder with 5 sub-folders named: basinA, basinB, basinC, basinD and basinE, respectively
         The names of the JPG files must be in specific format. E.g. basinA_2022_05_25_12_00_01.jpg
	 This folder is used to store the original photos.
        -create another folder
	 This folder is used to store the selected photos for the video.

Step 3: Execute video.py:
	-Directories must be revised accordingly befor executing the video.py 