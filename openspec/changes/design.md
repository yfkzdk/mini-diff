# Design — mini-diff

## ADR-1: 逐行 LCS 简化

**决策**: 不实现完整 Myers 算法。用简单的逐行迭代 + 相邻行匹配。

**理由**: mini-diff 用于演示统一 diff 格式，不用于大文件。几 KB 文件内 O(n²) 足够。实现 ~80 行。

## ADR-2: 单模块结构

```
src/mini_diff/
  __init__.py
  __main__.py    # CLI: python -m mini_diff old new
  diff.py        # compare() — LCS + hunk formatting
```

## ADR-3: 零依赖

Python stdlib only。`difflib` 本身是 stdlib——但我们不调 `difflib.unified_diff`，而是自己实现核心逻辑以展示理解。

## 预计 ~120 行
