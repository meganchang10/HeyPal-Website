HeyPal is data driven website that stores fun activities to do in your local area so you'll never be bored again. Information on the activities is stored in a database which contains a title, location, image, and tags so that users can filter their searches to find free activities or date night activities for example.

To begin using HeyPal, install Vagrant and VirtualBox, then launch the Vagrant Virtual Machine by executing the following commands from a terminal window inside the vagrant directory:

`vagrant up`
`vagrant provision`
`vagrant ssh`

The following commands must be executed from within the virtual machine in a terminal window from the command line.

First, create the database for HeyPal:

`python database_setup.py`

Then populate it with some activities:

`python lotsOfActivities.py`

Finally, execute the program that launches the site:

`python project.py`

Congratulations, the website should be ready for viewing. Open up a browser of your preference and access the HeyPal website by typing into the URL bar:

http://localhost:5000/heypal/

Explore the content! Only authorized users can add, edit, or delete activites on the public main page. However all logged in users have access to their own individual and private "My Activities" page where they can add, edit or delete their activities as they please.


More about HeyPal features:

Users can use a third-party authentication and authorization service (either Facebook or their Google Account) to login. Once logged in, users will have the ability to edit, delete or add new activities. They can also add activities to My Activities (similar to adding to Favorites). The My Activities page is user specific and private. It can only be accessed by the user who created it. Activities on the public page are available for all to see, but can only be editted by authorized users. 

In the flask environment, we create a templates folder that contains all the HTML files, as well as a static folder that will contain all Javascript, CSS files, and images. Templates in Flask are preconfigured to handle escape code (the code we are retrieving from our application and database and putting into our HTML). With HTML escaping, we have access to Python variables and functions.) 

Route decorators @app.route("/path") are used to execute associated functions that will automatically get called whenever the server receives a request with a url that matches its argument. Put another way, decorators bind functions to url paths. We can make this argument dynamic by using something like this: 

`@app.route('/activity/<int:activity_id>/')`

which will pull up a different page depending on the activity_id. We must also define the methods each decorator can handle. They automatically handle "GET" methods, but if you want them to handle "POST" as well, this must be specified as such:

`@app.route('/activity/<int:activity_id>/edit/', methods=['GET','POST'])
def newMenuItem(restaurant_id):`

In this case, we want to edit an activity. Which means we need "GET" to render the appropriate screen which presents a form that the user can fill out with the appropriate information (i.e. name of activity, location, image, etc.). When the user submits this form, we need a "POST" to update the activity in the database and redirect the user to the main screen.

The flash method provides feeback to the user alerting them when a change has been successfully made such as adding a new item. This increases the value of the user experience.

JSON endpoints exist for both Activities and My Activities which provides information on id, name, image, location, log_views, tags, and number of times added to My Activities. SQLAlchemy is used to execute queries on an SQLite database.

Activities have tags that further categorize them so that users can apply a filter to their searches such as "Free Activities" or "Rainy Day Activities". A log_views attribute allows the database to track how many times each Activity is being clicked on, as well as how many times it is being added to "My Activities" (similar to favorites). This information allows the main page of activities to be organized in order of descending popularity so that the most viewed/added Activities are displayed at the top of the page.






