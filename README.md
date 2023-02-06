## Local Setup

```
sudo pip3 install virtualenv
virtualenv --python python3.7 venv
source venv/bin/activate
```

## Install Dependencies
after activating venv run following command :
```
pip install -r requirements.txt
```
## Config Project 
create a .env file in the same directory as setting.py and add following lines to it 
```
SECRET_KEY=<Your SECRET KEY>
DEBUG=True #False for production
DB_NAME=<DATABASE_NAME>
DB_USER_NAME=<DATABASE_USER_NAME>
DB_PASSWORD=<DATABASE_PASSWORD>
DB_HOST=<DATABASE_HOST>
DB_PORT=<DATABASE_PORT>
```
## Run Migrations
```
python manage.py migrate
```
## Run Development WebApp
```
python manage.py runserver 
```
## Run Unit Tests
```
python manage.py test rates.tests
```

## Docker Setup 
-Open a terminal in the directory where the Dockerfile is located

-Build the Docker image using the following command:

```
docker build -t <image-name> .
```

Replace <image-name> with the desired name
for your image. The dot at the end specifies the current directory as the build context.

-Start a new Docker container using the following command:

```
docker run -p 8000:8000 <image-name>
```
The -p option maps port 8000 in the container to port 8000 on the host machine.

You can now access the Django development server in your web browser by visiting http://localhost:8000.

## Assumptions
I made two assumptions :
1. price is float (I understand that you may round price up or down in a real world scenario , but assumed it's a float )
2. I assumed that if there is no date in the database , but that date is in interval I should not include those times .

## Local Demo
use following curl command after running development server
```
curl --location --request GET 'localhost:8000/api/rates?date_from=2016-01-01&date_to=2016-12-05&origin=CNGGZ&destination=NOOSL'
```
response must be as follows
```json 
[
    {
        "day": "2016-01-01",
        "average_price": 1541.3333333333333
    },
    {
        "day": "2016-01-02",
        "average_price": 1541.0
    },
    {
        "day": "2016-01-05",
        "average_price": 1540.3333333333333
    },
    {
        "day": "2016-01-06",
        "average_price": 1539.6666666666667
    },
    {
        "day": "2016-01-07",
        "average_price": 1713.6666666666667
    },
    {
        "day": "2016-01-08",
        "average_price": 1713.3333333333333
    },
    {
        "day": "2016-01-09",
        "average_price": 1713.6666666666667
    },
    {
        "day": "2016-01-10",
        "average_price": 1713.6666666666667
    },
    {
        "day": "2016-01-11",
        "average_price": 1671.6666666666667
    },
    {
        "day": "2016-01-12",
        "average_price": 1672.3333333333333
    },
    {
        "day": "2016-01-13",
        "average_price": 1589.0
    },
    {
        "day": "2016-01-14",
        "average_price": 1589.6666666666667
    },
    {
        "day": "2016-01-15",
        "average_price": 1647.6666666666667
    },
    {
        "day": "2016-01-16",
        "average_price": 1647.6666666666667
    },
    {
        "day": "2016-01-17",
        "average_price": 1647.6666666666667
    },
    {
        "day": "2016-01-18",
        "average_price": 1564.0
    },
    {
        "day": "2016-01-19",
        "average_price": 1564.3333333333333
    },
    {
        "day": "2016-01-20",
        "average_price": 1564.0
    },
    {
        "day": "2016-01-21",
        "average_price": 1564.6666666666667
    },
    {
        "day": "2016-01-22",
        "average_price": 1458.0
    },
    {
        "day": "2016-01-23",
        "average_price": 1458.3333333333333
    },
    {
        "day": "2016-01-24",
        "average_price": 1458.3333333333333
    },
    {
        "day": "2016-01-25",
        "average_price": 1408.3333333333333
    },
    {
        "day": "2016-01-26",
        "average_price": 1375.3333333333333
    },
    {
        "day": "2016-01-27",
        "average_price": 1375.6666666666667
    },
    {
        "day": "2016-01-28",
        "average_price": 1376.3333333333333
    },
    {
        "day": "2016-01-29",
        "average_price": 1375.6666666666667
    },
    {
        "day": "2016-01-30",
        "average_price": 1375.6666666666667
    },
    {
        "day": "2016-01-31",
        "average_price": 1359.6666666666667
    }
]
```
