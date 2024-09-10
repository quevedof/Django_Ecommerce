# Django Ecommerce Web App

Fully functional eCommerce website with user and guest checkout capabilities with client-side paypal payment integration. 

Implementation of Django user registration, login authentication with use of forms, and decorators for role permissions.

Users and guests have the ability to add multiple products to cart, varying from physical to digital products. Guest checkout is enabled by using cookies.

Payment integration is handled with PayPal offering the ability to checkout with a PayPal account.

The core structure is HTML templates with Bootstrap styling and layouts; and the following 6 Models:

![alt text](https://github.com/quevedof/Django_Ecommerce/blob/main/static/images/models.png "Models")

1. USER - Built in Django user model, instance created for each customer who registers.

2. CUSTOMER - Along with a User model, each customer contains a Customer model that holds a one-to-one relationship to each User. (OneToOneFied)

3. PRODUCT - The Product model represents product types we have in store.

4. ORDER - The Order model represents a transaction that is placed or pending. The model holds information such as the transaction ID, data completed and order status. This model is a child of the Customer model but a parent to Order Items.

5. ORDERITEM - An Order Item is one Item with an Order. For example, a shopping cart may consist of many items but is all part of one order. Therefore the OrderItem model is a child of the PRODUCT model AND the ORDER Model.

6. SHIPPING - Not every Order needs shipping information. For orders containing physical products that need to be shipped, we need to create an instance of the Shipping model to know where to send the order. Shipping is simply a child of the Order model when necessary.

### Installation
1. Clone the repository
    ```
    git clone https://github.com/quevedof/Django_Ecommerce.git

    cd Django_Ecommerce
    ``` 
2. Enable virtual environment (optional)
    ```
    python -m venv .venv
    .venv/Scripts/activate
    ```
3. Install dependecies
    ```
    pip install -r requirements.txt
    ```
4. Run Django's SqliteDB migrations
    ```
    py manage.py makemigrations
    py manage.py migrate
    ```
5. Run server
    ```
    py manage.py runserver
    ```
