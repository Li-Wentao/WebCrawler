import requests
import json
import argparse
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.ie.service import Service
from time import sleep
from html import unescape
from bs4 import BeautifulSoup
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Web spider for database "data.world.com".')
parser.add_argument('-s', '--searchURL', type=str, help='Directory to a .txt file that store the URL of a search in "data.world.com" to be crawled.', required=True)
parser.add_argument('-o', '--outputDir', type=str, help='Path to save the output json files.', required=True)
parser.add_argument('-v', '--verbose', action="store_true", help='Print out the verbosity.')
args = parser.parse_args()

def main():
    """This is the main pipeline build for data.world database
    """
    # Inits
    NEXT = True
    page = 1
    n = 0
    outdir = args.outputDir
    with open(args.searchURL, 'r') as f:
        link = f.readline()
    # Configs of chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless") # mute browser windows
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
    while NEXT is True:
        print('==========Start crawling==========\n')
        print(f'Website:{link}')
        print(f'\n Now crawling page {page}...')
        driver.get(link)
        sleep(3) # sleep 3 sec to make sure all JS plugins are loaded
        htmlSource = driver.page_source
        results_dirs = re.findall('data-dw="DatasetCard-Title"><a href="(.+?)">', htmlSource)
        print(f'There are {len(results_dirs)} results in this page')
        for result_dir in tqdm(results_dirs):
    #         print(f'There are {len(results_dirs)} files in this page')
            url = 'https://data.world' + result_dir
            request = requests.get(url)
            n += 1
            soup = BeautifulSoup(request.text, 'html.parser')
            script = soup.find('script')
            pattern = re.compile('({.+})')
            result = pattern.findall(str(script))
            jsonData = json.loads(result[0])
            out_fname = json.loads(result[0])['name'].replace(' ', '_').replace('-', '_').replace('/', '_').replace(',', '').replace('/', '').replace('...', '') + f'({n}).json'
            with open(outdir + out_fname, 'w') as outfile:
                json.dump(jsonData, outfile)
        print('Done with crawling current page!')
        # If there is a 'Next' botton
        if re.findall('aria-label="Next"', htmlSource):
            next_page = re.findall('10</a></li><li class=""><a href="(.+?)"><span aria-label="Next">', htmlSource)
            # In case there is 'Next' botton but it is the last page...
            if next_page:
                NEXT = True
                link = 'https://data.world' + unescape(next_page[0])
                page += 1
            else:
                NEXT = False
                print('=========LAST PAGE!!=========')
        else:
            NEXT = False
            print('=========LAST PAGE!!=========')
    print(f'See all {n} crawled file(s) in {outdir}')
if __name__ == "__main__":
    main()