
# FastAPI Application with MongoDB

This is a FastAPI application that connects to a MongoDB database. Follow the steps below to clone the repository, set up the environment, and run the application.

## Prerequisites

Before you start, make sure you have the following installed:

- Python 3.7 or higher
- MongoDB (either locally or through a cloud provider like MongoDB Atlas)
- pip (Python package installer)

## Step 1: Clone the Repository

Start by cloning the Git repository to your local machine.

```bash
git clone https://github.com/sourabh-klizos/fastapi_application.git

<<<<<<< HEAD
create a .env file in root dir same as app level  copy content from .env_example file
=======
cd fastapi_application

create a .env file in root dir  copy content from .env_example file
>>>>>>> development

install dependencies
pip install -r requirements.txt

Run this command to start fastapi server 
uvicorn app.main:app

GET  http://localhost:8000/health

success response {"status":"I am healthy"} 

```


# Run with Docker

This FastAPI application can be run using Docker and Docker Compose as well.

## Step 1: Clone the Repository

Clone the Git repository to your local machine:

```bash
git clone https://github.com/sourabh-klizos/fastapi_application.git

<<<<<<< HEAD
=======
cd fastapi_application

>>>>>>> development
Run this command
docker-compose up


GET  http://localhost:8000/health

success response {"status":"I am healthy"} 


```

##

### Details of Endpoints

## User Signup API

### Endpoint
`POST http://localhost:8000/api/v1/auth/signup`  

### Description
This API endpoint is used to create a new user account by providing an email, password, and username.

### Request

#### Headers
- **Content-Type**: `application/json`

#### Request Body
The request body should contain the following JSON data:

- `email`: The user's email address (must be unique).
- `username`: The desired username (must be unique).

```json
{
  "email": "example@mail.com",
  "password": "12dss3",
  "username": "asddsddss8"
}

```

### success
- `success Response  with status code 201 created`.
```json 
{
  "message": "User account created successfully."
}

```



### if username already exists you will  get suggested usernames
- `Response  with status code 409 Conflict `.

```json 
{
    "detail": {
        "message": "User already exists with this username",
        "suggested_usernames": [
            "asdedssddss8sh",
            "asdedssddss8qw",
            "asdedssddss8kl",
            "asdedssddss8uj",
            "asdedssddss8gi"
        ]
    }
}
```

### if email already exists
- `Response  with status code 409 Conflict `.

```json 
{
    "detail": "User already exists with this email"
}
```

### if you send wrong payload
- `Response  with status code 422 Unprocessable Content `.



##
### This API is excatly same as Signup  same response and request follows

`POST http://localhost:8000/api/v1/auth/admin/signup`

##





## Login Endpoint

### Endpoint
`POST http://localhost:8000/api/v1/auth/login`

### Description
This endpoint allows users to log in by providing their email and password. Upon successful login, the API returns an `access_token` and a 
`refresh_token` which can be used for authenticated requests.

### Request

#### Headers
- **Content-Type**: `application/json`

#### Request Body:
The request body should include the user's email and password.

```json
{
  "email": "test@mail.com",
  "password": "test"
}
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjdiMzMxYTd......",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjdiMzMxYTdhNDhhYWNhY...."
}
```

### Error if not valid credentials 
```json
{
    "detail": "Incorrect email or password"
}
```





### List All Active Users
`GET http://localhost:8000/api/v1/auth/users`

### Description
This endpoint retrieves a list of users. It requires authentication via a Bearer token and is restricted to admin users only.

### Authorization
- **Bearer Token**: You must include a valid Bearer token in the `Authorization` header.
- **Admin Access**: This endpoint is restricted to admin users only.

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`

#### Example Request:
```bash
GET http://localhost:8000/api/v1/auth/users
Authorization: Bearer <your-token>


response with code 200

{
    "total": 44,
    "has_previous": null,
    "has_next": true,
    "data": [
        {
            "id": "67a99413dc65a0145ee73981",
            "email": "a@b.com",
            "role": "regular",
            "username": "skdeues",
            "created_at": "2025-02-10T11:22:19.096000",
            "updated_at": null,
            "is_deleted": false,
            "updated_by": null
        }
    ]
}


```

```bash
http://localhost:8000/api/v1/auth/users?q=sourabh
You can also perfome search via username  where sourabh is a user

http://localhost:8000/api/v1/auth/users?per_page=1&page=1

remember page and per_page should be positive number 
limit number of response per_page=5    maximum limit of per_page is 30
jump to another page = page=10 

```



## error if you don't provide right credentials

```
401 Unauthorized
{
    "detail": "Not a valid token "
}



if not admin user and try to use this api 
403
Forbidden
{
    "detail": "You don't have access to perform this action"
}
```

## User Detail Endpoint

### Endpoint
`GET http://localhost:8000/api/v1/auth/users/{user_id}`

### Description
This endpoint retrieves the details of a specific user. The user must either be an admin or the owner of the account to access the details.

### Authentication
- **Authorization**: `Bearer <your-token>` (The request must include a valid Bearer token for authentication).

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`

#### Example Request:

`GET http://localhost:8000/api/v1/auth/users/67a99cb53312d3bde5ccbd67`
`Authorization: Bearer <your-token>`
```json

{
    "id": "67a99cb53312d3bde5ccbd67",
    "email": "basdsssfde@gmail.com",
    "role": "regular",
    "username": "ssdbass",
    "created_at": "2025-02-10T11:59:09.669000",
    "updated_at": null,
    "is_deleted": false,
    "updated_by": null
}

```
`status code 200`

`If the user is neither an admin nor the owner of the account, access will be denied.`

`status code 403 Forbidden`
```json
{
    "detail": "You don't have access to perform this action"
}
```

`If no valid Bearer token is provided`
`status code 401 Unauthorized`
```json
{
    "detail": "Not a valid token "
}

```









## Edit User Endpoint

### Endpoint
`PUT http://localhost:8000/api/v1/auth/users/{user_id}`

### Description
This endpoint allows the owner of the account or an admin user to edit a user's details (username or email). The request must include either or both fields (username and email), and neither can be empty.

### Authentication
- **Authorization**: `Bearer <your-token>` (A valid Bearer token must be provided in the request header).
- **Permissions**: Only the owner of the account or an admin user can edit the user details.

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`
- **Content-Type**: `application/json`

#### Request Body:
You must include either or both `username` or `email`, and neither can be empty.

```json
{
  "username": "test",
  "email": "test@1.dom"
}
```
`if not admin or owner of account will get error status code 403`
```json
{
  "detail": "You don't have access to perform this action"
}
```





## Soft Deleted User Endpoint

### Endpoint
`DELETE http://localhost:8000/api/v1/auth/users/{user_id}?reason={reason}`

### Description
This endpoint allows the **owner** of the account or an **admin** user to delete a user’s account. The request must include a `reason` query parameter.
Only the owner of the account or an admin can delete the account. If anyone else tries to delete an account, they will receive a `403 Forbidden` error.

### Authentication
- **Authorization**: `Bearer <your-token>` (A valid Bearer token must be provided in the request header).
- **Permissions**: Only the **owner** of the account or an **admin** user can delete the account.

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`
- **Content-Type**: `application/json`

#### URL Parameters
- **user_id**: The unique ID of the user whose account you want to delete.

#### Query Parameters
- **reason**: A string representing the reason for deleting the account. This parameter is required.

Example request:

```bash
DELETE http://localhost:8000/api/v1/auth/users/67a9940edc65a0145ee73980?reason=testing
Authorization: Bearer <your-token>

success status code 204

```





## Refresh Token Endpoint

### Endpoint
`POST http://localhost:8000/api/v1/refresh/`

### Description
This endpoint allows you to exchange a valid **refresh token** for a new **access token**. This is typically used when the access token has expired, and you need a new one to continue making authorized API requests.

### Request

#### Headers
- **Content-Type**: `application/json`

#### Request Body
The request must include the **refresh token** in the body.
`status code 200`
```json
{
  "refresh_token": "<your-refresh-token>"
}

```





## List Soft Deleted Users Endpoint

### Endpoint
`GET http://localhost:8000/api/v1/trash/?per_page={per_page}`

### Description
This endpoint allows an **admin** to retrieve a list of **soft-deleted users**. The list is paginated based on the `per_page` query parameter. Only **admin users** have access to this endpoint. If anyone else tries to access it, they will receive a `403 Forbidden` error.

### Authentication
- **Authorization**: `Bearer <your-token>` (A valid Bearer token must be provided in the request header).
- **Permissions**: Only **admin users** can access this endpoint.

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`
- **Content-Type**: `application/json`

#### Query Parameters:
- **per_page**: The number of soft-deleted users to return per page (e.g., `per_page=20`).

Example request:

```bash
GET http://localhost:8000/api/v1/trash/?per_page=20
Authorization: Bearer <your-token>

status code 200

{
    "total": 1,
    "has_previous": null,
    "has_next": null,
    "data": [
        {
            "id": "67af2bb5a014588b6b2fe3f1",
            "user_id": "67a9940edc65a0145ee73980",
            "deleted_by": "67a990dedc65a0145ee7397e",
            "deleted_at": "2025-02-14T17:10:37.046000"
        }
    ]
}

```






## Bulk  Soft Delete Users Endpoint

### Endpoint
`POST http://localhost:8000/api/v1/trash/bulk-delete`

### Description
This endpoint allows an **admin** user to **bulk soft-delete users**. The request must include a list of user IDs to be deleted and a reason for deletion. Only **admin users** have access to this endpoint. If anyone else tries to access it, they will receive a `403 Forbidden` error.

### Authentication
- **Authorization**: `Bearer <your-token>` (A valid Bearer token must be provided in the request header).
- **Permissions**: Only **admin users** can access this endpoint.

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`
- **Content-Type**: `application/json`

#### Request Body:
The body should include:
- **ids**: A list of user IDs to be deleted.
- **reason**: A string explaining the reason for deleting the users.

Example request body:

```bash
    payload = {
    "ids": [
        "67a990a9dc65a0145ee7397d",
        "67a990dedc65a0145ee7397e",
        "67a9939fdc65a0145ee7397f",
        "67a99cb23312d3bde5ccbd66"
    ],
    "reason": "because I am admin"
    }

 ```
```bash
if user was alredy deleted it with show in alredy_deleted_user,  if deleted by this api call will show in deleted_now.
response with status 200 
{
    "alredy_deleted_user": [
        "67a990a9dc65a0145ee7397d",
        "67a990dedc65a0145ee7397e",
        "67a9939fdc65a0145ee7397f",
        "67a99cb23312d3bde5ccbd66"
    ],
    "deleted_now": []
}


```











## Restore Soft Deleted User Endpoint

### Endpoint
`PUT http://localhost:8000/api/v1/trash/restore/{user_id}`

### Description
This endpoint allows an **admin** user to **restore a soft-deleted user**. The request will restore the user’s account from the soft-deleted state. Only **admin users** can restore soft-deleted users. If anyone else tries to access this endpoint, they will receive a `403 Forbidden` error.

### Authentication
- **Authorization**: `Bearer <your-token>` (A valid Bearer token must be provided in the request header).
- **Permissions**: Only **admin users** can restore soft-deleted users.

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`
- **Content-Type**: `application/json`

#### URL Parameters:
- **user_id**: The unique ID of the user to restore from the soft-deleted state.

Example request:

```bash

PUT http://localhost:8000/api/v1/trash/restore/67a9939fdc65a0145ee7397f
Authorization: Bearer <your-token>



status code 200
response =   {
                "email": "as1ddsu@sb.com",
                "username": "sskod",
                "created_at": "2025-02-13T19:28:19.975000",
                "role": "admin",
                "is_deleted": false,
                "updated_at": null,
                "profile_image": "premium_photo-1664474619075-644dd191935f_16adcd34debb4cc9b907e74be4cc65c3.jpg",
                "id": "67adfa7ce6b9d72461a46bb7"
            }



 ```








 ## Permanent Delete Soft Deleted User Endpoint

### Endpoint
`DELETE http://localhost:8000/api/v1/trash/permanent/delete/{user_id}`

### Description
This endpoint allows an **admin** user to **permanently delete** a soft-deleted user. Once a user is permanently deleted, they cannot be recovered. Only **admin users** have access to this action. If anyone else tries to access this endpoint, they will receive a `403 Forbidden` error.

### Authentication
- **Authorization**: `Bearer <your-token>` (A valid Bearer token must be provided in the request header).
- **Permissions**: Only **admin users** can perform permanent deletion of soft-deleted users.

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`
- **Content-Type**: `application/json`

#### URL Parameters:
- **user_id**: The unique ID of the user to be permanently deleted.

Example request:

```
DELETE http://localhost:8000/api/v1/trash/permanent/delete/67adfa7ce6b9d72461a46bb7
Authorization: Bearer <your-token>

success status code 204

```





## Upload image to s3

This is a simple API built using **FastAPI** that allows users to upload profile images to an Amazon S3 bucket.

## API Endpoint

### `POST /api/v1/profile-upload-s3/`

This endpoint allows the user to upload an image file (profile picture) to S3. The image should be sent with the key `file` and should be an actual image file.

### Request Format

### ".jpg", ".jpeg", ".png"  supported types

**URL:** `http://localhost:8000/api/v1/profile-upload-s3/`

**Method:** `POST`

**Headers:**
- **Authorization:** Bearer token (You need to include your Bearer token for authentication)
- **Content-Type:** `multipart/form-data` (This will automatically be handled by `curl` or any HTTP client that supports file uploads.)

**Body:**
- **file**: The image file you want to upload.

### Example Request

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/profile-upload-s3/' \
  -H 'Authorization: Bearer YOUR_BEARER_TOKEN' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/image.jpg'


success code 200 and response data
{
    "message": "Image uploaded successfully!",
    "filename": "https://fastapi-s3-bucket-sourabh.s3.eu-north-1.amazonaws.com/pexels-hsapir-1054655.jpg_18cd00be-845c-47d5-9e4e-1ae7c00a5d70.jpg"
}



```




## Profile Image Upload Endpoint

### Endpoint
`POST http://localhost:8000/api/v1/profile-upload/`

### Description
This endpoint allows users to **upload a profile image**. The image must be in one of the allowed formats: `.jpg`, `.jpeg`, or `.png`. 

### Authentication
- **Authorization**: `Bearer <your-token>` (A valid Bearer token must be provided in the request header).

### Request

#### Headers
- **Authorization**: `Bearer <your-token>`
- **Content-Type**: `multipart/form-data`

#### Request Body:
The body should include the `image` key with the file. Only image files with the following extensions are allowed:
- `.jpg`
- `.jpeg`
- `.png`

Example request (using `curl`):

```
curl -X POST http://localhost:8000/api/v1/profile-upload/ \
  -H "Authorization: Bearer <your-token>" \
  -F "image=@path_to_your_image.jpg"


  success code 200

```