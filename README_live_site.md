

## Linux Server Configuration

For this project, I launched a virtual private web server through Amazon Lightwail. I used the Ubuntu computer operating system based on the Linux distribution, and an Apache web server to host my web application, HeyPal.

HeyPal is a social network that is actually designed to make you more social. It suggests fun local activities to you and takes the effort out of event planning. HeyPal provides you with awesome ideas, so you can focus on what matters, your pals! All you have to do is send the invite.

You can access the final website at [http://ec2-52-15-196-144.us-east-2.compute.amazonaws.com/]. The IP Address is 52.15.196.144

## Setup

We start at the begining. First I created an AWS account. Then select Launch a Virtual Machine with EC2. Go through all the steps to create an instance. Generate a key-pair (first_key_pair.pem) and download it into your .ssh folder.  Then cd into this folder. Use chmod to change the access permissions on the .pem files:

home$ `chmod 700 first_key_pair.pem`

## User Management

To connect to the Linux server from a remote location, we must employ the ssh command which specifies the private key (.pem) file and user_name@public_dns_name. For Ubuntu, the user name is ubuntu or root. Type the following command in the terminal (replacing PATHNAME with the actual path to the .pem file (i.e. )):

home$ `ssh -i PATHNAME/.ssh/first_key_pair.pem ubuntu@ec2-52-15-196-144.us-east-2.compute.amazonaws.com`

Now, you should see a message "Welcome to Ubuntu" and the command text line should now start with ubuntu@ip-172-31-6-85:~$

Now that we are connected to the server, we must first update the installed software on our server.

ubuntu@ip-172-31-6-85:~$ `sudo apt-get update`
ubuntu@ip-172-31-6-85:~$ `sudo apt-get upgrade`

Next I wanted to add a new user as a security measure and disable the ability for root and ubuntu to login remotely to stop hackers.

ubuntu@ip-172-31-6-85:~$ `sudo adduser student`

I used the same key-pair for each user, by first creating an ssh folder, then copying the authorized_keys file to the new user:

ubuntu@ip-172-31-6-85:~$ `sudo mkdir /home/student/.ssh`
ubuntu@ip-172-31-6-85:~$ `sudo cp /home/ubuntu/.ssh/authorized_keys /home/student/.ssh/`

Then change ownership to student for both the user and group:

ubuntu@ip-172-31-6-85:~$ `sudo chown student:student /home/student/.ssh`
ubuntu@ip-172-31-6-85:~$ `sudo chown student:student /home/student/.ssh/authorized_keys`

Then grant permission:

ubuntu@ip-172-31-6-85:~$ `sudo chmod 700 /home/student/.ssh`
ubuntu@ip-172-31-6-85:~$ `sudo chmod 700 /home/student/.ssh/authorized_keys`

Now, the student should be able to login remotely using the same ssh command as befored with the user_name student now:

home$ `ssh -i PATHNAME/.ssh/first_key_pair.pem student@ec2-52-15-196-144.us-east-2.compute.amazonaws.com`

To grant sudo access to student user, we first create a file for the user in the sudoers.d directory, then add a line that grants access:

ubuntu@ip-172-31-6-85:~$ `sudo touch /etc/sudoers.d/student`

>student ALL=(ALL) NOPASSWD:ALL

This process is necessary for the first sudoer user. Henceforth, we can simply copy this file using (and inputting the new user_name):
ubuntu@ip-172-31-6-85:~$ `sudo cp /etc/sudoers.d/student /etc/sudoers.d/user_name`

And editting the file by replacing the student part with the user_name:
ubuntu@ip-172-31-6-85:~$ `sudo nano /etc/sudoers.d/user_name`
>user_name ALL=(ALL) NOPASSWD:ALL

## Security

Next, we worked with setting up the firewall. Make sure the firewall is inactive while configurations are made by checking

ubuntu@ip-172-31-6-85:~$ `sudo ufw status`

Which should give a response of:

> Status: inactive

This is important because if the firewall is active, one can accidentally lock themselves out of the server and be forced to start the Linux configuration over with a new server.

We begin with defaults for all incoming and outgoing connections:

ubuntu@ip-172-31-6-85:~$ `sudo ufw default deny incoming`
ubuntu@ip-172-31-6-85:~$ `sudo ufw default allow outgoing`

It is a good practice to block everything coming in and only allow what you need. Now, we go through and allow the ports we know our server will need to support:

ubuntu@ip-172-31-6-85:~$ `sudo ufw allow ssh`
ubuntu@ip-172-31-6-85:~$ `sudo ufw allow 2200/tcp`
ubuntu@ip-172-31-6-85:~$ `sudo ufw allow www`
ubuntu@ip-172-31-6-85:~$ `sudo ufw allow 123/tcp`

Be sure that you are using the correct port number for 2200/tcp as this may vary depending on the setup. It could also be 22 or 2222 for example. We must also change the setting on the Amazon Lightsail side. Under Network & Security, Security Groups, Inbound, add the appropriate TCP protocols including allowing Port 2200. 

Next, we enforce key-based SSH authentication in

ubuntu@ip-172-31-6-85:~$ `sudo nano /etc/ssh/sshd_config`

and make sure the following lines are as written:

>   Port 2200
>   PasswordAuthentication no
>   PermitRootLogin no

Restart the ssh service:

ubuntu@ip-172-31-6-85:~$ `sudo service ssh restart`

## Installing Apache and mod-wsgi

Execute the following command

student@ip-172-31-6-85:~$ `sudo apt-get install apache2`

Now, when you navigate to the page, it should show the Apache Ubuntu Default page! Next, we will install mod-wsgi:

student@ip-172-31-6-85:~$ `sudo apt-get install libapache2-mod-wsgi python-dev`
student@ip-172-31-6-85:~$ `sudo apt-get install python-setuptools libapache2-mod-wsgi`
student@ip-172-31-6-85:~$ `sudo service apache2 restart`

Configure Apache to handle requests using the WSGI module by changing the following 2 files:

student@ip-172-31-6-85:~$ `sudo nano /etc/apache2/sites-enabled/000-default.conf`
student@ip-172-31-6-85:~$ `sudo nano /etc/apache2/sites-available/heypal.conf`

to contain the following information:

>   <VirtualHost *:80>
>   ServerName 52.15.196.144
>   ServerAdmin meganchang10@gmail.com
>   ServerAlias ec2-52-15-196-144.us-east-2.compute.amazonaws.com
>   DocumentRoot /var/www/HeyPal
>   ErrorLog ${APACHE_LOG_DIR}/error.log
>   CustomLog ${APACHE_LOG_DIR}/access.log combined
>   Alias /log/ "/var/log/"
>   <Directory "/var/log/">
>   Options Indexes MultiViews FollowSymLinks
>   AllowOverride None
>   Order deny,allow
>   Deny from all
>   Allow from all
>   Require all granted
>   </Directory>
>   WSGIScriptAlias / /var/www/HeyPal/heypal.wsgi
>   </VirtualHost>

Then restart the apache server

student@ip-172-31-6-85:~$ `sudo service apache2 restart`

Make sure module wsgi is enabled

student@ip-172-31-6-85:~$ `sudo a2enmod wsgi`


## Configure local time zone to UTC

Execute the following command:

student@ip-172-31-6-85:~$ `sudo dpkg-reconfigure tzdata`

Options should pop up. First choose None of the Above, then choose UTC.

## Clone my Application

A specific structure is necessary for everything to work, so we will create that now.

First, make sure git is installed:

student@ip-172-31-6-85:~$ `sudo apt-get install git`

Now cd into the www directory:

student@ip-172-31-6-85:~$ `cd /var/www`

Setup a directory folder:

student@ip-172-31-6-85:/var/www$ `sudo mkdir HeyPal`

Now cd into this directory and clone the git repository for the HeyPal website, renaming it to simply heypal:

student@ip-172-31-6-85:/var/www/HeyPal$ `sudo git clone https://github.com/meganchang10/HeyPal-Website.git heypal`



## Installing a Virtual Environment with the Required Packages

Now, we are ready to install our virtual environment and the necessary packages to run HeyPal. We run the following commands to install the virtual environment renaming it venv for short and granting it all permissions. Then we activate it.

student@ip-172-31-6-85:~$ `sudo apt-get install python-pip`
student@ip-172-31-6-85:~$ `sudo pip install virtualenv`

student@ip-172-31-6-85:~$ `sudo virtualenv venv`
student@ip-172-31-6-85:~$ `sudo chmod -R 777 venv`
student@ip-172-31-6-85:~$ `source ~/venv/bin/activate`

You should see a (venv) at the start of the command line. This is how you know the virtual environment is activated:

(venv) student@ip-172-31-6-85:~$ 

From inside the virtual environment, install all required packages using the requirements.txt found in the heypal git you just cloned. This requirements.txt file was created using the pip freeze command and lists all dependencies necessary to run HeyPal. To see these dependencies, please view the requirements.txt file in the GitHub repository:

(venv) student@ip-172-31-6-85:~$ `sudo apt-get install python-setuptools`
(venv) student@ip-172-31-6-85:~$ `sudo apt-get install python-psycopg2`
(venv) student@ip-172-31-6-85:~$ `sudo -H pip install -r /var/www/HeyPal/heypal/requirements.txt`

You can check to make sure everything was installed correctly using:

(venv) student@ip-172-31-6-85:~$ `sudo -H pip freeze`

which should display all the installed modules. NOTE: The -H option is important here. Not using this flag will give you the incorrect information.

Now we need to change a few files to contain the script below: 

student@ip-172-31-6-85:~$ `sudo nano /etc/apache2/sites-enabled/000-default.conf`
student@ip-172-31-6-85:~$ `sudo nano /etc/apache2/sites-available/heypal.conf`

<VirtualHost *:80>
ServerName 52.15.196.144
ServerAdmin meganchang10@gmail.com
ServerAlias ec2-52-15-196-144.us-east-2.compute.amazonaws.com

WSGIScriptAlias / /var/www/HeyPal/heypal.wsgi
<Directory /var/www/HeyPal/heypal/>
Order allow,deny
Allow from all
</Directory>
Alias /static /var/www/HeyPal/heypal/static
<Directory /var/www/HeyPal/heypal/static/>
Order allow,deny
Allow from all
</Directory>
ErrorLog ${APACHE_LOG_DIR}/error.log
LogLevel warn
CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

In addition, we will create a .wsgi file in the HeyPal directory to automatically activate the virtual encironment and run the application.

student@ip-172-31-6-85:$ `sudo nano /var/www/HeyPal/heypal.wsgi`

And type the following in the heypal.wsgi file: 

>#!/usr/sbin/apache2
>
>import sys
>import logging
>
>activate_this = '/home/student/venv/bin/activate_this.py'
>execfile(activate_this, dict(__file__=activate_this))
>logging.basicConfig(stream=sys.stderr)
>sys.path.insert(0,"/var/www/HeyPal/")
>
>from heypal import app as application
>application.secret_key = 'super_secret_key'

Finally, we enable the virtual host using:

student@ip-172-31-6-85:~$ `sudo a2ensite heypal`


## Install PSQL

To install PSQL:

(venv) student@ip-172-31-6-85:~$ `sudo apt-get install postgresql`
(venv) student@ip-172-31-6-85:~$ `sudo apt-get install postgresql-contrib`

In each file that this line is present: 

`engine = create_engine('sqlite:///heypal.db')`

change it to accomadate a PSQL database instead. The structure of this line is postgresql://username:password@host:port/database:

`engine = create_engine('postgresql://heypal:super_secret_password@localhost/heypal')`

In my case, it is the files: database_setup.py, __init__.py, lotsOfActivities.py, and filterSearchResults.py

student@ip-172-31-6-85:/var/www/HeyPal/heypal$ `sudo nano database_setup.py`
student@ip-172-31-6-85:/var/www/HeyPal/heypal$ `sudo nano project.py`
student@ip-172-31-6-85:/var/www/HeyPal/heypal$ `sudo nano lotsOfActivities.py`
student@ip-172-31-6-85:/var/www/HeyPal/heypal$ `sudo nano filterSearchResults.py`

Now, we can create the heypal PSQL database using the following steps (Note: This same process can be used if you want to reset your database up, so step 2 can be skipped the first time around):

1) Stop the apache2 server running
2) Delete the current heypal database using dropdp (skip this step if it's the first time)
3) Change to the default user postgres
4) Connect to the PSQL database
5) Create a new heypal database with owner heypal
6) Connect to the heypal database
7) Revoke all rights on the heypal database schema
8) Grant access only to user heypal
9) Exit postgresql
10) Exit postgres user
11) Start the apache2 server 
12) Change directories
13) Setup database


1) student@ip-172-31-6-85:~$ `sudo service apache2 stop`
2) student@ip-172-31-6-85:~$ `sudo -u postgres dropdb heypal`
3) student@ip-172-31-6-85:~$ `sudo su - postgres`
4) postgres@ip-172-31-6-85:~$ `psql`
5) postgres=# `CREATE DATABASE heypal WITH OWNER heypal;`
6) postgres=# `\c heypal`
7) heypal=# `REVOKE ALL ON SCHEMA public FROM public;`
8) heypal=# `GRANT ALL ON SCHEMA public TO heypal;`
9) heypal=# `\q`
10) postgres@ip-172-31-6-85:~$ `\exit`
11) student@ip-172-31-6-85:~$ `sudo service apache2 start`
12) student@ip-172-31-6-85:~$ `cd /var/www/HeyPal/heypal`
13) student@ip-172-31-6-85: /var/www/HeyPal/heypal$ `python database_setup.py`


## JSON files

We need to add an absolute path to any secret json files we have so that the third party authentication will work. So anywhere that a .json file is accessed, add the absolute path to the beginning like so:

> /var/www/HeyPal/heypal/client_secrets.json

In my case, this affected the __init__.py and login_handler.py files.

Furthermore, you will have to go to Facebook [https://developers.facebook.com/] to change the Valid OAuth redirect URIs. Finding this can be hard as they are often changing the location and names, but at the time of writing this README, this could be done by clicking on your app (HeyPal) from the dropdown menu at the top right. Then on the nav menu on the left, click on Facebook Login under Products. Then from within Client OAuth Settings there should be a section under Valid OAuth redirect URIs where you can add URIs. Add the link to your site. In my case [http://ec2-52-15-196-144.us-east-2.compute.amazonaws.com/].

For google, you follow a similar process, and remember to redownload the JSON file with the new permissions.


## Populating the Database

To populate the database :

14) Sign into HeyPal through FB to become user 1
15) student@ip-172-31-6-85:/var/www/HeyPal/heypal$ `python lotsOfActivities.py`

Now restart the apache server:

(venv) student@ip-172-31-6-85:$ `sudo service apache2 restart`

## Updating the git

If you are working on your website locally, and updating things on the github, you can use the following lines to re clone the updated version of your git:

student@ip-172-31-6-85:/var/www/HeyPal$ `sudo rm -rf heypal`
student@ip-172-31-6-85:/var/www/HeyPal$ `sudo git clone https://github.com/meganchang10/HeyPal-Website.git heypal`

## Debugging

When in doubt, restart the apache server:

student@ip-172-31-6-85:$ `sudo service apache2 restart`

If errors occur loading the page, check the error log:

student@ip-172-31-6-85:~$ `sudo tail -50 /var/log/apache2/error.log`

To check that sites are enabled:

student@ip-172-31-6-85:/etc/apache2/sites-available$ `ls -alh /etc/apache2/sites-enabled/`


## Resources Used

[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html]
[https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps]
[http://askubuntu.com/questions/138423/how-do-i-change-my-timezone-to-utc-gmt]
[https://stackoverflow.com/questions/7225900/how-to-pip-install-packages-according-to-requirements-txt-from-a-local-directory]
[http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/]


For README help:
[http://dillinger.io/]
[https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#blockquotes]


