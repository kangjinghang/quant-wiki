---
title: "lightRAG"
title_zh: 
type: entity
summary: "一种轻量化、模块化的检索增强生成（RAG）开源框架，专为实际应用中的部署效率与易用性设计。"
tags: [大语言模型, 多智能体系统, 固收量化, 券商研报, 华泰固收-金工, 深度研究, python]
sources:
  - "[[债市研究智能体-prompt-与多agent协同]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
entity_type: ""
review_by: ""
---
## 简介

lightRAG是一种轻量化、模块化的[[检索增强生成-rag|RAG]]架构。相较于传统的RAG框架（如基于Faiss或Llama Index的方案），lightRAG摒弃了过重的工程依赖，强调"即插即用"的组合能力，是当前在[[多智能体系统]]架构中引入本地知识增强的理想选择之一。

## 特性与应用

- **精简高效**：通过轻量的代码结构降低了集成和维护的门槛，特别适合中小型企业或个人开发者，同时保留了RAG的核心机制。
- **无缝集成**：支持与现有Agent框架（如LangChain Agent或自定义[[多智能体系统]]）无缝衔接，可作为Agent的知识接口。
- **安全可控**：支持本地部署与私有知识库接入，保障数据安全，适合对隐私性或实时性有较高要求的金融投研场景。

## 来源

- [[债市研究智能体-prompt-与多agent协同]]
