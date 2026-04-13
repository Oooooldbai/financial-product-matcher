#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行产品采集器
金融产品智能匹配工具 - 产品数据采集
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

CONFIG = {
    "output_dir": "./data/products",
    "delay_seconds": 2,
    "timeout": 30,
    "max_retries": 3,
}

@dataclass
class BankProduct:
    product_id: str = ""
    product_name: str = ""
    product_type: str = ""
    bank_name: str = ""
    bank_type: str = ""
    min_amount: str = ""
    max_amount: str = ""
    interest_rate: str = ""
    term_range: str = ""
    target_enterprise_types: List[str] = None
    target_industries: List[str] = None
    min_scale: str = ""
    credit_requirement: str = ""
    guarantee_type: str = ""
    core_enterprise_required: bool = False
    description: str = ""
    source_url: str = ""
    collected_at: str = ""
    
    def __post_init__(self):
        if self.target_enterprise_types is None:
            self.target_enterprise_types = []
        if self.target_industries is None:
            self.target_industries = []
    
    def to_dict(self):
        return asdict(self)


BANK_DATA = {
    "国有大行": [
        {"name": "工商银行", "url": "https://www.icbc.com.cn"},
        {"name": "农业银行", "url": "https://www.abchina.com"},
        {"name": "中国银行", "url": "https://www.boc.cn"},
        {"name": "建设银行", "url": "https://www.ccb.com"},
        {"name": "交通银行", "url": "https://www.bankcomm.com"},
        {"name": "邮储银行", "url": "https://www.psbc.com"},
    ],
    "股份制银行": [
        {"name": "招商银行", "url": "https://www.cmbchina.com"},
        {"name": "浦发银行", "url": "https://www.spdb.com.cn"},
        {"name": "中信银行", "url": "https://www.citicbank.com"},
        {"name": "民生银行", "url": "https://www.cmbc.com.cn"},
        {"name": "兴业银行", "url": "https://www.cib.com.cn"},
        {"name": "光大银行", "url": "https://www.cebbank.com"},
        {"name": "平安银行", "url": "https://bank.pingan.com"},
        {"name": "华夏银行", "url": "https://www.hxb.com.cn"},
        {"name": "广发银行", "url": "https://www.cgbchina.com.cn"},
        {"name": "浙商银行", "url": "https://www.czbank.com"},
        {"name": "渤海银行", "url": "https://www.cbhb.com.cn"},
        {"name": "恒丰银行", "url": "https://www.hfbank.com.cn"},
    ],
    "民营互联网银行": [
        {"name": "微众银行", "url": "https://www.webank.com"},
        {"name": "网商银行", "url": "https://mybank.cn"},
        {"name": "苏商银行", "url": "https://www.s-bank.com.cn"},
        {"name": "众邦银行", "url": "https://www.zhunjun.com"},
        {"name": "新网银行", "url": "https://www.xwbank.com"},
        {"name": "亿联银行", "url": "https://www.yillion.com"},
        {"name": "三湘银行", "url": "https://www.sx-bank.com"},
        {"name": "振兴银行", "url": "https://www.zx-bank.com"},
        {"name": "裕民银行", "url": "https://www.yuminbank.com"},
        {"name": "新安银行", "url": "https://www.xin-anbank.com"},
        {"name": "金城银行", "url": "https://www.jcbank.com.cn"},
        {"name": "梅州客商银行", "url": "https://www.mzskbank.com"},
        {"name": "锡商银行", "url": "https://www.xishangbank.com"},
        {"name": "华通银行", "url": "https://www.huotongbank.com"},
        {"name": "蓝海银行", "url": "https://www.bankofblueocean.com"},
        {"name": "中关村银行", "url": "https://www.zgcbank.com"},
        {"name": "富民银行", "url": "https://www.fuminbank.com"},
        {"name": "众裕银行", "url": "https://www.zy-bank.com.cn"},
        {"name": "民丰银行", "url": "https://www.minfengbank.com"},
    ],
    "外资银行": [
        {"name": "汇丰银行", "url": "https://www.hsbc.com.cn"},
        {"name": "花旗银行", "url": "https://www.citibank.com.cn"},
        {"name": "渣打银行", "url": "https://www.standardchartered.com.cn"},
        {"name": "星展银行", "url": "https://www.dbs.com.cn"},
        {"name": "摩根大通", "url": "https://www.jpmorgan.com.cn"},
    ],
}


class BankProductCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
        self.products = []
    
    def collect(self) -> List[BankProduct]:
        print("=" * 60)
        print("开始采集银行产品数据")
        print("=" * 60)
        
        for bank_type, banks in BANK_DATA.items():
            print(f"\n采集 {bank_type} ({len(banks)} 家)")
            for bank in banks:
                try:
                    products = self._collect_bank(bank, bank_type)
                    print(f"  {bank['name']}: {len(products)} 个产品")
                    self.products.extend(products)
                except Exception as e:
                    print(f"  {bank['name']} 采集失败: {e}")
        
        print(f"\n总计采集 {len(self.products)} 个产品")
        return self.products
    
    def _collect_bank(self, bank: dict, bank_type: str) -> List[BankProduct]:
        products = []
        time.sleep(CONFIG["delay_seconds"])
        
        try:
            response = self.session.get(bank["url"], timeout=CONFIG["timeout"])
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # 尝试提取产品信息
                products = self._extract_products(soup, bank, bank_type)
        except Exception as e:
            pass
        
        return products
    
    def _extract_products(self, soup: BeautifulSoup, bank: dict, bank_type: str) -> List[BankProduct]:
        products = []
        text = soup.get_text()[:5000]
        
        # 关键词匹配识别产品类型
        product_types = {
            "供应链金融": ["供应链金融", "SCF", "供应链"],
            "票据": ["票据", "银票", "商票", "承兑", "贴现"],
            "保理": ["保理", "应收账款融资"],
            "贷款": ["贷款", "流动资金", "信用贷款"],
        }
        
        for ptype, keywords in product_types.items():
            for kw in keywords:
                if kw in text:
                    product = BankProduct()
                    product.bank_name = bank["name"]
                    product.bank_type = bank_type
                    product.product_type = ptype
                    product.product_name = f"{bank['name']}-{ptype}"
                    product.description = f"从{bank['name']}官网识别到的{ptype}产品"
                    product.source_url = bank["url"]
                    product.collected_at = datetime.now().isoformat()
                    products.append(product)
                    break
        
        return products
    
    def save(self, filename: str = None):
        if not filename:
            filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        filepath = os.path.join(CONFIG["output_dir"], filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.products], f, ensure_ascii=False, indent=2)
        
        print(f"已保存 {len(self.products)} 条产品数据到 {filepath}")
        return filepath


def main():
    collector = BankProductCollector()
    products = collector.collect()
    if products:
        collector.save()

if __name__ == "__main__":
    main()
