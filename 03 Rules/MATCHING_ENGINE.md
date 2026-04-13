# 匹配规则引擎 v1.0

> 金融产品智能匹配工具 - 核心算法

---

## 引擎架构

```
输入：客户画像 OR 产品ID
  ↓
预处理：标准化字段、补全信息
  ↓
匹配计算：多维度匹配打分
  ↓
结果输出：排序后的推荐列表 + 匹配理由
```

---

## 场景一：以客户为中心的产品推荐

### 输入：客户画像

```json
{
  "customer_id": "CUST-001",
  "enterprise_type": "民企",
  "industry": "电子制造",
  "scale": {
    "annual_revenue": "5000万"
  },
  "supply_chain_position": "上游供应商",
  "core_enterprise": "华为",
  "pain_points": ["应收账款周期长", "订单增长但资金不足", "无抵押物"],
  "needs": ["快速回笼资金", "无抵押融资", "灵活额度"]
}
```

### 匹配算法

#### Step 1: 筛选候选产品

**筛选条件**：
```python
candidates = []

for product in all_products:
    # 供应链位置匹配
    if customer.supply_chain_position in product.supply_chain_position:
        # 企业类型匹配
        if customer.enterprise_type in product.entry_conditions.enterprise_type:
            # 规模匹配
            if check_scale(customer.scale, product.entry_conditions.scale):
                candidates.append(product)
```

#### Step 2: 多维度打分

**打分维度**（满分100分）：

| 维度 | 权重 | 说明 | 打分逻辑 |
|------|------|------|----------|
| 痛点匹配度 | 30% | 产品能否解决客户痛点 | 痛点重合度 × 30 |
| 需求匹配度 | 25% | 产品是否符合客户需求 | 需求重合度 × 25 |
| 准入条件匹配 | 20% | 客户是否符合准入条件 | 条件匹配度 × 20 |
| 利率优势 | 10% | 利率是否有竞争力 | (基准利率 - 产品利率) × 10 |
| 核心企业关联 | 10% | 是否有核心企业授信 | 有关联 = 10分 |
| 行业经验 | 5% | 银行是否有同行业案例 | 有案例 = 5分 |

**打分公式**：
```
总分 = 痛点匹配度×0.30
     + 需求匹配度×0.25
     + 准入条件匹配×0.20
     + 利率优势×0.10
     + 核心企业关联×0.10
     + 行业经验×0.05
```

#### Step 3: 输出推荐结果

```json
{
  "customer_id": "CUST-001",
  "recommendations": [
    {
      "product_id": "PROD-001",
      "product_name": "信e链",
      "bank": "中信银行",
      "score": 92,
      "match_reasons": [
        "完美匹配上游供应商身份",
        "解决应收账款周期长的痛点",
        "无需抵押物，符合客户需求",
        "华为核心企业有授信额度"
      ],
      "entry_angle": "痛点切入",
      "key_message": "利用华为信用，无需抵押，最快3天拿到钱",
      "risk_alert": "需确认贸易背景真实性"
    },
    {
      "product_id": "PROD-004",
      "product_name": "信保理",
      "bank": "中信银行",
      "score": 88,
      "match_reasons": [
        "反向保理适合上游供应商",
        "解决应收账款问题",
        "无需抵押"
      ],
      "entry_angle": "案例切入",
      "key_message": "同行业电子供应商成功案例"
    }
  ],
  "matching_time": "2026-04-12 23:35"
}
```

---

## 场景二：以产品为中心的客户筛选

### 输入：产品ID

```json
{
  "product_id": "PROD-001",
  "product_name": "信e链"
}
```

### 筛选算法

#### Step 1: 提取产品特征

```json
{
  "target_customer": "上游供应商",
  "entry_conditions": {
    "enterprise_type": ["国企", "民企", "外企"],
    "scale": "年营收>1000万",
    "guarantee": "无需抵押担保"
  },
  "supply_chain_position": ["上游"],
  "product_features": {
    "interest_rate": "4-6%",
    "term": "最长180天"
  }
}
```

#### Step 2: 筛选候选客户

```python
candidates = []

for customer in customer_database:
    # 供应链位置匹配
    if customer.supply_chain_position == "上游供应商":
        # 规模匹配
        if customer.scale.annual_revenue > 1000万:
            # 有核心企业关联
            if customer.core_enterprise:
                candidates.append(customer)
```

#### Step 3: 输出客户列表

```json
{
  "product_id": "PROD-001",
  "product_name": "信e链",
  "target_customers": [
    {
      "customer_id": "CUST-001",
      "customer_name": "深圳XX电子",
      "industry": "电子制造",
      "scale": "5000万",
      "core_enterprise": "华为",
      "pain_points": ["应收账款周期长"],
      "match_score": 95,
      "entry_angle": "痛点切入",
      "key_message": "华为信用加持，无需抵押"
    },
    {
      "customer_id": "CUST-002",
      "customer_name": "苏州XX精密",
      "industry": "汽车零部件",
      "scale": "8000万",
      "core_enterprise": "比亚迪",
      "pain_points": ["资金周转慢"],
      "match_score": 90,
      "entry_angle": "案例切入",
      "key_message": "比亚迪供应链成功案例"
    }
  ]
}
```

---

## 匹配规则配置

### 规则权重（可调整）

```json
{
  "weights": {
    "pain_point_match": 0.30,
    "need_match": 0.25,
    "entry_condition_match": 0.20,
    "interest_rate_advantage": 0.10,
    "core_enterprise_relation": 0.10,
    "industry_experience": 0.05
  },
  "thresholds": {
    "min_score": 60,
    "max_recommendations": 5
  }
}
```

### 禁止匹配规则

```json
{
  "contraindications": [
    {
      "condition": "customer.credit_rating == 'D'",
      "action": "exclude",
      "reason": "信用评级D级客户禁止推荐"
    },
    {
      "condition": "customer.industry in product.contraindications",
      "action": "exclude",
      "reason": "客户行业在产品禁忌列表中"
    },
    {
      "condition": "product.entry_conditions.enterprise_type not includes customer.enterprise_type",
      "action": "exclude",
      "reason": "企业类型不符合准入条件"
    }
  ]
}
```

---

## 话术路由逻辑

### 根据匹配结果选择话术

```python
def select_script(customer, product, match_result):
    # 根据切入角度选择话术模板
    entry_angle = match_result["entry_angle"]
    
    # 话术路由表
    script_map = {
        "痛点切入": get_script_by_angle("pain_point", customer, product),
        "利益切入": get_script_by_angle("benefit", customer, product),
        "案例切入": get_script_by_angle("case", customer, product),
        "时效切入": get_script_by_angle("urgency", customer, product)
    }
    
    return script_map[entry_angle]
```

### 话术生成逻辑

```
输入：客户画像 + 产品信息 + 匹配结果
  ↓
选择切入角度
  ↓
填充话术模板
  ↓
添加异议处理
  ↓
输出完整话术
```

---

## API接口设计

### 接口1：客户→产品推荐

```
POST /api/match/customer-to-products
Request:
{
  "customer": {...},
  "preferences": {
    "bank_filter": ["中信银行", "平安银行"],
    "product_type_filter": ["应收账款融资"],
    "max_interest_rate": "6%"
  }
}

Response:
{
  "recommendations": [...],
  "matching_time": "2026-04-12 23:35"
}
```

### 接口2：产品→客户筛选

```
POST /api/match/product-to-customers
Request:
{
  "product_id": "PROD-001",
  "filters": {
    "industry": ["电子制造", "汽车零部件"],
    "min_scale": "1000万"
  }
}

Response:
{
  "target_customers": [...]
}
```

---

*匹配规则引擎 v1.0 | 2026-04-12*
