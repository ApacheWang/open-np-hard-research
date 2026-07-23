# Open NP-Hard Research

> 本页是中文翻译；技术规则以 [English README](README.md) 及其所链接的英文规范为准。

一个面向 NP-困难问题的开放、全球化、严谨且可复现的研究实验室。

> 本项目尚未解决 P versus NP 问题。有限实验仅是关于已测试实例的证据；
> 它们不是关于无约束复杂性结论的证明。

## 入门

请阅读[路线图](ROADMAP.md)、[贡献指南](CONTRIBUTING.md)和[研究主张级别](docs/CLAIM_LEVELS.md)。最初的共同基础是[3-SAT 定义](foundations/3-sat.md)。

## 初始重点：3-SAT

我们的首个研究方向是建立可信、可复现的 3-SAT 基线：精确定义、参考求解器、小实例检查、文献梳理及可审查的假设。当工作范围和证据被精确说明时，我们欢迎精确算法、参数化算法、近似算法及启发式算法方面的工作。

## 贡献方式

新贡献者可以复现实验、添加测试、搜索反例、完善参考文献或翻译文档。请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)，了解新手路径和研究主张要求。

## 研究主张级别

主张从非正式想法到已发表工作均有标签，以便其审查状态可见。标签描述审查进展，而非数学真伪。规范定义见 [docs/CLAIM_LEVELS.md](docs/CLAIM_LEVELS.md)。

## 仓库地图

- [foundations/](foundations/) 存放定义、记号和阅读路径。
- [hypotheses/](hypotheses/) 存放精确且可证伪的猜想。
- [proofs/](proofs/) 存放可审查的证明草稿及其依赖关系。
- [experiments/](experiments/) 存放可执行、可复现的研究。
- [reductions/](reductions/) 存放明确的归约及其检查。
- [benchmarks/](benchmarks/) 存放带有来源信息的实例。
- [negative-results/](negative-results/) 保存被反驳的主张和失败路线。

## 可复现性

计算结果必须说明代码版本、命令、依赖项、数据来源，以及适用时的确定性随机种子。来自有限域的结果必须保留其有限域限制。

## 语言与翻译

英语是规范技术语言。欢迎社区维护翻译；可从[中文介绍](README.zh-CN.md)开始，并请将译文链接到其英文来源。

## 治理与行为准则

审查与决策规则见 [GOVERNANCE.md](GOVERNANCE.md)。所有参与者必须遵守[行为准则](CODE_OF_CONDUCT.md)。

## 许可与引用

代码采用 [Apache License 2.0](LICENSE-CODE) 许可。原创研究笔记、图表和文档采用 [CC BY 4.0](LICENSE-RESEARCH) 许可。归属信息见 [CITATION.cff](CITATION.cff)。
