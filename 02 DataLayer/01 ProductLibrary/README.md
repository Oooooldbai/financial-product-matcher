# 产品库

> 金融产品智能匹配工具 - 产品数据层

---

## 产品库结构

### 标准字段定义

```json
{
  "product_id": "PROD-YYYY-MM-DD-XXX",
  "product_name": "产品名称",
  "bank": "银行名称",
  "product_type": "产品类型",
  "target_customer": "目标客户",
  "entry_conditions": {
    "enterprise_type": ["国企", "民企", "外企"],
    "industry": ["制造业", "零售业", "..."],
    "scale": "年营收/员工数",
    "credit_rating": "信用等级要求",
    "guarantee": "担保方式"
  },
  "product_features": {
    "interest_rate": "利率区间",
    "term": "期限范围",
    "amount": "额度范围",
    "repayment": "还款方式"
  },
  "supply_chain_position": ["上游", "下游", "核心企业"],
  "risk_points": ["风险点1", "风险点2"],
  "competitive_advantage": "产品优势",
  "application_process": "申请流程",
  "related_policies": ["相关政策法规ID"],
  "selling_points": ["卖点1", "卖点2"],
  "contraindications": ["禁忌客户类型"],
  "update_time": "更新时间"
}
```

### 产品类型分类

| 类型 | 说明 | 典型产品 |
|------|------|----------|
| 应收账款融资 | 基于应收账款的融资 | 保理、反向保理、ABS |
| 预付账款融资 | 基于预付账款的融资 | 订单融资、保兑仓 |
| 存货融资 | 基于存货的融资 | 仓单质押、存货质押 |
| 商票融资 | 基于商业票据的融资 | 商票贴现、商票质押 |
| 信用融资 | 纯信用贷款 | 流动资金贷款、税贷 |
| 动态折扣 | 供应商提前收款折扣 | 动态折扣平台 |

### 供应链位置分类

| 位置 | 说明 | 典型产品 |
|------|------|----------|
| 上游供应商 | 核心企业的供应商 | 反向保理、订单融资 |
| 下游经销商 | 核心企业的经销商 | 预付融资、存货融资 |
| 核心企业 | 供应链核心企业 | 信用贷款、票据融资 |

### 银行分类

| 类型 | 代表银行 |
|------|----------|
| 国有大行 | 工行、农行、中行、建行、交行、邮储 |
| 股份制银行 | 招商、中信、浦发、民生、兴业、平安、光大、华夏、广发、浙商、渤海、恒丰 |
| 城商行 | 北京银行、上海银行、江苏银行等 |
| 农商行 | 重庆农商行、广州农商行等 |
| 民营银行 | 微众、网商、新网、苏宁等 |
| 外资银行 | 汇丰、渣打、花旗、东亚等 |

---

## 文件命名规范

- 单个产品：`{bank}_{product_name}.md`
- 银行汇总：`{bank}_products.md`
- 类型汇总：`{product_type}_products.md`

---

## 产品录入规范

### 必填字段
- product_id
- product_name
- bank
- product_type
- target_customer
- entry_conditions
- product_features

### 选填字段
- supply_chain_position
- risk_points
- competitive_advantage
- application_process
- related_policies
- selling_points
- contraindications

---

*产品库 | 2026-04-12*
