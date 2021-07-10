
# import jwt
#
# # 第一部分的header，一般不需要指定，有默认值
#
# # 第二部分，可以指定后端需要存放的一些非敏感的信息
# payload = {
#     'username': '小李',
#     'age': 18
# }
# # 服务端创建token令牌的过程
# token = jwt.encode(payload, key='666')
#
# # 服务端对前端用户传递的token进行解密过程
# one_var = jwt.decode(token, key='667')
# pass

