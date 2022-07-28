import time

import requests
import re
from bs4 import BeautifulSoup
import os

def download_PDF_Teknofest(url):
	fileType = ".pdf"
	response = requests.get(url)

	soup = BeautifulSoup(response.text, 'html.parser')

	competitionNameCharList = []
	h1 = soup.select("h1")
	for section in h1:
		competitionNameCharList.append(section.text)

	competitionName = competitionNameCharList[0]

	folder_location = rf'{competitionName}'
	if not os.path.exists(folder_location): os.mkdir(folder_location)

	links = soup.find_all('a')

	i = 0
	for link in links:
		fileLink = link.get('href', [])

		if fileType in fileLink:
			print(fileLink)
			downloadableLink = re.sub(r"\s+", "", fileLink)
			print(downloadableLink)

			i += 1
			print("Downloading file: ", i)
			response = requests.get(downloadableLink)

			# Write content in pdf file
			pdf = open(f"{folder_location}/PDF-{i}.pdf", "wb")
			pdf.write(response.content)
			pdf.close()
			print("File ", i, " downloaded")
			time.sleep(3)

	print("All PDF files downloaded")

url = "https://teknofest.org/tr/competitions/competition/33"

download_PDF_Teknofest(url)