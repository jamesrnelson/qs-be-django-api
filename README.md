
# README

## Quantified Self

Quantified Self is an iterated project. It is an API that was first built in Rails, then in Express, and then in Django.  The frontend for the Django API can be accessed at https://jamesrnelson.github.io/qs-fe-django

The Django backend API is hosted at https://polar-journey-23475.herokuapp.com/api/v1/foods

The backend express API repo can be found here: https://github.com/jamesrnelson/qs-be-express-api
The backend rails API repo can be found here: https://github.com/jamesrnelson/qs-be-rails-api

These APIs support a preexisting javascript frontend. The frontend and backend together allow an individual to create foods and add them to certain preexisting meals in order to keep track of their daily caloric intake.

### Python

Quantified Self was built using Python 3.7 and Django 2.1

### Set up and Use

* In order to run Quantified Self locally, you will first need to set up the front end by following the instructions at the following link: https://github.com/jamesrnelson/qs-fe-django.

* After you have set up the front end, set up the back end by running

```shell
git clone git@github.com:jamesrnelson/qs-be-django-api.git
```

* Activate the virtual environment for this project:

```shell
source venv/bin/activate
```

* Run the tests to make sure everything is passing:
```shell
python3 manage.py test
```

* If they do not pass you may need to create the database and run the migrations:

###### Create
```shell
psql
CREATE DATABASE qs_be_express_api;
\q
```
###### Migrate
```shell
python3 manage.py migrate
```

* In your local backend directory, run the server on http://localhost:8000 by running the following command:

```shell
python3 manage.py runserver
```
* In your local frontend directory, run the server on http://localhost:8080 by running the following command:

```shell
npm start
```

* In  your browser, navigate to http://localhost:8080. If everything has installed correctly you should be able to interact with the frontend app, which will communicate with the Django api to store your nutritional and caloric data in the appropriate places.

### How to run the test suite

 Quantified Self was thoroughly tested using Python's built-in testing suite. In order to run the tests, make sure that you have already followed the steps about creating and migrating your database, then from your backend root directory run the following test command:

```shell
python3 manage.py test
```

## Supported Endpoints:

## Food Endpoints:
#### GET /api/v1/foods

Returns all foods currently in the database

Each individual food will be returned in the following format:
```shell
{
    "id": 1,
    "name": "Banana",
    "calories": 150
}
```
#### GET /api/v1/foods/:id

Returns the food object with the specific :id you’ve passed in or 404 if the food is not found

#### POST /api/v1/foods

Allows creating a new food with the parameters:

{ "food": { "name": "Name of food here", "calories": "Calories here"} }

If food is successfully created, the food item will be returned. If the food is not successfully created, a 400 status code will be returned. Both name and calories are required fields.

#### PUT /api/v1/foods/:id

Allows one to update an existing food with the parameters:

{ "food": { "name": "Mint", "calories": "14"} }

If food is successfully updated (name and calories are required fields), the food item will be returned. If the food is not successfully updated, a 400 status code will be returned.

#### DELETE /api/v1/foods/:id

Will delete the food with the id passed in and return a 204 status code. If the food can’t be found, a 404 will be returned.

## Meal Endpoints:

#### GET /api/v1/meals

Returns all the meals in the database along with their associated foods

If successful, this request will return a response in the following format:

```shell
[
    {
        "id": 1,
        "name": "Breakfast",
        "foods": [
            {
                "id": 1,
                "name": "Banana",
                "calories": 150
            },
            {
                "id": 6,
                "name": "Yogurt",
                "calories": 550
            },
            {
                "id": 12,
                "name": "Apple",
                "calories": 220
            }
        ]
    },
    {
        "id": 2,
        "name": "Snack",
        "foods": [
            {
                "id": 1,
                "name": "Banana",
                "calories": 150
            },
            {
                "id": 9,
                "name": "Gum",
                "calories": 50
            },
            {
                "id": 10,
                "name": "Cheese",
                "calories": 400
            }
        ]
    },
    {
        "id": 3,
        "name": "Lunch",
        "foods": [
            {
                "id": 2,
                "name": "Bagel Bites - Four Cheese",
                "calories": 650
            },
            {
                "id": 3,
                "name": "Chicken Burrito",
                "calories": 800
            },
            {
                "id": 12,
                "name": "Apple",
                "calories": 220
            }
        ]
    },
    {
        "id": 4,
        "name": "Dinner",
        "foods": [
            {
                "id": 1,
                "name": "Banana",
                "calories": 150
            },
            {
                "id": 2,
                "name": "Bagel Bites - Four Cheese",
                "calories": 650
            },
            {
                "id": 3,
                "name": "Chicken Burrito",
                "calories": 800
            }
        ]
    }
]
```

#### GET /api/v1/meals/:meal_id/foods

Returns all the foods associated with the meal with an id specified by :meal_id or a 404 if the meal is not found

If successful, this request will return a response in the following format:

```shell
{
    "id": 1,
    "name": "Breakfast",
    "foods": [
        {
            "id": 1,
            "name": "Banana",
            "calories": 150
        },
        {
            "id": 6,
            "name": "Yogurt",
            "calories": 550
        },
        {
            "id": 12,
            "name": "Apple",
            "calories": 220
        }
    ]
}
```

#### POST /api/v1/meals/:meal_id/foods/:id

Adds the food with :id to the meal with :meal_id

This creates a new record in the MealFoods table to establish the relationship between this food and meal. If the meal/food cannot be found, a 404 will be returned.

If successful, this request will return a status code of 201 with the following body:
```shell
{
    "message": "Successfully added FOODNAME to MEALNAME"
}
```

#### DELETE /api/v1/meals/:meal_id/foods/:id

Removes the food with :id from the meal with :meal_id

This deletes the existing record in the MealFoods table that creates the relationship between this food and meal. If the meal/food cannot be found, a 404 will be returned.

If successful, this request will return:
```shell
{
    "message": "Successfully removed FOODNAME to MEALNAME"
}
```
