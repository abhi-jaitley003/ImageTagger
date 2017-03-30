



from flask import Response
from flask import request
#from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask,url_for,render_template
from DownloadImageService import *
from TagImageService import *
from SetDbDetails import *
import psycopg2
#from Version1.testDb import *
from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import JSON, JSONB

app = Flask(__name__)
dbDetails = SetDbDetails()
dbDetails.setDatabaseConnectionString()
app.config['SQLALCHEMY_DATABASE_URI'] = dbDetails.getDatabaseConnectionString()
db = SQLAlchemy(app)
downloadLocation= input('Enter the download location for images')

class Image(db.Model) :
    """
    This class is used to create a model for the image object that we store in our PostGresSql database.It contains the attributes
    of an Image search query : Querystring, imageUrl, tags, metadata of the image
    """

    queryString = db.Column(db.String(200),primary_key=True)
    imageLink = db.Column(db.String(200))
    tags = db.Column(db.JSON)
    imgMetadata = db.Column(db.JSON)

    def __init__(self,queryString,imageLink,tags,imgMetadata):
        """
           Used to initalize an image object

           :param
               queryString(str) : represents the query string entered by the user
               imageLink(str) :  represents the url of the image
               imgMetadata(JSON object) : represents the metadata of the image in a JSON object
               tags(JSON object ) : represents the image tags associated with an image in a JSON object.
        """

        self.queryString = queryString
        self.imageLink = imageLink
        self.tags = tags
        self.imgMetadata = imgMetadata

@app.route('/image', methods = ['GET'])
def api_message():
    """

    This function is called when we receive a GET request with a /image URI. It receives the query string from the request
    and then prints the result on another page depending on the query

    Args:
        Receives query string from the HTTP GET request

    Returns :
        Renders the Resulting HTML based on the query string


    """
    userAgentString = request.headers.get('User-Agent')
    dis = DownloadImagesService(userAgentString,downloadLocation)
    tis= TagImages()
    db.create_all()
    #db.reflect()
    #db.drop_all()

    if 'query' in request.args:

        downloadStatus=0
        imageTagstatus=0
        imageTags=[]
        metadata = []

        errorMessage = ''


       # print ('received query from ')
       # print (request.args['query'])
        query= request.args['query']

        if len(query) == 0 :
            errorMessage = 'Error : empty query string'
            return render_template("result.html", result=[], imageTagstatus=imageTagstatus,
                                   downloadStatus=downloadStatus, errmsg=errorMessage)

        else :
            myimgs = Image.query.filter_by(queryString=query).all()
            # if len(myimgs) = 0 it means query is not present in db
            if len(myimgs) == 0 :

                #print ('calling download')
                imageUrlList,metadata =  dis.downloadImagesFromSearch(query)
               # print ('printing ImageurlList')
               # print (imageUrlList)
                if len(imageUrlList)==0 :
                    errorMessage = ' unable to download images'
                    downloadStatus=404
                else :
                    downloadStatus=200

                    imageTags,imageTagstatus=tis.getTagsFromUrlList(imageUrlList)
                  #  print ('printing status from image tag service')
                  #  print (imageTagstatus)
                  #  print (type(imageTags))
                    if imageTagstatus!=200 :
                        errorMessage= 'error '+str(imageTagstatus)+' while tagging image(s)'
                    else :
                        #print ('adding to db here')
                        i =0
                        for url in imageTags :


                            metadata[i]['path']=os.getcwd()+metadata[i]['path']
                            img = Image(query ,url ,json.dumps(imageTags[url]),json.dumps(metadata[i])  )
                            db.session.add(img)
                            db.session.commit()
                            i+=1
                        #img = Image(query, url, tagsJson, metadataJson)


                        # print ('displaying current db state')
                        # myimgs = Image.query.all()
                        # for myimg in myimgs:
                        #     print (myimg.queryString)
                        #     print (myimg.imageLink)
                        #     print (myimg.tags)
                        #     print (myimg.imgMetadata)



                return render_template("result.html", result=imageTags,imageTagstatus=imageTagstatus,downloadStatus = downloadStatus,errmsg =errorMessage )
            else :

                #querystring already present in the db fetch data from db in this case
                #print ('query already present in db, fetching from db')
                try :
                    tags=[]
                    dict = {}
                    #myimgs = Image.query.all()
                    myimgs=Image.query.filter_by(queryString=query).all()
                    for myimg in myimgs:

                        tags = myimg.tags
                        json1_data = json.loads(tags)
                        # print (tags)
                        # print (type(tags))
                        # print (type(json1_data))
                        # print (json1_data)
                        url =   (myimg.imageLink)
                        dict[url] = json1_data

                    return render_template('result.html',result =dict,imageTagstatus=200,downloadStatus=200,errmsg=errorMessage)
                except Exception as e:
                    #print ("db error while fetching data ")
                    errorMessage= 'db error while fetching data'
                    return render_template("result.html", result=[], imageTagstatus=400,
                                           downloadStatus=400, errmsg=errorMessage)


@app.route('/')
def frontpage() :
    """
    This function is used to render the front page of the web application when we try to access the URL : http://127.0.0.1:5000/
    """
    return render_template('index.html')

def main() :

    app.run()

if __name__ == '__main__':
    main()
