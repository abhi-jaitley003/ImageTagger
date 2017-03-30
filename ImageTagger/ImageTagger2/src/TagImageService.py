

import json
import requests


class TagImages :
     """
     This class provides a service to get tags for an image using the imagga api. There are various ways to use the immage API
     to fetch the tags that is by uploading a file or by sending the image url this class provides the fucntionality to use all the methods
     available to fetch the tags for an image.
     """

     def __init__(self):
        """
              Used to initialize an object of the Tag images class
              Sets the value of an api key and secret that will be used to access the immaga api.
        """
        #print ("Object created")
        self.apikey='acc_4fc1a435b3188b5'
        self.secret = 'f49c4be14a048d5de7e7f6c564b52022'
        self.fileToIdMap = {}

     def uploadFile(self,path):
         """

         Used to upload a file using the imagga API and recevies a resource Id in response from the API that
              can be used later to fetch the tags for that image


            :param path :
                    The file path where the image that we want to upload is located
         """

         response = requests.post('https://api.imagga.com/v1/content',
                    auth=(self.apikey, self.secret),
                    files={'image': open(path, 'r')})
         json_data = json.loads(response.text)
         uploadedData=json_data[u'uploaded'][0]
         resourceId=uploadedData[u'id']
         filename = uploadedData[u'filename']
         self.fileToIdMap[filename] = resourceId
         self.getTagsUsingId(resourceId)

     def getTagsUsingId(self,resourceId):
          """
              This function is used to get tags from the imagga API using the resource Id of an image that has been already
              uploaded suing the API

              :param
                resourceId(string) : the resource Id of the image that has already been uploaded using the API

          """
          response = requests.get('https://api.imagga.com/v1/tagging?content=%s' % resourceId,
                     auth=(self.apikey, self.secret))
          #print ('printing response')
          #print (response.json())

     def getTagsFromUrlList(self,ImageUrlList):

         """
            Used to get the correspoinding tags for an image using the Imagga api . Sends the URL of the image to the immaga
            Web Service and receives the tags
            :param ImageUrlList : List of image urls for which the tags are required
            :returns
               dict(dict) :  a dictionary which maps image url to the tags for that image
               status(int) ; status code in the response received from the imagga api

         """
         dict={}
         #print ImageUrlList
         #print ('printing each url')
         for imageUrl in ImageUrlList :
             #print (imageUrl[0])
             tagsJson,status = self.getTagsUsingImageUrl(imageUrl[0])
             tagList,jsonParseStatus=self.parseJson(tagsJson)
             dict[imageUrl[0]]=tagList
         #print (dict)
         return dict,max(status,jsonParseStatus)

     def getTagsUsingImageUrl(self,ImageUrl):
         """
         Used to get the tags for a single image

         :param ImageUrl: the image url of the image for which the tags are required
         :return:
                response(response) :  the response from the api containing the tags
                status(int) : value representing the status code in the response

         """
         #print ('printing type')
         #print (type(ImageUrl))
         response = requests.get('https://api.imagga.com/v1/tagging?url=%s' %ImageUrl,
                                 auth=(self.apikey, self.secret))
         status = response.status_code
         return response,status

     def parseJson(self,tagsJson):
         """
         :param tagsJson: The tags object received from the imagga api
         :return:
            taglist(list) : a list of tags obtained by parsing the JSON received from the Imagga API.
            status (int)  : if there is an error while parsing the JSON returns 400 as status otherwise 200(OK)
         """
         taglist = []
         try :
             json_data = json.loads(tagsJson.text)
             results = json_data['results'][0]
             #print (results)
             tags = results['tags']
             #print (tags)
             for currentDict in tags :
                currentConfidence = currentDict['confidence']
                currentTag = currentDict['tag']
                taglist.append(currentTag)
             return  taglist,200
         except Exception as e:
             #print ('exception while parsing json')
             return taglist,400

def main():
    tags = TagImages()
    #print 'creating tags'
    #path='/Users/abhishekjaitley/PycharmProjects/Image/Backend/DownloadedImages/harry+potter/jpg_1.jpg'
    #tags.uploadFile(path)
    dict = {'http://s.hswstatic.com/gif/water-life-crop.jpg':'jpg'}
    tags.getTagsFromUrlList(dict)

if __name__ == '__main__':
    main()