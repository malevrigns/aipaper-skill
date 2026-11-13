# 修改前后案例

全部为演示构造的片段。数字、方法和结果只在案例中成立，不来自真实投稿，不能复制进论文作为证据。

## 1. 把限制写进主张

**修改前**

> It is worth noting that our method may potentially be useful in some cases. We do not claim universal effectiveness. These findings should be interpreted with caution.

**材料前提**：固定布局与车队规模下，吞吐量由每分钟 100 个任务升至 112 个。其他设置尚未测试。打乱交通观测的对照无法区分收益是否来自观测信息。

**修改后**

> In the fixed-layout, fixed-fleet evaluation, throughput rose from 100 to 112 tasks per minute. Transfer to other settings remains untested, and the shuffled-input control leaves the source of the gain unresolved.

改写先报告已观察到的收益，再交代尚未验证的适用范围与机制归因。真实限制仍然影响读者如何理解结果。

## 2. 引言与方法承担不同任务

**修改前**：两节都出现同一句。

> We use recent local traffic observations to adjust traversal costs during online planning.

**修改后**

引言：解释静态代价为什么无法反映短时拥堵，以及在线调整希望改善什么。

方法：给出输入窗口、更新时刻、代价计算和规划器调用关系。信息尚未提供时列为作者需补充项，不替作者设计新算法。

改变：第二次出现真正增加实现信息，单纯换同义词仍是复读。

## 3. 先解释变化，再给必要数字

**修改前**

> Baseline throughput was 100.000000 tasks/min. Our method achieved 112.000000 tasks/min. The runtime was 8.700000 ms. The baseline runtime was 8.200000 ms.

**修改后**

> In this setting, throughput increased from 100 to 112 tasks/min (+12%), while planning time rose from 8.2 to 8.7 ms (+0.5 ms).

改变：保留同一批数值，解释收益与代价，删除无意义尾零。本例未提供独立重复，不能补写显著性或 CI。

## 4. 关键置信区间可以在正文

**已提供的案例结果**：准确率差为 2.1 个百分点，95% CI 为 [0.4, 3.8]，计算方法和独立重复已在实验设置中交代。

**可保留的写法**

> Accuracy increased by 2.1 percentage points (95% CI [0.4, 3.8]) in this setting.

这里不用为了“去 AI 味”把不确定性赶到附录，也不应把百分点改成相对百分比。

## 5. 不确定结果要改变结论

**修改前**

> The shuffled-input control produced mixed results. We cannot draw robust conclusions. Our method effectively exploits the information in the shared trace.

**材料前提**：真实 trace 和打乱 trace 的结果尚不能区分。

**修改后**

> The current comparison does not distinguish the true trace from the shuffled input. It therefore does not establish that the gain comes from trace information; that attribution remains unresolved.

改变：保留核心反证，撤回无证据的机制归因。不能只删第一句让故事更顺。

## 6. 把“实验很多”变成问题明确

**修改前**：按运行顺序写 Experiment 1–7，每节末尾重复“结果仍需进一步研究”。

**修改后**：按主要效果、关键机制、适用范围组织。说明哪些结果有区分力、哪些仍不确定；重复探索的配置和日志放附录并保留正文引用。

改变：按实验功能组织，不按结果正负筛选。中心主张缺证据时明确记录，结构调整不能替代补证据。

## 7. 说清比较对象和结果

**修改前**

> Under the condition in which the layout and fleet size were held constant, the implementation of the proposed planner was associated with the observation of a throughput increase from 100 to 112 tasks per minute relative to the baseline, alongside an increase from 8.2 to 8.7 ms in the time required for planning.

**修改后**

> With layout and fleet size held fixed, throughput was 112 tasks per minute with the proposed planner and 100 with the baseline. Planning time was 8.7 ms with the proposed planner and 8.2 ms with the baseline.

第一句交代比较条件、对象和主要结果，第二句交代代价。保留了原来的数值和单位，结论仍限于这次比较。
