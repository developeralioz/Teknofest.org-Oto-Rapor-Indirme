import requests
import re
from bs4 import BeautifulSoup
import os

# "Yarışma Adı" şeklinde klasör açmamızı sağlar.
def createFolderCompetition():
    sectionList = []
    global folder_location
    
    h1 = soup.select("h1")
    for section in h1:
        sectionList.append(section.text)

    competitionName = sectionList[0]
    
    folder_location = rf'{competitionName}'
    if not os.path.exists(folder_location): os.mkdir(folder_location)


def download_PDF_Teknofest(url):
    global soup
    fileType = ".pdf"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    createFolderCompetition()
    links = soup.find_all('a')

    i = 0
    for link in links:
        fileLink = link.get('href', [])

        if fileType in fileLink:
            downloadableLink = re.sub(r"\s+", "", fileLink)

            i += 1
            print("Downloading file: ", i)
            response = requests.get(downloadableLink)

            # Write content in pdf file
            pdf = open(f"{folder_location}/PDF-{i}.pdf", "wb")
            pdf.write(response.content)
            pdf.close()
            print("File ", i, " downloaded")

    print("All PDF files downloaded")


url = "https://teknofest.org/tr/competitions/competition/29"
download_PDF_Teknofest(url)
