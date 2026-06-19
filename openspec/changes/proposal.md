# mini-diff — 形式化规格

## Step 0a: 外部需求

**来源**: GNU Diffutils 官方文档 (gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html)
**性质**: 成熟行业标准——非自编

## 目标

比较两个文本文件，输出 unified diff 格式。和 `diff -u old new` 兼容。

成功标准: 给定两个文件，输出符合 GNU Diffutils 规范的 unified diff。

## 边界

### 范围内
- 读取两个文本文件，逐行比较
- 输出 unified diff header（`---`/`+++`）+ hunks（`@@`）
- 识别相同行（context）、删除行（`-`）、新增行（`+`）
- 支持多个 hunks（文件中有多处修改时）
- 零依赖 Python stdlib

### 范围外
- 二进制文件比较
- 目录比较（只做单文件）
- 彩色输出
- 合并/补丁应用
- 忽略空白选项

## 数据模型

```
Hunk:
  old_start: int
  old_count: int
  new_start: int
  new_count: int
  lines: list[str]    # 每行以 ' ' / '-' / '+' 开头

DiffResult:
  old_file: str
  new_file: str
  hunks: list[Hunk]
```

## 不变量

1. **Hunk 非空**: 每个 hunk 至少包含 1 行变更（删除或新增）
2. **Context 最小化**: 相邻 hunks 之间有 ≥1 行不重叠的 context
3. **@@ 头正确**: old_count = 删除行数 + context 行数, new_count = 新增行数 + context 行数

## 函数规格

### compare(old_lines, new_lines) → DiffResult
```
前置: old_lines, new_lines 为 list[str]
后置: 返回 DiffResult——包含 old/new 文件名和所有 hunks
```

## 测试场景

| ID | 场景 | 期望 |
|----|------|------|
| T1 | 完全相同的文件 | 无 hunks |
| T2 | 新增一行 | `@@ -1,0 +1,1 @@` + 一行 `+` |
| T3 | 删除一行 | `@@ -1,1 +1,0 @@` + 一行 `-` |
| T4 | 修改一行 | `@@ -1,1 +1,1 @@` + 一行 `-` 一行 `+` |
| T5 | 多 hunks | 两个 `@@` 块 |
| T6 | 空文件 | 无 hunks |
