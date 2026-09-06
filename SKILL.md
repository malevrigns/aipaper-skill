---
name: ai-paper-review
description: >
  Detect AI-generated / AI-assisted research papers. Scores "AI flavor" (over-hedging,
  repetition, missing storyline, messy data reporting, raw-log style results, padding)
  and checks whether figures meet academic standards. Use when reviewing a paper for
  AIGC traces or when an author wants a pre-submission self-check.
version: 1.0.0
license: MIT
tags: [aigc-detection, peer-review, paper-quality, research-figures]
input: paper PDF/text + optional figure images
output: structured review report (AI-flavor score + figure audit + actionable issues)
---

# Skill: AI Paper Review（AI 论文审查）

## 这个 skill 解决什么问题
现在的 AI 写作问题，**已经不是"降低 AIGC 率"那么简单**。真正让审稿人抓狂的，是这些：

| # | 症状 | 典型表现 |
|---|------|---------|
| 1 | **过度防御，免责声明满天飞** | 话不敢说满，满纸 hedging；严谨全靠免责声明硬撑 |
| 2 | **车轱辘话复读** | 语言匮乏，同一整句话在 Introduction 和 Methodology 里原样出现两遍 |
| 3 | **没有灵魂的主线** | 讲不清为什么做这个研究，动机都不立，一堆实验无主次硬堆 |
| 4 | **数据汇报混乱** | 通篇六位小数、格式前后不一；CI / p-value 直接怼进正文不进表格/appendix |
| 5 | **写成未加工实验日志** | 六七个实验大半是 "cannot draw any robust conclusion"，有效信息为零 |
| 6 | **硬凑页数** | 正文留白，靠拉长 Related Work、塞巨型大图、超长 Limitation 勉强凑够页数 |

本 skill = **大量审稿人经验的沉淀**。它给出可执行的检测清单 + 评分量表 + 报告模板，
让你（人或 AI agent）能一致地识别出"AI 味"并指出科研图是否规范。



## 工作流程（Workflow）
按顺序执行，每一步都对应一个 checklist：

1. **通读主线（Storyline Check）**
   - 能否一句话说清这篇 paper "为什么做 + 做了什么 + 证明了什么"？
   - Introduction / Methodology / Experiments 之间是否有真正的**推进关系**？
   - → 详见 `checklists/ai_flavor.md` §A、§C

2. **AI 味检测（AI-Flavor Scan）**
   - 逐条过 `checklists/ai_flavor.md` 的 6 大症状，标记命中项与原文证据（引用具体句子）。
   - 特别检查：跨章节重复句、hedging 密度、raw data 是否进正文。

3. **科研图规范性审查（Figure Audit）**
   - 对每张关键图过 `checklists/figure_standards.md`：
     框架图清晰度、结果图学术规范（坐标轴/单位/误差棒/legend/分辨率）、AI 生成痕迹（水印/风格不统一）。

4. **打分（Scoring）**
   - 用 `rubric.md` 给出：
     - **AI-flavor score (0–10)**：越高越像 AI 写的
     - **Figure standards score (0–10)**：越低越不规范
     - **Overall verdict**：Likely human / Mixed / Likely AIGC

5. **出报告（Report）**
   - 用 `templates/review_report.md` 输出结构化报告：结论先行 + 证据引用 + 可执行修改建议。

## 使用方式
- **给人用**：把 `checklists/*.md` 当审稿辅助清单，逐条打勾并摘录证据。
- **给 AI agent 用**：将本 `SKILL.md` + 两个 checklist + rubric 作为 system prompt 注入，
  喂入 paper 文本/图片，要求 agent 严格按 workflow 输出 report 模板格式。
- **给作者自检**：投稿前跑一遍，重点看 AI-flavor score 和 figure audit 的红灯项。

## 设计原则
- **只列可观察、可引用的信号**，不靠玄学。每条命中必须能贴出原文句子或指出具体图。
- **"严谨"本身不是缺点**。诚实汇报 negative results 是好事；问题在于"通篇都 inconclusive"或"堆砌无主次"。skill 区分"好严谨"和"防御性废话"。
- **面向 AI 写作 vs 面向人类阅读**：本 skill 的核心假设是——如果一篇论文只有 AI 读得顺、人类翻两页就放弃，它大概率是 AI 味的。

