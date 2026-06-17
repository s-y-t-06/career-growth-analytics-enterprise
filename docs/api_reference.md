# API 参考

后端默认运行在 `http://localhost:8000`，交互式文档位于 `/docs`。这里的 `localhost` 表示评审机器上的本地服务地址，不代表云端部署地址。

## GET /health

返回服务健康状态。

## GET /overview

返回整体 KPI，包括用户数、事件数、流失率、D7 留存和模型核心指标。

## GET /funnel

返回核心用户路径每一步的用户数、转化率和 drop-off。

## GET /retention

返回 cohort 留存矩阵，用于观察 D1、D7、D14 留存表现。

## GET /experiment

返回 onboarding 实验结果，包括 variant 对比、激活指标和 SRM 检查。

## GET /model/metrics

返回模型选择结果、PR-AUC、ROC-AUC、Brier score、F1 和阈值。

## GET /model/risk-distribution

返回预测风险分布，用于前端绘制风险直方图。

## GET /model/subgroups

返回按渠道、职业阶段等维度聚合的分群风险表现。

## GET /users

返回用户列表，支持前端展示用户概览。

## GET /users/{user_id}

返回单用户画像、事件时间线、风险因素和推荐动作。

## GET /nba/{user_id}

返回指定用户的 Next Best Action。推荐结果基于预测风险和业务规则，不使用真实 churn label。
