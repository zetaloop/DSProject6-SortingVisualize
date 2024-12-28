"""
数据生成模块

提供用于生成测试数据的工具函数。
"""

import random

def generate_data(n=10000, low=1, high=100000):
    """
    生成指定范围内的随机整数数组
    
    :param n: 要生成的随机数个数
    :param low: 随机数的最小值（包含）
    :param high: 随机数的最大值（包含）
    :return: 包含 n 个随机整数的列表
    """
    return [random.randint(low, high) for _ in range(n)]
