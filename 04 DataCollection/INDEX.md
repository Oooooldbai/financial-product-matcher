# 数据采集器索引

> 更新时间: 2026-04-13

---

## 采集器架构

```
数据源 → 采集器 → 标准化处理 → 知识库存储
                              ↓
                         Rules层调用
```

---

## 采集器文件结构

| 文件 | 功能 | 优先级 | 状态 |
|------|------|--------|------|
| **policy_collector.py** | 政策法规采集器 | P0 | ✅ 已完成 |
| **customer_collector.py** | 客户画像采集器 | P0 | ✅ 已完成 |
| **supply_chain_discoverer.py** | 供应链关系发现器 | P0 | ✅ 已完成 |
| **run_all_collectors.py** | 运行所有采集器 | P1 | ⏳ 待创建 |

---

## 一、政策法规采集器（policy_collector.py）

### 功能
从央行、金监局、证监会等机构采集政策文件

### 数据源
- 央行
- 国家金融监督管理总局
- 证监会
- 财政部

### 关键词过滤
- 供应链金融
- 票据
- 应收账款
- 保理
- 中小企业
- 融资
- 风险管理
- 合规
- 票据法
- 民法典
- 支付结算

### 输出格式
```json
{
  "policy_id": "POL-20260413-0001",
  "title": "政策标题",
  "url": "政策URL",
  "pub_date": "发布日期",
  "content": "政策内容（限制5000字符）",
  "attachments": [
    {
      "type": "PDF",
      "url": "附件URL",
      "name": "附件名称"
    }
  ],
  "keywords": ["关键词1", "关键词2"],
  "source": "来源机构",
  "category": "政策分类",
  "collected_at": "采集时间"
}
```

### 使用方法
```bash
cd /workspace/projects/workspace/projects/financial-product-matcher/04 DataCollection/collectors
python policy_collector.py
```

---

## 二、客户画像采集器（customer_collector.py）

### 功能
从公开渠道采集企业基本信息、财务数据、供应链信息

### 数据源
- 企查查
- 天眼查
- 启信宝

### 采集内容
- 基础信息：企业类型、行业、成立日期、注册资本、法人代表
- 财务信息：年营收、净利润、总资产、负债率、现金流、应付账款、平均账期
- 供应链信息：主要客户、主要供应商、供应链位置、依赖度
- 信用信息：信用评级、违约记录、诉讼、银行授信

### 输出格式
```json
{
  "customer_id": "CUST-20260413-0001",
  "customer_name": "企业名称",
  "basic_info": {
    "enterprise_type": "民营",
    "industry": "电子制造",
    "established_date": "2010-01-01",
    "registered_capital": "1亿",
    "legal_representative": "张三",
    "stock_code": "600519.SH",
    "listing_status": "上市"
  },
  "financial_info": {
    "annual_revenue": "100亿",
    "net_profit": "10亿",
    "total_assets": "50亿",
    "total_liabilities": "20亿",
    "debt_ratio": "40%",
    "cash_flow": "稳定",
    "accounts_payable": "20亿",
    "average_payment_period": "90天"
  },
  "supply_chain_info": {
    "major_customers": [
      {"name": "华为", "ratio": "30%", "amount": "30亿"}
    ],
    "major_suppliers": [
      {"name": "供应商A", "ratio": "25%", "amount": "25亿"}
    ],
    "supply_chain_position": "一级供应商",
    "dependency_ratio": "50%"
  },
  "credit_info": {
    "credit_rating": "AA",
    "breach_record": [],
    "litigation": [],
    "bank_limit": "50亿"
  },
  "collected_at": "采集时间"
}
```

### 使用方法
```bash
cd /workspace/projects/workspace/projects/financial-product-matcher/04 DataCollection/collectors
python customer_collector.py
```

---

## 三、供应链关系发现器（supply_chain_discoverer.py）v1.1

### 功能
从年报提取客户-核心企业关系，识别多链条供应链

### 数据源
- 巨潮资讯网
- 上交所
- 深交所

### 核心特性
- **动态关系模型**：不使用静态字段，使用关系数组
- **多链条识别**：识别上游链、下游链、交叉链
- **关系强度计算**：基于占比计算关系强度（0-100）

### 采集内容
- 主要客户：名称、金额、占比、关系强度
- 主要供应商：名称、金额、占比、关系强度
- 供应链关系：关系类型（上游/下游）、角色、金额、占比、强度
- 多链条：上游链、下游链、交叉链

### 输出格式
```json
{
  "stock_code": "000858.SZ",
  "year": 2023,
  "company_name": "五粮液股份有限公司",
  "major_customers": [
    {
      "name": "经销商A",
      "amount": "100亿",
      "ratio": "30%",
      "type": "customer"
    }
  ],
  "major_suppliers": [
    {
      "name": "供应商A",
      "amount": "50亿",
      "ratio": "25%",
      "type": "supplier"
    }
  ],
  "supply_chain_relations": [
    {
      "relation_type": "downstream",
      "party_name": "经销商A",
      "role": "customer",
      "amount": "100亿",
      "ratio": "30%",
      "strength": 60
    }
  ],
  "multi_chain": [
    {
      "chain_type": "upstream",
      "chain_name": "上游链-3条",
      "parties": [...]
    },
    {
      "chain_type": "downstream",
      "chain_name": "下游链-5条",
      "parties": [...]
    },
    {
      "chain_type": "cross",
      "chain_name": "交叉链-2个",
      "parties": ["企业A", "企业B"]
    }
  ],
  "discovered_at": "采集时间"
}
```

### 使用方法
```bash
cd /workspace/projects/workspace/projects/financial-product-matcher/04 DataCollection/collectors
python supply_chain_discoverer.py
```

---

## 采集流程

### 流程图

```
Step 1: 政策采集
  ↓
  采集央行、金监局、证监会政策文件
  ↓
  过滤关键词（供应链金融、票据等）
  ↓
  保存到 data/policies/

Step 2: 客户画像采集
  ↓
  输入企业名称或证券代码
  ↓
  从企查查/天眼查采集基础信息
  ↓
  从年报提取财务数据、供应链信息
  ↓
  保存到 data/customers/

Step 3: 供应链关系发现
  ↓
  输入证券代码
  ↓
  下载年报PDF
  ↓
  解析"前五大客户"、"前五大供应商"
  ↓
  构建动态关系模型
  ↓
  识别多链条供应链
  ↓
  保存到 data/supply_chain/
```

---

## 数据标准化

### 政策标准化
```python
# policy_collector.py
{
  "policy_id": f"POL-{date}-{index}",
  "title": title_text,
  "source": source_name,
  "category": category,
  "pub_date": pub_date,
  "content": content[:5000],
  "attachments": [...],
  "keywords": extracted_keywords
}
```

### 客户标准化
```python
# customer_collector.py
{
  "customer_id": f"CUST-{date}-{hash}",
  "customer_name": company_name,
  "basic_info": {...},
  "financial_info": {...},
  "supply_chain_info": {...},
  "credit_info": {...}
}
```

### 供应链关系标准化
```python
# supply_chain_discoverer.py
{
  "stock_code": stock_code,
  "year": year,
  "company_name": company_name,
  "major_customers": [...],
  "major_suppliers": [...],
  "supply_chain_relations": [...],
  "multi_chain": [...]
}
```

---

## 与Rules层对接

### 对接方式

```
数据采集器 → 知识库存储 → Rules层调用
```

### 调用示例

```python
# Rules层调用客户画像
from collectors.customer_collector import CustomerCollector

collector = CustomerCollector()
profile = collector.collect_customer_profile("华为技术有限公司")

# 传递给匹配引擎
from match_engine import MatchingEngine

engine = MatchingEngine()
recommendations = engine.match_customer_to_products(profile)
```

```python
# Rules层调用供应链关系
from collectors.supply_chain_discoverer import SupplyChainDiscoverer

discoverer = SupplyChainDiscoverer()
supply_chain = discoverer.discover_supply_chain_from_annual_report("000858.SZ", 2023)

# 传递给匹配引擎
recommendations = engine.match_product_to_customers_with_supply_chain(product_id, supply_chain)
```

---

## 数据质量保证

### 采集质量
- ✅ 多源验证（多个数据源交叉验证）
- ✅ 时间校验（检查发布日期）
- ✅ 格式校验（检查JSON格式）
- ✅ 内容校验（检查关键字段）

### 数据更新
- 政策：每周更新（采集最近30天）
- 客户画像：按需更新（客户查询时）
- 供应链关系：按年更新（每年年报发布后）

### 数据备份
- 本地备份：每天备份到 backup/
- 远程备份：定期同步到GitHub

---

## 后续优化

### 已完成
- ✅ 政策法规采集器
- ✅ 客户画像采集器
- ✅ 供应链关系发现器v1.1

### 待优化
- [ ] 产品采集器（从银行官网采集产品信息）
- [ ] 风险案例采集器（采集监管处罚案例）
- [ ] 统一运行脚本（run_all_collectors.py）
- [ ] 数据质量校验模块
- [ ] 数据更新调度器（定时采集）

---

*数据采集器索引 | 2026-04-13*
