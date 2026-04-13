# Claudecode 访问金融产品智能匹配工具项目指南

## 🎯 快速开始

### 1. 克隆项目

```bash
cd ~/projects
git clone https://github.com/Oooooldbai/financial-product-matcher.git
cd financial-product-matcher
```

### 2. 阅读项目文档

```bash
# 阅读项目概述
cat PROJECT.md

# 阅读产品库结构
cat "02 DataLayer/01 ProductLibrary/INDEX.md"

# 阅读Rules层（匹配规则）
cat "03 Rules/INDEX.md"
```

---

## 📋 Claude Code 完整指令

复制以下内容，粘贴到Claude Code中：

---

```
请帮我开发一个金融产品智能匹配工具的MVP 1 Web应用。

## 项目仓库
https://github.com/Oooooldbai/financial-product-matcher

## 项目概述
这是一个面向金融从业人员的随身产品助手，帮助业务员快速匹配产品和客户。

## 项目已完成的内容

### 数据层（91个产品，113家核心企业）
- 产品库：42家银行，91个+供应链金融产品
  - 国有大行（6家）：工行、农行、中行、建行、交行、邮储
  - 股份制银行（12家）：招商、平安、中信、民生等
  - 民营互联网银行（19家）：微众、网商、众邦等
  - 外资银行（5家）：汇丰、花旗、渣打、星展

- 客户库：113家核心企业，覆盖10大行业
  - 电子/通信：华为、苹果、小米、OPPO、vivo
  - 汽车/新能源：特斯拉、比亚迪、宁德时代、蔚来
  - 房地产/建筑：万科、保利、中国建筑
  - 电力/能源：国家电网、南方电网
  - 钢铁/金属：宝钢、河钢
  - 光伏/新能源：隆基绿能、通威股份
  - 化工：万华化学、荣盛石化

### Rules层（匹配规则和话术库）
- 匹配规则：6维度匹配算法
  - 痛点匹配度（30%）
  - 需求匹配度（25%）
  - 准入条件匹配（20%）
  - 利率优势（10%）
  - 核心企业关联（10%）
  - 行业经验（5%）

- 话术库：9套完整话术模板
  - 类型A：民营上市×DD×痛点切入
  - 类型B：国央企×SCF×合规切入
  - 类型C：大型民企×SCF×关系切入
  - 类型D：银行×资产质量切入
  - 类型E：保理公司×风险控制切入

### 后端API（18个接口）
- 产品相关：6个接口
- 客户相关：7个接口
- 匹配相关：2个核心接口
- 客群筛选：2个接口

## MVP 1 四大核心功能

### 功能1：客户→产品匹配
用户输入客户画像 → 系统推荐适配产品 → 展示匹配理由和话术

### 功能2：产品→客户筛选
用户选择产品 → 系统筛选目标客户 → 展示客户列表

### 功能3：客群→产品筛选
用户选择客群特征（如"中型制造业民企"） → 系统筛选适合的产品

### 功能4：产品对比
用户选择2-3个产品 → 系统对比目标客户特征 → 展示差异

## 技术栈
- 前端：React + TypeScript + Tailwind CSS + React Router + React Query
- 后端：Node.js + Express + Prisma + SQLite（开发）/ PostgreSQL（生产）
- 状态管理：Redux Toolkit

## 当前状态
- ✅ 后端API：已实现（server/src/routes/）
- ✅ 数据库模型：已设计（server/prisma/schema.prisma）
- ✅ 匹配算法：已实现
- ⏳ 前端页面：待开发

## 待完成的前端任务

### 1. 创建项目结构
```bash
mkdir -p client/src/{pages,components,store,hooks,types,utils}
```

### 2. 安装依赖
```bash
cd client
npm install
```

### 3. 创建页面组件
- src/App.tsx - 主应用（React Router导航）
- src/pages/CustomerMatch.tsx - 客户→产品匹配
- src/pages/ProductFilter.tsx - 产品→客户筛选
- src/pages/GroupFilter.tsx - 客群→产品筛选
- src/pages/ProductCompare.tsx - 产品对比
- src/pages/Home.tsx - 首页

### 4. 创建UI组件
- src/components/Navigation.tsx - 导航栏
- src/components/ProductCard.tsx - 产品卡片
- src/components/CustomerCard.tsx - 客户卡片
- src/components/MatchResult.tsx - 匹配结果
- src/components/ScriptDisplay.tsx - 话术展示
- src/components/FilterForm.tsx - 筛选表单

### 5. 创建API服务
- src/services/api.ts - API客户端
- src/hooks/useProducts.ts - 产品Hook
- src/hooks/useCustomers.ts - 客户Hook
- src/hooks/useMatch.ts - 匹配Hook

### 6. 创建类型定义
- src/types/product.ts - 产品类型
- src/types/customer.ts - 客户类型
- src/types/match.ts - 匹配类型

## 参考文件

### 核心规则文件
- PROJECT.md - 项目全貌
- "03 Rules/RULES.md" - 匹配规则框架
- "03 Rules/MATCHING_ENGINE.md" - 匹配引擎
- "03 Rules/MATCHING_RULES_DETAIL.md" - 匹配规则细化
- "03 Rules/SCRIPTS.md" - 话术库

### 数据文件
- "02 DataLayer/01 ProductLibrary/INDEX.md" - 产品库索引
- "02 DataLayer/02 CustomerLibrary/INDEX.md" - 客户库索引
- "02 DataLayer/02 CustomerLibrary/CORE_ENTERPRISES.md" - 核心企业详情

### 后端文件
- server/src/routes/match.ts - 匹配API
- server/src/routes/products.ts - 产品API
- server/src/routes/customers.ts - 客户API
- server/src/routes/group.ts - 客群筛选API

## API接口

### 1. 客户→产品匹配
POST /api/match/customer-to-products
Request: { customerProfile: {...} }
Response: { recommendations: [...] }

### 2. 产品→客户筛选
POST /api/match/product-to-customers
Request: { productId: "xxx" }
Response: { targetCustomers: [...] }

### 3. 客群→产品筛选
POST /api/group/filter-products
Request: { enterpriseType: ["民营"], scale: ["中型"], industry: ["制造业"] }
Response: { filteredProducts: [...] }

### 4. 产品对比
POST /api/products/compare
Request: { productIds: ["id1", "id2"] }
Response: { comparison: {...} }

## 请帮我完成

1. 初始化React项目
2. 创建所有页面组件（4个核心页面+首页）
3. 创建UI组件库
4. 连接后端API
5. 实现完整交互流程
6. 添加样式（Tailwind CSS）

请先阅读项目文档，了解业务背景后再开始开发。
```

---

## 📁 快速查看关键文件

```bash
# 项目概述
cat PROJECT.md

# 匹配规则（核心业务逻辑）
cat "03 Rules/RULES.md"
cat "03 Rules/MATCHING_RULES_DETAIL.md"

# 话术库（营销话术）
cat "03 Rules/SCRIPTS.md"

# 产品库索引
cat "02 DataLayer/01 ProductLibrary/INDEX.md"

# 客户库索引
cat "02 DataLayer/02 CustomerLibrary/INDEX.md"

# 核心企业列表
cat "02 DataLayer/02 CustomerLibrary/CORE_ENTERPRISES.md"
```

---

## 🎯 开发建议

1. **先读懂业务**：阅读PROJECT.md和RULES.md，理解匹配逻辑
2. **参考话术库**：SCRIPTS.md有完整的9套话术模板
3. **复用数据**：产品库和客户库已有完整数据，可以直接使用
4. **渐进开发**：先完成一个功能页面，再扩展其他

---

## 📞 如需帮助

阅读以下文件获取更多细节：
- `PROJECT.md` - 项目全貌
- `03 Rules/INDEX.md` - Rules层完整说明
- `04 DataCollection/INDEX.md` - 数据采集器说明
```

---

## 📋 一键复制指令

```
请帮我开发一个金融产品智能匹配工具的MVP 1 Web应用。

## 项目仓库
https://github.com/Oooooldbai/financial-product-matcher

## 项目概述
这是一个面向金融从业人员的随身产品助手，帮助业务员快速匹配产品和客户。

## 项目已完成的内容

### 数据层（91个产品，113家核心企业）
- 产品库：42家银行，91个+供应链金融产品
- 客户库：113家核心企业，覆盖10大行业

### Rules层（匹配规则和话术库）
- 匹配规则：6维度匹配算法
- 话术库：9套完整话术模板

### 后端API（18个接口）
- 产品相关：6个接口
- 客户相关：7个接口
- 匹配相关：2个核心接口

## MVP 1 四大核心功能

1. 客户→产品匹配
2. 产品→客户筛选
3. 客群→产品筛选
4. 产品对比

## 技术栈
- 前端：React + TypeScript + Tailwind CSS + React Router + React Query
- 后端：Node.js + Express + Prisma

## 待完成的前端任务

1. 初始化React项目
2. 创建4个核心页面（客户匹配、产品筛选、客群筛选、产品对比）
3. 创建UI组件库
4. 连接后端API

请先阅读项目文档（PROJECT.md、RULES.md、SCRIPTS.md），了解业务背景后再开始开发。
```
