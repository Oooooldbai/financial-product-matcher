# 客户库示例数据

> 更新时间: 2026-04-12

---

## 示例客户1：制造业上游供应商

### CUST-2026-04-001: 深圳XX电子科技有限公司

```json
{
  "customer_id": "CUST-2026-04-001",
  "customer_name": "深圳XX电子科技有限公司",
  "enterprise_type": "民企",
  "industry": "电子制造",
  "sub_industry": "电子元器件",
  "scale": {
    "annual_revenue": "5000万",
    "employee_count": "80人",
    "asset_size": "3000万"
  },
  "supply_chain_position": "上游供应商",
  "core_enterprise": "华为",
  "business_scenario": "为华为供应电子元器件，月订单200-300万，账期90-120天",
  "financial_status": {
    "credit_rating": "BBB",
    "debt_ratio": "45%",
    "cash_flow": "季节性波动，Q3-Q4资金紧张"
  },
  "pain_points": [
    "应收账款周期长（90-120天）",
    "订单增长但资金不足",
    "无抵押物"
  ],
  "needs": [
    "快速回笼资金",
    "无抵押融资",
    "灵活额度"
  ],
  "constraints": {
    "guarantee_capability": "无抵押物",
    "collateral": "无",
    "time_sensitivity": "高（订单增长快）"
  },
  "decision_factors": [
    "放款速度",
    "利率成本",
    "操作便利性"
  ],
  "taboos": [
    "手续复杂",
    "隐性费用"
  ],
  "matching_products": [
    "PROD-001: 信e链",
    "PROD-004: 信保理"
  ],
  "matching_score": {
    "信e链": 92,
    "信保理": 88,
    "商票e贷": 75
  },
  "update_time": "2026-04-12"
}
```

**适配产品分析**：

| 产品 | 匹配度 | 切入角度 | 核心信息 |
|------|--------|----------|----------|
| 信e链 | 92分 | 痛点切入 | 华为信用加持，无需抵押，最快3天 |
| 信保理 | 88分 | 案例切入 | 同行业供应商成功案例 |
| 商票e贷 | 75分 | 利益切入 | 利率低，线上操作 |

---

## 示例客户2：商贸流通企业

### CUST-2026-04-002: 苏州XX商贸有限公司

```json
{
  "customer_id": "CUST-2026-04-002",
  "customer_name": "苏州XX商贸有限公司",
  "enterprise_type": "民企",
  "industry": "商贸零售",
  "sub_industry": "快消品分销",
  "scale": {
    "annual_revenue": "8000万",
    "employee_count": "50人",
    "asset_size": "2000万"
  },
  "supply_chain_position": "下游经销商",
  "core_enterprise": "宝洁",
  "business_scenario": "宝洁产品华东区经销商，季度订货任务压力大",
  "financial_status": {
    "credit_rating": "A",
    "debt_ratio": "40%",
    "cash_flow": "季节性波动，春节前资金需求大"
  },
  "pain_points": [
    "备货资金压力大",
    "季节性资金需求",
    "库存周转慢"
  ],
  "needs": [
    "预付融资",
    "存货融资",
    "灵活还款"
  ],
  "constraints": {
    "guarantee_capability": "有存货可质押",
    "collateral": "库存商品",
    "time_sensitivity": "高（春节前旺季）"
  },
  "decision_factors": [
    "额度充足",
    "还款灵活",
    "手续简单"
  ],
  "taboos": [
    "额度不足",
    "还款压力大"
  ],
  "matching_products": [
    "PROD-002: 信e采",
    "PROD-008: 预付线上融资"
  ],
  "matching_score": {
    "信e采": 90,
    "预付线上融资": 88,
    "存货线上融资": 85
  },
  "update_time": "2026-04-12"
}
```

**适配产品分析**：

| 产品 | 匹配度 | 切入角度 | 核心信息 |
|------|--------|----------|----------|
| 信e采 | 90分 | 时效切入 | 备货资金，春节前充足 |
| 预付线上融资 | 88分 | 利益切入 | 利率优惠，灵活还款 |
| 存货线上融资 | 85分 | 痛点切入 | 存货质押，盘活资产 |

---

## 示例客户3：建筑核心企业

### CUST-2026-04-003: 江苏XX建设集团有限公司

```json
{
  "customer_id": "CUST-2026-04-003",
  "customer_name": "江苏XX建设集团有限公司",
  "enterprise_type": "国企",
  "industry": "建筑施工",
  "sub_industry": "房屋建筑",
  "scale": {
    "annual_revenue": "50亿",
    "employee_count": "2000人",
    "asset_size": "30亿"
  },
  "supply_chain_position": "核心企业",
  "core_enterprise": "自身",
  "business_scenario": "大型建筑企业，上游供应商众多，应付账款管理需求",
  "financial_status": {
    "credit_rating": "AA",
    "debt_ratio": "60%",
    "cash_flow": "稳定"
  },
  "pain_points": [
    "上游供应商账期长，供应商投诉",
    "项目资金需求大",
    "信用体系建设需求"
  ],
  "needs": [
    "供应链金融平台",
    "降低应付账款压力",
    "供应商管理工具"
  ],
  "constraints": {
    "guarantee_capability": "强",
    "collateral": "充足",
    "time_sensitivity": "中"
  },
  "decision_factors": [
    "平台功能完善",
    "供应商接受度",
    "品牌信誉"
  ],
  "taboos": [
    "平台不稳定",
    "供应商体验差"
  ],
  "matching_products": [
    "PROD-007: 供应链金融2.0",
    "PROD-016: 招赢通"
  ],
  "matching_score": {
    "供应链金融2.0": 88,
    "招赢通": 85,
    "票据池": 80
  },
  "update_time": "2026-04-12"
}
```

---

## 示例客户4：小微企业

### CUST-2026-04-004: 广州XX贸易商行

```json
{
  "customer_id": "CUST-2026-04-004",
  "customer_name": "广州XX贸易商行",
  "enterprise_type": "个体户",
  "industry": "商贸零售",
  "sub_industry": "日用品批发",
  "scale": {
    "annual_revenue": "500万",
    "employee_count": "5人",
    "asset_size": "100万"
  },
  "supply_chain_position": "下游经销商",
  "core_enterprise": "无",
  "business_scenario": "日用品批发，资金需求灵活",
  "financial_status": {
    "credit_rating": "B",
    "debt_ratio": "50%",
    "cash_flow": "波动大"
  },
  "pain_points": [
    "资金周转困难",
    "无抵押物",
    "银行贷款难"
  ],
  "needs": [
    "信用贷款",
    "快速放款",
    "随借随还"
  ],
  "constraints": {
    "guarantee_capability": "无",
    "collateral": "无",
    "time_sensitivity": "极高"
  },
  "decision_factors": [
    "放款速度",
    "申请便利性",
    "额度灵活"
  ],
  "taboos": [
    "手续复杂",
    "审批时间长"
  ],
  "matching_products": [
    "PROD-033: 微业贷",
    "PROD-037: 网商贷"
  ],
  "matching_score": {
    "微业贷": 95,
    "网商贷": 92
  },
  "update_time": "2026-04-12"
}
```

---

## 客户库统计

| 企业性质 | 数量 | 占比 |
|----------|------|------|
| 民企 | 2 | 50% |
| 国企 | 1 | 25% |
| 个体户 | 1 | 25% |

| 供应链位置 | 数量 | 占比 |
|------------|------|------|
| 上游供应商 | 1 | 25% |
| 下游经销商 | 2 | 50% |
| 核心企业 | 1 | 25% |

| 规模 | 数量 | 占比 |
|------|------|------|
| 大型企业 | 1 | 25% |
| 中型企业 | 1 | 25% |
| 小型企业 | 1 | 25% |
| 微型企业 | 1 | 25% |

---

*客户库示例数据 | 2026-04-12*
