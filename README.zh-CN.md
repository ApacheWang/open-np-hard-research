# Open NP-Hard Research

[English](README.md) | **简体中文**

> 本页为简体中文译文。记录的源文档为 [README.md](README.md)，源版本为公开
> `main` 上的[准确提交](https://github.com/ApacheWang/open-np-hard-research/commit/884194b7ff6ec2ce1845feccd690de70f727014c)
> `884194b7ff6ec2ce1845feccd690de70f727014c`。若译文与记录的源版本不同，以该源版本
> 作为核对基准；翻译问题通过公开、可审查的变更修正。

本项目围绕 NP-困难问题开展公开协作。工作通过明确的定义、可复现实验、可审查
的主张和有记录的责任分工进行组织。

项目面向所有贡献者开放；参与、审查与成果署名不因所在地、使用语言、所属机构、个人背景或经验水平而改变。
贡献依据其有记录的内容与证据接受评估。

> 本项目尚未解决 P versus NP 问题。有限实验仅是关于已测试实例的证据；
> 它们不是关于无约束复杂性结论的证明。

## 入门

请阅读[路线图](ROADMAP.md)、[贡献指南](CONTRIBUTING.md)和[研究主张级别](docs/CLAIM_LEVELS.md)。最初的共同基础是[3-SAT 定义](foundations/3-sat.md)。

## 初始重点：3-SAT

我们的首个研究方向是建立有文档记录、可审查且可复现的 3-SAT 基线：精确定义、
参考求解器、小实例检查、文献梳理及可审查的假设。当工作范围和证据被精确说明时，
我们欢迎精确算法、参数化算法、近似算法及启发式算法方面的工作。

## 贡献方式

新贡献者可以复现实验、添加测试、搜索反例、完善参考文献或翻译文档。请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)，了解新手路径和研究主张要求。

## 研究主张级别

主张从非正式想法到已发表工作均有标签，以便其审查状态可见。标签描述审查进展，而非数学真伪。规范定义见 [docs/CLAIM_LEVELS.md](docs/CLAIM_LEVELS.md)。

## 数学成果署名

数学成果的功劳归于作出有记录的实质数学贡献、认可最终形式化陈述和证明版本，
并对其负责部分承担责任的贡献者。仓库所有权、项目发起、维护、资助或一般参与，
不会自动带来“问题解决者”或定理作者身份。当实质数学贡献无法可靠分割时，成果
必须归于针对该成果公开记录的协作团队，而不是仓库全体参与者。上述贡献均按实际角色记录并致谢。
完整规则见 [GOVERNANCE.md](GOVERNANCE.md)。

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

每份译文都记录源文档和准确的源提交。译文不同步时，以该记录的源版本作为核对
基准；源文档所用语言不影响参与、审查或成果署名。现有译文及同步状态见
[翻译索引](translations/README.md)。

## 治理与行为准则

审查与决策规则见 [GOVERNANCE.md](GOVERNANCE.md)。所有参与者必须遵守[行为准则](CODE_OF_CONDUCT.md)。

## 许可与引用

代码采用 [Apache License 2.0](LICENSE-CODE) 许可。原创研究笔记、图表和文档采用 [CC BY 4.0](LICENSE-RESEARCH) 许可。归属信息见 [CITATION.cff](CITATION.cff)。
