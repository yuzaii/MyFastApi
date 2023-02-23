#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:encrypt.py
@time:2023/02/23
"""
import hashlib


def sha256_encrypt(password):
    # 将密码编码为二进制格式
    password_bytes = password.encode('utf-8')
    # 创建SHA-256哈希算法对象
    sha256 = hashlib.sha256()
    # 更新哈希对象的输入数据
    sha256.update(password_bytes)
    # 获取SHA-256哈希值的二进制表示
    encrypted_password = sha256.digest()
    # 将哈希值转换为16进制字符串表示
    encrypted_password_hex = encrypted_password.hex()
    # 返回加密后的密码
    return encrypted_password_hex


if __name__ == '__main__':
    password = '123456'
    encrypted_password = sha256_encrypt(password)
    print('加密后的密码：', encrypted_password)
