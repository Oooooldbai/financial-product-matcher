#!/usr/bin/env python3
"""
供应链关系发现器 v0.1

定位：金融产品匹配工具的客户库数据采集模块
功能：从公开数据源自动发现企业供应链关系

当前实现：
- 模拟解析上市公司年报中的大客户/供应商信息
- 输出与匹配引擎兼容的格式
"""

import json
from typing import Dict, List, Optional

# ==================== 模拟年报数据库 ====================

# 模拟已解析的上市公司年报数据（前五大客户/供应商）
MOCK_ANNUAL_REPORT_DB = {
    "立讯精密": {
        "is_listed": True,
        "stock_code": "002475",
        "report_year": 2023,
        "top_5_customers": [
            {"name": "苹果公司", "percentage": 73.28, "amount": 1728.0},  # 单位：亿元
            {"name": "华为技术有限公司", "percentage": 8.15, "amount": 192.1},
            {"name": "中兴通讯", "percentage": 3.24, "amount": 76.4},
            {"name": "小米集团", "percentage": 2.89, "amount": 68.1},
            {"name": "比亚迪", "percentage": 1.83, "amount": 43.1}
        ],
        "top_5_suppliers": [
            {"name": "苹果公司", "percentage": 12.3},  # 核心零部件
            {"name": "富士康", "percentage": 8.5},
            {"name": "中国电子", "percentage": 6.2},
            {"name": "台积电", "percentage": 4.8},
            {"name": "日月光", "percentage": 3.5}
        ]
    },
    "欧菲光": {
        "is_listed": True,
        "stock_code": "002456",
        "report_year": 2023,
        "top_5_customers": [
            {"name": "华为技术有限公司", "percentage": 32.45, "amount": 156.2},
            {"name": "荣耀终端有限公司", "percentage": 18.23, "amount": 87.8},
            {"name": "OPPO", "percentage": 12.56, "amount": 60.5},
            {"name": "vivo", "percentage": 9.34, "amount": 45.0},
            {"name": "传音控股", "percentage": 6.12, "amount": 29.5}
        ],
        "top_5_suppliers": [
            {"name": "三星电子", "percentage": 15.3},
            {"name": "京东方", "percentage": 11.2},
            {"name": "索尼", "percentage": 8.7}
        ]
    },
    "歌尔股份": {
        "is_listed": True,
        "stock_code": "002241",
        "report_year": 2023,
        "top_5_customers": [
            {"name": "Meta", "percentage": 38.5, "amount": 320.4},
            {"name": "苹果公司", "percentage": 35.2, "amount": 293.0},
            {"name": "索尼", "percentage": 12.8, "amount": 106.6}
        ],
        "top_5_suppliers": []
    }
}

# 模拟招标中标数据（部分公开数据）
MOCK_BID_DATA = [
    {
        "project_name": "华为2024年度供应链供应商招标",
        "winner": "深圳XX电子科技有限公司",
        "core_enterprise": "华为",
        "position": "上游供应商",
        "bid_amount": 50000000,
        "bid_date": "2024-03-15",
        "source": "中国招标投标公共服务平台"
    },
    {
        "project_name": "比亚迪新能源汽车电池组件采购",
        "winner": "宁德时代",
        "core_enterprise": "比亚迪",
        "position": "上游供应商",
        "bid_amount": 1200000000,
        "bid_date": "2024-02-20",
        "source": "中国政府采购网"
    },
    {
        "project_name": "某三甲医院医疗设备采购",
        "winner": "杭州XX科技有限公司",
        "core_enterprise": "西门子",
        "position": "下游经销商",
        "bid_amount": 28000000,
        "bid_date": "2024-01-10",
        "source": "各省公共资源交易中心"
    }
]


# ==================== 核心发现引擎 ====================

def discover_from_annual_report(company_name: str) -> Optional[List[Dict]]:
    """
    从年报数据发现供应链关系
    
    逻辑：
    1. 查询公司是否上市
    2. 如果是：提取前五大客户（作为下游）和供应商（作为上游）
    3. 生成供应链关系列表
    
    Returns:
        [{core_enterprise, position, evidence_source, confidence, percentage}, ...]
    """
    if company_name not in MOCK_ANNUAL_REPORT_DB:
        return None
    
    report = MOCK_ANNUAL_REPORT_DB[company_name]
    relations = []
    
    # 前五大客户 = 该公司是这些客户的上游供应商
    for customer in report.get("top_5_customers", []):
        relations.append({
            "core_enterprise": customer["name"],
            "position": "上游供应商",
            "relationship_type": "核心客户",
            "evidence_source": f"{company_name} {report['report_year']}年报",
            "evidence_url": f"https://www.cninfo.com.cn/{report['stock_code']}.pdf",
            "confidence": "high",
            "revenue_percentage": customer.get("percentage"),
            "annual_amount_wan": customer.get("amount", 0) * 10000  # 亿元转万元
        })
    
    # 前五大供应商 = 该公司是这些供应商的下游客户
    for supplier in report.get("top_5_suppliers", []):
        relations.append({
            "core_enterprise": supplier["name"],
            "position": "下游客户",
            "relationship_type": "核心供应商",
            "evidence_source": f"{company_name} {report['report_year']}年报",
            "evidence_url": f"https://www.cninfo.com.cn/{report['stock_code']}.pdf",
            "confidence": "high",
            "procurement_percentage": supplier.get("percentage")
        })
    
    return relations


def discover_from_bid_data(company_name: str) -> Optional[List[Dict]]:
    """
    从招标中标数据发现供应链关系
    
    逻辑：查询公司是否在公开中标公告中出现
    """
    relations = []
    
    for bid in MOCK_BID_DATA:
        if bid["winner"] == company_name:
            relations.append({
                "core_enterprise": bid["core_enterprise"],
                "position": bid["position"],
                "relationship_type": "中标供应商",
                "bid_amount": bid["bid_amount"],
                "bid_date": bid["bid_date"],
                "evidence_source": bid["source"],
                "confidence": "high",
                "evidence_url": f"https://ggzy.court.gov.cn/{bid['bid_date'].replace('-', '')}"
            })
    
    return relations if relations else None


def discover_supply_chain_relations(company_name: str) -> Dict:
    """
    供应链关系发现主函数
    
    聚合多个数据源的信息
    
    Returns:
        {
            "company_name": str,
            "data_sources": [str],
            "supply_chain_relations": [{...}],
            "discovery_time": str,
            "note": str
        }
    """
    from datetime import datetime
    
    all_relations = []
    data_sources = []
    
    # 数据源1：年报
    annual_relations = discover_from_annual_report(company_name)
    if annual_relations:
        all_relations.extend(annual_relations)
        data_sources.append("年报")
    
    # 数据源2：招标
    bid_relations = discover_from_bid_data(company_name)
    if bid_relations:
        all_relations.extend(bid_relations)
        data_sources.append("招标公告")
    
    # 去重（基于 core_enterprise + position）
    seen = set()
    unique_relations = []
    for rel in all_relations:
        key = f"{rel['core_enterprise']}#{rel['position']}"
        if key not in seen:
            seen.add(key)
            unique_relations.append(rel)
    
    return {
        "company_name": company_name,
        "data_sources": data_sources,
        "supply_chain_relations": unique_relations,
        "discovery_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": "仅包含公开数据源" if data_sources else "未发现公开供应链关系数据"
    }


def format_for_matching_engine(result: Dict) -> Dict:
    """
    将发现结果转换为匹配引擎兼容格式
    
    输出与 matching_engine.py 中的 SAMPLE_CUSTOMER 结构一致
    """
    relations = result.get("supply_chain_relations", [])
    
    # 构建匹配引擎需要的格式
    formatted_relations = []
    for rel in relations:
        formatted_relations.append({
            "core_enterprise": rel["core_enterprise"],
            "position": rel["position"],
            "relationship_type": rel.get("relationship_type", "供应关系"),
            "evidence_source": rel["evidence_source"],
            "confidence": rel.get("confidence", "medium")
        })
    
    return {
        "company_name": result["company_name"],
        "supply_chain_relations": formatted_relations,
        "discovery_summary": {
            "total_relations": len(formatted_relations),
            "data_sources": result["data_sources"],
            "discovery_time": result["discovery_time"]
        }
    }


# ==================== 演示运行 ====================

if __name__ == "__main__":
    print("\n🔍 供应链关系发现器 v0.1 - 演示运行\n")
    
    test_companies = [
        "立讯精密",           # 上市公司，有年报数据
        "深圳XX电子科技有限公司",  # 非上市，但有招标数据
        "不存在的公司"        # 无数据
    ]
    
    for company in test_companies:
        print(f"\n{'='*60}")
        print(f"📍 查询公司: {company}")
        print("="*60)
        
        result = discover_supply_chain_relations(company)
        
        if not result["supply_chain_relations"]:
            print(f"\n⚠️ 未发现公开供应链关系数据")
            continue
        
        print(f"\n📊 数据来源: {', '.join(result['data_sources'])}")
        print(f"📎 发现 {len(result['supply_chain_relations'])} 条供应链关系:\n")
        
        for i, rel in enumerate(result["supply_chain_relations"], 1):
            print(f"  {i}. {rel['core_enterprise']}")
            print(f"     → 位置: {rel['position']}")
            print(f"     → 关系: {rel.get('relationship_type', '供应关系')}")
            print(f"     → 来源: {rel['evidence_source']}")
            
            # 展示金额信息
            if "revenue_percentage" in rel:
                print(f"     → 营收占比: {rel['revenue_percentage']}%")
            if "procurement_percentage" in rel:
                print(f"     → 采购占比: {rel['procurement_percentage']}%")
            if "bid_amount" in rel:
                print(f"     → 中标金额: {rel['bid_amount']/10000:.0f}万元")
            
            print(f"     → 置信度: {rel.get('confidence', 'medium')}")
            print()
        
        # 输出匹配引擎格式
        print("\n🔄 匹配引擎兼容格式:")
        matching_format = format_for_matching_engine(result)
        print(json.dumps(matching_format, ensure_ascii=False, indent=2))
    
    print(f"\n{'='*60}")
    print("✅ 演示完成")
    print("="*60 + "\n")
