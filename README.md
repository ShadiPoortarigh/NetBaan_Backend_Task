# NetBaan_Backend_Task


### requirements.txt
pip install -r requirements.txt



### admin page
username = maryam,
password = 123456



### model test
python3 manage.py test



### endpoints
'/api/create/' : to sign up

'/api/login/' : to sign in

'/api/list/' : returns a list of books and filters if there is a specific genre as query parameter 

'/api/suggest/' : suggests books based on the user's favorite genres

'/api/'update/<str:title>/' : It gets the title of a book, and the authenticated user is able to change, add or delete the book's rating

