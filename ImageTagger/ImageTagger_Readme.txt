

Description :
	Image Tagger is a simple web application developed using Python that takes in a query from the user, downloads all the images related to that topic from google search page results to the local computer, and displays that image along with image tags that describe what the image is all about. (Imagga API is used to get the image tags for an image).



Prerequisites:

	-Python 3.6
	-Postgres database
	-Install the packages by running the bash script
	
Installation : 
	
	To install the packages run the install.sh file. If there is some issue installing a package then please refer to the packages and the versions below to install manually
	using pip install or using the functionality in an IDE.
	
	Package          	Version
  
	Flask	      		0.12 
	Flask-SQLAlchemy 	2.2
	Jinja2			2.9.5
	MarkupSafe		1.0
	SQLAlchemy		1.1.6
	Werkzeug		0.12.1
	beautifulsoup4		4.5.3
	bs4			0.0.1
	click			6.7
	itsdangerous		0.24
	psycopg2		2.7.1
	requests		2.13.0
	urrlib3			1.20
	yield.urllib.request	0.1.1
	

Configuration:
	The Application requires a Postgres database and  we need to enter the name of the database  inside which the code creates the table named ‘image’.We also need to enter 	the user details for the connection.On running the application the program will prompt the user for the name of the database in postgres along with the username and 		password for the same. The database is used to cache the queries that have already been searched by the user and if the query has been already searched the data for that 	image is restored from the cache instead of searching and downloading again. 
	
Running the application:
	Run the app.py file located in the src package inside the project ImageTagger2 directory. The user will be prompted to enter the database connection and download location 	details through the console.Once that is done, open http://127.0.0.1:5000/ url in the browser to get the frontage of the app. Enter the search query and hit submit 	button. 	The image along with the tags will be returned. Use the back button in the browser to navigate back to the frontage.

Built with :
	Flask (Web application framework)
	Jinja2(Rendering HTML template framework)
	SQLAlchemy(Connecting the application with Postgres, providing object relational mapping)

Author:
	Abhishek Jaitley
