#!/usr/bin/env python3
"""
政策法规采集器
目标：采集央行、银保监、证监会等政策文件
优先级：P0
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import re
import os

class PolicyCollector:
    """政策文件采集器"""

    def __init__(self, output_dir="data/policies"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 政策来源配置
        self.sources = {
            "央行": {
                "rss": "http://www.pbc.gov.cn/rss.xml",
                "base_url": "http://www.pbc.gov.cn",
                "category": "货币政策"
            },
            "国家金融监督管理总局": {
                "rss": "http://www.nfra.gov.cn/rss.xml",
                "base_url": "http://www.nfra.gov.cn",
                "category": "监管政策"
            },
            "证监会": {
                "rss": "http://www.csrc.gov.cn/rss.xml",
                "base_url": "http://www.csrc.gov.cn",
                "category": "证券监管"
            },
            "财政部": {
                "rss": "http://www.mof.gov.cn/rss.xml",
                "base_url": "http://www.mof.gov.cn",
                "category": "财政政策"
            },
        }

        # 关键词过滤
        self.keywords = [
            "供应链金融", "票据", "应收账款", "保理",
            "中小企业", "融资", "风险管理", "合规",
            "票据法", "民法典", "支付结算", "流动性"
        ]

    def collect_policies(self, days=30):
        """
        采集最近N天的政策文件

        Args:
            days: 采集最近多少天的政策
        """
        results = []

        for source_name, source_config in self.sources.items():
            print(f"采集 {source_name} 政策...")

            try:
                rss_url = source_config["rss"]
                base_url = source_config["base_url"]
                category = source_config["category"]

                # 读取RSS
                feed = feedparser.parse(rss_url)

                for entry in feed.entries:
                    # 检查日期
                    pub_date = entry.get('published_parsed')
                    if pub_date:
                        pub_date = datetime(*pub_date[:6])
                        if datetime.now() - pub_date > timedelta(days=days):
                            continue

                    # 检查关键词
                    title = entry.get('title', '')
                    content = entry.get('description', '')
                    text = title + " " + content

                    if not any(keyword in text for keyword in self.keywords):
                        continue

                    # 提取政策详情
                    policy_url = entry.get('link')
                    policy = self.extract_policy_details(policy_url, base_url)

                    if policy:
                        policy.update({
                            "source": source_name,
                            "category": category,
                            "collected_at": datetime.now().isoformat()
                        })
                        results.append(policy)

                        print(f"  ✓ 采集: {title[:50]}...")

            except Exception as e:
                print(f"  ✗ 错误: {str(e)}")

        return results

    def extract_policy_details(self, url, base_url):
        """
        提取政策详情

        Args:
            url: 政策URL
            base_url: 基础URL（用于处理相对链接）

        Returns:
            政策详情字典
        """
        try:
            response = requests.get(url, timeout=30)
            response.encoding = 'utf-8'
            html = response.text

            soup = BeautifulSoup(html, 'html.parser')

            # 提取标题
            title = soup.find('h1')
            if not title:
                title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ""

            # 提取发布日期
            pub_date = None
            date_patterns = [
                r'(\d{4})年(\d{1,2})月(\d{1,2})日',
                r'(\d{4}-\d{1,2}-\d{1,2})',
                r'(\d{4}/\d{1,2}/\d{1,2})'
            ]
            for pattern in date_patterns:
                match = re.search(pattern, html)
                if match:
                    pub_date = match.group(0)
                    break

            # 提取正文
            content_div = soup.find('div', class_='content')
            if not content_div:
                content_div = soup.find('div', class_='article')
            if not content_div:
                content_div = soup.find('div', id='content')

            if content_div:
                # 移除脚本和样式
                for script in content_div(['script', 'style']):
                    script.decompose()
                content_text = content_div.get_text(separator='\n', strip=True)
            else:
                # 备用方案：提取所有段落
                paragraphs = soup.find_all('p')
                content_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])

            # 提取附件（PDF、DOC等）
            attachments = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if any(ext in href for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                    # 处理相对URL
                    if href.startswith('/'):
                        href = base_url + href
                    elif not href.startswith('http'):
                        continue

                    attachments.append({
                        "type": href.split('.')[-1].upper(),
                        "url": href,
                        "name": link.get_text(strip=True)
                    })

            return {
                "policy_id": f"POL-{datetime.now().strftime('%Y%m%d')}-{len(os.listdir(self.output_dir))}",
                "title": title_text,
                "url": url,
                "pub_date": pub_date,
                "content": content_text[:5000],  # 限制长度
                "attachments": attachments,
                "keywords": self._extract_keywords(title_text + content_text)
            }

        except Exception as e:
            print(f"    ✗ 提取详情失败: {str(e)}")
            return None

    def _extract_keywords(self, text):
        """
        提取关键词

        Args:
            text: 文本内容

        Returns:
            关键词列表
        """
        keywords = []
        for keyword in self.keywords:
            if keyword in text:
                keywords.append(keyword)
        return keywords

    def save_policies(self, policies):
        """
        保存政策到文件

        Args:
            policies: 政策列表
        """
        for policy in policies:
            policy_id = policy.get("policy_id")
            filename = f"{policy_id}.json"
            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(policy, f, ensure_ascii=False, indent=2)

            print(f"  ✓ 保存: {filename}")

        print(f"\n✅ 共保存 {len(policies)} 条政策")

    def generate_index(self):
        """
        生成政策索引文件
        """
        policies = []
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    policy = json.load(f)
                    policies.append({
                        "policy_id": policy.get("policy_id"),
                        "title": policy.get("title"),
                        "source": policy.get("source"),
                        "category": policy.get("category"),
                        "pub_date": policy.get("pub_date"),
                        "keywords": policy.get("keywords"),
                        "url": policy.get("url")
                    })

        # 按发布日期排序
        policies.sort(key=lambda x: x.get("pub_date", ""), reverse=True)

        # 保存索引
        index_file = os.path.join(self.output_dir, "index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(policies, f, ensure_ascii=False, indent=2)

        print(f"✅ 生成政策索引: {len(policies)} 条")


def main():
    """主函数"""
    collector = PolicyCollector()

    print("="*60)
    print("政策法规采集器")
    print("="*60)

    # 采集最近30天的政策
    print("\n开始采集最近30天的政策...")
    policies = collector.collect_policies(days=30)

    if policies:
        # 保存政策
        print("\n保存政策文件...")
        collector.save_policies(policies)

        # 生成索引
        print("\n生成政策索引...")
        collector.generate_index()
    else:
        print("\n⚠️  未采集到政策文件")


if __name__ == "__main__":
    main()
