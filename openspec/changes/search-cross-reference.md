# 交叉推理 — mini-diff

## 通道间矛盾
无。GNU Diffutils 规范是唯一权威来源。GitHub 参考实现和规范一致。

## 通道间互补
Web 规范提供了 `@@` 头的精确格式。GitHub 参考实现（agent 运行中）将提供实现层面的算法选择。

## 推理
统一 diff 格式的复杂度集中在 hunk 划分算法（LCS/Myers）。对 mini-diff 的规模，逐行比较足够。
