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

## 幻灯片 5: 语义的降维打击 —— 向量化 (Vectorization) 与 Embedding
- **文本查询的局限性**: *[动画步进 1: 举例说明痛点]*
  - 传统的关键字匹配（如 SQL 的 `LIKE` 或 Elasticsearch 的 TF-IDF）很难理解**语义相近**的词。
  - **例子**: 假设问题是 `“查询苹果的营养价值”`，而知识库里只有 `“雪梨”` 和 `“米饭”` 的数据。
  - **痛点**: 在字面上，“苹果”与“雪梨”、“米饭”完全不包含相同的字。传统的文本比较无法判断“苹果”和“雪梨”在语义上属于同类（水果），从而导致检索失败。
- **引入向量化 (Vectorization)**: *[动画步进 2: 概念与图例]*
  - **什么是向量化？**: 将人类理解的自然语言（词语、句子、段落）转换为计算机能理解的**高维浮点数数组**（如 768 维、1536 维的向量）。
  - **高维空间的距离**: 在这个高维空间中，语义相近的词（苹果、雪梨）距离会非常近，而语义无关的词（苹果、米饭）距离会很远。
  - **[预留图例占位符]**: *（插入一张 3D 坐标系图，展示 Apple 和 Pear 聚集在一起，而 Rice 离得较远的散点图）*
- **什么是 Embedding 模型？**: *[动画步进 3: Embedding 介绍与常见模型]*
  - **概念**: 专门用来执行“向量化”动作的 AI 模型就叫 Embedding Model。它负责把文本编码成带有语义坐标的向量。
  - **常见模型**: OpenAI `text-embedding-3-small/large`，开源的 `BGE-M3` (智源)，`Nomic-embed-text` 等。
- **抽象化代码示例 (OOP 延续)**: *[动画步进 4: 代码展示]*
  ```python
  from abc import ABC, abstractmethod

  # 定义 Embedding 的抽象基类
  class BaseEmbedder(ABC):
      @abstractmethod
      def embed_text(self, text: str) -> list[float]:
          pass

  # 具体实现子类：调用 OpenAI 的 Embedding 服务
  class OpenAIEmbedder(BaseEmbedder):
      def embed_text(self, text: str) -> list[float]:
          # 返回类似 [-0.012, 0.045, 0.111, ...] 的高维数组
          return openai_client.embeddings.create(input=text, model="text-embedding-3-small").data[0].embedding
  ```

## 幻灯片 6: 知识库的碎片化加工 —— Chunking (分块) 的艺术
- **为何需要 Chunking？**: *[动画步进 1: 逐条展示痛点与案例]*
  - **痛点 1: 文档粒度过大**。知识库导入通常以“整篇文档”（如 100 页的《员工手册》PDF）为单位。
  - **痛点 2: 上下文噪音与 Token 限制**。
    - *例子*: 假设用户提问 `“带薪年假有几天？”`。如果我们把整本 100 页的员工手册塞给大模型，由于里面还包含了“病假、产假、报销、考勤”等大量无关内容，不仅可能直接撑爆大模型的 Token 上限，还会产生严重的上下文噪音，导致 LLM 混淆各类假期的规定（幻觉）。
  - **痛点 3: 溯源与相关度 (Top-K) 的要求**。企业级 RAG 的输出不能只有光秃秃的答案，必须带有参考出处。
    - *输出示例*: `回答：您的带薪年假有 5 天。 [参考来源: 《员工手册》第12页第3段] (相关度: 0.95)`。
    - *结论*: 只有将文档切分成细粒度的段落 (Chunk)，我们才能在海量内容中只把最相关的几个小片段 (Top-K) 召回给 LLM。
- **如何 Chunking？及 Overlap 的重要性**: *[动画步进 2: 常见策略]*
  - **常见方法**: 按固定字符长度 (Character)、按 Token 数量、按文档语义结构 (如 Markdown 标题/段落)。
  - **重叠度 (Overlap)**: 为了防止一个完整的长句被无情地一刀劈成两半（导致语义断层），相邻的 Chunk 之间会保留一定比例的重叠量（例如 `Chunk Size=500, Overlap=50`），保证上下文连贯。
- **处理流程与 OOP 代码演示**: *[动画步进 3: 先切分，后 Embedding 的流水线]*
  - **核心流程**: 整篇 Document -> 切分为 N 个 Chunk -> 对每一个 Chunk 单独进行 Embedding 向量化。
  - **代码示例 (抽象化)**:
    ```python
    from abc import ABC, abstractmethod

    # 1. 定义抽象切分器
    class BaseSplitter(ABC):
        @abstractmethod
        def split_document(self, document_text: str) -> list[str]:
            pass

    # 2. 具体子类：带 Overlap 的递归文本切分器
    class RecursiveTextSplitter(BaseSplitter):
        def __init__(self, chunk_size=500, overlap=50):
            self.chunk_size = chunk_size
            self.overlap = overlap
            
        def split_document(self, document_text: str) -> list[str]:
            # 执行带重叠的分块逻辑...
            return ["chunk_1", "chunk_2", "chunk_3"] # 返回切分后的文本片段

    # 3. 知识入库预处理 Pipeline (结合前一页的 Embedder)
    splitter = RecursiveTextSplitter()
    embedder = OpenAIEmbedder() # 复用上一页讲解的 Embedder

    chunks = splitter.split_document(full_pdf_text)
    # 对每一个 Chunk 单独做向量化
    chunk_embeddings = [embedder.embed_text(chunk) for chunk in chunks] 
    ```
- **引出下文**: *[动画步进 4: 过渡]* 切好的成千上万个 Chunk 和它们对应的长长的高维向量（Embedding），该存在哪里？下一页，我们将揭开 **VectorDB（向量数据库）** 的神秘面纱，并剖析常见的知识库表结构。

## 幻灯片 7: 向量数据库 (Vector DB) 与知识库表结构设计
- **什么是 Vector DB？及其常见选型**: *[动画步进 1: 概念与产品]*
  - **概念**: 专门为存储、管理和快速检索（相似度计算，如余弦相似度）高维向量数据而优化的数据库。
  - **常见选型**: `PostgreSQL` (配合 `pgvector` 扩展，最推荐的企业级方案)、Google `AlloyDB`、`BigQuery` 向量检索，以及专用的 Milvus / Pinecone 等。
- **核心表结构 1: `document_chunks` (存放知识碎片的仓库)**: *[动画步进 2: 重点字段解析]*
  - 这张表用来存放我们上一页切分好的数据。核心字段包含：`id`, `doc_id`, `content` (TEXT), `embedding` (VECTOR)。
  - **核心问题探讨: 为什么存了 Vector 还要存 `content` 原文本？**
    - *解释*: 向量 (`embedding`) 只在 **Retriever (检索)** 阶段发挥作用，用于通过空间距离计算出 Top-K。但 LLM (大模型) 读不懂向量数组！所以在 **Generator (生成)** 阶段，我们必须把查出来的对应的原文本 (`content`) 喂给 LLM，让它做“开卷考试”式的阅读理解。
- **核心表结构 2: `document_topics` (元数据与主题分类)**: *[动画步进 3: 引入 Topic 与混合检索]*
  - **表作用**: 记录文档属于哪个 Topic (例如：'credit_risk' 信用风险, 'retail_banking' 零售业务)。
  - **为何要用 Topic 分类？(Metadata Pre-filtering 混合检索)**:
    - *痛点*: 如果不分类，面对海量混合文档进行全局向量检索，既耗时又容易“跨界张冠李戴”。
    - *通俗案例*: 假设企业的知识库里同时存了 **《中餐食谱》** 和 **《洗衣机维修手册》**。当用户提问 `“怎么炖排骨汤最好喝？”` 时，如果不做分类，系统会在全库里算向量距离。但如果有了 Topic 分类，系统就可以先用 SQL 的 `WHERE topic = '食谱'`，把洗衣机说明书瞬间过滤掉。
    - *收益*: 这样一来，向量计算只在“食谱”这个小池子里进行。不仅检索速度起飞，还彻底杜绝了模型从“洗衣机说明书”里找炖排骨答案的荒唐幻觉。
- **SQL 实战演示 (Topic 过滤 + 向量检索)**: *[动画步进 4: 展现混合检索代码]*
  ```sql
  -- 这是一个典型的 Metadata Pre-filtering (混合检索) 语句
  SELECT 
      dc.content, 
      1 - (dc.embedding <=> '[0.11, 0.04, ...]') AS similarity_score
  FROM document_chunks dc
  -- 1. 先通过关联表精确过滤 Topic，大幅缩小扫描范围
  JOIN document_topics dt ON dc.doc_id = dt.doc_id
  JOIN topics t ON dt.topic_id = t.topic_id
  WHERE t.topic_name = 'credit_risk' 
  -- 2. 然后在缩小的范围内，计算向量余弦相似度并取 Top 3
  ORDER BY dc.embedding <=> '[0.11, 0.04, ...]' 
  LIMIT 3;
  ```

## 幻灯片 8: 最后一块拼图 —— Generator (生成器) 与 Top-K 调优
- **什么是 Generator？**: *[动画步进 1: 概念引入]*
  - Retriever 已经通过 SQL + 向量计算把最相关的“知识碎片”找出来了。Generator 的任务就是把 **用户问题** 和 **检索出的上下文碎片** 拼装成提示词 (Prompt)，交给大模型 (LLM) 进行“开卷考试”。
- **代码与 Prompt 实战演示**: *[动画步进 2: 渐显组装逻辑]*
  ```python
  def generate_answer(user_query, retrieved_chunks):
      # 1. 组装 System Prompt (赋予大模型背景知识)
      prompt = "你是一个智能助手。请严格基于以下【参考资料】回答用户问题。严禁胡编乱造。\n\n"
      for i, chunk in enumerate(retrieved_chunks):
          prompt += f"[参考资料 {i+1}] (相关度: {chunk.score}): {chunk.content}\n"
      
      prompt += f"\n用户问题: {user_query}"
      
      # 2. 调用大模型 (LLM 参与)
      response = llm_client.chat(prompt)
      return response
  ```
- **带溯源的完美 Output 示例**: *[动画步进 3: 展示 LLM 的最终回答]*
  - **最终呈现给用户的效果**:
    > **🤖 回答:** 炖排骨汤的最佳时间是 1.5 到 2 小时，建议在最后 20 分钟加盐，这样肉质更鲜嫩。
    > 
    > **【参考来源】:**
    > - `[资料 1]` (相关度: 0.92): 《中餐食谱-汤类》第12页 - 炖排骨汤时长建议...
    > - `[资料 2]` (相关度: 0.88): 《中餐食谱-调味技巧》第5页 - 盐的添加时机...
    > - `[资料 3]` (相关度: 0.75): 《厨房常见问题》 - 肉类炖煮常识...
- **关键参数调优 —— Top-K (查几条？)**: *[动画步进 4: Top-K 权衡探讨]*
  - Retriever 到底该返回几个 Chunk (Top-K) 给 Generator 呢？这是 RAG 调优的重中之重！
  - **K 太小 (例如 K=1)**: 容易漏掉关键信息，导致 LLM 回答不完整 (Recall 低)。
  - **K 太大 (例如 K=20)**:
    1. 💸 **贵且慢**: 极大地增加 Token 消耗和推理延迟。
    2. 🚫 **超限**: 可能直接撑爆大模型的 Context Window (上下文窗口限制)。
    3. 😵 **Lost in the Middle (中间迷失效应)**: 塞给大模型的噪音太多，它反而抓不住重点，甚至忘了原本的问题。
  - **实战经验**: 企业级应用通常将 Top-K 设定在 **3 到 5** 之间，配合优质的 Chunking 策略达到最佳平衡。

## 幻灯片 9: RAG Agent 的核心调度与架构决策
- **Agent 的核心职责 (Orchestrator)**: *[动画步进 1: 概念引入]*
  - 前面我们把 Retriever 和 Generator 都造好了，现在需要一个大管家把它们串起来，这就是 RAG Agent。
  - 它负责暴露出对外的 `ask()` 接口，接收用户问题，调度底层组件，并打包最终的结构化响应。
- **架构决策: LCEL 链式 vs 命令式 (Imperative)**: *[动画步进 2: 架构对比与探讨]*
  - **业界流行 (纯 LCEL)**: 很多教程喜欢用一行代码串联全流程，例如 `chain = retriever | prompt | llm`。虽然代码短，但调试如同黑盒。
  - **企业级推荐 (命令式编排)**: 在真实项目中，我们强烈建议用**显式的 Python 代码进行调度**。
    - *优势*: 易于打断点调试、状态透明，最重要的是——**可以非常轻松地实现业务分支阻断 (Early Exit)**。
- **核心代码拆解 (动态讲解 `rag_agent.py`)**: *[动画步进 3: 展示代码与高光逻辑]*
  - *(配合 GitHub 源码讲解: src/agents/rag_agent.py)*
  - **依赖注入与多态 (OOP 巅峰展现)**: Agent 本身不关心底层是查 PG 还是查本地文件，也不关心用的是 Gemini 还是 GPT。一切由外部传入！
  ```python
  class RAGAgent:
      # 依赖注入 (Dependency Injection)：接收抽象基类，实现解耦
      def __init__(self, retriever: BaseRetriever, generator: ILLMGenerator):
          self.retriever = retriever
          self.generator = generator

      async def ask(self, question: str, top_k=3, topic_filters=None) -> RAGResponse:
          # 1. Retriever 阶段
          retrieved_contexts = await self.retriever.ainvoke(
              input=question, config={"top_k": top_k, "topic_filters": topic_filters}
          )
          
          # 💡 高光时刻: 提前阻断 (Early Exit) 预防幻觉并节省 API 成本
          if not retrieved_contexts:
              return RAGResponse(query=question, generated_answer="抱歉，知识库未找到相关内容。", retrieved_contexts=[])

          # 2. Generator 阶段 (仅在找到上下文时执行)
          answer = await self.generator.ainvoke({"context": retrieved_contexts, "question": question})
          return RAGResponse(query=question, generated_answer=answer, retrieved_contexts=retrieved_contexts)
          
  # =========================================
  # 外层调用示例：展现纯正的 OOP 组装之美
  # =========================================
  # 1. 实例化具体的 Retriever 和 Generator 子类
  my_retriever = PgVectorRetriever(db_conn)
  my_generator = GeminiGenerator(model_name="gemini-2.5-pro")

  # 2. 将它们注入给 RAGAgent (如果明天要换成 GPT-4，Agent 代码一行都不用改！)
  agent = RAGAgent(retriever=my_retriever, generator=my_generator)

  # 3. 发起业务调用
  result = await agent.ask(question="请问带薪年假怎么算？", topic_filters=["hr_policy"])
  ```

## 幻灯片 10: 评估与挑战 (Evaluation)
- **如何评估 RAG 的好坏**:
  - 检索指标 (Context Relevance): 查得准不准？
  - 生成指标 (Faithfulness / Answer Relevance): 答得对不对？有没有幻觉？
  - *参考框架: Ragas, TruLens。*
- **面临的挑战**:
  - 数据隐私与权限控制。
  - 多轮对话中的 Context 长度灾难与遗忘。

## 幻灯片 11: 总结与展望
- RAG 是企业级 LLM 落地不可或缺的基石。
- Agent 化是 RAG 的演进方向，从被动回答变为主动解决问题。
- Q&A 互动环节。
