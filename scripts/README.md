# 文本扫描器

Python 3.9+，仅标准库。本地读取文件，不调用模型或网络。输出带来源、章节、行号的编辑候选，供人工或 agent 结合上下文判断。

```bash
python scripts/ai_paper_check.py examples/demo_paper.md
python scripts/ai_paper_check.py paper.md --json report.json --markdown report.md
python scripts/ai_paper_check.py --sections intro.txt method.txt results.txt
python scripts/ai_paper_check.py paper.md --include-appendix
```

## 能检查什么

| 输出 | 行为 |
| --- | --- |
| B1_DEFENSE_CLUSTER | 一段中成串出现空泛限定短语，默认至少 3 次；单独 may / might 不触发 |
| B2_REPETITION | 足够长的句子精确或近似重复，默认 12 tokens、5-gram Jaccard ≥ 0.8；中文按单字 token |
| C1_TABLE_PRECISION | Markdown 表格同列数字显示精度不一致；不同列分开看，p 值列跳过 |
| C2_STATS_CLUSTER | 正文一段至少 4 次统计摘要提及；仅提示核对解释，不判定不规范 |
| E1_PLACEHOLDER | 正文或 Markdown 表格中可能未替换的占位文字 |
| observations | 谨慎短语、不确定句子、统计量和高精度数字的出现次数，不换算实验占比或评分 |

Markdown 标题、常见英文/中文章节标题和简单 LaTeX section 可提供章节边界。默认跳过识别到的参考文献、致谢、附录、围栏代码和 LaTeX 表格/公式环境；表格内容不计入正文统计密度。摘要不参与重复句比较。同一文本文件中也能检测重复。

这是启发式解析器，不是完整 Markdown/LaTeX 解释器，不读取 PDF 图片，也不能重建复杂宏、HTML 表格、OCR 错误或语义。没有空行的抽取文本可能被当作一个长段落；先恢复章节和段落。显示的行号属于输入文本，不是原 PDF 页码。一次扫描最多展示 50 对重复例子，JSON 同时保留重复总数和截断标记。

## 参数与退出码

可调参数：`--similarity`、`--min-repeat-tokens`、`--defense-threshold`、`--stat-threshold`。这些阈值未经检测准确率校准。

- `0`：扫描完成，包括发现候选的情况。
- `1`：仅在显式使用 `--fail-on-findings` 且存在候选时返回，适合自主选择的 CI 门槛。
- `2`：参数、输入编码或文件错误。

输入为 UTF-8 `.txt`、`.md`、简单 `.tex`。重复输入、相同报告路径、用报告覆盖输入会被拒绝。完整来源路径保留，`method_1.txt` 和 `method_2.txt` 不会互相覆盖。

## v2 JSON 迁移

新增 `schema_version`、`summary`、`findings`、`observations`、`coverage`、`settings`。取消 v1 的 `ai_flavor_score`、`verdict`、`score_breakdown` 和默认以分数作为退出码。使用这些字段的下游需要适配；本版本不输出写作来源、生成概率或录用建议。

## 验证

```bash
python -m unittest discover -s tests -v
```

测试涵盖位置定位、中英文重复、合法统计表达、表格分离、附录/引用/代码排除、同名章节路径和失败退出码。它验证工具行为，不代表论文判断能力已经通过真实投稿测试。
