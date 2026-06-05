---
title: "如何使用DeepSeek提高投研效率"
title_zh: 
type: source
summary: "本文系统梳理了以DeepSeek为代表的大语言模型（LLMs）在金融投研领域的应用框架与前景。文章不仅回顾了DeepSeek、GPT、BERT等通用大模型及BloombergGPT、FinBERT等金融大模型的发展脉络，还结合具体实例，详细探讨了LLMs在语言任务、情感分析、时序分析、金融推理及多智能体建模等五大金融场景中的落地潜力与挑战。"
tags: []
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
source_type: ""
source_language: ""
raw_path: "raw/articles/[202502240941]广发金工如何使用DeepSeek提高投研效率.md"
review_by: ""
raw_hash: "b7b93379398333e7b31c5ca9f72698ff055ddebde036dbde6cc77f3cbb281005"
---
## 核心内容

本文是一篇关于大语言模型（LLMs）在金融领域应用的深度综述。文章首先回顾了从统计语言模型、RNN到Transformer架构的演进，重点解析了DeepSeek系列模型（特别是基于强化学习和冷启动数据的DeepSeek-R1）的技术突破与低成本优势。随后，文章横向对比了GPT、BERT、T5、Llama等通用模型及其金融衍生模型（如BloombergGPT、FinBERT、FinLlama等）的特点。

## 关键发现

1. **DeepSeek-R1的技术突破**：通过群组相对策略优化（GRPO）和多阶段训练（冷启动+强化学习），DeepSeek-R1在数学和代码推理任务上媲美OpenAI o1，但训练成本极低。
2. **五大金融应用场景**：LLMs在金融领域的应用可归纳为语言任务（如年报总结、NER）、情感分析（如市场情绪监测）、时序分析（如股价预测）、金融推理（如资产配置建议）和基于代理的建模（如多智能体交易模拟）。
3. **多智能体系统（MAS）的崛起**：结合LLMs的MAS（如StockAgent、TradingGPT）能够模拟真实市场投资者的异质行为，为策略开发和市场微观结构研究提供新范式。
4. **面临的挑战**：数据污染、模型幻觉、信号衰减、回测中的未来函数以及可解释性不足是LLMs在金融落地中的主要障碍。

## 相关概念

- [[大语言模型]]
- [[深度学习]]
- [[强化学习]]
- [[注意力机制]]
- [[文本情感分析]]
- [[多智能体系统]]
- [[transformer模型]]
- [[多模态大语言模型]]

## 来源

- [[如何使用deepseek提高投研效率]]
