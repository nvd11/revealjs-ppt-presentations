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

## 幻灯片 2.5: 为什么需要 RAG？大模型的局限与破局
- **痛点演示: 当大模型遇到“私有知识”**
  - **Prompt**: `请问 Jacky 有多少个女儿？`
  - **LLM 回答**: 表示无法解答，因为世界上有很多叫 Jacky 的人，没有足够的上下文信息。
  - **解析**: 用一个代码例子表明，大模型需要常识类知识丰富，但是无法解答特定方面（私有领域）的问题。

- **破局演示: 赋予大模型“上下文” (RAG 本质)**
  - **System Prompt 构建**: `Jacky 一共有 4 个孩子，其中 2 个是男孩。`
  - **结合提问**: 将用户问题 `请问 Jacky 有多少个女儿？` 结合 System Prompt 一起发给 LLM。
  - **LLM 回答**: 这次 LLM 轻松且精准地回答了这个问题。
  - **解析**: 所谓 RAG，就是把上下文结合问题一起让 LLM 基于上下文回答问题。

- **引出下文**: 至于如何获得这个相关的上下文，后面的 Slide 会详细讲解。

## 幻灯片 3: 解构 RAG - 核心组件 Retriever 与 Generator
- **代码拆解 (回顾 Slide 2.5)**: *[动画步进 1: 出现拆解说明]*
  - 可以将刚才 Demo 的代码分割为两部分核心动作：
    1. **Retriever (检索器)**: 负责获取私有上下文 `Jacky 一共有 4 个孩子，其中 2 个是男孩` (虽然上一个 Demo 是 hardcode，但在真实场景中，这就是 Retriever 的角色)。
    2. **Generator (生成器)**: 负责将检索到的上下文与用户 Query 结合，让 LLM 进行推理并生成答案。
- **企业级抽象化**: *[动画步进 2: 出现抽象化说明]*
  - Retriever 和 Generator 就是 RAG (Retrieval-Augmented Generation) 的两大灵魂组件。
  - 在企业级 RAG Agent 的架构中，这两个组件会被高度抽象化、封装化，以对接庞大的向量数据库和多种大模型。
- **抽象化代码示例**: *[动画步进 3: 渐显代码块]*
  ```python
  # 1. 实例化检索器 (连接到企业向量数据库)
  retriever = VectorStoreRetriever(db_connection)
  
  # 2. 实例化生成器 (包含 LLM 引擎和 Prompt 策略)
  generator = AnswerGenerator(llm_engine)
  
  # 3. 核心 RAG Pipeline
  query = "请问 Jacky 有多少个女儿？"
  context = retriever.retrieve(query)        # 检索阶段
  answer = generator.generate(query, context) # 生成阶段
  ```

## 幻灯片 4: 知识库构建与 Retriever 的“羁绊” (OOP 视角)
- **核心观点**: *[动画步进 1: 抛出核心结论与基类]*
  - **知识库的形态，决定了 Retriever 的实现方式**。在企业级开发中，我们会定义一个统一的 `BaseRetriever` 抽象接口，而底层存数据的方式决定了我们要写什么样的子类去实现它。
  - **定义抽象基类**:
    ```python
    from abc import ABC, abstractmethod

    class BaseRetriever(ABC):
        @abstractmethod
        def retrieve(self, query: str) -> str:
            pass # 强制所有子类必须实现 retrieve 方法
    ```
- **形态 1: 文本文件 (Text File)** *[动画步进 2: 出现形态1及子类实现]*
  - 如果私有知识是以纯文本文件构建的，Retriever 子类就必须实现**读取磁盘文件**的逻辑。
  - **子类实现**:
    ```python
    class FileRetriever(BaseRetriever):
        def __init__(self, file_path: str):
            self.file_path = file_path

        def retrieve(self, query: str) -> str:
            # 读取本地磁盘文件内容作为上下文
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return extract_relevant_info(query, content)
    ```
- **形态 2: 关系型数据库 (RDBMS)** *[动画步进 3: 出现形态2及子类实现]*
  - 如果企业知识被结构化存入了 MySQL 等关系型数据库，Retriever 子类就必须包含**执行 SQL 甚至拼装查询**的逻辑。
  - **子类实现**:
    ```python
    class DatabaseRetriever(BaseRetriever):
        def __init__(self, db_connection):
            self.db_connection = db_connection

        def retrieve(self, query: str) -> str:
            # 连接数据库并执行 SQL 查询获取上下文
            cursor = self.db_connection.cursor()
            sql = "SELECT knowledge_text FROM rag_docs WHERE topic = %s"
            cursor.execute(sql, (query,))
            result = cursor.fetchone()
            return result[0] if result else ""
    ```
- **引出后续**: 基于多态，我们的 Generator 完全不需要关心底层是查文件还是查 DB。但如果面对海量的非结构化文档（PDF、Word），磁盘扫文件太慢，SQL 匹配又不准，我们该怎么存？这就需要引入全新的检索形态——**向量数据库 (VectorDatabaseRetriever)**。

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
