# Instructions
1. Power on the virtual machine - ICRIS Ubuntu 64-bit
2. Login to the paradox account
3. Open ml-licensees folder on desktop
4. Right click on the folder directory
5. Select "Open Terminal", you are now in directory ~/Desktop/ml-licensees
6. Copy the list of company names to companies.txt, each company should be separated with a new line, e.g.: \
	Superyield Finance Limited \
	Tung Tai Finance Limited \
	Kwong Yee Hing Land & Finance Limited
7. Run command: ./scrape.py
	- Wait until all the companies are scraped
	- The downloaded html are stored in /results folder
	- This will delete all the previously scraped html files, please parse the downloaded html first
	- Find the companies that could not be scraped in skipped.txt
8. Run command: ./parse.py
	- This will parse the downloaded html files in results/ to MongoDB
	- This will delete all the previously parsed items inside MongoDB, please export all the previously parsed items first
9. Run command: ./export.py
	- Find the exported CSV files in export/$latest_datetime_folder
	- This will NOT delete the previously exported files

# Important Notes
1. Try not to terminate the scraper program once it is running.
2. If you terminate the scraper accidentally, please wait for 10 minutes until the next round. Because your previous session on ICRIS prevents you to login once again.
3. After scraping a company, the scraper will sleep for 3 seconds then continue. This will give the server a break. If you wish to modify the sleep time, change line 93 of scrape.py.

 
