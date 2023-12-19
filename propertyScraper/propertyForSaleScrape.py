from propertyScraper.spiders.propertySpider import PropertyspiderSpider
from propertyScraper.spiders.rentSpider import RentspiderSpider
from propertyScraper.spiders.propertySpider import PropertyspiderWebTwoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
import os

def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # List of spiders to crawl
    spiders = [PropertyspiderSpider, PropertyspiderWebTwoSpider]

    for spider_class in spiders:
        spider_name = spider_class.name
        output_file = f'../data/{spider_name}_output.xlsx'

        # Checking if the file exists, and remove it to create a new one
        if os.path.exists(output_file):
            os.remove(output_file)

        process.crawl(spider_class, FEEDS={output_file: {'format': 'xlsx', 'overwrite': True}})
    
    process.start()

    #Excel files get combined after the spiders have finished
    combine_excel_files()

def combine_excel_files():
    file_path1 = '../propertyScraper/data/propertyData_WebOne.xlsx'
    file_path2 = '../propertyScraper/data/propertyData_WebTwo.xlsx'
    output_combined_path = '../data/Properties for sale Ireland.xlsx'

    if os.path.exists(file_path1) and os.path.exists(file_path2):
        df1 = pd.read_excel(file_path1)
        df2 = pd.read_excel(file_path2)

        combined_df = pd.concat([df1, df2], ignore_index=True)

        # Write the combined DataFrame to a new Excel file
        combined_df.to_excel(output_combined_path, index=False)
        print("Files combined successfully.")
    else:
        print("One or both input files do not exist.")

if __name__ == "__main__":
    main()