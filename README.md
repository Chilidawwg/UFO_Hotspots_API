# UFO Hotspot Sightings API

IMPORTANT: Make sure you read the requirements.txt file and install all the required libraries.

#### Installation/Setup

I chose to use django as my framework for this project because it is very versatile and sleek.
Also the admin abilities are amazing for CRUD and RESTful services.

#####We need to make our environment first.



I recommend going to Anaconda's site to download the desktop application. Here is the link https://www.anaconda.com/distribution/#download-section.

Once that is download follow these steps in your terminal to get your environment started:

        $conda create --name enter_name_here python=3.7        
        $source activate enter_name_here (If using windows it would be just "activate enter_name_here"
        $cd enter_name_here

Now lets install Django:

        $conda install django

Once we have django installed lets get the framework for our API running:

        $django-admin startproject ufo_hotspots
        $cd ufo_hotspots
        
You should now see these files
        
        $__init__.py asgi.py settings.py urls.py wsgi.py manage.py
        
Now that our framework is up we can get the ball rollin

Lets take our sightings_data.csv file that has been provided and pull it into our base_directory

Once we have that done go to the settings.py file and add the database credentials

        #ufo_hotspots/ufo_hotspots/settings.py
        
        DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sightings',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}


Save the settings.py file and jump back over to the base_directory.

So our Mysql database is ready to connect now lets connect to it and migrate to it. Make sure you cd into the ufo_hotspots folder that has the manage.py folder:

        $python manage.py makemigrations
        $python manage.py migrate
        
Great we have migrated to our database now lets test run the server:

        $python manage.py runserver
        
You should now be able to open up your internet browser and go to http:\\\127.0.0.0.1:8000 where it show's your site running.

Lets now get our data into the database: 

1. Use the data_import_tool that has been provided and drag it into our base_directory along with our sightings_data.csv file.
2. Here is the code on how on how to build our data tool to transfer our data to our MYSQL database.
  * I used Pandas to read and structure the data for the database.
  * SQLalchemy was used to gain access to our database so we can import the data.
 
        from sqlalchemy import create_engine 
        import pandas as pd
        
        # read CSV file
        
        column_names = ['date_time', 'shape', 'duration', 'city', 'state', 'latitude', 'longitude', 'comments']
        df = pd.read_csv('sightings_data.csv', header=None, names=column_names)
        
        print(df)
        
        df = pd.read_csv('sightings_data.csv', header=0)
        print(df)
        
        # get authenticated by database and import csv.
        engine = create_engine('mysql://root:root@127.0.0.1/sightings', pool_pre_ping=True)
        with engine.connect() as conn, conn.begin():
        df.to_sql('ufo_api_sighting', conn, if_exists='append', index=False)

Open up your terminal and lets run the script:
 
        $python data_import_tool.py
        
So we have our database up and running. Now lets get the web app running. Note# should already have these files that were provided but will show how to create the app anyways.

Open your terminal inside your base directory and run this:

        $django-admin startapp ufo_api
        #should see these files added to app directory.
        $ migrations __init__.py admin.py apps.py models.py test.py 
        #files provided will have all of these files along with serializers.py and urls.py if you aren't building from scratch.

We got our app structure now so lets get the required code implemented in our files to get it running.

Open the models.py file in the ufo_api app folder and make sure this code is in there:
        
        from django.db import models
        
        # Create your models here.
        # This file will allow us to interacte our database table
         
        date_time = 'id'
        class Sighting(models.Model):
        date_time = models.CharField(primary_key=True, max_length=100)
        shape = models.CharField(max_length=100)
        duration = models.CharField(max_length=100)
        city = models.CharField(max_length=100)
        state = models.CharField(max_length=100)
        latitude = models.CharField(max_length=100)
        longitude = models.CharField(max_length=100)
        comments = models.TextField(max_length=100)

        class Meta:
            ordering = ['date_time']

        def __str__(self):
            return self.date_time

Now lets edit our serialzers.py file so we can implement the Django Rest Framework:

        #so we can access all the fields in our database
        
        from rest_framework import serializers
        from ufo_api.models import Sighting


        class SightingSerializer(serializers.ModelSerializer):
            class Meta:
                model = Sighting
                fields = '__all__'
                
Next we will edit our views.py file:

        #so we can view and interact with the data
        
        from rest_framework import generics
        from ufo_api.models import Sighting
        from ufo_api.serializers import SightingSerializer


        class UFOData(generics.ListCreateAPIView):
            queryset = Sighting.objects.all()
            serializer_class = SightingSerializer


        class UFODataDetails(generics.RetrieveUpdateDestroyAPIView):
            queryset = Sighting.objects.all()
            serializer_class = SightingSerializer
            
We now need to set our views path to our urls.py file so we can view the app on our site:

        from django.urls import path
        from rest_framework.urlpatterns import format_suffix_patterns
        from ufo_api import views

        urlpatterns = [
            path('ufo_api/', views.UFOData.as_view()),
            path('ufo_api/<int:pk>/', views.UFODataDetails.as_view()),
        ]
        urlpatterns = format_suffix_patterns(urlpatterns)
        
Ok great. Let's add our app to the apps.py file:

        from django.apps import AppConfig


        class UfoApiConfig(AppConfig):
            name = 'ufo_api'
            
Also we need to add our app and the rest framework to our apps section of our ufo_hotspots settings.py file:

        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'ufo_api',
            'rest_framework',
        ]
        
Add code to admin.py:

        from django.contrib import admin

        from ufo_api.models import Sighting

        # make models data available in admin site
        
        admin.site.register(Sighting)
        
Now you should be able to open your command prompt create your admin profile to access admin site:

        $python manage.py createsuperuser
        # it will ask you to create credentials
        
Lets run the server and login to the admin site.

        $python manage.py runserver

Now got to your browser and type in http//:127.0.0.0.1:8000/admin and login.
From here you can create, read, update and deleted the sightings data.

Now if you want to access the Rest Framework. Type in http//:127.0.0.0.1:8000/ufo_api.
From here you can make post, get, and update requests via api or json format.

###Solution

To access the data for all the sightings within a 750 mile radius of the UFO hot spots, open up your terminal and enter the following:

        $mysql
        mysql<SELECT
                sightings.ufo_api_sighting.date_time,shape,duration,city,state,latitude,longitude,comments,(
                3959 * acos (
                    cos ( radians(38.897663) )
                    * cos( radians( latitude ) )
                    * cos( radians( longitude ) - radians(-77.036575) )
                    + sin ( radians(38.897663) )
                    * sin( radians( latitude ) )
                )
            ) AS distance
            FROM sightings.ufo_api_sighting
            HAVING distance < 750
            ORDER BY distance
            LIMIT 0 , 750;
            
        # Enter in the coordinate for each hotspot and you will get all the sightings within a 750 mile radius of that hotspot.
    
All of the hotspots with their sightings have been created into json files in the base_directory of the project they are as follows:

* Surrounding_Area_51.json 
* Surrounding_Disney_World.json
* Surrounding_Pops_Soda_Bottle.json
* Surrounding_the_Worlds_Tallest_Therm.json
* Surrounding_Whitehouse.json
    
Database schema:
        
        create schema if not exists sightings collate utf8mb4_0900_ai_ci;

        create table if not exists auth_group
        (
	        id int auto_increment
		        primary key,
	        name varchar(150) not null,
	        constraint name
		        unique (name)
        );

        create table if not exists auth_user
        (
	        id int auto_increment
		        primary key,
	        password varchar(128) not null,
	        last_login datetime(6) null,
	        is_superuser tinyint(1) not null,
	        username varchar(150) not null,
	        first_name varchar(30) not null,
	        last_name varchar(150) not null,
	        email varchar(254) not null,
	        is_staff tinyint(1) not null,
	        is_active tinyint(1) not null,
	        date_joined datetime(6) not null,
	        constraint username
		        unique (username)
        );

        create table if not exists auth_user_groups
        (
	        id int auto_increment
		        primary key,
	        user_id int not null,
	        group_id int not null,
	        constraint auth_user_groups_user_id_group_id_94350c0c_uniq
		        unique (user_id, group_id),
	        constraint auth_user_groups_group_id_97559544_fk_auth_group_id
		        foreign key (group_id) references auth_group (id),
	        constraint auth_user_groups_user_id_6a12ed8b_fk_auth_user_id
		        foreign key (user_id) references auth_user (id)
        );

        create table if not exists django_content_type
        (
	        id int auto_increment
		        primary key,
	        app_label varchar(100) not null,
	        model varchar(100) not null,
	        constraint django_content_type_app_label_model_76bd3d3b_uniq
		        unique (app_label, model)
        );

        create table if not exists auth_permission
        (
	        id int auto_increment
		        primary key,
	        name varchar(255) not null,
	        content_type_id int not null,
	        codename varchar(100) not null,
	        constraint auth_permission_content_type_id_codename_01ab375a_uniq
		        unique (content_type_id, codename),
	        constraint auth_permission_content_type_id_2f476e4b_fk_django_co
		        foreign key (content_type_id) references django_content_type (id)
        );

        create table if not exists auth_group_permissions
        (
	        id int auto_increment
		        primary key,
	        group_id int not null,
	        permission_id int not null,
	        constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
		        unique (group_id, permission_id),
	        constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
		        foreign key (permission_id) references auth_permission (id),
	        constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
		        foreign key (group_id) references auth_group (id)
        );

        create table if not exists auth_user_user_permissions
        (
	        id int auto_increment
		        primary key,
	        user_id int not null,
	        permission_id int not null,
	        constraint auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
		        unique (user_id, permission_id),
	        constraint auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm
		        foreign key (permission_id) references auth_permission (id),
	        constraint auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id
		        foreign key (user_id) references auth_user (id)
        );

        create table if not exists django_admin_log
        (
	        id int auto_increment
		        primary key,
	        action_time datetime(6) not null,
	        object_id longtext null,
	        object_repr varchar(200) not null,
	        action_flag smallint unsigned not null,
	        change_message longtext not null,
	        content_type_id int null,
	        user_id int not null,
	        constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
		        foreign key (content_type_id) references django_content_type (id),
	        constraint django_admin_log_user_id_c564eba6_fk_auth_user_id
		        foreign key (user_id) references auth_user (id)
        );

        create table if not exists django_migrations
        (
	        id int auto_increment
		        primary key,
	        app varchar(255) not null,
	        name varchar(255) not null,
	        applied datetime(6) not null
        );

        create table if not exists django_session
        (
	        session_key varchar(40) not null
		        primary key,
	        session_data longtext not null,
	        expire_date datetime(6) not null
        );

        create index django_session_expire_date_a5c62663
	        on django_session (expire_date);

        create table if not exists ufo_api_sighting
        (
	        Date_Time text null,
	        Shape text null,
	        Duration text null,
	        City text null,
	        State text null,
	        Latitude double null,
	        Longitude double null,
	        Comments text null
        );


###Challenges faced:

* Time
* Some libraries were having bug issues and would error out.
* Wanted to implement mysql query command in web api admin site so I could pull hotspot radius sightings data with a gui interface for interactive map, but their were some bug issues and not enough time.

###Assumptions:

* I thought the geo libraries would be more cooperative but there were other requirements needed to run some of the operations that weren't listed in some of the research I found. Hence is why it took too much time researching.

### Next steps: 

* is to implement mysql queries with python in webapp to pull hotspot data in a nice gui and interactive map not just from the command line. I started the html template for the live sightings map but of course didn't have time.
its located in templates folder in base_directory of the project folder.

###Feedback
* I thought the challenge itself was a cool and fun idea. I really want to finish this api with all the bells and whistles on my own time.

###Questions:
* The only question I have is when can I start this job?
 
