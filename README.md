# Project Name: Shopping Sys
The project is for the merchants of self operated store
## Functions:
- Login/Register: Click "NO ACCOUNT? CREATE ONE" to create an account, wait for a 5 seconds, enter your email and password to login
### User part:
- Top-Up: Enter the amount of pounds that you want to save in your wallet
- Profile check: Press "Profile" button to edit user's profile, user have to click "Edit" to enable the input labels, if user wants to edit password, they have to enter the original password and click "Confirm" to enable the new password input label
- Add to Cart: Each user has a cart, the item can be added into the cart by click "Add to Cart" button (Change the number they want to add, there is an input label in each item card, default is 1).
- Pay Now: Add into the cart is not necessary, user can buy item directly by "Pay Now" button
- My Cart: Check the items have been added into the cart, there will be a modal box after clicked the "My Cart", it will list the items and items' details that user has been added, users can edit the cart(remove items or pay all items)
- Search: Search items by keywords (can find table by "tab", "ta", "ble", or "t")
### Manager part:
- Profile check: Press "Profile" button to edit user's profile, user have to click "Edit" to enable the input labels, if user wants to edit password, they have to enter the original password and click "Confirm" to enable the new password input label
- Edit users: Edit users' username and email by clicked the "Edit" button, "Save" to save the edit
- Delete users: Delete users by "Delete" button in the table 
- Next/Prev button: Switch the 3 tables by "Next Table" and "Previous Table"
- Edit items: Edit items' item name, quantity, and price by clicked the "Edit" button, "Save" to save the edit
- Delete items: Delete items by "Delete" button in the table
- Check orders: Check orders' detail, click "View" for checking information on the top
- Search: search users and orders by users' email, search items by items' name.
- Add items: Add items by entered item name, price, and quantity
## Technology stack
### Front-End:
- HTML, CSS, JavaScript
### Back-End:
- Python, Django
### Database:
- Sqlite3
### Server:
- pythonanywhere
### Environment:
- Python 3.7
- Django 2.1.5
## Installation(Windows)
- Python (Download from the official web)
- Django - pip install Django==2.1.5
### Installing in Virtual environment by conda
- conda create -n rango python3.7.5
- conda activate rango
- conda install django==2.1.5
- conda install pillow
## Before python manage.py runserver
- python manage.py makemigrations to create migration file
- python manage.py migrate to migrate data (create tables that we set in models.py in database)


