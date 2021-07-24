# -*- coding: utf-8 -*-
def get_file_content(filename, chunk_size=1024):
    #chunk_size=1024 表示每次获取1024个字节
    with open(filename, encoding='utf-8') as file:
        while True:
            content = file.read(chunk_size)
            # 如果文件结尾，那么content为None
            if not content:
                break
            yield content
