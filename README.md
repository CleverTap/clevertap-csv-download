## CleverTap python csv download tool

### Note:
- this project is now moved to python3
- python 2.x support is deprecated for this project 
- for using python2 use release https://github.com/CleverTap/clevertap-csv-download/releases/tag/v1.0

### Usage
to download user profiles/events to a csv:
- git clone the repo (or simply copy-paste the files clevertap.py and csvdownload.py, and place them in the same folder)
- cd to cloned directory (or the directory where you have created the above two files)
- run csvdownload.py passing your CleverTap Account ID, Passcode, absolute path to your json file and the absolute path to your csv file. 
-  e.g. python csvdownload.py -a WWW-YYY-ZZZZ -c AAA-BBB-CCCC -pjson ~/Desktop/query_example.json -pcsv ~/Desktop/event.csv -t event



```
arguments:
  -h, --help                        show this help message and exit
  -a ID, --id ID                    CleverTap Account ID
  -c PASSCODE, --passcode PASSCODE  CleverTap Account Passcode
  -r REGION, --region REGION        Dedicated CleverTap Account Regioni, optional
  -pjson PATH, --path PATH          Absolute path to the json file
  -pcsv PATH, --path PATH           Absolute path to the csv file
  -t TYPE, --type TYPE              The type of query, either profile or event, defaults to profile
```

NOTE: The .csv file generated will be utf-8 encoded. This file might cause unusual behaviour in Excel application depending on your encoding settings. It can be viewed without any problem on Google Spreadsheets or Numbers application. 

