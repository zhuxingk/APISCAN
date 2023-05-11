# 接口文档

## 接口1

- URL: /api/v1/user
- Method: GET
- Request:
    {
        "user_id": 1,
        "name": "John"
    }
- Response(TRUE):
    {
        "errorcode": 0
    }
- Response(FALSE):
    {
        "errorcode": 13213,
        "errmsg": "xxxx"
    }

## 接口2

- URL: /api/v1/book
- Method: POST
- Request:
    {
        "book_name": "Harry Potter",
        "author": "J.K. Rowling",
        "price": 30.0
    }
- Response(TRUE):
    {
        "errorcode": 0
    }
- Response(FALSE):
    {
        "errorcode": 500,
        "errmsg": "Server error"
    }
