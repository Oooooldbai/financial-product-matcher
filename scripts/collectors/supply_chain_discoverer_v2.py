#!/usr/bin/env python3
"""
供应链关系发现器 v0.2 - P0阶段实现
上市公司年报大客户/供应商解析器

定位：金融产品智能匹配工具的数据采集模块
阶段：P0 - 沪深A股上市公司

架构说明：
- DataSource: 数据源抽象层（目前用Mock，后续替换为真实API）
- Parser: 年报解析器（从PDF/HTML提取结构化数据）
- DiscoveryEngine: 发现引擎（聚合多源数据生成关系图谱）
"""

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path


# ==================== 数据模型 ====================

@dataclass
class SupplyChainRelation:
    """供应链关系数据模型"""
    company_name: str           # 本公司名称
    core_enterprise: str        # 核心企业名称（客户/供应商）
    position: str              # 位置：上游供应商 / 下游客户
    relationship_type: str     # 关系类型：核心客户 / 核心供应商
    amount: Optional[float]    # 金额（万元）
    percentage: Optional[float]  # 占比（%）
    year: int                  # 年报年份
    evidence_source: str       # 证据来源
    evidence_url: Optional[str] = None
    confidence: str = "high"   # 置信度：high / medium / low
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class AnnualReport:
    """年报数据模型"""
    company_name: str          # 公司名称
    stock_code: str           # 股票代码
    year: int                 # 年报年份
    top_customers: List[Dict]  # 前五大客户
    top_suppliers: List[Dict]  # 前五大供应商
    report_url: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "company_name": self.company_name,
            "stock_code": self.stock_code,
            "year": self.year,
            "top_customers": self.top_customers,
            "top_suppliers": self.top_suppliers,
            "report_url": self.report_url
        }


# ==================== 数据源抽象层 ====================

class DataSource(ABC):
    """数据源抽象基类"""
    
    @abstractmethod
    def get_annual_report(self, stock_code: str, year: int) -> Optional[AnnualReport]:
        """获取指定公司指定年份的年报"""
        pass
    
    @abstractmethod
    def search_company(self, keyword: str) -> List[Dict]:
        """搜索公司"""
        pass


class MockDataSource(DataSource):
    """
    Mock数据源 - 用于演示和测试
    
    【TODO】后续替换为真实数据源：
    - 巨潮资讯网 API: http://www.cninfo.com.cn/new/information/topSearch/query
    - 东方财富 API
    - 同花顺 iFinD API
    """
    
    # 模拟年报数据库（真实场景从数据库/API获取）
    MOCK_DB = {
        "002475": {  # 立讯精密
            "company_name": "立讯精密",
            "reports": {
                2023: {
                    "top_customers": [
                        {"name": "苹果公司", "amount": 17280000, "percentage": 73.28},
                        {"name": "华为技术有限公司", "amount": 1921000, "percentage": 8.15},
                        {"name": "中兴通讯", "amount": 764000, "percentage": 3.24},
                        {"name": "小米集团", "amount": 681000, "percentage": 2.89},
                        {"name": "比亚迪", "amount": 431000, "percentage": 1.83}
                    ],
                    "top_suppliers": [
                        {"name": "苹果公司", "amount": None, "percentage": 12.3},
                        {"name": "富士康", "amount": None, "percentage": 8.5},
                        {"name": "中国电子", "amount": None, "percentage": 6.2},
                        {"name": "台积电", "amount": None, "percentage": 4.8},
                        {"name": "日月光", "amount": None, "percentage": 3.5}
                    ]
                },
                2022: {
                    "top_customers": [
                        {"name": "苹果公司", "amount": 15600000, "percentage": 75.2},
                        {"name": "华为技术有限公司", "amount": 1800000, "percentage": 8.7}
                    ],
                    "top_suppliers": []
                }
            }
        },
        "002456": {  # 欧菲光
            "company_name": "欧菲光",
            "reports": {
                2023: {
                    "top_customers": [
                        {"name": "华为技术有限公司", "amount": 1562000, "percentage": 32.45},
                        {"name": "荣耀终端有限公司", "amount": 878000, "percentage": 18.23},
                        {"name": "OPPO", "amount": 605000, "percentage": 12.56},
                        {"name": "vivo", "amount": 450000, "percentage": 9.34},
                        {"name": "传音控股", "amount": 295000, "percentage": 6.12}
                    ],
                    "top_suppliers": [
                        {"name": "三星电子", "amount": None, "percentage": 15.3},
                        {"name": "京东方", "amount": None, "percentage": 11.2}
                    ]
                }
            }
        },
        "002241": {  # 歌尔股份
            "company_name": "歌尔股份",
            "reports": {
                2023: {
                    "top_customers": [
                        {"name": "Meta", "amount": 3204000, "percentage": 38.5},
                        {"name": "苹果公司", "amount": 2930000, "percentage": 35.2},
                        {"name": "索尼", "amount": 1066000, "percentage": 12.8}
                    ],
                    "top_suppliers": []
                }
            }
        },
        "300750": {  # 宁德时代
            "company_name": "宁德时代",
            "reports": {
                2023: {
                    "top_customers": [
                        {"name": "特斯拉", "amount": 5200000, "percentage": 18.2},
                        {"name": "比亚迪", "amount": 4800000, "percentage": 16.8},
                        {"name": "蔚来汽车", "amount": 2100000, "percentage": 7.3},
                        {"name": "理想汽车", "amount": 1950000, "percentage": 6.8},
                        {"name": "小鹏汽车", "amount": 1680000, "percentage": 5.9}
                    ],
                    "top_suppliers": [
                        {"name": "赣锋锂业", "amount": None, "percentage": 8.5},
                        {"name": "天齐锂业", "amount": None, "percentage": 7.2}
                    ]
                }
            }
        }
    }
    
    def get_annual_report(self, stock_code: str, year: int) -> Optional[AnnualReport]:
        """获取年报数据"""
        company_data = self.MOCK_DB.get(stock_code)
        if not company_data:
            return None
        
        report_data = company_data["reports"].get(year)
        if not report_data:
            return None
        
        return AnnualReport(
            company_name=company_data["company_name"],
            stock_code=stock_code,
            year=year,
            top_customers=report_data.get("top_customers", []),
            top_suppliers=report_data.get("top_suppliers", []),
            report_url=f"http://www.cninfo.com.cn/new/disclosure/detail?plate=sse&stockCode={stock_code}&announcementId=..."
        )
    
    def search_company(self, keyword: str) -> List[Dict]:
        """搜索公司"""
        results = []
        for code, data in self.MOCK_DB.items():
            if keyword in data["company_name"] or keyword in code:
                results.append({
                    "stock_code": code,
                    "company_name": data["company_name"]
                })
        return results


class CNInfoDataSource(DataSource):
    """
    【预留】巨潮资讯网真实数据源
    
    实现时需要：
    1. 申请API权限或实现爬虫
    2. 处理反爬机制（IP池、请求频率控制）
    3. 解析PDF年报（可用pdfplumber或PyMuPDF）
    4. 提取"前五大客户"和"前五大供应商"章节
    """
    
    BASE_URL = "http://www.cninfo.com.cn"
    
    def get_annual_report(self, stock_code: str, year: int) -> Optional[AnnualReport]:
        # TODO: 实现真实的API调用
        # 1. 搜索年报公告
        # 2. 下载PDF文件
        # 3. 解析PDF提取客户/供应商数据
        raise NotImplementedError("真实数据源待实现")
    
    def search_company(self, keyword: str) -> List[Dict]:
        # TODO: 实现真实的搜索API
        raise NotImplementedError("真实数据源待实现")


# ==================== 年报解析器 ====================

class AnnualReportParser:
    """
    年报解析器
    
    功能：
    1. 从PDF/HTML提取文本
    2. 定位"前五大客户"和"前五大供应商"章节
    3. 结构化提取数据
    """
    
    @staticmethod
    def extract_from_pdf(pdf_path: str) -> AnnualReport:
        """
        从PDF文件提取年报数据
        
        【TODO】实现真实的PDF解析
        可用库：
        - pdfplumber: 适合表格提取
        - PyMuPDF: 速度快，适合文本提取
        - pdf2text: 简单文本提取
        """
        # 模拟解析流程
        # 1. 打开PDF
        # 2. 搜索"前五名客户"、"前五名供应商"关键词
        # 3. 提取表格数据
        # 4. 结构化返回
        
        raise NotImplementedError("PDF解析功能待实现")
    
    @staticmethod
    def extract_from_html(html_content: str) -> AnnualReport:
        """
        从HTML内容提取年报数据
        
        适用于巨潮资讯网的网页版年报
        """
        # 使用BeautifulSoup解析HTML
        # 定位包含客户/供应商信息的表格
        
        raise NotImplementedError("HTML解析功能待实现")


# ==================== 发现引擎 ====================

class SupplyChainDiscoveryEngine:
    """
    供应链关系发现引擎
    
    核心功能：
    1. 聚合多源数据（年报、招标、工商等）
    2. 去重和置信度评估
    3. 生成标准化的供应链关系图谱
    """
    
    def __init__(self, data_source: DataSource):
        self.data_source = data_source
    
    def discover_from_annual_report(
        self, 
        stock_code: str, 
        year: int = 2023
    ) -> List[SupplyChainRelation]:
        """
        从年报发现供应链关系
        
        Args:
            stock_code: 股票代码
            year: 年报年份
            
        Returns:
            供应链关系列表
        """
        # 获取年报数据
        report = self.data_source.get_annual_report(stock_code, year)
        if not report:
            return []
        
        relations = []
        
        # 处理前五大客户（本公司是这些客户的上游供应商）
        for customer in report.top_customers:
            relations.append(SupplyChainRelation(
                company_name=report.company_name,
                core_enterprise=customer["name"],
                position="上游供应商",
                relationship_type="核心客户",
                amount=customer.get("amount"),
                percentage=customer.get("percentage"),
                year=year,
                evidence_source=f"{report.company_name} {year}年报",
                evidence_url=report.report_url,
                confidence="high"
            ))
        
        # 处理前五大供应商（本公司是这些供应商的下游客户）
        for supplier in report.top_suppliers:
            relations.append(SupplyChainRelation(
                company_name=report.company_name,
                core_enterprise=supplier["name"],
                position="下游客户",
                relationship_type="核心供应商",
                amount=supplier.get("amount"),
                percentage=supplier.get("percentage"),
                year=year,
                evidence_source=f"{report.company_name} {year}年报",
                evidence_url=report.report_url,
                confidence="high"
            ))
        
        return relations
    
    def discover_company(
        self, 
        stock_code: str, 
        years: List[int] = None
    ) -> Dict:
        """
        全面发现指定公司的供应链关系
        
        Args:
            stock_code: 股票代码
            years: 查询年份列表（默认最近3年）
            
        Returns:
            完整的供应链关系报告
        """
        if years is None:
            years = [2023, 2022, 2021]
        
        all_relations = []
        data_sources = []
        
        # 从年报发现
        for year in years:
            relations = self.discover_from_annual_report(stock_code, year)
            if relations:
                all_relations.extend(relations)
                data_sources.append(f"{year}年报")
        
        # 【TODO】后续添加其他数据源
        # - 招标公告数据
        # - 工商数据
        # - 新闻舆情
        
        # 去重（基于核心企业+位置+年份）
        seen = set()
        unique_relations = []
        for rel in all_relations:
            key = f"{rel.core_enterprise}#{rel.position}#{rel.year}"
            if key not in seen:
                seen.add(key)
                unique_relations.append(rel)
        
        return {
            "stock_code": stock_code,
            "company_name": all_relations[0].company_name if all_relations else "未知",
            "data_sources": list(set(data_sources)),
            "supply_chain_relations": [r.to_dict() for r in unique_relations],
            "discovery_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_relations": len(unique_relations),
            "note": "数据来源：上市公司年报（前五大客户/供应商）"
        }
    
    def discover_by_core_enterprise(
        self, 
        core_enterprise: str
    ) -> List[Dict]:
        """
        反向发现：查找所有与指定核心企业有关联的公司
        
        适用于：找到华为的所有供应商/客户
        """
        # 【TODO】需要建立倒排索引或全文搜索
        # 目前Mock数据不支持，真实场景需要数据库支持
        
        results = []
        # 遍历所有公司，查找包含该核心企业的关系
        # ...
        
        return results


# ==================== 格式化输出 ====================

class OutputFormatter:
    """格式化输出，兼容匹配引擎"""
    
    @staticmethod
    def to_matching_engine_format(discovery_result: Dict) -> Dict:
        """
        转换为匹配引擎兼容格式
        """
        relations = discovery_result.get("supply_chain_relations", [])
        
        return {
            "company_name": discovery_result["company_name"],
            "stock_code": discovery_result["stock_code"],
            "supply_chain_relations": [
                {
                    "core_enterprise": r["core_enterprise"],
                    "position": r["position"],
                    "relationship_type": r["relationship_type"],
                    "percentage": r.get("percentage"),
                    "evidence_source": r["evidence_source"],
                    "confidence": r["confidence"]
                }
                for r in relations
            ],
            "discovery_summary": {
                "total_relations": discovery_result["total_relations"],
                "data_sources": discovery_result["data_sources"],
                "discovery_time": discovery_result["discovery_time"]
            }
        }
    
    @staticmethod
    def to_markdown_report(discovery_result: Dict) -> str:
        """生成Markdown格式的报告"""
        lines = [
            f"# 供应链关系发现报告",
            f"",
            f"**公司名称**: {discovery_result['company_name']}",
            f"**股票代码**: {discovery_result['stock_code']}",
            f"**数据来源**: {', '.join(discovery_result['data_sources'])}",
            f"**发现时间**: {discovery_result['discovery_time']}",
            f"",
            f"## 供应链关系（共{discovery_result['total_relations']}条）",
            f""
        ]
        
        for i, rel in enumerate(discovery_result["supply_chain_relations"], 1):
            lines.extend([
                f"### {i}. {rel['core_enterprise']}",
                f"- **位置**: {rel['position']}",
                f"- **关系类型**: {rel['relationship_type']}",
                f"- **年份**: {rel['year']}",
            ])
            if rel.get('percentage'):
                lines.append(f"- **占比**: {rel['percentage']}%")
            if rel.get('amount'):
                lines.append(f"- **金额**: {rel['amount']/10000:.0f}万元")
            lines.extend([
                f"- **证据来源**: {rel['evidence_source']}",
                f"- **置信度**: {rel['confidence']}",
                f""
            ])
        
        return "\n".join(lines)


# ==================== 演示运行 ====================

def main():
    """主函数 - 演示供应链发现器P0阶段功能"""
    
    print("=" * 70)
    print("🔍 供应链关系发现器 v0.2 - P0阶段演示")
    print("=" * 70)
    print()
    
    # 初始化引擎（使用Mock数据源）
    data_source = MockDataSource()
    engine = SupplyChainDiscoveryEngine(data_source)
    formatter = OutputFormatter()
    
    # 测试案例
    test_cases = [
        ("002475", "立讯精密"),
        ("002456", "欧菲光"),
        ("300750", "宁德时代"),
        ("999999", "不存在公司")  # 测试无数据情况
    ]
    
    for stock_code, company_name in test_cases:
        print(f"\n{'='*70}")
        print(f"📍 查询: {company_name} ({stock_code})")
        print("="*70)
        
        # 执行发现
        result = engine.discover_company(stock_code, years=[2023, 2022])
        
        if not result["supply_chain_relations"]:
            print(f"\n⚠️  未发现供应链关系数据")
            continue
        
        # 展示结果
        print(f"\n📊 发现 {result['total_relations']} 条供应链关系")
        print(f"📎 数据来源: {', '.join(result['data_sources'])}\n")
        
        # 按位置分组
        upstream = [r for r in result["supply_chain_relations"] if r["position"] == "上游供应商"]
        downstream = [r for r in result["supply_chain_relations"] if r["position"] == "下游客户"]
        
        if upstream:
            print(f"📈 作为上游供应商（客户维度）：")
            for rel in upstream[:5]:  # 最多显示5个
                pct = f"({rel.get('percentage', 'N/A')}%)" if rel.get('percentage') else ""
                print(f"   → {rel['core_enterprise']} {pct}")
        
        if downstream:
            print(f"\n📉 作为下游客户（供应商维度）：")
            for rel in downstream[:5]:
                pct = f"({rel.get('percentage', 'N/A')}%)" if rel.get('percentage') else ""
                print(f"   → {rel['core_enterprise']} {pct}")
        
        # 输出匹配引擎格式
        print(f"\n🔄 匹配引擎兼容格式:")
        matching_format = formatter.to_matching_engine_format(result)
        print(json.dumps(matching_format, ensure_ascii=False, indent=2))
    
    # 生成完整报告示例
    print(f"\n{'='*70}")
    print("📝 完整报告示例（立讯精密）")
    print("="*70)
    report = engine.discover_company("002475")
    md_report = formatter.to_markdown_report(report)
    print(md_report[:1500] + "...\n")
    
    # 保存报告到文件
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    report_file = output_dir / f"supply_chain_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(md_report)
    
    print(f"✅ 报告已保存: {report_file}")
    
    print(f"\n{'='*70}")
    print("📋 P0阶段功能总结")
    print("="*70)
    print("""
✅ 已实现：
   1. 数据源抽象层（Mock数据源，可替换为真实API）
   2. 年报大客户/供应商解析
   3. 供应链关系结构化输出
   4. 匹配引擎兼容格式
   5. Markdown报告生成

📝 【TODO】后续扩展：
   1. 接入巨潮资讯网真实API
   2. PDF年报自动解析
   3. 招标公告数据源
   4. 工商数据穿透
   5. 反向查询（给定核心企业找所有供应商）

🎯 与主项目对接：
   可直接将 discovery_result 中的 supply_chain_relations 
   传给 matching_engine.match_customer_to_products()
""")


if __name__ == "__main__":
    main()
