The aim of the project was to develop a desktop application using the Python programming language to “scrape” Irish property websites, convert the results and parse them into an excel spreadsheet for the user to view at their discretion.
The idea behind the application is to reduce the time it takes going through multiple websites for properties since it can be very time consuming going between the websites in the attempt to find a suitable property. When triggered the application will run in the background scraping the property websites and give the user the “scraped” information in an easy-to-read spreadsheet that is emailed to their desired email address.

Steps to run:
1. Create a .env file in the outermost section and add a valid email address and password to send the emails from. 
   The variable names have to be SMTP_USERNAME and SMTP_PASSWORD to be able to have the program run correctly.
2. Create a new terminal in the propertyScraper folder.
3. Run "cd ../venv ; .\Scripts\activate ; cd ../propertyScraper" in the terminal to activate the Virtual environment.
4. Run python .\propertyForRentScrape.py in the terminal to get Rented properties.
5. Run python .\propertyForSaleScrape.py in the terminal to get For Sale properties.

*Notes*
- To do a full scrape can take up to 1 hour to fully complete.

- ctrl + c in terminal after the program is running will end the scraping but still send an email with the gathered information.

- The smtpServer on line 148 in both propertyForSaleScrape.py & propertyForRentScrape.py might have to be changed if the email your planning to 
  use is not outlook.

- Currently as it stands the .exe files for the programs launch the GUI correctly but dont run the rest of the program once valid input has been 
  submitted

