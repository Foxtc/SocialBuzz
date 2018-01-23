This is a Django project to collect data from Facebook. Django is a high-level Python Web framework.

## Instructions
1. You need install Django
2. These application use database tables, so we need to create the tables in the database before we can use them. To do that, run the following command:
    ```
    python manage.py migrate
    ```
3. To include the facebook app run another command:
    ```
    python manage.py makemigrations facebook
    ```
4. Run migrate again to create those model tables in database:
    ```
    python manage.py migrate
    ```
5. To run the project do:
    ```
    python manage.py runserver
    ```
