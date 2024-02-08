The aim of the project was to develop a desktop application using the Python programming language to “scrape” Irish property websites, convert the results and parse them into an excel spreadsheet
Steps to run:
1.  Create a .env file in the outermost section and add a valid email address and password to send the emails from. 
    The variable names have to be SMTP_USERNAME and SMTP_PASSWORD to be able to have the program run correctly.

2.  Create a new terminal in the propertyScraper folder should look like this: PS C:\Users\<NAME>\Desktop\propertyScraper-main\

3.  Run "mkdir data" in the termial to create a data folder.

4.  Run "python -m virtualenv venv" to install virtual environment. 

5.  Run "cd venv ; .\Scripts\activate ; cd ../propertyScraper" in the terminal to activate the Virtual environment.

6.  Run "pip install Scrapy pandas python-dotenv scrapy-xlsx" to install required packages.

10. Run python .\propertyForRentScrape.py in the terminal to get Rented properties.

11. Run python .\propertyForSaleScrape.py in the terminal to get For Sale properties.

*Notes*
- To do a full scrape can take up to 1 hour to fully complete for the For Sale option 10-15 for the For Rent.

- ctrl + c in terminal after the program is running will end the scraping but still send an email with the gathered information.

- The smtpServer on line 148 in both propertyForSaleScrape.py & propertyForRentScrape.py might have to be changed if the email your planning to 
  use is not outlook.

- Currently as it stands the .exe files for the programs launch the GUI correctly but dont run the rest of the program once valid input has been 
  submitted.

- If an error occurs after the program has been working where it fails to send an email the email account might have ben flagged check if the
  account needs re-activation.

![UML](https://github.com/CmcG93/propertyScraper/assets/131525742/90051f46-cfb4-4d03-970e-faa180beb012)
