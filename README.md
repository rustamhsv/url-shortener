# URL-Shortener

You can access the website at https://urlbutshorter.herokuapp.com

**urlbutshorter** is URL shortening service. You enter some URL and the app produces short URL pointing to the original URL. When you put the short URL on your browser it redirects to the original web page. 

You should first register and login to use the service. You can log out at any time.

You can check the history of your shortened URLs at **My URLs page**. 

Here are the basic use cases:
  1) URL shortening: given a long URL => return a much shorter URL
  2) URL redirecting: given a shorter URL => redirect to the original URL

## Requirements
* This program requires python3.+ (and pip) installed, a guide on how to install python on various platforms can be found [here](https://www.python.org/)
* PostgresSQL was used in this project as the database client. To download postgres, follow this [link](https://www.postgresql.org/download/)

## Installation and Set-up

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

* Clone this repository using git clone https://github.com/rustamhsv/url-shortener.git
* Create and activate a virtual environment
* Download the all dependencies in the requirements.txt using ```pip install -r requirements.txt```
* To set up postgresql database run the following commands:
```
sudo -u postgres psql
```
In postgres terminal:
Create database:
```
CREATE DATABASE myproject;
```

Next, you create a database user which you will use to connect to and interact with the database.
```
CREATE USER myprojectuser WITH PASSWORD 'password';
```
Now, you need to do is give your database user access rights to the database you created:
```
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

* Create .env file and add environment variables to access POSTGRESQL_USER, POSTGRESQL_PASSWORD, and URLSHORTENER_SECRET_KEY variables.
* Run database migrations with following commands:
```
python manage.py makemigrations
python manage.py migrate
```
* To run the application in your local server type the following command:
```
python manage.py runserver
```

* To run the application in Docker container, change the Database settings in settings.py file:
```
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'postgres',
'USER': 'postgres',
'PASSWORD': 'postgres',
"HOST": "db",  # set in docker-compose.yml
"PORT": 5432,  # default postgres port  
```

## Running the tests
To run the test you can use the following commands:
```
python manage.py test shortener.tests
```

To run the tests with coverage run the following command:
```
coverage run --source='shortener' manage.py test
```
You can read about Coverage [here](https://coverage.readthedocs.io/en/6.4.1/)

## Deployment
The application is deployed to heroku for testing.


## System Architecture

Below is Database design for the application.

![image](https://user-images.githubusercontent.com/75800756/173936182-f8a7642a-c99e-40be-8ac0-ff8497560d94.png)

URL table stores long URL, short URL, and user who converted long URL to short one. 

**Base62 conversion** was used as a hash algorithm for URL Shortener. Base conversion
helps to convert the same number between its different number representation systems. Base
62 conversion is used as there are 62 possible characters for hashValue.


The features of Base62 conversion:
* The length of short URL is not fixed, it goes up with the ID
* It requires unique ID generation
* Duplication of short URLs (collision) is not possible because ID is unique
* It is simple and functional, but there is a security concern if ID increments by 1. In this case it becomes easy to figure out the next available short URL.

Alternative method would be **hash + collision resolution** algorithm. It can use hash functions like CRC32 and MD5 to generate hash values. We then have to take first few characters from the hash value (depending on the system requirements).
The features of Hash + collision resolution conversion:
* The length of short URL is fixed
* It doesn't require unique ID generation
* Duplication of short URLs (collision) is possible band should be handled
* It is not possible to figure out the next available short URL as it is random.

We decided to use base62 conversion for its simplicity and functionality.

URL Shortening Flow:
  1) longURL is the input
  2) A new unique ID (primary key) is generated.
  3) Convert the ID to shortURL with base 62 conversion.
  4) Create a new database row with the ID, shortURL, and longURL.

URL Redirecting Flow:
  1) A user clicks a short URL link
  2) If short URL is not in the database, return to home page.
  3) If short URL is in the database, return original long URL.

**302 redirect** method was used for redirection. It means that URL is “temporarily” moved to the long URL meaning that the requests for the same URL will be sent to the URL shortening
service first. Then, they are redirected to the long URL server. It can track click rate and source of click easily, so it would be useful if analytics will be integrated in the future.

Alternative would be to use **301 redirect**. It means that URL is “permanently” moved to the long URL. It reduces the server load because browser can cache the responses for future requests.


### Features to be added & Changes
  1) URL table can also store creation and expiration dates for URLs.
  2) When long URL is entered for shortening, it can be checked if this URL is already shortened before for that user and if it is, then return short URL from database instead of generating new one. In this way we can save more space in the database.
  3) When guest user tries to shorten the URL, he/she is redirected to login page. "You should log in first" message can be displayed in this transition.
  4) We can order history of URLs so that the latest URLs are shown on the top in My URLs page.
  5) Pagination can be added to My URLs page.
  6) longURL and shortURL fields in URL model should be changed to long_url and short_url accordingly to comply with PEP8 standarts.
  7) Update and Delete functionalities can be added to shortened URLs.
  8) More tests should be written to cover all parts of the application (especially views).

