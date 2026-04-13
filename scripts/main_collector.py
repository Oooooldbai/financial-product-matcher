#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主采集程序
金融产品智能匹配工具 - 一键采集所有数据

功能：
- 采集银行产品（国有大行/股份制/民营互联网/外资）
- 采集政策法规（央行/银保监会/证监会/财政部）
- 采集财经媒体产品线索
- 统一保存到data目录

使用方法：
    python main_collector.py              # 采集所有
    python main_collector.py --products   # 仅采集产品
    python main_collector.py --policies  # 仅采集政策
"""

import argparse
import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collectors.bank_product_collector import BankProductCollector
from collectors.policy_collector import PolicyCollector
from datetime import datetime


def collect_products():
    """采集产品数据"""
    print("\n" + "=" * 60)
    print("采集产品数据")
    print("=" * 60)
    
    # 银行产品采集器
    collector = BankProductCollector()
    products = collector.collect()
    
    # 保存
    if products:
        collector.save()
    
    print(f"\n产品采集完成，共 {len(products)} 条")
    return products


def collect_policies():
    """采集政策数据"""
    print("\n" + "=" * 60)
    print("采集政策数据")
    print("=" * 60)
    
    collector = PolicyCollector()
    policies = collector.collect()
    
    if policies:
        collector.save()
    
    print(f"\n✓ 政策采集完成，共 {len(policies)} 条")
    return policies


def main():
    parser = argparse.ArgumentParser(description="金融产品采集程序")
    parser.add_argument("--products", action="store_true", help="仅采集产品")
    parser.add_argument("--policies", action="store_true", help="仅采集政策")
    parser.add_argument("--all", action="store_true", help="采集所有（默认）")
    
    args = parser.parse_args()
    
    # 确定采集范围
    collect_all = args.all or (not args.products and not args.policies)
    
    start_time = datetime.now()
    
    print("\n" + "=" * 60)
    print("金融产品智能匹配工具 - 数据采集")
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    total_products = 0
    total_policies = 0
    
    if collect_all or args.products:
        products = collect_products()
        total_products = len(products)
    
    if collect_all or args.policies:
        policies = collect_policies()
        total_policies = len(policies)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("采集完成")
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"耗时: {duration:.1f} 秒")
    print(f"产品: {total_products} 条")
    print(f"政策: {total_policies} 条")
    print("=" * 60)


if __name__ == "__main__":
    main()
