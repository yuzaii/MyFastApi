#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:Pagination.py
@time:2023/02/27
"""


class Pagination(object):
    """
    一个自定义的分页器。
    """

    def __init__(self, query, page=1, per_page=10):
        """

        :param query: sqlalchemy的qurey对象
        :param page: 页数 也就是第几页
        :param per_page: 每页多少条数据
        """
        self.query = query
        self.page = page
        self.per_page = per_page

    def paginate(self):
        total = self.query.count()
        if total == 0:
            return [], total
        pages = (total - 1) // self.per_page + 1
        if self.page > pages:
            # 超出总页数时返回最后一页的所有数据
            self.page = pages
        offset = (self.page - 1) * self.per_page
        limit = min(self.per_page, total - offset)
        data = self.query.offset(offset).limit(limit).all()
        return data, total
    # def paginate(self):
    #     """
    #     实现分页器的核心逻辑，返回查询结果中对应页的数据和总页数。
    #     得修改一下如果超出了数据 就返回
    #     """
    #     total = self.query.count()  # 查询结果的总数
    #     print("获取到的总数：", total)
    #     offset = (self.page - 1) * self.per_page  # 计算查询结果的偏移量
    #     print('offset:', offset)
    #     data = self.query.offset(offset).limit(self.per_page).all()  # 获取查询结果的分页数据
    #     pages = (total - 1) // self.per_page + 1  # 计算查询结果的总页数
    #
    #     return data, pages
