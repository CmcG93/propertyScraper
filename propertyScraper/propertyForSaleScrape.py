from propertyScraper.spiders.propertySpider import PropertyspiderSpider
from propertyScraper.spiders.propertySpider import PropertyspiderWebThreeSpider
from propertyScraper.spiders.propertySpider import PropertyspiderWebTwoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
from openpyxl import Workbook
import os

def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # List of spiders to crawl
    spiders = [PropertyspiderSpider, PropertyspiderWebTwoSpider, PropertyspiderWebThreeSpider]

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
    Data_WebOne = '../propertyScraper/data/propertyData_WebOne.xlsx'
    Data_WebTwo = '../propertyScraper/data/propertyData_WebTwo.xlsx'
    Data_WebThree = '../propertyScraper/data/propertyData_WebThree.xlsx'
    outputCombined = '../data/Properties for sale Ireland.xlsx'

    if os.path.exists(Data_WebOne) and os.path.exists(Data_WebTwo) and os.path.exists(Data_WebThree):
        dataFrameOne = pd.read_excel(Data_WebOne)
        dataFrameTwo = pd.read_excel(Data_WebTwo)
        dataFrameThree = pd.read_excel(Data_WebThree)

        combinedDataFrames = pd.concat([dataFrameOne, dataFrameTwo, dataFrameThree], ignore_index=True)

        # Remove duplicates based on the "address" column
        combinedDataFrames = combinedDataFrames.drop_duplicates(subset='address', keep='first')

        # Write the combined DataFrame to a new Excel file 
        with pd.ExcelWriter(outputCombined, engine='openpyxl', mode='w') as writer:
            combinedDataFrames.to_excel(writer, index=False, sheet_name='Properties For Sale')

            worksheet = writer.sheets['Properties For Sale']
            #adjusting the width of the columns for better readability
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                try:
                    max_length = max(len(str(cell.value)) for cell in column)
                    adjusted_width = (max_length + 1)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
                except (TypeError, AttributeError):
                    pass

        print("Files combined successfully.")
    else:
        print("One or both input files do not exist.")

if __name__ == "__main__":
    main()