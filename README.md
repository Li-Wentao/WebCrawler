# WebCrawler
-------------
WebCrawler is a web spider built for data repository https://data.world/search. 

## Pre-requests
* Have conda installed
-----------------------

## Installation
----------------
1. Unzip the file and enter the folder directory
2. Create a new conda environment with requirements
```bash
conda create --name <new environment name> --file 
conda activate <new environment name>
```
3. Create a directory to save outputs
```bash
mkdir <directory to save json files>
```

## Preparations
----------------
1. Check the file `searchURL.txt` and make sure it has the correct link to data repository. If you have another search quotes other than this one, replace current one with a new URL link.


## Usage
-----------
```
usage: WebCrawler.py [-h] -s SEARCHURL -o OUTPUTDIR [-v]

Web spider for database "data.world.com".

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCHURL, --searchURL SEARCHURL
                        Directory to a .txt file that store the URL of a search in "data.world.com" to be crawled.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to save the output json files.
  -v, --verbose         Print out the verbosity.
```

## Example
-------------
```bash
python3 WebCrawler.py -s searchURL.txt -o <directory to save json files>
```

## License
[MIT](https://choosealicense.com/licenses/mit/)