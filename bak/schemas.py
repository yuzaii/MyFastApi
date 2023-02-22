# from typing import List, Optional
#
# from pydantic import BaseModel, Field
#
# """
# 这是用 Pydantic 定义数据模型的代码片段。在这个例子中，我们定义了一个 UserBase 模型，它表示一个用户，具有以下属性：
#
#     name：一个字符串类型的字段，表示用户的名字。
#     email：一个字符串类型的字段，表示用户的电子邮件地址。
#
# 这个模型被用于在 FastAPI 应用程序的 API 中定义请求体和响应体的格式。
#
# 我们还定义了一个 UserResponse 模型，表示在响应中返回给客户端的用户数据，它继承自 UserBase 并添加了一个 id 属性，表示用户的唯一 ID。
#
# 注意到这个模型中有一个名为 Config 的内部类，它有一个名为 orm_mode 的属性，将其设置为 True。
# 这个配置类的作用是告诉 Pydantic 模型在 ORM 模式下使用。
# 这样，Pydantic 就可以将从数据库中获取的 ORM 模型实例转换为 Pydantic 模型实例，以便我们可以将其作为 JSON 响应发送给客户端。
# """
#
#
# class UserBase(BaseModel):
#     # Option是可选的 默认为none 唯一性约束
#     # id: Optional[int] = Field(None, unique=True)
#     id: Optional[int]
#     name: str
#     password: str
#
#
# # class UserCreate(UserBase):
#
#
# class UserResponse(UserBase):
#     id: int
#
#     # 自动转成对象
#     class Config:
#         orm_mode = True
#
#
# class UserListResponse(UserBase):
#     id: int
#
#     # 自动转成对象
#     class Config:
#         orm_mode = True
#
#
# class UserCountResponse(BaseModel):
#     count: int
#
#
# class UserInfoResponse(BaseModel):
#     code: int
#     count: int
#     data: List[UserBase]
