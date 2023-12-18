from propertyScraper.spiders.propertySpider import PropertyspiderSpider
from propertyScraper.spiders.rentSpider import RentspiderSpider
from propertyScraper.spiders.propertySpiderWebTwo import PropertyspiderWebTwoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(PropertyspiderSpider)
    process.crawl(PropertyspiderWebTwoSpider)
    process.crawl(RentspiderSpider)
    process.start()

if __name__ == "__main__":
    main()