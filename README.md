## Setup Local Environment
1. Clone this repo
2. Create `.env` file in the root directory and add the following
   ```.env
    DEBUG=True
    ALLOWED_HOSTS=['*']
    DB_NAME='<database_name>'
    DB_USER_NAME='<database_user_name>'
    DB_PASSWORD='<database_password>'
    DB_PORT='5432'
    SECRET_KEY='<secret key>'
    ```
    ```python
    # importing the function from utils
    from django.core.management.utils import get_random_secret_key

    # generating and printing the SECRET_KEY
    print(get_random_secret_key())
    ```
3. Two Ways to setup this project:
   - Using Docker
     - Setup [Docker](https://docs.docker.com/get-started/introduction/get-docker-desktop/)
     - Run `docker-compose up`
       ![docker compose command](https://github.com/user-attachments/assets/9b3c2863-957b-4868-a85c-27193736463c)
       This output ☝️ indicates that your Docker setup is working correctly and containers are running as expected.

   - Using Non Docker method
      1. Setup Postgres
      2. Setup Python 3.13
      3. (Optional) Setup [Pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv):
      4. (Optional) Make sure that you are using virtual-env before installing dependencies
      5. Install the requirements and run migrate command
         ```bash
         pip install -r requirements.txt
         ./manage.py migrate
         ```
      6. Fire up the server by running the following command
         ```bash
         ./manage.py runserver
         ```
## API
1. Create Product
   - API URL: `/api/product/`
   - Method: `POST`
   - Request Payload:
     ```json
     {
         "name": "Sample New Product",
         "description": "Sample New Description",
         "price": 6.44,
         "stock": 20
     }
     ```
   - Response:
     ```json
     {
         "id": 4,
         "name": "Sample New Product",
         "description": "Sample New Description",
         "price": 6.44,
         "stock": 20
     }
     ```
   - Sample Request & Response
     ![1  create_product](https://github.com/user-attachments/assets/f1ba73bb-3bb8-478b-b43f-27e680cead94)

2. Update Product
   - API URL: `/api/product/<product_id>/`
   - Method: `PATCH`
   - Request payload:
     ```json
     {
         "name": "Update Sample Product",
         "description": "Update Sample Description",
         "stock": 15
     }   
     ```
   - Response
     ```json
     {
         "id": 1,
         "name": "Update Sample Product",
         "description": "Update Sample Description",
         "price": 1.5,
         "stock": 15
     }

     ```
   - Sample Request & Response
     ![2  update_product](https://github.com/user-attachments/assets/f699990a-8aa9-48a7-969d-82205ef9e279)

3. Get All Products
   - API URL: `/api/product/`
   - Method: `GET`
   - Resonse:
     ```json
     [
        {
            "id": 2,
            "name": "New Sample Product 2",
            "description": "New Sample Product Description 2",
            "price": 2.6,
            "stock": 35
        },
        {
            "id": 3,
            "name": "Sample Product",
            "description": "Sample Product",
            "price": 1.34,
            "stock": 40
        },
        {
            "id": 4,
            "name": "Sample New Product",
            "description": "Sample New Description",
            "price": 6.44,
            "stock": 20
        },
        {
            "id": 1,
            "name": "Update Sample Product",
            "description": "Update Sample Description",
            "price": 1.5,
            "stock": 15
        }
     ]
     ```
   - Sample Request & Response
     ![3  get_all_products](https://github.com/user-attachments/assets/b4eaee9e-21b9-4b51-afc6-6963161b482e)


4. Get Product By ID
   - API URL: `/api/product/<product_id>/`
   - Method: `GET`
   - Response:
     ```json
     {
         "id": 1,
         "name": "Update Sample Product",
         "description": "Update Sample Description",
         "price": 1.5,
         "stock": 15
      }
     ```
   - Sample Request & Response
     ![4  get_product_by_id](https://github.com/user-attachments/assets/bb2ccf50-dc9a-42ca-8724-b2ad70ce3fa7)


5. Create Order
   - API URL: `/api/order/`
   - Method: `POST`
   - Request Payload:
     ```json
     {
         "products": {
             "1": 6,
             "2": 10
         }
     }
     ```
   - Response:
     ```json
     {
         "id": 8,
         "products": {
             "1": 6,
             "2": 10
         },
         "status": "PENDING"
     }
     ```
   - Sample Request & Response
     ![5  create_order](https://github.com/user-attachments/assets/8fa1d8bb-5df2-4952-9776-7348f8bfb993)

     
6. Update Order
   - API URL: `/api/order/<order_id>/`
   - Method: `PATCH`
   - Request Payload:
     ```json
     {
         "products": {
             "1": 6,
             "2": 10
         }
     }
     ```
   - Response:
     ```json
     {
         "id": 1,
         "products": {
             "1": 6,
             "2": 10
         },
         "status": "PENDING"
     }
     ```
   - Sample Request & Response
     ![6  update_order](https://github.com/user-attachments/assets/ecd8db0e-ea1d-4bcd-90d6-fd932c71e2b1)

  
7. Get All Orders
   - API URL: `/api/order/`
   - Method: `GET`
   - Resonse:
     ```json
     [
         {
             "id": 8,
             "products": {
                 "1": 6,
                 "2": 10
             },
             "status": "PENDING"
         },
         {
             "id": 1,
             "products": {
                 "1": 6,
                 "2": 10
             },
             "status": "PENDING"
         },
         {
             "id": 6,
             "products": {
                 "1": 6
             },
             "status": "PENDING"
         },
         {
             "id": 5,
             "products": {
                 "3": 6
             },
             "status": "PENDING"
         },
         {
             "id": 4,
             "products": {
                 "1": 4,
                 "3": 6
             },
             "status": "PENDING"
         },
         {
             "id": 3,
             "products": {
                 "3": 6,
                 "4": 4
             },
             "status": "PENDING"
         },
         {
             "id": 2,
             "products": {
                 "1": 6,
                 "2": 10
             },
             "status": "COMPLETED"
         },
         {
             "id": 7,
             "products": {
                 "1": 5
             },
             "status": "COMPLETED"
         }
     ]
     ```
   - Sample Request & Response
     ![7  get_all_orders](https://github.com/user-attachments/assets/7b6e7ddd-c79b-436e-adff-dfe599979892)


9. Get Order By ID
   - API URL: `/api/order/<order_id>/`
   - Method: `GET`
   - Resonse:
     ```json
     {
         "id": 7,
         "products": {
             "1": 5
         },
         "status": "COMPLETED"
     }
     ```
   - Sample Request & Response
     ![8  get_order_by_id](https://github.com/user-attachments/assets/4e7dcc55-28ef-4fee-a1f7-2fc0cead4cdd)


11. Process Order
   - API URL: `/api/order/<order_id>/process_order/`
   - Method: `PATCH`
   - Response
     - Asked Quantity is more than Available Quantity (Error Message) - This check is also done at the time of placing an order (i.e. Create/Update Order API)
       ```json
       {
           "is_success": "False",
           "product_ids_quantity_mismatch": {
               "1": {
                   "available_quantity": "4",
                   "asked_quantity": "6"
               }
           }
       }
       ```
       - Sample Request & Response
         ![9  process_order_fail](https://github.com/user-attachments/assets/4a1d7ad3-ce6b-4b2a-b854-3cbbeed85402)

     
     - Order is Already Proccessed
       ```json
       {
           "error": "Order is already processed"
       }
       ```
       - Sample Request & Response
         ![10  process_order_fail](https://github.com/user-attachments/assets/ce4556a5-6bcb-4d06-a576-b1a1597543a8)
      
     - Successfully
       ```json
       {
           "id": 8,
           "products": {
               "1": 6,
               "2": 10
           },
           "status": "COMPLETED"
       }
       ```
       - Sample Request & Response
         ![11  process_order_success](https://github.com/user-attachments/assets/23828b20-b83f-4531-83bb-150915d8d41c)

     
