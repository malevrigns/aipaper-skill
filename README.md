# 🧐 AI Paper Review — 识别 AI 味论文的 Skill

> **现在的 AI 写作问题，已经不是"降低 AIGC 率"那么简单了。**
> 真正让审稿人抓狂的，是那些"看起来挺严谨、其实全是 AI 痕迹"的论文。
> 这个 skill 把**大量审稿人的实战经验**沉淀成一套可复用的检测清单 + 评分量表 + 报告模板。

---

## 它解决什么问题？

AI 写的论文，毛病早已不是"降重能解决的"：

| # | 症状 | 典型表现 |
|---|------|---------|
| 1 | 🔰 **过度防御，免责声明满天飞** | 话不敢说满，满纸 hedging；严谨全靠免责声明硬撑 |
| 2 | 🔁 **车轱辘话复读** | 语言匮乏，同一整句话在 Introduction 和 Methodology 里原样出现两遍 |
| 3 | 🧵 **没有灵魂的主线** | 讲不清为什么做这个研究，动机都不立，一堆实验无主次硬堆 |
| 4 | 📊 **数据汇报混乱** | 通篇六位小数、格式前后不一；CI / p-value 直接怼进正文不进表格/appendix |
| 5 | 📓 **写成未加工实验日志** | 六七个实验大半是 "cannot draw any robust conclusion"，有效信息为零 |
| 6 | 📄 **硬凑页数** | 正文留白，靠拉长 Related Work、塞巨型大图、超长 Limitation 勉强凑够页数 |

**为了解决这个问题，我们收集了大量审稿人对 AIGC 论文的共性观察，组成这个 skill。**



## 它能做什么？
- ✅ **AI 味检测**：逐条扫描 6 大症状，命中即要求贴出原文证据（不靠玄学）。
- ✅ **科研图规范性审查**：框架图清晰度、结果图学术规范（坐标轴/单位/误差棒/legend/分辨率）、AI 生成痕迹（工具水印、风格拼凑）。
- ✅ **量化评分**：AI-Flavor Score (0–10) + Figure Standards Score (0–10) + Overall Verdict。
- ✅ **结构化报告**：结论先行 + Top-3 问题（带证据）+ 可执行修改建议。

## 核心设计原则
1. **只列可观察、可引用的信号** —— 每条命中必须能贴出原文句子或指出具体图。
2. **"严谨"本身不是缺点** —— 诚实汇报 negative results 是好事；skill 区分"好严谨"和"防御性废话"、区分"一个 inconclusive"和"通篇 inconclusive"。
3. **面向 AI 写作 vs 面向人类阅读** —— 如果一篇论文只有 AI 读得顺、人类翻两页就放弃，它大概率是 AI 味的。

## 目录结构
```
aipaper-skill/
├── SKILL.md                     # ★ skill 定义：触发条件 + 5步工作流 + 设计原则
├── checklists/
│   ├── ai_flavor.md             # AI 味检测清单（A主线/B语言/C实验/D篇幅/E诚信 + 量化指标）
│   └── figure_standards.md      # 科研图规范性清单（F框架/R结果/G溯源）
├── rubric.md                    # 评分量表：加权计分 + verdict 映射 + 示例
├── templates/
│   └── review_report.md         # 审查报告输出模板
└── README.md
```

## 快速开始
### 给人用（审稿辅助）
把 `checklists/*.md` 当审稿清单，逐条打勾并摘录证据 → 用 `rubric.md` 打分 → 按 `templates/review_report.md` 出报告。

### 给 AI agent 用
将 `SKILL.md` + 两个 checklist + `rubric.md` 作为 system prompt 注入，喂入 paper 文本 / 图片，
要求 agent 严格按 SKILL workflow 的 5 步输出 report 模板格式。

### 给作者自检
投稿前跑一遍，重点看 **AI-Flavor Score** 和 **Figure Audit 的红灯项**（尤其 E1 工具水印、F1 无主框架图、B2 跨章节复读）。



## License
MIT — 自由使用、修改、分发（审稿辅助 / agent prompt / 作者自检均可）。

---
*经验来源：多位 AAAI / ICLR / CSSCI 义务审稿人对 AIGC 论文的共性观察，去重归类后沉淀为本 skill。*

