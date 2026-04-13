#!/usr/bin/env python3
"""
金融产品智能匹配引擎 v1.0
测试版本
"""

import json
from datetime import datetime
from typing import Dict, List, Any

# ==================== 数据准备 ====================

# 示例客户画像 - 【修正版】
# 供应链位置 = 相对于特定核心企业的关系，不是一个固定值
SAMPLE_CUSTOMER = {
    "customer_id": "CUST-TEST-001",
    "name": "深圳XX电子科技有限公司",
    "enterprise_type": "民企",
    "industry": "电子制造",
    "scale": {
        "annual_revenue": 50000000,  # 5000万
        "employee_count": 150
    },
    # 【关键修正】供应链关系 = 按核心企业区分位置
    "supply_chain_relations": [
        {
            "core_enterprise": "华为",
            "position": "上游供应商",  # 对华为是上游
            "relationship_type": "元器件供应商",
            "annual_volume": 20000000  # 2亿
        },
        {
            "core_enterprise": "小米",
            "position": "下游经销商",  # 对小米是下游
            "relationship_type": "代理商",
            "annual_volume": 10000000  # 1亿
        }
    ],
    # 兼容旧字段（只取第一条或标记为"多链条"）
    "supply_chain_position": "多链条",
    "core_enterprise": "华为",  # 主链条
    "pain_points": ["应收账款周期长(90天)", "订单增长但资金不足", "无抵押物"],
    "needs": ["快速回笼资金", "无抵押融资", "灵活额度"],
    "credit_rating": "A"
}

# 测试客户2
TEST_CUSTOMER_2 = {
    "customer_id": "CUST-TEST-002",
    "name": "杭州XX科技有限公司",
    "enterprise_type": "民企",
    "industry": "医疗器械",
    "scale": {"annual_revenue": 30000000},
    # 单一核心企业关系
    "supply_chain_relations": [
        {
            "core_enterprise": "西门子",
            "position": "下游经销商",
            "relationship_type": "区域代理",
            "annual_volume": 15000000
        }
    ],
    "supply_chain_position": "下游经销商",
    "core_enterprise": "西门子",
    "pain_points": ["库存积压资金占用大", "账期长(120天)"],
    "needs": ["采购资金", "延长账期"],
    "credit_rating": "A"
}

# 示例产品库 - 【增强版】
# 增加 applicable_core_enterprises 字段，支持按核心企业筛选
PRODUCTS_DB = [
    {
        "product_id": "PROD-001",
        "product_name": "信e链",
        "bank": "中信银行",
        "product_type": "供应链应收账款融资",
        "supply_chain_position": ["上游"],
        "applicable_core_enterprises": ["华为", "中兴", "腾讯", "阿里"],  # 只服务这些核心企业的上游
        "target_enterprise_type": ["国企", "民企", "外企"],
        "min_scale": 10000000,
        "max_scale": None,
        "interest_rate": "4.5%",
        "max_term_days": 180,
        "guarantee": "无需抵押担保",
        "features": ["核心企业确权", "线上化操作", "T+3放款"],
        "core_enterprise_required": True,
        "cases": ["电子制造", "通信设备"]
    },
    {
        "product_id": "PROD-002",
        "product_name": "链e贷",
        "bank": "平安银行",
        "product_type": "供应链信用贷",
        "supply_chain_position": ["上游", "下游"],
        "applicable_core_enterprises": [],  # 空=不限制
        "target_enterprise_type": ["民企", "外企"],
        "min_scale": 5000000,
        "max_scale": None,
        "interest_rate": "6.0%",
        "max_term_days": 90,
        "guarantee": "无需抵押",
        "features": ["信用方式", "随借随还"],
        "core_enterprise_required": True,
        "cases": ["制造业", "零售"]
    },
    {
        "product_id": "PROD-003",
        "product_name": "保理通",
        "bank": "招商银行",
        "product_type": "应收账款保理",
        "supply_chain_position": ["上游"],
        "applicable_core_enterprises": [],  # 不限制核心企业
        "target_enterprise_type": ["国企", "民企"],
        "min_scale": 20000000,
        "max_scale": None,
        "interest_rate": "5.5%",
        "max_term_days": 365,
        "guarantee": "应收账款转让",
        "features": ["不限核心企业", "可做暗保理"],
        "core_enterprise_required": False,
        "cases": ["建筑", "医药"]
    },
    {
        "product_id": "PROD-004",
        "product_name": "e单通",
        "bank": "浙商银行",
        "product_type": "电子债权凭证",
        "supply_chain_position": ["上游"],
        "applicable_core_enterprises": ["比亚迪", "吉利", "长安"],  # 只服务汽车核心企业
        "target_enterprise_type": ["国企", "民企", "外企"],
        "min_scale": 10000000,
        "max_scale": None,
        "interest_rate": "5.0%",
        "max_term_days": 180,
        "guarantee": "核心企业确权",
        "features": ["可拆分流转", "多级穿透"],
        "core_enterprise_required": True,
        "cases": ["汽车", "电子"]
    },
    {
        "product_id": "PROD-005",
        "product_name": "经销商贷",
        "bank": "微众银行",
        "product_type": "下游经销商融资",
        "supply_chain_position": ["下游"],
        "applicable_core_enterprises": [],  # 不限制
        "target_enterprise_type": ["民企"],
        "min_scale": 1000000,
        "max_scale": None,
        "interest_rate": "8.0%",
        "max_term_days": 180,
        "guarantee": "下游采购合同",
        "features": ["专供下游经销商", "随借随还", "采购即可融资"],
        "core_enterprise_required": True,
        "cases": ["快消", "医疗设备"]
    }
]

# 权重配置
WEIGHTS = {
    "pain_point_match": 0.30,
    "need_match": 0.25,
    "entry_condition_match": 0.20,
    "core_enterprise_relation": 0.15,
    "industry_experience": 0.10
}


# ==================== 匹配引擎 ====================

def get_supply_chain_info(customer: Dict, product: Dict = None) -> tuple:
    """
    获取匹配的供应链关系信息
    
    返回: (匹配的供应链关系 或 None, 匹配说明)
    
    【核心逻辑】
    1. 如果客户有多条供应链关系，尝试找到与产品核心企业匹配的那条
    2. 如果产品不指定核心企业，返回主链条或第一条关系
    3. 匹配优先级：产品指定核心企业 > 主核心企业 > 第一条关系
    """
    relations = customer.get("supply_chain_relations", [])
    
    if not relations:
        # 兼容旧格式：直接从主字段读取
        return {
            "core_enterprise": customer.get("core_enterprise", ""),
            "position": customer.get("supply_chain_position", "")
        }, "基于主核心企业"
    
    # 尝试找匹配的供应链关系
    product_core = product.get("core_enterprise_required", None) if product else None
    
    # 方式1：找与产品核心企业匹配的关系
    if product and product_core:
        for rel in relations:
            if rel["core_enterprise"] == product_core:
                return rel, f"匹配产品核心企业{product_core}"
    
    # 方式2：找与产品适用核心企业匹配的关系
    if product and "applicable_core_enterprises" in product:
        for rel in relations:
            if rel["core_enterprise"] in product.get("applicable_core_enterprises", []):
                return rel, f"在{rel['core_enterprise']}供应链中"
    
    # 方式3：使用主核心企业对应的关系
    main_core = customer.get("core_enterprise", "")
    for rel in relations:
        if rel["core_enterprise"] == main_core:
            return rel, f"主链条({main_core})"
    
    # 方式4：使用第一条关系
    return relations[0], f"首条链条({relations[0]['core_enterprise']})"


def check_entry_conditions(customer: Dict, product: Dict) -> tuple:
    """检查准入条件，返回(是否通过, 原因, 供应链关系)"""
    reasons = []
    
    # 【关键】获取该产品对应的供应链关系
    supply_chain_info, match_note = get_supply_chain_info(customer, product)
    position = supply_chain_info.get("position", "")
    
    # 企业类型
    if customer["enterprise_type"] not in product["target_enterprise_type"]:
        return False, f"企业类型不匹配({customer['enterprise_type']} not in {product['target_enterprise_type']})", None
    reasons.append(f"✓ 企业类型匹配({customer['enterprise_type']})")
    
    # 规模
    revenue = customer["scale"]["annual_revenue"]
    if revenue < product["min_scale"]:
        return False, f"营收规模不足({revenue//10000}万 < {product['min_scale']//10000}万)", None
    reasons.append(f"✓ 营收规模达标({revenue//10000}万)")
    
    # 【关键修正】供应链位置 - 基于具体核心企业关系动态匹配
    prod_pos_list = product["supply_chain_position"]
    
    position_match = False
    matched_position = ""
    
    # 多种匹配方式
    for pp in prod_pos_list:
        # 直接包含
        if pp in position or position in pp:
            position_match = True
            matched_position = position
            break
        # 关键词匹配
        if "上游" in pp and "上游" in position:
            position_match = True
            matched_position = position
            break
        if "下游" in pp and "下游" in position:
            position_match = True
            matched_position = position
            break
        if "核心企业" in pp or "不限制" in pp:
            position_match = True
            matched_position = "不限制"
            break
    
    if not position_match:
        return False, f"供应链位置不匹配({position} not in {prod_pos_list})", None
    
    reasons.append(f"✓ 供应链位置匹配({matched_position}) [{match_note}]")
    reasons.append(f"  → {supply_chain_info['core_enterprise']}的{position}")
    
    return True, reasons, supply_chain_info


def calculate_pain_point_match(customer: Dict, product: Dict) -> float:
    """计算痛点匹配度"""
    pain_points = customer.get("pain_points", [])
    features = product.get("features", [])
    
    # 痛点关键词映射到产品特性
    mapping = {
        "应收账款": ["应收账款", "保理", "确权", "e链"],
        "资金不足": ["信用", "贷款", "融资"],
        "无抵押物": ["无需抵押", "信用"],
        "灵活额度": ["灵活", "随借随还"],
        "快速": ["T+", "快速", "线上"]
    }
    
    score = 0
    matched_pain_points = []
    
    for pain in pain_points:
        for key, feature_keywords in mapping.items():
            if key in pain:
                for feature in features:
                    for fk in feature_keywords:
                        if fk in feature:
                            score += 25  # 每个痛点最高25分
                            matched_pain_points.append(f"{pain} → {feature}")
                            break
    
    return min(score, 100), matched_pain_points


def calculate_need_match(customer: Dict, product: Dict) -> float:
    """计算需求匹配度"""
    needs = customer.get("needs", [])
    features = product.get("features", [])
    
    score = 0
    matched_needs = []
    
    need_keywords = {
        "回笼资金": ["应收账款", "保理", "融资"],
        "无抵押": ["无需抵押", "信用"],
        "灵活": ["灵活", "随借随还"],
        "快速": ["T+", "快速", "线上"],
        "长期": ["365", "长"]
    }
    
    for need in needs:
        for key, keywords in need_keywords.items():
            if key in need:
                for feature in features:
                    for kw in keywords:
                        if kw in feature:
                            score += 25
                            matched_needs.append(f"{need} → {feature}")
                            break
    
    return min(score, 100), matched_needs


def calculate_core_enterprise_bonus(customer: Dict, product: Dict) -> float:
    """计算核心企业关联加分"""
    if product.get("core_enterprise_required") and customer.get("core_enterprise"):
        return 100, f"核心企业关联({customer['core_enterprise']})"
    elif not product.get("core_enterprise_required"):
        return 50, "不要求核心企业"
    return 0, "无核心企业关联"


def calculate_industry_bonus(customer: Dict, product: Dict) -> float:
    """计算行业经验加分"""
    industry = customer.get("industry", "")
    cases = product.get("cases", [])
    
    for case in cases:
        if case in industry or industry in case:
            return 100, f"有{industry}行业案例"
    
    return 30, "跨行业适用"


def check_core_enterprise_fit(customer: Dict, product: Dict, supply_chain_info: Dict) -> tuple:
    """
    检查核心企业适配性
    
    返回: (是否适配, 得分, 说明)
    """
    product_core_list = product.get("applicable_core_enterprises", [])
    customer_core = supply_chain_info.get("core_enterprise", "")
    
    # 产品不限制核心企业 -> 完全适配
    if not product_core_list:
        return True, 100, f"不限核心企业"
    
    # 产品指定了核心企业列表 -> 检查客户是否在其中
    if customer_core in product_core_list:
        return True, 100, f"核心企业匹配({customer_core})"
    
    # 客户核心企业不在产品适用列表 -> 排除
    return False, 0, f"该产品仅限{','.join(product_core_list)}的供应链"


def match_customer_to_products(customer: Dict, products: List[Dict] = None) -> Dict:
    """客户→产品匹配"""
    if products is None:
        products = PRODUCTS_DB
    
    results = []
    
    # 展示客户的供应链关系
    relations = customer.get("supply_chain_relations", [])
    
    for product in products:
        # Step 1: 准入条件检查（包含供应链关系匹配）
        passed, entry_result, supply_chain_info = check_entry_conditions(customer, product)
        
        if not passed:
            continue
        
        # Step 1.5: 核心企业适配性检查
        core_fit, core_score, core_note = check_core_enterprise_fit(
            customer, product, supply_chain_info
        )
        
        if not core_fit:
            # 记录排除原因但不直接排除，而是降低优先级
            entry_result.append(f"⚠ {core_note}")
        
        # Step 2: 多维度打分
        scores = {}
        
        # 痛点匹配度
        pain_score, pain_matches = calculate_pain_point_match(customer, product)
        scores["pain_point"] = pain_score
        
        # 需求匹配度
        need_score, need_matches = calculate_need_match(customer, product)
        scores["need"] = need_score
        
        # 核心企业关联（基于具体链条）
        core_enterprise_score = core_score if core_fit else core_score * 0.3
        scores["core_enterprise"] = core_enterprise_score
        
        # 行业经验
        industry_score, industry_reason = calculate_industry_bonus(customer, product)
        scores["industry"] = industry_score
        
        # 计算总分
        total_score = (
            scores["pain_point"] * WEIGHTS["pain_point_match"] +
            scores["need"] * WEIGHTS["need_match"] +
            scores["core_enterprise"] * WEIGHTS["core_enterprise_relation"] +
            scores["industry"] * WEIGHTS["industry_experience"]
        )
        
        # 准入条件权重
        entry_score = 100 if core_fit else 50
        total_score = total_score * 0.8 + entry_score * 0.2
        
        # Step 3: 生成匹配理由
        match_reasons = entry_result if isinstance(entry_result, list) else [str(entry_result)]
        if pain_matches:
            match_reasons.extend([f"痛点匹配: {m}" for m in pain_matches[:2]])
        if need_matches:
            match_reasons.extend([f"需求匹配: {m}" for m in need_matches[:2]])
        match_reasons.append(f"核心企业: {core_note}")
        match_reasons.append(industry_reason)
        
        # Step 4: 确定切入角度
        if pain_matches:
            entry_angle = "痛点切入"
            key_message = f"针对{customer['pain_points'][0]}，{product['product_name']}可以解决"
        elif need_matches:
            entry_angle = "需求切入"
            key_message = f"满足{customer['needs'][0]}的需求"
        else:
            entry_angle = "优势切入"
            key_message = f"{product['bank']}{product['product_name']}，利率{product['interest_rate']}"
        
        # 增加适配的核心企业信息
        matched_core = supply_chain_info.get("core_enterprise", "")
        matched_position = supply_chain_info.get("position", "")
        
        results.append({
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "bank": product["bank"],
            "product_type": product["product_type"],
            "score": round(total_score, 1),
            "score_breakdown": scores,
            "match_reasons": match_reasons,
            "entry_angle": entry_angle,
            "key_message": key_message,
            "interest_rate": product["interest_rate"],
            "term_days": product["max_term_days"],
            "guarantee": product["guarantee"],
            # 新增：供应链链条信息
            "supply_chain_chain": {
                "core_enterprise": matched_core,
                "position": matched_position,
                "core_fit": core_fit,
                "note": core_note
            }
        })
    
    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "customer_id": customer["customer_id"],
        "customer_name": customer.get("name", "未知"),
        "supply_chain_relations": [
            {"core_enterprise": r["core_enterprise"], "position": r["position"]} 
            for r in relations
        ] if relations else [{"core_enterprise": customer.get("core_enterprise"), "position": customer.get("supply_chain_position")}],
        "recommendations": results[:5],
        "matching_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def print_result(result: Dict):
    """格式化打印结果"""
    print("\n" + "="*70)
    print(f"🔍 匹配结果 | 客户: {result['customer_name']}")
    print("="*70)
    
    # 展示客户的供应链关系
    print(f"\n📎 供应链关系:")
    for rel in result["supply_chain_relations"]:
        print(f"   • {rel['core_enterprise']} → {rel['position']}")
    
    for i, rec in enumerate(result["recommendations"], 1):
        print(f"\n📌 推荐 #{i}: {rec['bank']} - {rec['product_name']}")
        print(f"   匹配分数: {rec['score']}/100")
        print(f"   产品类型: {rec['product_type']}")
        print(f"   利率: {rec['interest_rate']} | 期限: {rec['term_days']}天 | 担保: {rec['guarantee']}")
        
        # 供应链链条信息
        chain = rec.get("supply_chain_chain", {})
        if chain:
            core_fit = "✅" if chain.get("core_fit", True) else "⚠️"
            print(f"   供应链链条: {core_fit} {chain.get('core_enterprise')} → {chain.get('position')}")
        
        print(f"   切入角度: {rec['entry_angle']}")
        print(f"   核心话术: {rec['key_message']}")
        print(f"   匹配理由:")
        for reason in rec["match_reasons"][:5]:
            print(f"     • {reason}")
    
    print(f"\n⏱️  匹配时间: {result['matching_time']}")
    print("="*70 + "\n")


# ==================== 测试运行 ====================

if __name__ == "__main__":
    print("\n🚀 金融产品智能匹配引擎 v1.1 - 供应链关系重构版\n")
    
    # 测试1: 多链条客户（同时是华为上游、小米下游）
    print("📋 测试客户画像 #1 (多链条客户):")
    print(f"   名称: {SAMPLE_CUSTOMER['name']}")
    print(f"   企业类型: {SAMPLE_CUSTOMER['enterprise_type']}")
    print(f"   行业: {SAMPLE_CUSTOMER['industry']}")
    print(f"   年营收: {SAMPLE_CUSTOMER['scale']['annual_revenue']//10000}万")
    print(f"   供应链关系:")
    for rel in SAMPLE_CUSTOMER.get("supply_chain_relations", []):
        print(f"     → 对 {rel['core_enterprise']}: {rel['position']}")
    print(f"   痛点: {', '.join(SAMPLE_CUSTOMER['pain_points'])}")
    print(f"   需求: {', '.join(SAMPLE_CUSTOMER['needs'])}")
    
    # 执行匹配
    result = match_customer_to_products(SAMPLE_CUSTOMER)
    print_result(result)
    
    # 测试2: 单一链条客户
    print("\n📋 测试客户画像 #2 (单一链条客户):")
    print(f"   名称: {TEST_CUSTOMER_2['name']}")
    print(f"   行业: {TEST_CUSTOMER_2['industry']}")
    for rel in TEST_CUSTOMER_2.get("supply_chain_relations", []):
        print(f"   供应链关系: 对 {rel['core_enterprise']}: {rel['position']}")
    print(f"   痛点: {', '.join(TEST_CUSTOMER_2['pain_points'])}")
    
    result2 = match_customer_to_products(TEST_CUSTOMER_2)
    print_result(result2)
