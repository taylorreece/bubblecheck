# API Documentation
## User
**Endpoint**: /api/user/current_user

**Method**: GET

**Requires**: Login

**Sample Output**:
```json
{
	"email": "foo@bar.com", 
	"id": 123, 
	"public_uuid": "0dc9e8f5-3b1e-4a5e-97ad-1280512ef8e4", 
	"teachername": "Mr. Smith"
}
```
----
**Endpoint**: /api/user/token/request

**Method**: POST

**Sample Input**:
```json
{
	"email": "foo@bar.com",
	"password": "foobar123!"
}
```
**Sample Output**:
```json
{
	"jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkZha2VFbWFpbEBmb29iYXIuY29tIiwiZXhwIjozMjUyNTc0NzcxMX0.GUbxfg3OWSp4yei5GTzXRNF_KF5xacNSb4mcrcr6LoI"
}
```
----
**Endpoint**: /api/user/token/check

**Method**: GET

**Requires**: JWT Token in header

**Sample Output**:
```json
{
	"expires": "2018-04-24 12:32:19"
}
```
----
**Endpoint**: /api/user/token/renew

**Method**: GET

**Requires**: JWT Token in header

**Sample Output**:
```json
{
	"jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkZha2VFbWFpbEBmb29iYXIuY29tIiwiZXhwIjozMjUyNTc0NzcxMX0.GUbxfg3OWSp4yei5GTzXRNF_KF5xacNSb4mcrcr6LoI"
}
```
----
## Course
**Endpoint**: /api/course/list

**Method**: GET

**Requires**: Login

**Sample Output**:
```json
{
  "courses": [
    {
      "id": 1, 
      "name": "Geometry", 
      "permission": "own"
    }, 
    {
      "id": 2, 
      "name": "Algebra", 
      "permission": "edit"
    }
  ]
}
```
----
**Endpoint**: /api/course/get/\<int:course_id\>

**Method**: GET

**Requires**: Login, Course view

**Sample Output**:
```json
{
  "exams": [
      {
          "id": 12,
          "name": "Final Exam"
      }
  ], 
  "id": 1, 
  "name": "Geometry", 
  "other_users": [
    {
      "permission": "edit", 
      "public_uuid": "1fd653b5-ea1d-4cde-84ab-37ce6e488e38", 
      "teachername": "Mrs. Sillypants"
    }
  ], 
  "permission": "own", 
  "sections": [
    {
      "id": 1, 
      "name": "Hour 1"
    }, 
    {
      "id": 2, 
      "name": "Hour 2"
    }, 
    {
      "id": 3, 
      "name": "Hour 3"
    }, 
    {
      "id": 4, 
      "name": "Hour 4"
    }
  ]
}
```
----
**Endpoint**: /api/course/add

**Method**: POST

**Requires**: Login

**Sample Input**:
```json
{
    "name": "US History",
    "sections": [
        "Hour 3",
        "Hour 5"
    ]
}
```

**Sample Output**:
```json
{
  "id": 123, 
  "name": "US History",
  "permission": "own", 
  "sections": [
    {
      "id": 1, 
      "name": "Hour 3"
    }, 
    {
      "id": 2, 
      "name": "Hour 5"
    }
  ]
}
```
## Exam