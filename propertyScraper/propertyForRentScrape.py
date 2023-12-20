from propertyScraper.spiders.rentSpider import RentspiderSpider
from propertyScraper.spiders.rentSpider import RentspiderWebTwoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
import os

def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # List of spiders to crawl
    spiders = [RentspiderSpider, RentspiderWebTwoSpider]

    for spider in spiders:
        spiderName = spider.name
        output_file = f'../data/{spiderName}_output.xlsx'

        # Checking if the file exists, and remove it to create a new one
        if os.path.exists(output_file):
            os.remove(output_file)

        process.crawl(spider, FEEDS={output_file: {'format': 'xlsx', 'overwrite': True}})
    
    process.start()

    #Excel files get combined after the spiders have finished
    combineExcelFiles()

def combineExcelFiles():
    Data_WebOne = '../propertyScraper/data/rentData_WebOne.xlsx'
    Data_WebTwo = '../propertyScraper/data/rentData_WebTwo.xlsx'
    outputCombined = '../data/Properties for rent Ireland.xlsx'

    if os.path.exists(Data_WebOne) and os.path.exists(Data_WebTwo):
        dataFrameOne = pd.read_excel(Data_WebOne)
        dataFrameTwo = pd.read_excel(Data_WebTwo)

        combinedDataFrames = pd.concat([dataFrameOne, dataFrameTwo], ignore_index=True)

        # Write the combined DataFrame to a new Excel file
        combinedDataFrames.to_excel(outputCombined, index=False)
        print("Files combined successfully.")
    else:
        print("One or both input files do not exist.")

if __name__ == "__main__":
    main()