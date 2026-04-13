#!/usr/bin/env python3
"""
客户画像采集器
目标：从公开渠道采集企业基本信息、财务数据、供应链信息
优先级：P0
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os


class CustomerCollector:
    """客户画像采集器"""

    def __init__(self, output_dir="data/customers"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 数据源配置
        self.sources = {
            "企查查": {
                "base_url": "https://www.qcc.com",
                "search_url": "https://www.qcc.com/web/search?key={keyword}"
            },
            "天眼查": {
                "base_url": "https://www.tianyancha.com",
                "search_url": "https://www.tianyancha.com/search?key={keyword}"
            },
            "启信宝": {
                "base_url": "https://www.qixin.com",
                "search_url": "https://www.qixin.com/search?key={keyword}"
            }
        }

        # 证券代码正则（A股、港股、美股）
        self.stock_code_pattern = re.compile(r'(SH|SZ|HK|US)\d{6}|\d{6}\.(SH|SZ)')

    def collect_customer_profile(self, company_name):
        """
        采集企业客户画像

        Args:
            company_name: 企业名称

        Returns:
            客户画像字典
        """
        print(f"采集客户画像: {company_name}")

        profile = {
            "customer_id": f"CUST-{datetime.now().strftime('%Y%m%d')}-{hash(company_name) % 10000}",
            "customer_name": company_name,
            "basic_info": {},
            "financial_info": {},
            "supply_chain_info": {},
            "credit_info": {},
            "collected_at": datetime.now().isoformat()
        }

        # 采集基础信息
        profile["basic_info"] = self._collect_basic_info(company_name)

        # 采集财务信息
        if profile["basic_info"].get("stock_code"):
            profile["financial_info"] = self._collect_financial_info(
                profile["basic_info"]["stock_code"]
            )

        # 采集供应链信息（从年报）
        if profile["basic_info"].get("stock_code"):
            profile["supply_chain_info"] = self._collect_supply_chain_from_annual_report(
                profile["basic_info"]["stock_code"]
            )

        # 采集信用信息
        profile["credit_info"] = self._collect_credit_info(company_name)

        return profile

    def _collect_basic_info(self, company_name):
        """
        采集企业基础信息

        Args:
            company_name: 企业名称

        Returns:
            基础信息字典
        """
        # 尝试从多个来源采集
        for source_name, source_config in self.sources.items():
            try:
                print(f"  尝试 {source_name}...")

                # 搜索企业
                search_url = source_config["search_url"].format(keyword=company_name)
                # 注意：实际使用需要处理反爬，这里仅展示逻辑
                # response = requests.get(search_url, headers=headers)
                # soup = BeautifulSoup(response.text, 'html.parser')

                # 提取基础信息
                basic_info = {
                    "enterprise_type": "未知",
                    "industry": "未知",
                    "established_date": "未知",
                    "registered_capital": "未知",
                    "legal_representative": "未知",
                    "stock_code": None,
                    "listing_status": None
                }

                # 解析证券代码
                # stock_code_match = self.stock_code_pattern.search(company_name)
                # if stock_code_match:
                #     basic_info["stock_code"] = stock_code_match.group()
                #     basic_info["listing_status"] = "上市"

                # print(f"  ✓ 从 {source_name} 采集基础信息")
                return basic_info

            except Exception as e:
                print(f"  ✗ {source_name} 失败: {str(e)}")
                continue

        return {}

    def _collect_financial_info(self, stock_code):
        """
        采集财务信息

        Args:
            stock_code: 证券代码

        Returns:
            财务信息字典
        """
        # 从年报、季报中提取财务数据
        # 数据源：东方财富、同花顺等
        financial_info = {
            "annual_revenue": "未知",
            "net_profit": "未知",
            "total_assets": "未知",
            "total_liabilities": "未知",
            "debt_ratio": "未知",
            "cash_flow": "未知",
            "accounts_payable": "未知",
            "average_payment_period": "未知"
        }

        print(f"  采集财务信息: {stock_code}")
        # 实际实现需要调用具体的数据API

        return financial_info

    def _collect_supply_chain_from_annual_report(self, stock_code):
        """
        从年报采集供应链信息（大客户、供应商）

        Args:
            stock_code: 证券代码

        Returns:
            供应链信息字典
        """
        supply_chain_info = {
            "major_customers": [],
            "major_suppliers": [],
            "supply_chain_position": "未知",
            "dependency_ratio": "未知"
        }

        print(f"  从年报采集供应链信息: {stock_code}")

        # 数据源：
        # 1. 巨潮资讯网：http://www.cninfo.com.cn
        # 2. 上交所年报：http://www.sse.com.cn
        # 3. 深交所年报：http://www.szse.cn

        # 实际实现需要：
        # 1. 下载年报PDF
        # 2. 解析"前五大客户"、"前五大供应商"章节
        # 3. 提取客户名称、供应商名称、占比

        # 示例数据（实际应从年报解析）
        supply_chain_info["major_customers"] = [
            {"name": "核心企业A", "ratio": "30%", "amount": "150亿"},
            {"name": "核心企业B", "ratio": "20%", "amount": "100亿"}
        ]
        supply_chain_info["major_suppliers"] = [
            {"name": "供应商A", "ratio": "25%", "amount": "125亿"},
            {"name": "供应商B", "ratio": "15%", "amount": "75亿"}
        ]
        supply_chain_info["supply_chain_position"] = "一级供应商"
        supply_chain_info["dependency_ratio"] = "50%"

        return supply_chain_info

    def _collect_credit_info(self, company_name):
        """
        采集信用信息

        Args:
            company_name: 企业名称

        Returns:
            信用信息字典
        """
        credit_info = {
            "credit_rating": "未知",
            "breach_record": [],
            "litigation": [],
            "bank_limit": "未知"
        }

        print(f"  采集信用信息")
        # 实际实现需要调用信用数据API

        return credit_info

    def save_customer_profile(self, profile):
        """
        保存客户画像到文件

        Args:
            profile: 客户画像字典
        """
        customer_id = profile.get("customer_id")
        filename = f"{customer_id}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)

        print(f"  ✓ 保存客户画像: {filename}")

    def batch_collect(self, company_names):
        """
        批量采集客户画像

        Args:
            company_names: 企业名称列表
        """
        results = []

        for company_name in company_names:
            try:
                profile = self.collect_customer_profile(company_name)
                self.save_customer_profile(profile)
                results.append(profile)
            except Exception as e:
                print(f"✗ 采集失败: {company_name}, 错误: {str(e)}")

        print(f"\n✅ 批量采集完成，成功 {len(results)} 个")

        return results


def main():
    """主函数"""
    collector = CustomerCollector()

    print("="*60)
    print("客户画像采集器")
    print("="*60)

    # 示例：采集核心企业画像
    core_enterprises = [
        "华为技术有限公司",
        "比亚迪股份有限公司",
        "万科企业股份有限公司",
        "宁德时代新能源科技股份有限公司"
    ]

    print("\n批量采集核心企业画像...")
    results = collector.batch_collect(core_enterprises)


if __name__ == "__main__":
    main()
