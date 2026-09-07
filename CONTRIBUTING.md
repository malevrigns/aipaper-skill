# 参与改进

欢迎提交能让审查更准确的案例、反例或修复。请包含原规则、最小片段、误报/漏报、预期判断及理由。使用公开或合成材料，不要提交无权公开的评审稿件。

规则要指出研究或表达问题及其影响，不根据常用词、作者语言背景或画风推断写作来源。新规则需要一个问题示例和一个应放行的近似反例。

修改扫描器后运行：

```bash
python -m unittest discover -s tests -v
python scripts/ai_paper_check.py examples/demo_paper.md
```

扫描器保持标准库依赖。宣发图片集中放在 `media/images/`，README 横幅放在 `assets/`。不要用虚构的 AI 检测准确率或自动审稿得分证明有效性。
