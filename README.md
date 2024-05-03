# Database_FinalProject
1. python manage.py runserver (run the server)
2. python manage.py makemigrations
   python manage.py migrate (These two commond to apply change on database)

3. change setting.py to connect to database, you dont have to connect to a exist finihsed schema. Just connect to a new schema and use makeigration and migrate to apply change on it.
   DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'Jerry200ou59Z!',
        'HOST': 'localhost',
        'PORT': '5432',
        #         'OPTIONS': {
        #     'options': '-c search_path=finalproject' 
        # }
    }
}

4. edit the model.py in app users to change the database structure
5. urls and views to connect the frontend
   

