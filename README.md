# MyFastApi
pip install python-jose[cryptography]
学习FastApi
接口说明:
登录：
code:20000 正常返回
常见错误
code:20001
注册：

    200 OK - 请求成功。
    201 请求虽成功 但是有信息错误不能返回信息detail为错误信息
    204 token失效或认证不通过    


    201 Created - 请求已经被成功处理，并创建了新的资源。
    204 No Content - 请求已经被成功处理，但是没有返回任何数据。
    
错误码

常见的错误码定义如下：

    400 Bad Request - 请求参数不正确或格式不正确。
    401 Unauthorized - 用户未授权，需要登录或提供有效的凭据。
    403 Forbidden - 用户已授权，但是无权访问该资源。
    404 Not Found - 请求的资源不存在。
    405 Method Not Allowed - 请求方法不允许，比如使用了不支持的 HTTP 方法。
    500 Internal Server Error - 服务器内部错误，无法处理请求。
    503 Service Unavailable - 服务器暂时无法处理请求。