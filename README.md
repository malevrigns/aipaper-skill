<a id="top"></a>

<div align="center">

<img src="assets/hero-editorial.png" alt="AI 论文写作，早已不只是降低 AIGC 率。调研多位审稿人，阅读 2026 年大量 AI 论文后的观察。" width="100%">

<h1>AI Paper Review</h1>
<p><strong>从审稿人的问题出发，重新审视 AI 协助完成的论文。</strong></p>
<p>研究动机 · 论证结构 · 结果解释 · 具体修改</p>

[![MIT License](https://img.shields.io/badge/License-MIT-242321?style=flat-square)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-242321?style=flat-square)](scripts/README.md)
[![Standard library](https://img.shields.io/badge/Scanner-stdlib_only-c74735?style=flat-square)](scripts/README.md)

**[开始检查论文](#quickstart)** · **[先看修改案例](#example)** · **[查看五张图片](#gallery)**

[项目缘起](#why) · [六类痛点](#problems) · [审查方法](#workflow) · [资源导航](#resources) · [English](README.en.md)

</div>

---

<a id="why"></a>

## 写得像论文，为什么还是讲不清研究？

调研多位审稿人，并阅读了 **2026 年大量 AI 论文**后，我反复遇到同一类问题：语言很流畅，措辞很谨慎，统计分析也列得完整，但读完仍然说不清这项研究为什么值得做、发现了什么、证据又在哪里。

这些问题已经深入到**研究动机、论证结构和结果解释**。换词、调句式、降低 AIGC 率，补不上缺失的论证。

**这个 skill 把调研中反复出现的问题，整理成可以逐项核对、定位到原文、落实到修改的工作方法。**

<a id="problems"></a>

## 六类反复出现的问题

<table>
<tr>
<td width="50%" valign="top">
<h3>01 · 过度防御</h3>
<p><strong>免责声明写满了，核心主张却不见了。</strong></p>
<p>每个判断后都跟着限定语，读者仍不知道作者究竟主张什么，适用边界又在哪里。</p>
</td>
<td width="50%" valign="top">
<h3>02 · 跨章节复读</h3>
<p><strong>从 Introduction 到 Methodology，读到同一句话。</strong></p>
<p>章节换了，信息没有推进。该补定义、实现和证据的位置，仍在重复背景与动机。</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>03 · 研究主线缺失</h3>
<p><strong>实验做了不少，为什么做这个问题？</strong></p>
<p>背景、方法和实验各说各的，没有解释问题为何重要，也没有区分核心验证与补充分析。</p>
</td>
<td width="50%" valign="top">
<h3>04 · 结果汇报混乱</h3>
<p><strong>六位小数很精确，关键发现很模糊。</strong></p>
<p>同一指标精度不一，统计摘要成段粘贴。读者看到很多数字，却找不到收益、代价与适用范围。</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>05 · 实验日志化</h3>
<p><strong>一连串实验，最后只留下“无法得出结论”。</strong></p>
<p>没有说明这些结果排除了什么、保留了什么认识，以及它们如何影响核心主张。</p>
</td>
<td width="50%" valign="top">
<h3>06 · 篇幅与信息失衡</h3>
<p><strong>页数凑够了，关键解释还是缺席。</strong></p>
<p>冗长相关工作、巨型图和大段 Limitation 占据版面，研究设计与结果含义却没有充分交代。</p>
</td>
</tr>
</table>

> **还需要警惕“面向 AI 评价”的写作。**
>
> 如果评审把谨慎措辞直接当作主张严谨，把统计细节齐全当作分析充分，研究没有讲清的论文也可能获得过高评价。调研让我更加关注这一偏差：评价应该回到问题是否重要、主张是否清楚、证据是否支持结论。

<a id="workflow"></a>

## 从发现问题，到改动原文

<table>
<tr>
<td width="33%" valign="top">
<h3>01 / 读主线</h3>
<p>为什么研究这个问题？<br>方法针对哪个困难？<br>核心实验回答什么？</p>
<p><a href="references/storyline.md">研究主线检查 →</a></p>
</td>
<td width="34%" valign="top">
<h3>02 / 核证据</h3>
<p>哪项证据支持哪条主张？<br>收益和代价分别是什么？<br>反例会怎样改变结论？</p>
<p><a href="templates/claim_evidence.md">主张与证据表 →</a></p>
</td>
<td width="33%" valign="top">
<h3>03 / 改原文</h3>
<p>定位章节、段落和句子。<br>分清补证据与改表达。<br>给出可以执行的修改。</p>
<p><a href="templates/author_revision.md">作者修改模板 →</a></p>
</td>
</tr>
</table>

每条审查意见都包含 **原文位置、问题依据、实际影响和具体改法**，优先处理影响研究结论的缺口。

| 优先级 | 先处理什么 |
| :--- | :--- |
| **P0 · 核心证据** | 核心主张缺少支持，或与已有结果矛盾 |
| **P1 · 重要解释** | 动机、方法或结果解释存在论证断点 |
| **P2 · 局部表达** | 重复、精度和图文组织妨碍阅读 |

[查看完整审查示范 →](examples/demo_review.md)

<a id="example"></a>

## 一次具体修改，比一句“去 AI 味”更有用

<table>
<tr>
<th align="left" width="50%">修改前 · 逐条抄录数值</th>
<th align="left" width="50%">修改后 · 讲清收益与代价</th>
</tr>
<tr>
<td valign="top">
<p>Baseline throughput was 100.000000 tasks/min. Our method achieved 112.000000 tasks/min. The runtime was 8.700000 ms. The baseline runtime was 8.200000 ms.</p>
</td>
<td valign="top">
<p>In this setting, throughput increased from <strong>100 to 112 tasks/min (+12%)</strong>, while planning time rose from <strong>8.2 to 8.7 ms (+0.5 ms)</strong>.</p>
</td>
</tr>
</table>

<sub>合成案例，两侧使用同一批数值。没有独立重复数据，因此没有补造显著性结论。</sub>

一段话交代关键比较、收益、代价和范围。[查看全部六个修改案例 →](examples/before_after.md)

<a id="quickstart"></a>

## 现在检查一份稿件

把仓库放入支持 `SKILL.md` 的客户端技能目录，文件夹命名为 `ai-paper-review`。也可以让当前 agent 直接读取仓库根目录的 `SKILL.md`，再提供稿件。安装入口依客户端而定。

**审查整篇论文：**

```text
使用 ai-paper-review 检查这份论文。
先看研究主线和核心主张对应的证据，再看重复、结果解释和图表。
最多给三个优先问题，每条指出原文位置、影响和具体改法。
```

**直接修改一段内容：**

```text
按 ai-paper-review 检查这段 Results，并直接给我改好的内容。
保留真实数值、必要限定和负面结果，不新增实验或结论。
```

<details>
<summary><strong>运行本地文本扫描器</strong> · Python 3.9+，仅标准库</summary>

```bash
git clone https://github.com/malevrigns/aipaper-skill.git
cd aipaper-skill
python scripts/ai_paper_check.py examples/demo_paper.md
```

```bash
# 输出带章节、行号和证据片段的报告
python scripts/ai_paper_check.py paper.md --json report.json --markdown report.md

# 按章节输入
python scripts/ai_paper_check.py --sections intro.txt method.txt results.txt
```

扫描器无网络调用，支持 UTF-8 文本、Markdown 和简单 LaTeX。PDF 需先提取文本，图像与版面另行检查。

随仓库提供的 demo 可复现四类候选：限定语成串、跨章节复读、未替换参数和同列表格精度。脚本定位文本候选，完整语义审查仍需结合稿件内容。

[参数、退出码与解析范围 →](scripts/README.md)

</details>

<a id="gallery"></a>

## 五张图片，讲清项目针对的问题

一张横版头图，四张竖版海报。点击缩略图查看原图，可用于项目介绍、社交平台图文与视频画面。

<p align="center">
<a href="media/images/campaign-poster.png"><img src="media/images/campaign-poster.png" alt="写得很谨慎，研究讲清楚了吗？" width="170"></a>
<a href="media/images/six-review-issues.png"><img src="media/images/six-review-issues.png" alt="投稿前，再读一遍：六类论文问题" width="170"></a>
<a href="media/images/experiments-to-findings.png"><img src="media/images/experiments-to-findings.png" alt="实验做了很多，发现是什么？" width="170"></a>
<a href="media/images/author-revision.png"><img src="media/images/author-revision.png" alt="AI 写完之后，作者的工作还没结束。" width="170"></a>
</p>
<p align="center"><sub><a href="media/images/campaign-poster.png">02 · 谨慎与贡献</a> · <a href="media/images/six-review-issues.png">03 · 六类问题</a> · <a href="media/images/experiments-to-findings.png">04 · 实验与发现</a> · <a href="media/images/author-revision.png">05 · 作者的工作</a></sub></p>

[01 / 首页横幅原图](assets/hero-editorial.png) · [五图目录与使用说明](media/README.md)

<a id="resources"></a>

## 按任务找到入口

| 你要做什么 | 从这里开始 |
| :--- | :--- |
| 让 agent 审查或修改稿件 | [Skill 入口](SKILL.md) · [检查清单](checklists/ai_flavor.md) |
| 梳理研究主线与证据 | [主线检查](references/storyline.md) · [主张与证据表](templates/claim_evidence.md) |
| 整理结果与图表 | [结果汇报](references/results_reporting.md) · [图表检查](checklists/figure_standards.md) |
| 输出审查意见或修改计划 | [报告模板](templates/review_report.md) · [修改模板](templates/author_revision.md) |
| 看效果，运行示例 | [修改案例](examples/before_after.md) · [示范审查](examples/demo_review.md) · [扫描器](scripts/README.md) |
| 补充问题与反例 | [贡献指南](CONTRIBUTING.md) · [审查校准](references/reviewer_calibration.md) |

<details>
<summary><strong>统计汇报、审查边界与版本兼容</strong></summary>

每条意见都要回到原稿与实际影响，优点也需要依据。

| 容易误判的情况 | 这里的处理 |
| --- | --- |
| 正文中出现 CI / p 值 | 核对解释与可读性，关键统计量可以留在正文 |
| 负结果很多 | 判断信息价值及对主张的影响，保留核心反证 |
| 措辞谨慎、limitation 很长 | 继续核对研究问题与证据，不自动奖励“严谨” |
| 某句重复、留有工具署名 | 核对信息增量与署名用途，不推断作者身份 |
| 没有框架图或图比较大 | 判断是否影响实际理解，不按固定图数和面积扣分 |

v2 将旧版的 `AI-Flavor Score` 和作者身份标签替换为编辑候选与质量问题。本项目没有提供经验证的 AI 检测准确率或录用预测。[量表与迁移说明 →](rubric.md)

</details>

---

<div align="center">
<p><strong>为什么做这项研究？发现了什么？证据在哪里？</strong></p>
<p>把这三个问题讲清楚，是这套 skill 的出发点。</p>
<p><a href="CONTRIBUTING.md">贡献问题案例</a> · <a href="LICENSE">MIT License</a> · <a href="#top">回到顶部 ↑</a></p>
</div>
