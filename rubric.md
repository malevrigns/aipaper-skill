# Scoring Rubric（AI 论文审查评分量表）

> 基于 `checklists/ai_flavor.md` 和 `checklists/figure_standards.md` 的命中项打分。
> 原则：**每条命中必须有原文证据**，无证据不计分。区分"好严谨"与"防御性废话"。

---

## 一、AI-Flavor Score（0–10，越高越像 AI 写的）
按命中的症状加权累加（封顶 10）。权重体现"审稿人抓狂程度"：

| 组 | 项目 | 单项权重 |
|----|------|---------|
| A | A1 无主线 / A2 缺动机 / A3 术语堆砌 | 各 1.5 |
| B | **B1 过度防御 ⭐** / **B2 跨章节复读 ⭐** / B3 低信息密度 | B1=2, B2=2, B3=1 |
| C | C1 数据格式混乱 / C2 raw data 进正文 / C3 overclaim / C4 baseline弱 / **C5 实验日志化 ⭐** | 各 1.5（C5=2） |
| D | D1 凑页数 / D2 AI过度设计 | 各 1.5 |
| E | E1 工具痕迹残留 / E2 疑似洗稿 | E1=3（硬信号）, E2=2 |

### 计分规则
- 单项命中即加对应权重；同一症状在多处出现只计一次。
- **E1（图里留 DeepScientist 等水印）** 是硬信号：单独出现即可让总分 ≥6。
- **B2（Intro 和 Method 原样重复整句）** 是高置信信号：单独 ≥4。

### Verdict 映射
| AI-Flavor Score | Verdict |
|-----------------|---------|
| 0–2 | Likely human（可能有轻微 AI 辅助润色） |
| 3–5 | Mixed（明显 AI 辅助，需人工核对主线与实验） |
| 6–8 | Likely AIGC（建议重点核查 motivation、消融完整性、数据规范） |
| 9–10 | Very likely raw-AutoResearch（作者可能未充分检查，考虑 desk reject 理由） |



## 二、Figure Standards Score（0–10，越低越不规范）
从满分 10 起扣，命中即扣分：

| 组 | 项目 | 扣分 |
|----|------|------|
| F | F1 无主框架图 / F2 框架混乱 / F3 巨型低密度 | F1=-3, F2=-1.5, F3=-1 |
| R | R1 缺轴/单位 / R2 legend问题 / R3 误差棒或raw stat / R4 模糊 / R5 风格不一 | 各 -1.5（R4/R5 各 -1） |
| G | **G1 工具水印残留 ⭐** / G2 拼凑感 / G3 图文不符 / G4 过度装饰 | G1=-3, G2=-1.5, G3=-2, G4=-1 |

- 最低 0 分。G1（留水印）是硬信号，单独出现 → ≤7。

### Figure Verdict
| Score | Verdict |
|-------|---------|
| 8–10 | Figures meet academic standards |
| 5–7 | Minor issues（列出需修的点） |
| <5 | Figures below standard（框架图/结果图/AI痕迹需重点整改） |

---

## 三、Overall Verdict（综合结论）
取 AI-Flavor 与 Figure 两维的较高风险档：
```
Overall = max(AI-flavor verdict severity, Figure verdict severity)
```
输出时必须给出：**一句话结论 + Top-3 最严重问题（带证据）+ 可执行修改建议**。

## 四、打分示例（示意）
某 AAAI paper：B1 过度防御(2) + B2 Intro/Method重复整句(2) + C5 六实验五inconclusive(2) + D1 靠Related Work+大图凑页(1.5) = **AI-Flavor 7.5 → Likely AIGC**。
Figure：F1 无主框架图(-3) + G1 图里留"DeepScientist"(-3) + R4 模糊(-1) = **3 → Below standard**。
→ Overall: **Likely AIGC, figures below standard**；Top-3：①跨章节复读整句 ②大半实验 inconclusive ③图留工具水印。

