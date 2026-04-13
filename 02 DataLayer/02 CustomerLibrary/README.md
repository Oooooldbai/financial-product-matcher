# 客户库

> 金融产品智能匹配工具 - 客户数据层

---

## 客户库结构

### 标准字段定义

```json
{
  "customer_id": "CUST-YYYY-MM-DD-XXX",
  "customer_name": "客户名称",
  "enterprise_type": "国企/民企/外企/合资",
  "industry": "所属行业",
  "sub_industry": "细分行业",
  "scale": {
    "annual_revenue": "年营收范围",
    "employee_count": "员工数量",
    "asset_size": "资产规模"
  },
  "supply_chain_position": "上游/下游/核心企业",
  "core_enterprise": "关联核心企业",
  "business_scenario": "业务场景描述",
  "financial_status": {
    "credit_rating": "信用等级",
    "debt_ratio": "负债率",
    "cash_flow": "现金流状况"
  },
  "pain_points": ["痛点1", "痛点2", "痛点3"],
  "needs": ["需求1", "需求2", "需求3"],
  "constraints": {
    "guarantee_capability": "担保能力",
    "collateral": "抵押物",
    "time_sensitivity": "时间敏感度"
  },
  "decision_factors": ["决策因素1", "决策因素2"],
  "taboos": ["禁忌点1", "禁忌点2"],
  "matching_products": ["适配产品ID列表"],
  "matching_score": "适配度评分",
  "update_time": "更新时间"
}
```

### 客户分类维度

#### 1. 企业性质
- 国有企业
- 民营企业
- 外资企业
- 合资企业
- 上市公司
- 中小微企业

#### 2. 行业分类
- 制造业
  - 电子制造
  - 汽车制造
  - 医药制造
  - 食品加工
- 零售业
- 建筑业
- 农业
- 物流业
- 医疗健康
- 教育
- 其他

#### 3. 规模分类
| 类型 | 年营收 | 员工数 |
|------|--------|--------|
| 大型企业 | >10亿 | >1000人 |
| 中型企业 | 1-10亿 | 100-1000人 |
| 小型企业 | 1000万-1亿 | 10-100人 |
| 微型企业 | <1000万 | <10人 |

#### 4. 供应链位置
- 核心企业：供应链主导方
- 上游供应商：原材料/零部件供应商
- 下游经销商：产品分销商/零售商
- 物流服务商：仓储/运输服务商

---

## 客户画像模板

### 模板1：制造业中小企业（上游供应商）
```
企业性质：民营
行业：电子制造
规模：年营收5000万，员工80人
供应链位置：上游供应商
核心企业：华为/小米等电子品牌
痛点：
  - 应收账款周期长（90-120天）
  - 订单增长但资金不足
  - 无抵押物
需求：
  - 快速回笼资金
  - 无抵押融资
  - 灵活额度
适配产品：
  - 反向保理（优先）
  - 订单融资
  - 信用贷款
```

### 模板2：商贸流通企业（下游经销商）
```
企业性质：民营
行业：商贸零售
规模：年营收8000万，员工50人
供应链位置：下游经销商
核心企业：快消品牌/家电品牌
痛点：
  - 备货资金压力大
  - 季节性资金需求
  - 库存周转慢
需求：
  - 预付融资
  - 存货融资
  - 灵活还款
适配产品：
  - 预付融资（优先）
  - 存货质押
  - 动态折扣
```

### 模板3：建筑企业（核心企业）
```
企业性质：国有
行业：建筑施工
规模：年营收50亿，员工2000人
供应链位置：核心企业
痛点：
  - 上游供应商账期长，供应商投诉
  - 项目资金需求大
  - 信用体系建设
需求：
  - 供应链金融平台
  - 降低应付账款压力
  - 供应商管理
适配产品：
  - 反向保理平台
  - 商票融资
  - 供应链ABS
```

---

## 文件命名规范

- 单个客户：`{customer_name}.md`
- 行业汇总：`{industry}_customers.md`
- 类型汇总：`{enterprise_type}_customers.md`

---

## 客户录入规范

### 必填字段
- customer_id
- customer_name
- enterprise_type
- industry
- scale
- supply_chain_position
- pain_points
- needs

### 选填字段
- core_enterprise
- business_scenario
- financial_status
- constraints
- decision_factors
- taboos
- matching_products
- matching_score

---

*客户库 | 2026-04-12*
