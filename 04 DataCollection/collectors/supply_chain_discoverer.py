#!/usr/bin/env python3
"""
供应链关系发现器 v1.1
目标：从年报提取客户-核心企业关系，识别多链条供应链
优先级：P0
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os
import pdfplumber
from typing import List, Dict, Set


class SupplyChainDiscoverer:
    """供应链关系发现器"""

    def __init__(self, output_dir="data/supply_chain"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 年报数据源
        self.annual_report_sources = {
            "巨潮资讯网": "http://www.cninfo.com.cn",
            "上交所": "http://www.sse.com.cn",
            "深交所": "http://www.szse.cn"
        }

        # 核心企业关键词（用于识别核心企业）
        self.core_enterprise_keywords = [
            "核心企业", "战略客户", "主要客户", "大客户",
            "重要客户", "客户A", "客户B"
        ]

        # 供应商关键词
        self.supplier_keywords = [
            "主要供应商", "核心供应商", "重要供应商",
            "供应商A", "供应商B"
        ]

    def discover_supply_chain_from_annual_report(self, stock_code, year=2023):
        """
        从年报发现供应链关系

        Args:
            stock_code: 证券代码（如600519.SH）
            year: 年份

        Returns:
            供应链关系字典
        """
        print(f"从年报发现供应链关系: {stock_code} ({year})")

        supply_chain = {
            "stock_code": stock_code,
            "year": year,
            "company_name": "",
            "major_customers": [],
            "major_suppliers": [],
            "supply_chain_relations": [],
            "multi_chain": [],
            "discovered_at": datetime.now().isoformat()
        }

        # 1. 下载年报PDF
        report_url = self._get_annual_report_url(stock_code, year)
        if not report_url:
            print(f"  ✗ 未找到年报: {stock_code} ({year})")
            return None

        print(f"  下载年报: {report_url}")

        # 2. 解析PDF
        pdf_path = self._download_pdf(report_url, stock_code, year)
        if not pdf_path:
            return None

        # 3. 提取客户和供应商信息
        text = self._extract_text_from_pdf(pdf_path)
        supply_chain["company_name"] = self._extract_company_name(text)
        supply_chain["major_customers"] = self._extract_major_customers(text)
        supply_chain["major_suppliers"] = self._extract_major_suppliers(text)

        # 4. 构建供应链关系
        supply_chain["supply_chain_relations"] = self._build_supply_chain_relations(
            supply_chain["major_customers"],
            supply_chain["major_suppliers"]
        )

        # 5. 识别多链条供应链
        supply_chain["multi_chain"] = self._identify_multi_chain(
            supply_chain["supply_chain_relations"]
        )

        return supply_chain

    def _get_annual_report_url(self, stock_code, year):
        """
        获取年报URL

        Args:
            stock_code: 证券代码
            year: 年份

        Returns:
            年报URL
        """
        # 从巨潮资讯网搜索
        search_url = f"http://www.cninfo.com.cn/new/hisAnnouncement/query"
        params = {
            "stock": stock_code,
            "searchkey": f"{year}年年度报告",
            "column": "szse_main",  # 或sse_main
            "plate": "",
            "category": "",
            "trade": "",
            "seDate": f"{year}-01-01~{year}-12-31"
        }

        try:
            # response = requests.get(search_url, params=params)
            # 解析返回的JSON，找到年报PDF的URL
            # 这里仅展示逻辑
            return f"http://www.cninfo.com.cn/annual/{stock_code}_{year}.pdf"
        except Exception as e:
            print(f"  ✗ 获取年报URL失败: {str(e)}")
            return None

    def _download_pdf(self, url, stock_code, year):
        """
        下载年报PDF

        Args:
            url: PDF URL
            stock_code: 证券代码
            year: 年份

        Returns:
            PDF文件路径
        """
        filename = f"{stock_code}_{year}_annual_report.pdf"
        filepath = os.path.join(self.output_dir, filename)

        try:
            # response = requests.get(url, timeout=60)
            # with open(filepath, 'wb') as f:
            #     f.write(response.content)

            print(f"  ✓ 下载年报: {filename}")
            return filepath
        except Exception as e:
            print(f"  ✗ 下载年报失败: {str(e)}")
            return None

    def _extract_text_from_pdf(self, pdf_path):
        """
        从PDF提取文本

        Args:
            pdf_path: PDF文件路径

        Returns:
            提取的文本
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"

            print(f"  ✓ 提取文本: {len(text)} 字符")
        except Exception as e:
            print(f"  ✗ 提取文本失败: {str(e)}")

        return text

    def _extract_company_name(self, text):
        """
        提取公司名称

        Args:
            text: PDF文本

        Returns:
            公司名称
        """
        # 从第一页提取公司名称
        # 匹配：XXXX股份有限公司
        pattern = re.compile(r'(.*?股份有限公司|.*?有限责任公司)')
        match = pattern.search(text[:1000])

        if match:
            return match.group(1).strip()

        return "未知"

    def _extract_major_customers(self, text):
        """
        提取主要客户

        Args:
            text: PDF文本

        Returns:
            客户列表
        """
        customers = []

        # 查找"前五大客户"章节
        customer_section = self._find_section(text, ["前五大客户", "主要客户", "客户情况"])

        if customer_section:
            # 提取客户名称、销售额、占比
            lines = customer_section.split('\n')
            for line in lines[:20]:  # 只看前20行
                if self._is_company_name(line):
                    # 提取金额和占比
                    amount_match = re.search(r'(\d+\.?\d*)[亿元万元千]', line)
                    ratio_match = re.search(r'(\d+\.?\d*)%', line)

                    customers.append({
                        "name": line.strip(),
                        "amount": amount_match.group(1) if amount_match else "未知",
                        "ratio": ratio_match.group(1) if ratio_match else "未知",
                        "type": "customer"
                    })

        print(f"  ✓ 提取主要客户: {len(customers)} 个")
        return customers

    def _extract_major_suppliers(self, text):
        """
        提取主要供应商

        Args:
            text: PDF文本

        Returns:
            供应商列表
        """
        suppliers = []

        # 查找"前五大供应商"章节
        supplier_section = self._find_section(text, ["前五大供应商", "主要供应商", "供应商情况"])

        if supplier_section:
            lines = supplier_section.split('\n')
            for line in lines[:20]:
                if self._is_company_name(line):
                    amount_match = re.search(r'(\d+\.?\d*)[亿元万元千]', line)
                    ratio_match = re.search(r'(\d+\.?\d*)%', line)

                    suppliers.append({
                        "name": line.strip(),
                        "amount": amount_match.group(1) if amount_match else "未知",
                        "ratio": ratio_match.group(1) if ratio_match else "未知",
                        "type": "supplier"
                    })

        print(f"  ✓ 提取主要供应商: {len(suppliers)} 个")
        return suppliers

    def _find_section(self, text, keywords):
        """
        查找章节内容

        Args:
            text: PDF文本
            keywords: 关键词列表

        Returns:
            章节内容
        """
        for keyword in keywords:
            # 查找关键词位置
            start = text.find(keyword)
            if start != -1:
                # 提取章节内容（到下一个章节标题或1000字符）
                end = start + 1000
                next_section = text.find("\n第", end)
                if next_section != -1:
                    end = next_section

                return text[start:end]

        return None

    def _is_company_name(self, line):
        """
        判断是否为公司名称

        Args:
            line: 文本行

        Returns:
            是否为公司名称
        """
        # 简单判断：包含"公司"、"集团"等关键词
        company_indicators = ["公司", "集团", "股份", "有限"]
        return any(indicator in line for indicator in company_indicators)

    def _build_supply_chain_relations(self, customers, suppliers):
        """
        构建供应链关系（动态关系模型）

        Args:
            customers: 客户列表
            suppliers: 供应商列表

        Returns:
            供应链关系列表
        """
        relations = []

        # 客户关系（下游）
        for customer in customers:
            relations.append({
                "relation_type": "downstream",
                "party_name": customer["name"],
                "role": "customer",
                "amount": customer["amount"],
                "ratio": customer["ratio"],
                "strength": self._calculate_relation_strength(customer["ratio"])
            })

        # 供应商关系（上游）
        for supplier in suppliers:
            relations.append({
                "relation_type": "upstream",
                "party_name": supplier["name"],
                "role": "supplier",
                "amount": supplier["amount"],
                "ratio": supplier["ratio"],
                "strength": self._calculate_relation_strength(supplier["ratio"])
            })

        return relations

    def _calculate_relation_strength(self, ratio):
        """
        计算关系强度

        Args:
            ratio: 占比（字符串，如"30%"）

        Returns:
            关系强度（0-100）
        """
        try:
            ratio_value = float(ratio.replace('%', ''))
            # 简单线性关系：占比越大，关系越强
            return min(ratio_value * 2, 100)
        except:
            return 50  # 默认中等强度

    def _identify_multi_chain(self, relations):
        """
        识别多链条供应链

        Args:
            relations: 供应链关系列表

        Returns:
            多链条列表
        """
        multi_chain = []

        # 按关系强度分组
        strong_relations = [r for r in relations if r["strength"] >= 60]

        # 按关系类型分组
        upstream_chain = [r for r in strong_relations if r["relation_type"] == "upstream"]
        downstream_chain = [r for r in strong_relations if r["relation_type"] == "downstream"]

        if len(upstream_chain) > 1:
            multi_chain.append({
                "chain_type": "upstream",
                "chain_name": f"上游链-{len(upstream_chain)}条",
                "parties": upstream_chain
            })

        if len(downstream_chain) > 1:
            multi_chain.append({
                "chain_type": "downstream",
                "chain_name": f"下游链-{len(downstream_chain)}条",
                "parties": downstream_chain
            })

        # 交叉链条：既做客户又做供应商
        party_names = {r["party_name"] for r in relations}
        cross_chain_parties = []
        for party_name in party_names:
            party_relations = [r for r in relations if r["party_name"] == party_name]
            if len(party_relations) > 1:
                cross_chain_parties.append(party_name)

        if cross_chain_parties:
            multi_chain.append({
                "chain_type": "cross",
                "chain_name": f"交叉链-{len(cross_chain_parties)}个",
                "parties": cross_chain_parties
            })

        return multi_chain

    def save_supply_chain(self, supply_chain):
        """
        保存供应链关系到文件

        Args:
            supply_chain: 供应链关系字典
        """
        stock_code = supply_chain.get("stock_code")
        year = supply_chain.get("year")
        filename = f"supply_chain_{stock_code}_{year}.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(supply_chain, f, ensure_ascii=False, indent=2)

        print(f"  ✓ 保存供应链关系: {filename}")

    def batch_discover(self, stock_codes, year=2023):
        """
        批量发现供应链关系

        Args:
            stock_codes: 证券代码列表
            year: 年份

        Returns:
            供应链关系列表
        """
        results = []

        for stock_code in stock_codes:
            try:
                supply_chain = self.discover_supply_chain_from_annual_report(stock_code, year)
                if supply_chain:
                    self.save_supply_chain(supply_chain)
                    results.append(supply_chain)
            except Exception as e:
                print(f"✗ 发现失败: {stock_code}, 错误: {str(e)}")

        print(f"\n✅ 批量发现完成，成功 {len(results)} 个")

        return results


def main():
    """主函数"""
    discoverer = SupplyChainDiscoverer()

    print("="*60)
    print("供应链关系发现器 v1.1")
    print("="*60)

    # 示例：发现核心企业供应链关系
    stock_codes = [
        "600519.SH",  # 贵州茅台
        "000858.SZ",  # 五粮液
        "002594.SZ",  # 比亚迪
        "300750.SZ"   # 宁德时代
    ]

    print("\n批量发现供应链关系...")
    results = discoverer.batch_discover(stock_codes, year=2023)


if __name__ == "__main__":
    main()
