# RAG Agent 关键知识分享大纲

## 幻灯片 1: 封面
- **标题**: RAG Agent 核心架构与实战指南
- **副标题**: 赋予大模型外部记忆与行动能力
- **分享人**: Jason
- **日期**: [演讲日期]

## 幻灯片 2: 什么是 RAG Agent？
- **概念对比**:
  - LLM（大脑，存在知识盲区和幻觉）
  - RAG（大脑 + 搜索引擎/知识库，提供事实依据）
  - RAG Agent（大脑 + 知识库 + 工具/四肢，能自主规划和执行操作）
- **核心价值**: 解决信息滞后、幻觉问题，实现复杂任务的自动化处理。

## 幻灯片 3: RAG 的核心链路 (Retrieval-Augmented Generation)
- **Indexing (索引阶段)**: 文档解析 -> 切块 (Chunking) -> 向量化 (Embedding) -> 向量数据库。
- **Retrieval (检索阶段)**: 用户 Query -> Query 向量化 -> 相似度计算 (Top-K 检索)。
- **Generation (生成阶段)**: Prompt 组装 (Context + Query) -> LLM 生成回答。
- *图示: RAG 经典三步曲流程图。*

## 幻灯片 4: 进阶检索技巧 (Advanced RAG)
- **痛点**: 简单 Top-K 检索往往匹配不到核心意图。
- **解决方案**:
  - **Query 重写 (Query Rewriting / HyDE)**: 扩展用户原始提问。
  - **混合检索 (Hybrid Search)**: 向量检索 (Semantic) + 关键词检索 (BM25)。
  - **重排序 (Reranking)**: 引入专门的 Reranker 模型二次打分，提高 Top-K 的相关性。

## 幻灯片 5: 从 RAG 到 Agent (引入 Tool Calling)
- **Agent 的定义**: 感知 (Perception) -> 大脑 (Brain/LLM) -> 记忆 (Memory) -> 行动 (Action/Tools)。
- **Tool Calling (函数调用)**: LLM 根据 RAG 检索到的缺失信息，决定是否需要调用外部工具（例如：API 查询、数据库查询、Web 搜索）。
- **Router 机制**: 动态判断当前 Query 是直接回答，还是要走 RAG，还是需要调用外部工具链。

## 幻灯片 6: RAG Agent 典型架构与工作流
- **ReAct 框架 (Reason + Act)**:
  - `Thought`: 我需要查找 XXX 资料。
  - `Action`: 调用 Knowledge Base 检索工具。
  - `Observation`: 拿到检索结果。
  - `Thought`: 结合检索结果，我还需要 XXX。
- **Multi-Agent 协作**: Retriever Agent 负责找资料，Summarizer Agent 负责总结，Reviewer Agent 负责防幻觉。

## 幻灯片 7: 评估与挑战 (Evaluation)
- **如何评估 RAG 的好坏**:
  - 检索指标 (Context Relevance): 查得准不准？
  - 生成指标 (Faithfulness / Answer Relevance): 答得对不对？有没有幻觉？
  - *参考框架: Ragas, TruLens。*
- **面临的挑战**:
  - 数据隐私与权限控制。
  - 多轮对话中的 Context 长度灾难与遗忘。

## 幻灯片 8: 总结与展望
- RAG 是企业级 LLM 落地不可或缺的基石。
- Agent 化是 RAG 的演进方向，从被动回答变为主动解决问题。
- Q&A 互动环节。
