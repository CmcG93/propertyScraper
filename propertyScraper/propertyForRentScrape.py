from email.mime.application import MIMEApplication
from tkinter import Tk, Label, StringVar, messagebox, ttk
from propertyScraper.spiders.rentSpider import RentspiderSpider, RentspiderWebTwoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

class GUI:
    def __init__(self, master):
        #os.system("cd ../venv ; .\Scripts\activate ; cd ../propertyScraper")
        self.master = master
        master.title("Irish Property Scraper - TO RENT")
        master.geometry("400x350")  # Set the size of the window

        style = ttk.Style()
        style.theme_use("clam")

        self.label = Label(master, text="Welcome to the Irish Property Scraper tool!\n\nThis tool scrapes property information from listing websites,\nfrom that it creates an Excel for your viewing with inbuilt filters.\nDue to the number of listings, it can take some time to complete.\nOnce done, we email a copy of the results, so enter your details below.\n\n\nWhen submitted the tool will begin running in the background\nThank you!")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label = Label(master, text="Name:")
        self.label.grid(row=4, column=0, padx=10, sticky="w")

        self.nameVar = StringVar()
        self.nameEntry = ttk.Entry(master, textvariable=self.nameVar, width=62)
        self.nameEntry.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.label = Label(master, text="Email Address:")
        self.label.grid(row=6, column=0, padx=10, sticky="w")

        self.emailVar = StringVar()
        self.emailEntry = ttk.Entry(master, textvariable=self.emailVar, width=62)
        self.emailEntry.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.clearButton = ttk.Button(master, text="Clear Text", command=self.clearFields)
        self.clearButton.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.submitButton = ttk.Button(master, text="Submit", command=self.submit)
        self.submitButton.grid(row=8, column=0, padx=10, pady=10, sticky="e")

    def submit(self):
        name = self.nameVar.get()
        email = self.emailVar.get()

        if name and email:
            self.master.destroy()  # Close the GUI

            # Run the spiders
            main()

            # Combine Excel files
            combineExcelFiles()

            # Send email with the combined file
            sendEmail(name, email)
        else:
            messagebox.showinfo("Error", "Please enter both Name and Email Address.")

    def clearFields(self):
        # Clear all text fields
        self.nameVar.set("")
        self.emailVar.set("")

def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # List of spiders to crawl
    spiders = [RentspiderSpider, RentspiderWebTwoSpider]

    for spider in spiders:
        spiderName = spider.name
        outputFile = f'../data/{spiderName}_output.xlsx'

        # Checking if the file exists, and remove it to create a new one
        if os.path.exists(outputFile):
            os.remove(outputFile)

        process.crawl(spider, FEEDS={outputFile: {'format': 'xlsx', 'overwrite': True}})
    
    process.start()

    # Excel files get combined after the spiders have finished
    combineExcelFiles()

def combineExcelFiles():
    dataWebOne = '../propertyScraper/data/rentData_WebOne.xlsx'
    dataWebTwo = '../propertyScraper/data/rentData_WebTwo.xlsx'
    outputCombined = '../data/Properties for rent Ireland.xlsx'

    if os.path.exists(dataWebOne) and os.path.exists(dataWebTwo):
        dataFrameOne = pd.read_excel(dataWebOne)
        dataFrameTwo = pd.read_excel(dataWebTwo)

        combinedDataFrames = pd.concat([dataFrameOne, dataFrameTwo], ignore_index=True)

        # Remove duplicates based on the "address" column
        combinedDataFrames = combinedDataFrames.drop_duplicates(subset='address', keep='first')

        # Write the combined DataFrame to a new Excel file 
        with pd.ExcelWriter(outputCombined, engine='openpyxl', mode='w') as writer:
            combinedDataFrames.to_excel(writer, index=False, sheet_name='Properties For Rent')

            worksheet = writer.sheets['Properties For Rent']
            # Adjust the width of the columns for better readability
            for column in worksheet.columns:
                maxLength = 0
                column = [cell for cell in column]
                try:
                    maxLength = max(len(str(cell.value)) for cell in column)
                    adjustedWidth = (maxLength + 1)
                    worksheet.column_dimensions[column[0].column_letter].width = adjustedWidth
                except (TypeError, AttributeError):
                    pass
            # Add filters to the headings
            for colNum, value in enumerate(combinedDataFrames.columns.values):
                worksheet.auto_filter.ref = worksheet.dimensions
                worksheet.auto_filter.add_filter_column(colNum, list(combinedDataFrames[value].unique()))

        print("Files combined successfully.")
    else:
        print("One or both input files do not exist.")

def sendEmail(name, email):
    load_dotenv()
    # Email configuration
    smtpServer = 'smtp-mail.outlook.com'
    smtpPort = 587
    smtpUsername = os.getenv("SMTP_USERNAME")
    smtpPassword = os.getenv("SMTP_PASSWORD")
    senderEmail = os.getenv("SMTP_USERNAME")
    receiverEmail = email
    subject = 'Irish Property Scraper - Properties for Rent in Ireland'
    body = f'Dear {name},\n\nAttached is the completed file containing properties for rent in Ireland.\n\n1- To start you must enable editing first once the file is opened on your device.\n2- To filter the best initial results go to the Counties tab and click the drop-down arrow and type the location you\'re looking for.\n3- Then the Amenities tab and search for the number of bedrooms or bathrooms required to narrow the results further.\n\nTo clear any filters that you may have set, you remove them by going to Data > Sort & Filter and clicking clear.\n\nBest regards,\nIrish Property Scraper'

    msg = MIMEMultipart()
    msg['From'] = senderEmail
    msg['To'] = receiverEmail
    msg['Subject'] = subject  

    # Attach the body of the email with encoding
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Attach the combined Excel file
    attachmentPath = '../data/Properties for rent Ireland.xlsx'
    with open(attachmentPath, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name='Properties_for_rent_Ireland.xlsx')
        part['Content-Disposition'] = f'attachment; filename=Properties for rent Ireland.xlsx'
        msg.attach(part)

    # Send the email
    with smtplib.SMTP(smtpServer, smtpPort) as server:
        server.starttls()
        server.login(smtpUsername, smtpPassword)
        server.sendmail(senderEmail, receiverEmail, msg.as_bytes())  # Use as_bytes() instead of as_string()

    print("Email sent successfully.")

if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
    root.mainloop()
