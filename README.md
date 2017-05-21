In this app, we CRUD: Create,Read,Update, and Delete. We create a database which stores information about our restaurants, menu items, and users.

In the flask environment, we create a static folder that will contain all Javascript, CSS files and images.

We import the flask class and create an instance of this class which is our application. 

We use route decorators @app.route("/path") which execute their associated functions that will automatically get called whenever the server receives a request with a url that matches its argument. Put another way, decorators bind functions to url paths. We can make this argument dynamic by using something like this: 

`@app.route('/restaurant/<int:restaurant_id>/')`

which will pull up a different page depending on the restaurant_id. We must also define the methods each decorator can handle. They automatically handle "GET" methods, but if you want them to handle "POST" as well, this must be specified as such:

`@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):`

In this case, we want to create a new menu item. Which means we need "GET" to render the appropriate screen which presents a form that the user can fill out with the appropriate information (i.e. name of menu item, price, description, etc.). When the user submits this form, we need a "POST" to create a new instance of the menu item to be added to the database and redirect the user to the menu screen.

We use the flash method to provide feeback to the user alerting them when a change has been successfully made such as adding a new item.

We store our HTML files in the template folder. Flask configures a template engine where we can store our HTML code and use render_template(template_name.html, variable1 = keyword1, variable2 = keyword2, etc.). Templates in Flask are preconfigured to handle escape code (the code we are retrieving from our application and database and putting into our HTML). With HTML escaping, we have access to Python variables and functions.) 

For login, we have included google and facebook login capabilities. We use a unique id and secret which is specific to the app and must be changed directly in both the json files and the login.html template.

We also created JSON endpoints so that APIs can be used easily. We use SQLAlchemy to execute queries. 

This app authorizes all users to view all the restaurant menus stored in our database. However, if they would like to add a restaurant or make changes to an existing entry that they previously created, they must authenticate themselves by logging. They are provided with two options of verification: Google and Facebook.

I have included a log_views attribute for the Activities so that we can track how many times the Activity is being clicked on, as well as how many times it is being added to "My Activities" (similar to favorites). I organize the activities in descending popularity so that the most viewed/added Activities are displayed at the top of the page.

Activities are available for the public, but can only be editted by authorized users. In order to add activities to your favorites (My Activity), the user must login.

Activities have tags that further categorize them
