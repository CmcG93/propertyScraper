from email.mime.application import MIMEApplication
from tkinter import Tk, Label,StringVar, messagebox, ttk
from propertyScraper.spiders.rentSpider import RentspiderSpider, RentspiderWebTwoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class GUI:
    def __init__(self, master):
        self.master = master
        #self.StartupPopup()
        master.title("Irish Property Scraper - TO RENT")
        master.geometry("400x350")  # Set the size of the window

        style = ttk.Style()
        style.theme_use("clam")

        self.label = Label(master, text="Welcome to the Irish Property Scraper tool!\n\nThis tool scrapes property information from listing websites,\nfrom that it creates an Excel for your viewing with inbuilt filters.\nDue to the number of listings, it can take some time to complete.\nOnce done, we email a copy of the results, so enter your details below.\n\n\nWhen submitted the tool will begin running in the background\nThank you!")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label = Label(master, text="Name:")
        self.label.grid(row=4, column=0, padx=10, sticky="w")

        self.name_var = StringVar()
        self.name_entry = ttk.Entry(master, textvariable=self.name_var)
        self.name_entry.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.label = Label(master, text="Email Address:")
        self.label.grid(row=6, column=0, padx=10, sticky="w")

        self.email_var = StringVar()
        self.email_entry = ttk.Entry(master, textvariable=self.email_var)
        self.email_entry.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.clear_button = ttk.Button(master, text="Clear Text", command=self.clearFields)
        self.clear_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.submit_button = ttk.Button(master, text="Submit", command=self.submit)
        self.submit_button.grid(row=8, column=0, padx=10, pady=10, sticky="e")

    def submit(self):
        name = self.name_var.get()
        email = self.email_var.get()

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
        self.name_var.set("")
        self.email_var.set("")

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

         # Remove duplicates based on the "address" column
        combinedDataFrames = combinedDataFrames.drop_duplicates(subset='address', keep='first')

        # Write the combined DataFrame to a new Excel file 
        with pd.ExcelWriter(outputCombined, engine='openpyxl', mode='w') as writer:
            combinedDataFrames.to_excel(writer, index=False, sheet_name='Properties For Rent')

            worksheet = writer.sheets['Properties For Rent']
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
            # Add filters to the headings
            for col_num, value in enumerate(combinedDataFrames.columns.values):
                worksheet.auto_filter.ref = worksheet.dimensions
                worksheet.auto_filter.add_filter_column(col_num, list(combinedDataFrames[value].unique()))

        print("Files combined successfully.")
    else:
        print("One or both input files do not exist.")

def sendEmail(name, email):
    # Email configuration
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = 'IrishPropertyScraper@outlook.com'
    smtp_password = 'TempPassword'

    sender_email = 'IrishPropertyScraper@outlook.com'
    receiver_email = email
    subject = 'Irish Property Scraper - Properties for Rent in Ireland'
    body = f'Dear {name},\n\nAttached is the completed file containing properties for rent in Ireland.\n\n1- To start you must enable editing first once the file is opened on your device.\n2- To filter the best initial results go to the Counties tab and click the drop down arrow and type the location your looking for.\n3- Then the Amenities tab and search for the number of bedrooms or bathrooms required to narrow the results further.\n\nTo clear any filters that you may have set you remove them by going to Data > Sort & Filter and clicking clear.\n\nBest regards,\nIrish Property Scraper'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject  

    # Attach the body of the email with encoding
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # Attach the combined Excel file
    attachment_path = '../data/Properties for rent Ireland.xlsx'
    with open(attachment_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name='Properties_for_rent_Ireland.xlsx')
        part['Content-Disposition'] = f'attachment; filename=Properties for rent Ireland.xlsx'
        msg.attach(part)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_bytes())  # Use as_bytes() instead of as_string()

    print("Email sent successfully.")

if __name__ == "__main__":
    root = Tk()
    gui = GUI(root)
    root.mainloop()