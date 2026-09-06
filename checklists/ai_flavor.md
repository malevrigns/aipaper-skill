# AI-Flavor Detection Checklist（AI 味检测清单）

> 用法：逐条检查，命中即在 `[x]` 并**摘录原文证据**（引用具体句子 / 标注章节）。
> 每条给出「信号」「为什么是 AI 味」「反例（好严谨 vs AI 废话）」。
> 经验来源：多位 AAAI/ICLR/CSSCI 义务审稿人对 AIGC 论文的共性观察。

---

## §A. 结构与主线（Storyline & Motivation）

### A1. 没有清晰的 storyline / 各部分无推进关系
- [ ] **信号**：单看小标题猜不出这节要论证什么；Intro→Method→Experiments 之间没有逻辑递进。
- **证据**：`引用目录或小标题，指出断裂处`
- **为什么**："假设框架是 AI 搭的……各个部分之间没有真正的推进关系，空洞不扎实。"
- **反例**：好论文也结构清晰——区别在于每节是否真的在推进同一个 argument。

### A2. 动机缺失（不 justify 为什么要做这个研究）
- [ ] **信号**：Introduction 只堆背景，讲不清 "gap → why it matters → what we do"；或直接跳进方法。
- **证据**：`指出缺 motivation 的位置`
- **为什么**："根本讲不清为什么要做这个 research，连动机都懒得立。"
- **注意**：区分"motivation 写得弱"和"根本没写"。

### A3. 专有名词堆砌 / 术语过载
- [ ] **信号**：密集堆叠 niche terms，人类读不懂；用生僻词替代简单表达。
- **证据**：`摘录堆砌句`



## §B. 语言表达层（AI 废话 / 防御性）

### B1. 过度防御，免责声明满天飞 ⭐
- [ ] **信号**：满纸 hedging —— "may / might / could be argued / to some extent / it is worth noting that"；
      每个 claim 后面都跟一串限定词和免责声明。
- **证据**：`统计全文 hedging 密度；摘录 2-3 句最典型的`
- **为什么**："严谨全靠免责声明硬撑""段落有 AI 特有的防御性"。
- **反例（关键区分）**：
  - ✅ 好严谨 = 对**真正不确定**的地方谨慎措辞，claim 本身清晰有力。
  - ❌ AI 废话 = **所有**地方都加免责，导致没有一句敢把话说满，读者抓不到核心主张。
  - **判据**：删掉所有限定词后，如果论文的主张反而变清楚了 → 防御是多余的 → AI 味 +1。

### B2. 车轱辘话复读（跨章节原样重复）⭐
- [ ] **信号**：**完全一模一样的一整句话**在 Introduction 和 Methodology（或 Experiments）里各出现一次；
      或同一段落反复用不同说法讲同一个意思。
- **证据**：`贴出重复的两句原文 + 各自所在章节`
- **为什么**："完全相同的一句话我能在 introduction 和 methodology 里见到两遍"。这是 AI 生成时上下文复用的典型痕迹。
- **自动化提示**：可用 n-gram / sentence embedding 相似度扫描跨章节重复（见 SKILL workflow）。

### B3. 信息密度极低
- [ ] **信号**：一大段绕来绕去只讲一个意思；正确的废话多，看不到作者自己的思考/观点。
- **证据**：`摘录低密度长段`
- **为什么**："信息密度极低……全是正确的废话，看不到作者思考痕迹。"



## §C. 实验与数据汇报层

### C1. 数据汇报混乱，格式随心所欲 ⭐
- [ ] **信号**：同一篇里小数位不统一（有的通篇 6 位小数）；表格格式前后不一致；单位缺失。
- **证据**：`指出格式不一致的具体表/段`
- **为什么**："通篇保留六位小数""数据格式完全不统一"。

### C2. raw data 直接怼进正文 ⭐
- [ ] **信号**：confidence interval、p-value 等 raw statistics 直接写在正文段落里，而不是放进表格 / appendix。
- **证据**：`摘录正文里的 CI/p-value 句`
- **为什么**："CI、p-value 这种 raw data 连个表格或 appendix 都懒得塞，直接硬怼进正文"。

### C3. 消融不完整 → overclaim
- [ ] **信号**：Method 设计了 N 个模块，但消融只测其中几个，其余连提都不提却仍下整体结论。
- **证据**：`列出声称的模块 vs 实际做消融的模块`
- **为什么**："Method 写了 8 个子章节占 3 页半……消融只做了其中 3 个模块 → overclaim"。

### C4. baseline 单薄 / 陈旧
- [ ] **信号**：baseline 只有一个 base model；或用 2023/2024 的老模型当对手刷三年。
- **证据**：`列出 baseline 列表及年份`

### C5. 写成未加工实验日志 ⭐
- [ ] **信号**：六七个实验，大半结论都是 "we cannot draw any robust conclusion from these results"；有效信息为零。
- **证据**：`统计 inconclusive 实验占比`
- **反例（关键区分）**：诚实报告 negative results 是好事 ✅；问题是**通篇**都 inconclusive、堆砌无主次 ❌。



## §D. 结构与篇幅层

### D1. 硬凑页数的痕迹 ⭐
- [ ] **信号**：正文大片留白 / 内容单薄，却靠以下方式凑够页数：
      - Related Work 被疯狂拉长（与本文关系不大的文献也塞进来）
      - 塞几个**巨型大图**占版面
      - 超长一段 Limitation
- **证据**：`指出哪个 section 异常膨胀、哪张图异常大`
- **为什么**："肚子里没货导致正文留白，全靠拉长 Related Work + 巨型大图 + 老长 Limitation 才勉强凑齐页数"。

### D2. AI 过度设计（子章节爆炸）
- [ ] **信号**：Method 拆成过多子章节（如 8 个）占了大半篇幅，但每个都没实质内容。
- **证据**：`列出 Method 子章节数及占比`


## §E. 作者态度 / 诚信层（"根本没看一眼"）

### E1. AI 生成后未人工检查，痕迹没删干净
- [ ] **信号**：正文/补充材料留着工具水印或占位符（如 "DeepScientist"、"NEEDS REAL VALUE"、TODO）。
- **证据**：`贴出残留痕迹原文/图`
- **为什么**："好歹 auto research 完自己看一眼啊。"

### E2. 疑似拿老文章用 AI 洗稿
- [ ] **信号**：supplementary 用了别的会议模板、年份是 201X、内容几乎不变。
- **证据**：`指出模板/年份矛盾`

---

## 快速量化指标（可选自动化）
| 指标 | 计算方式 | 阈值提示 |
|------|---------|---------|
| Hedging density | (may/might/could/worth noting/to some extent...) 次数 ÷ 段落数 | >3/段 → 红灯 |
| Cross-section duplication | sentence embedding 相似度>0.9 且跨不同章节的句子对数量 | ≥1 → B2 命中 |
| Inconclusive ratio | "cannot draw robust conclusion"-类结论数 ÷ 实验总数 | >50% → C5 命中 |
| Decimal inconsistency | 同一表格内小数位种类数 | >1 → C1 命中 |
| Raw-stat-in-body | 正文（非表格）出现的 CI/p-value 句数 | ≥3 → C2 命中 |
| Section bloat | Related Work / Limitation 字数占比 vs 同类论文中位数 | 显著偏高 → D1 命中 |
