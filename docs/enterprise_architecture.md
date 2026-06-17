# Enterprise 系统架构

## 架构目标

Enterprise 版本在 MVP 算法流程基础上增加本地可运行的前后端系统，使评审能够通过浏览器查看指标、图表和单用户推荐结果。

## 分层设计

```text
React Frontend
    |
FastAPI Routers
    |
Service Layer
    |
SQLite + CSV + Model Artifacts
    |
MVP Analytics Package
```

## 后端

FastAPI 后端负责暴露本地 API。路由层只处理请求和响应，核心计算放在 service 层，便于测试和维护。

主要模块：

- `health`：健康检查。
- `overview`：整体 KPI。
- `funnel`：漏斗指标。
- `retention`：cohort 留存。
- `experiment`：A/B 实验分析。
- `model`：模型指标和风险分布。
- `users`：用户列表和详情。
- `nba`：Next Best Action 推荐。

## 数据层

SQLite 用于本地演示和查询。初始化脚本会读取样例 CSV 和模型 artifacts，构建本地数据库。当前 API 计算层仍主要复用 CSV 与模型 artifacts，以保持 MVP 分析流程和 Enterprise 展示层一致；SQLite 在本版本中承担本地初始化、演示查询和后续扩展的 materialized store 角色。生产化时应将用户风险、NBA 结果和核心聚合指标统一写入数据库或特征存储，由 API 分页查询预计算结果。项目没有引入 Redis、Kafka、Flink 或 PostgreSQL，因为当前本地评审场景不需要这些组件。

## 前端

前端使用 React + Vite + TypeScript，并通过 API client 调用 FastAPI。页面设计以评审快速理解为目标，覆盖 Overview、Funnel、Retention、Experiment、Churn Risk 和 User Detail。

## 可复现性

所有数据均可由脚本重新生成，模型训练和后端数据库初始化都有明确命令。系统不依赖云端服务。
