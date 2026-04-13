#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政策采集器
金融产品智能匹配工具 - 政策法规数据采集
"""

import requests
from bs4 import BeautifulSoup
import feedparser
import json
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

CONFIG = {
    "output_dir": "./data/policies",
    "delay_seconds": 2,
    "timeout": 30,
}

@dataclass
class Policy:
    policy_id: str = ""
    title: str = ""
    document_number: str = ""
    source: str = ""
    issued_by: str = ""
    issued_at: str = ""
    category: str = ""
    keywords: List[str] = None
    summary: str = ""
    key_points: List[str] = None
    affected_products: List[str] = None
    source_url: str = ""
    collected_at: str = ""
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.key_points is None:
            self.key_points = []
        if self.affected_products is None:
            self.affected_products = []
    
    def to_dict(self):
        return asdict(self)


RSS_SOURCES = {
    "央行": {
        "name": "中国人民银行",
        "rss": "http://www.pbc.gov.cn/rss.xml",
        "website": "http://www.pbc.gov.cn/",
    },
    "银保监会": {
        "name": "国家金融监督管理总局",
        "rss": "http://www.cbirc.gov.cn/rss.xml",
        "website": "http://www.cbirc.gov.cn/",
    },
    "证监会": {
        "name": "中国证券监督管理委员会",
        "rss": "http://www.csrc.gov.cn/rss.xml",
        "website": "http://www.csrc.gov.cn/",
    },
}


class PolicyCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
        self.policies = []
    
    def collect(self) -> List[Policy]:
        print("=" * 60)
        print("开始采集政策法规")
        print("=" * 60)
        
        for source, info in RSS_SOURCES.items():
            if "rss" not in info:
                continue
            
            print(f"\n采集 {source}...")
            try:
                feed = feedparser.parse(info["rss"])
                for entry in feed.entries[:20]:
                    policy = self._parse_entry(entry, source, info)
                    if policy:
                        self.policies.append(policy)
                print(f"  {source}: {len(feed.entries[:20])} 条")
            except Exception as e:
                print(f"  {source} 采集失败: {e}")
            
            time.sleep(CONFIG["delay_seconds"])
        
        print(f"\n总计采集 {len(self.policies)} 条政策")
        return self.policies
    
    def _parse_entry(self, entry, source: str, info: dict) -> Optional[Policy]:
        try:
            policy = Policy()
            policy.source = source
            policy.issued_by = info["name"]
            policy.title = entry.title
            policy.source_url = entry.link
            policy.collected_at = datetime.now().isoformat()
            
            if hasattr(entry, "published"):
                policy.issued_at = entry.published
            
            # 分类
            policy.category = self._classify(entry.title)
            
            return policy
        except:
            return None
    
    def _classify(self, text: str) -> str:
        categories = {
            "供应链金融": ["供应链金融", "SCF", "供应链"],
            "票据": ["票据", "银票", "商票", "票据"],
            "保理": ["保理", "应收账款"],
            "ABS": ["资产支持", "ABS", "证券化"],
            "贷款": ["贷款", "信贷", "流动资金"],
        }
        
        for cat, keywords in categories.items():
            for kw in keywords:
                if kw in text:
                    return cat
        return "其他"
    
    def save(self, filename: str = None):
        if not filename:
            filename = f"policies_{datetime.now().strftime('%Y%m%d')}.json"
        
        import os
        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        filepath = os.path.join(CONFIG["output_dir"], filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.policies], f, ensure_ascii=False, indent=2)
        
        print(f"已保存到 {filepath}")
        return filepath


def main():
    collector = PolicyCollector()
    policies = collector.collect()
    if policies:
        collector.save()

if __name__ == "__main__":
    main()
