



from bs4 import BeautifulSoup

import ssl
#import urllib2
import os
import json
import requests
import urllib
import urllib.request
from urllib.request import urlopen

class DownloadImagesService(object):

    """
    This class provides a functionality to download images from google search based on a query string
    The service downloads the image to a specified location and also returns a list of the image urls of images
    which can be used by the tagging service to get the tags for the images
    """

    def __init__(self,ua,location):
        """
        :param ua: User agent for the computer which will be used to construct the header object
        """

        self.directory = location
        self.header ={'User-Agent':ua}

    def extractImagesFromHtml(self,html):
        """
        :param html: the html of the google image search results page
        :return: returns a list of the image urls extracted from the html
        """
        ActualImages = []
        for a in html.find_all("div", {"class": "rg_meta"}):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            ActualImages.append((link, Type))
        #print (ActualImages)
        #print (len(ActualImages))
        return ActualImages

    def get_soup(self,url):

        """
        used to get the html in a form that we can parse using the library beautiful soup
        :param url(str): url of the page that we want to parse using beautiful soup
        :return: html of the url page
        """
        #return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

        soup =None
        ssl._create_default_https_context = ssl._create_unverified_context
        req = urllib.request.Request(url, headers=self.header)
        with urllib.request.urlopen(req) as response:
            soup = BeautifulSoup(response,'html.parser')
        return soup

    def downloadImages(self,ActualImages,query) :
        """
        Used to download the images extracted using from the html of the google search page
        The qquery string is used to create a new folder based on query string

        :param ActualImages(list): A list of image urls that we want to download
        :param query(str): query string for which we need the images
        :return: metadata of the images downloaded
        """


        metadata=[]
        #this dictionary keeps a count of each of the file types and their count in the downloads folder
        #this is important because when we are downloading images we need to name them accordingly
        imageTypes = {'jpg': 0, 'gif': 0, 'png': 0, 'jpeg': 0}
        #print (imageTypes)

        #creating a folder for the downloadedImages
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        #creating a folder for the current query
        dir = os.path.join(self.directory, query)
        #print (dir)
        if not os.path.exists(dir):
            os.mkdir(dir)
        #  for i in range(0,len(ActualImages)) : for 100 image
        for i in range(0,min(1,len(ActualImages))) :
            metadataDict={}
            data = ActualImages[i]
            imageLink = data[0]
            imageType = data[1]
            metadataDict['type'] = imageType
            #print (imageType)
            if(len(imageType) > 0 and imageType in imageTypes) :
                #print (imageType)
                #print (i)
                imageTypes[imageType]+=1
                cnt = imageTypes[imageType]
                try:
                    Image = ''
                    req = urllib.request.Request(imageLink, headers=self.header)
                    with urllib.request.urlopen(req) as response:
                        Image = response.read()
                    #req = request(imageLink, headers={'User-Agent': self.header})
                    #Image = urllib2.urlopen(req).read()
                    #creating the exact file path for the image
                    metadataDict['path'] = os.path.join(dir, imageType + "_" + str(cnt) + "." + imageType)
                    f = open(os.path.join(dir, imageType + "_" + str(cnt) + "." + imageType), 'wb')
                    # print dir
                    f.write(Image)
                    f.close()
                    metadata.append(metadataDict)

                except Exception as e:
                    print ("could not load : " + imageLink)
                    #print (e)
            else:
                imageType = 'jpg'
                metadataDict['type'] = imageType
                #print (imageType)
                #print (i)
                imageTypes[imageType] += 1
                cnt = imageTypes[imageType]
                try:
                    #req = requests.get(imageLink,headers = {'User-Agent': self.header})
                    #req = urllib.Request(imageLink, headers={'User-Agent': self.header})
                    #Image = urllib2.urlopen(req).read()
                    Image = ''
                    req = urllib.request.Request(imageLink, headers=self.header)
                    with urllib.request.urlopen(req) as response:
                        Image = response.read()
                    # creating the exact file path for the image
                    metadataDict['path'] = os.path.join(dir, imageType + "_" + str(cnt) + "." + imageType)
                    f = open(os.path.join(dir, imageType + "_" + str(cnt) + "." + imageType), 'wb')
                    # print dir
                    f.write(Image)
                    f.close()
                    metadata.append(metadataDict)
                except Exception as e:
                     print ("could not load : " + imageLink)
                    # print (e)
        return metadata

    def downloadImagesFromSearch(self,query):
        """
        performs all the tasks invovlved in  downloading images like getting html of results page and then parsing the html and extracting img links and
        finally to download the images

        :param query(str): query string for image
        :return:
            imageLinksList(list) : a list of image url strings
            metdata(list) :  metadata of the images
        """
        query = query.split()
        query = '+'.join(query)
        prettyHtml = self.getHtml(query)
        imageLinksList  = self.extractImagesFromHtml(prettyHtml)
        #print (len(imageLinksList))
        #print (imageLinksList)
        if len(imageLinksList) == 0 :
            return imageLinksList,[]
        metadata = self.downloadImages(imageLinksList,query)
        #print ('printing metadata of downloaded images ')
        #print (metadata)
        return imageLinksList[:1],metadata

    def getHtml(self,query):
        """
        gets the html from the google search results page

        :param query(str): query string
        :return: returns the beautiful soup version of html of the search results page
        """

        #print(query)
        #print (query.split()[0])
        url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
        #print (url)
        return self.get_soup(url)
    #print(html)

def main():
    downloads = DownloadImagesService()

    query = "harry potter"
    downloads.downloadImagesFromSearch(query)

if __name__ == '__main__':
    main()



