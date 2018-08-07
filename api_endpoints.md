# API Endpoints
* [User](#user)
    * [/api/user/current_user](#apiusercurrent_user)
    * [/api/user/flash_messages](#apiuserflash_messages)
    * [/api/user/token/request](#apiusertokenrequest)
    * [/api/user/token/check](#apiusertokencheck)
    * [/api/user/token/renew](#apiusertokenrenew)
* [Course](#course)
    * [/api/course/list](#apicourselist)
    * [/api/course/get/\<course_id\>](#apicoursegetcourse_id)
    * [/api/course/add](#apicourseadd)
    * [/api/course/update/\<course_id\>](#apicourseupdatecourse_id)
    * [/api/course/\<course_id\>/section/add](#apicoursecourseidsectionadd)
    * [/api/course/\<course_id\>/section/\<section_id\>/update](#apicoursecourseidsectionsectionidupdate)

## User
### /api/user/current_user

**Method**: GET

**Requires**: Login

**Sample Output**:
```json
{
	"user": {
    "email": "foo@bar.com", 
    "id": 123, 
    "public_uuid": "0dc9e8f5-3b1e-4a5e-97ad-1280512ef8e4", 
    "teachername": "Mr. Smith"
  },
  "success": true
}
```
----
### /api/user/flash_messages

**Method**: GET

**Requires**: None

**Sample Output**:
```json
{
  "messages": [
    {
      "category": "error",
      "message": "Login Incorrect"
    }
  ],
  "success": true
}
```
----
### /api/user/token/request

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
  "jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkZha2VFbWFpbEBmb29iYXIuY29tIiwiZXhwIjozMjUyNTc0NzcxMX0.GUbxfg3OWSp4yei5GTzXRNF_KF5xacNSb4mcrcr6LoI",
  "success": true
}
```
----
### /api/user/token/check

**Method**: GET

**Requires**: JWT Token in header

**Sample Output**:
```json
{
  "expires": "2018-04-24 12:32:19",
  "success": true
}
```
----
### /api/user/token/renew

**Method**: GET

**Requires**: JWT Token in header

**Sample Output**:
```json
{
  "jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkZha2VFbWFpbEBmb29iYXIuY29tIiwiZXhwIjozMjUyNTc0NzcxMX0.GUbxfg3OWSp4yei5GTzXRNF_KF5xacNSb4mcrcr6LoI",
  "success": true
}
```
----
## Course
### /api/course/list

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
  ],
  "success": true
}
```
----
### /api/course/get/\<course_id\>

**Method**: GET

**Requires**: Login, Course view

**Sample Output**:
```json
{
  "course": {
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
    ],
  },
  "success": true
}
```
----
### /api/course/add

**Method**: POST

**Requires**: Login

**Sample Input**:
```json
{
    "name": "US History",
    "sections": [
        "Hour 3",
        "Hour 5"
    ],
    "success": true
}
```

**Sample Output**:
```json
{
  "course": {
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
    ],
  },
  "success": true
}
```
----
### /api/course/update/\<course_id\>

**Method**: POST

**Requires**: Login, course edit

**Sample Input**:
```json
{
    "name": "Early US History"
}
```

**Sample Output**:
```json
{
  "course": {
    "id": 123, 
    "name": "Early US History",
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
    ],
  },
  "success": true
}
```
----
### /api/course/\<course_id\>/section/add

**Method**: POST

**Requires**: Login, course edit

**Sample Input**:
```json
{
  "name": "Hour 6"
}
```

**Sample Output**:
```json
{
  "section": {
    "id": 456,
    "name": "Hour 6"
  },
  "success": true
}
```
----
### /api/course/<course_id>/section/<section_id>/update

**Method**: POST

**Requires**: Login, course edit

**Sample Input**:
```json
{
  "name": "Hour 6a",
}
```

**Sample Output**:
```json
{
  "section": {
    "id": 456,
    "name": "Hour 6a"
  },
  "success": true
}
```
----
## Exam