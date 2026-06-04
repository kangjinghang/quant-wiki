![cover_image](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWeeAUcB6n8Y0ia3E4ibvtHOCjhmdu2nk55ibUDjIDib7cPP0z17rpz3f0rFGvia3QFpNtFs7s7iajlfDnmw/0?wx_fmt=jpeg)

#  【广发金工】从知识库到知识图谱：DeepSeek&GraphRAG

原创  安宁宁  安宁宁  [ 广发金融工程研究 ](javascript:void\(0\);)

_2025年02月26日 13:06_ __ _ _ _ _ _ 北京  _

在小说阅读器读本章

去阅读

** 广发证券首席金工分析师 安宁宁  **

** SAC: S0260512020003  **

anningning@gf.com.cn

** 广发证券资深金工分析师 陈原文  **

** SAC: S0260517080003  **

chenyuanwen@gf.com.cn

** 广发证券资深金工分析师 王小康  **

** ** SAC: S0260525020002  ** **

wangxiaokang@gf.com.cn

** 广发金工安宁宁陈原文团队  ** **摘要**

  

** DeepSeek部署与运行测试  ：  **
国内大模型公司“深度求索”开发的DeepSeek-V3和DeepSeek-R1引起了市场广泛关注，以极低的训练成本，实现了与GPT-4o等顶尖模型相媲美的性能。我们在本篇报告中详细介绍了如何使用Ollama这一开源框架快速在本地实现模型部署和调用，列举了不同参数版本模型和显卡硬件需求对应关系。简单测试了本地部署14B版本模型和满血版模型的回答效果差异。

** GraphRAG与大模型应用介绍  ： **
开源框架Langchain就集成了包括RAG和Agent功能作为LLM的外挂工具，提升大模型在专业垂直领域的回答水平。RAG能使大模型在生成回答时读取外部信息，即在外部数据库中检索出相关信息作为参考，经过思考后再进行回答。从而能有效减少模型幻觉，避免其在缺乏相关知识的情况下无中生有、胡乱做答，生成更精准的答案。但在过往的实际体验中，我们发现RAG的效果并未充分满足预期。主要在于其难以从全局考虑问题，将不同信息串联起来。
而GraphRAG的出现在一定程度上解决了以上问题，该框架通过构建基于实体的知识图谱和社区摘要来扩展RAG系统的能力，使其能够处理更广泛的用户问题和更大量的源文本。其主要优点在于：捕捉概念和实体之间的复杂关系，通过可视化的图结构增强可解释性等。
** 金融知识图谱与GraphRAG&DeepSeek实践  ： **
目前，市场上关于金融类GraphRAG的应用较少，而我们认为二级投研市场由于涉及大量的上市公司、产品、供应链、上下游产业链等实体和关系，是高效实现LLM+GraphRAG的绝佳应用场景。为此，我们使用目前在多个测评数据集上排名靠前的DeepSeek-R1模型作为LLM，使用微软开源版本的GraphRAG进行知识图谱的构建，探究其实际应用效果。

我们分别选择一篇来自传媒行业的游戏板块研究报告和一篇计算机行业的个股研究报告作为输入文本语料，通过公司的并购关系、投资逻辑梳理等问题测试，发现模型回答质量较高，关键信息点均能做到无误、不遗漏地呈现出来。此外，框架所生成社区报告、实体关系表等结构化数据也可以用于投研时后续的筛选、处理工作。

** 风险提示：  **
大语言模型基于上下文预测进行回答，不能保证回答准确性，由此可能产生误导影响用户判断。GraphRAG或RAG框架的回答质量同样很大程度取决于用户所输入文本语料的内容质量，若文本本身具有误导性或重要信息遗漏，可能对投资决策判断产生重要影响。市场若出现超出模型预期的变化，过往逻辑链条适用性下降可能会导致策略失效，需要动态对模型进行微调以修正偏差。

**一、DeepSeek部署与运行测试**

自2022年底OpenAI推出ChatGPT以来，国内外多家厂商开始自研各类大模型。由国内大模型公司“深度求索”开发的DeepSeek-V3和DeepSeek-R1引起了市场广泛关注，以极低的训练成本，实现了与GPT-4o等顶尖模型相媲美的性能。在本篇报告中，我们首先简要介绍模型的部署方法和简单测试对比，接下来以GraphRAG知识图谱的形式将模型更高效地应用在投研工作中。

**（一）各版本DeepSeek模型与部署所需硬件对应关系**

由于目前各个大模型的基座基本均为Transformer类的神经网络模型，在训练和推理时涉及大量的简单矩阵运算，而使用英伟达显卡搭配CUDA平台的方案几乎已经成为必选项。一般而言，部署模型所需显存主要用于保存模型权重、中间计算过程和一些高效处理过程中的额外开销。其对应关系存在如下规律：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VW3V087icNefSkUkHGYibVyMvpOhC66mH3sqljNtJyicxzpMlPTF9rAqtCg/640?wx_fmt=png&from=appmsg)

其中，M为所需显存（GB），P为模型参数量，4B为4bytes/parameter（考虑FP32或FP16），Q为模型参数精度（FP16即为16-bit,INT8即为8-bit），1.2为用于额外开销的膨胀系数。

举例而言，若模型参数量P=7B（700亿），Q为16位浮点精度，则可求得M=((7B*4)/(32/16))*1.2=14B*1.2=16.8GB。由此，其他各版本模型所需显存均可估算得到：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWib0sFcrHsuUYdPC2ZNLuIp5DqibxnclFVRHicxTHgexjaJXdQzwDJB8gA/640?wx_fmt=png&from=appmsg)

**（二）部署流程介绍**

DeepSeek模型由于已经开源，模型的参数可以在互联网公开下载。目前主流的本地化部署大模型的方式包括：（1）直接从HuggingFace下载模型文件，使用Transformers库通过代码形式进行调用，（2）Ollama和LM
Studio这种独立平台，仅使用命令行或UI界面快速部署并开放端口服务。

此处以使用范围更广的后者介绍：Ollama是一个发展较早的开源框架，安装运行比较简单，通过命令行形式可快速部署、微调各类大模型，适用于有一定技术基础的用户。而LM
Studio提供了更广泛的各类功能，更方便操作的UI界面，所提供模型更加广泛，但不开源。此处我们以更高效便捷的Ollama为例介绍DeepSeek模型的部署方式：

1\.  首先访问https://ollama.com/，并下载适合自己操作系统的终端。

2\. 在官网中点击Models，搜索需要的DeepSeek模型版本。

3\. 根据其命令提示，在cmd中直接输入命令即可，如：ollama run deepseek-r1:32b。

下载需要一段时间，完成后就已经可以本地进行大模型对话了。此外，Ollama在本地模型的默认端口为11434，若其他应用需要调用该模型，将访问请求的base_url改为http://localhost:11434/v1即可。

**（三）简单问答测试**

此处我们测试了若干逻辑问题，以探究本地部署的14B模型推理能力如何，与满血版DeepSeek-R1的差距几何？

第一个问题为：在一个黑暗的房间里，有三个开关，分别控制着房间外的三个灯泡。你站在房间里，不能看到灯泡，只能通过开关控制它们。你只能走一次出去检查灯泡，如何确定每个开关控制哪个灯泡？

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWSen2k3AQlOPywmOzJMwspXDV0tSooiabSU6QZ91bzlo7WjGNsD3AMSQ/640?wx_fmt=png&from=appmsg)

可以看出，14B版本模型也展现出了较强的推理能力，能快速、准确地给出思考逻辑和操作步骤。

不过在部分逻辑题的测试下，14B模型展现出了和满血版模型的差距。问题为：3,10,15,26，下一个数字为？

以下为14B模型的回答，由于逻辑链过长，此处仅展示最后部分答案：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWRZ4AibhpyAlUJxmK60kBXbWWNm5sss9Enhd494seUgwWLqVNic80l3Bw/640?wx_fmt=png&from=appmsg)

而对比网页中满血版DeepSeek-R1，可以看出，模型在对比了多种可能存在的规律后，快速给出了正确答案。说明在某些存在一定复杂逻辑推理的任务中，大参数量模型依然有其优势。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWJDuA9ibKYu3LUHciaLXdm1ahnv2AaGficC9t3vR4vFiarewWgbTFrYHFQw/640?wx_fmt=png&from=appmsg)

**二、GraphRAG与大模型应用介绍言模型简介**

**  
**

**（一）Langchain与RAG介绍**

除了直接通过对话形式向大模型提问，基于大模型开发各类外挂应用逐渐受到广泛认可。其中开源框架Langchain就集成了包括RAG和Agent功能作为LLM的外挂工具，提升大模型在专业垂直领域的回答水平。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWqwd3SP4E6TJnr0mZEu5dchFryegzZow02uI52W7sfMcAzq4gBiaVg2Q/640?wx_fmt=png&from=appmsg)

其中RAG（Retrieve-Augmented
Generation）的中文名是检索增强生成，能使大模型在生成回答时读取外部信息，即在外部数据库中检索出相关信息作为参考，经过思考后再进行回答。从而能有效减少模型幻觉，避免其在缺乏相关知识的情况下无中生有、胡乱做答，生成更精准的答案。

如上图中框架结构，用户在使用前需要先将本地各类文件格式进行读取并简单清洗处理，由于受到LLM最大输入token的限制，我们需要根据文本实际情况进行分段处理，得到向量化之后的数据后将其存入本地向量数据库。后续如有新增文本数据，仅需用同样Embedding模型向量化之后添加到向量数据库中即可。用户在针对某些文档相关问题进行提问时，Langchain会使用向量化之后的提问文本与向量数据库中的文本进行相似性搜索，得到相关性最高的K条文档后，将提问和匹配文档嵌入固定的提示模板中，最后对LLM提问得到回复结果。即检索、增强、生成三步：

1\. 检索（Retrieve）：把用户的问题送到知识库中进行检索相关内容，返回相似的前n个内容。

2\. 增强（Augment）：用户的问题和检索的内容放在一起，构成一个prompt。

3\. 生成（Generate）：将prompt送入LLM中。

Agent 是一种可以自主感知环境、做出决策并执行行动的智能体系统，可以“理解”用户设定的流程、规则后按自己的想法来处理一系列任务。

Agent通常基于大语言模型（LLM），创建者用提示词模板（Prompt
Template）来指定它的角色和工作内容；Agent拥有记忆（Memory）,从而不但可以记得会话的上下文，也可以记得用户的偏好和个性化要求，更好地满足用户的需求；同时，Agent拥有“行为自主性”（Action），它在接收指令后，可以通过大语言模型来判断是否需要使用相应的工具来自主完成任务。因此，Agent比较适用于自动化任务、数字助理、游戏角色等应用。

**（二）GraphRAG**

在过往的实际体验中，我们发现RAG的效果并未充分满足预期。在处理数据时，可能会出现数据切分错乱、清洗流程复杂。在进行相关性搜索时，由于RAG的文本索引都是基于文本块的，难以捕捉不同实体之间的复杂关系和层次结构，且只能检索固定数量的文本块，因此会出现最终回答质量不高的情况。其主要缺点可概括为：

1\. 难以从全局考虑问题，将不同信息串联起来。当一个问题涉及多方面多角度，需要将不同属性结合起来进行综合推断时，RAG很可能会遗漏一些关键信息。

2\.
当进行全局梳理时，RAG由于其工作原理，只能将相似度最高的文本块作为提示词喂入LLM，无法站在更高的视角回答问题。因此总结、归纳等任务也并非RAG的强项。

一个典型的场景为若用户提出问题：谁导演了一部科幻电影，且该电影的主角也出演了《荒野猎人》？

一个标准的RAG系统会检索关于《荒野猎人》的文本块，找出演职人员信息，但未能找到主角莱昂纳多出演的其他电影。而一个理想的情况应该是找出主角后，通过实体对应关系遍历其主演的所有电影，最终检索出某部科幻电影的导演。

而GraphRAG的出现在一定程度上解决了以上问题，该框架由微软开源，通过构建基于实体的知识图谱和社区摘要来扩展RAG系统的能力，使其能够处理更广泛的用户问题和更大量的源文本。而知识图谱就是通过互联的节点和实体捕捉知识，以结构化的形式表示关系和信息，这种信息存储和查询方式也更贴近我们一般的人脑思维习惯。相比于传统RAG，GraphRAG主要有以下特点：

1\. 增强知识表示：捕捉概念和实体之间的复杂关系。

2\. 可解释和可验证：图结构可以可视化，有助于得到结果时进行检查调试。

3\. 复杂推理：LLM集成能使GraphRAG更好理解用户查询，提供更相关和连贯的响应。

4\. 知识来源的灵活性：可以适应包括结构化数据、非结构化文本数据等。

此外，相比传统 RAG 方法，GraphRAG 对 Token 的需求显著降低，能够帮助开发者节省成本。例如，通过动态社区选择功能，GraphRAG
在改善全局搜索的同时，Token 成本减少了 77%。并且GraphRAG
支持增量索引和动态更新，能够在不重建整个索引的情况下快速整合新数据。这一特性使其特别适用于动态环境（如新闻或实时分析）。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWFsbTyXI4kh7hUDld4jEFt61gZMaWUhADGRA5OMCv00Mic5mwN1DVIgQ/640?wx_fmt=png&from=appmsg)

为实现以上目标，GraphRAG主要有如下流程：

1\. 文本单元切分：将输入文本切割为Text Units，每个Text Unit都是一个可分析的单元，用于提取关键信息。

2\. 实体和关系提取：使用大模型从Text Units中提取实体、关系和关键声明。

3\. 实体消解：对于代表同一实体但名称不同的节点，利用LLM将其合并。

4\. 图构建：构建知识图谱，使用 Leiden 算法进行实体的层次聚类。每个实体用节点表示，节点的大小和颜色分别代表实体的度数和所属社区。Leiden
算法是一种层次化聚类算法，能够高效地将图划分为多个社区，每个社区内的节点连接紧密，而社区间的连接较弱

5\. 社区总结：从下到上生成每个社区及其成员的总结，帮助全局理解数据集。

在构建完成知识图谱后，用户进行检索时，同样可以选择不同的检索方案：

1\. 全局搜索：当我们想了解整个语料库或数据集的整体概况时，GraphRAG
可以利用社区总结来快速推理和获取信息。这种方式适用于大范围问题，如某个主题的总体理解。

2\. 局部搜索：如果问题关注于某个特定的实体，GraphRAG 会向该实体的邻居（即相关实体）扩展搜索，以获得更详细和精准的答案。

3\. DRIFT搜索：这是对局部搜索的增强，除了获取邻居和相关概念，还引入了社区信息的上下文，从而提供更深入的推理和连接。

此外蚂蚁也基于GraphRAG框架构建了自己的系统DB-
GPT，蚂蚁构建GraphRAG通过LLM服务实现文档的三元组提取，写入图数据库；检索（子图召回）：通过LLM服务实现查询的关键词提取和泛化（大小写、别称、同义词等），并基于关键词实现子图遍历（DFS/BFS），搜索N跳以内的局部子图；生成（子图上下文）：将局部子图数据格式化为文本，作为上下文和问题一起提交给大模型处理。

基于此所构建的DB-
GPT是一个开源的AI原生数据应用开发框架，目的是构建大模型领域的基础设施，通过开发多模型管理(SMMF)、Text2SQL效果优化、RAG框架以及优化、Multi-
Agents框架协作、AWEL(智能体工作流编排)等多种技术能力，让围绕数据库构建大模型应用更简单，更方便。

目前GraphRAG在应用场景上已经拓宽到了金融、医疗、法律等领域。例如：

1\.
在学术研究领域，每一篇论文由一位或多位研究人员创作，并与某个研究领域相关联。作者隶属于机构，并且作者之间存在诸如合作或者共同的机构隶属关系等关联。这些元素能够构建为图的形式。在这个图上使用
GraphRAG 有助于学术探索，包括为作者预测潜在的合作者、识别特定领域内的趋势等等。

2\.
在法律情境中，案例与司法意见之间存在着广泛的引用关联，因为法官在做出新决策时常常参考以往的意见。这自然形成了一个结构化的图，其中节点代表意见、意见集群、案件记录和法院，边涵盖了诸如“意见引用”“意见集群”“集群案件记录”“案件记录法院”等关系。GraphRAG
在法律场景中的应用能够助力律师和法律研究人员完成各类任务，比如案例分析和法律咨询。

3\. 用户和产品之间的历史交互能够自然地形成一个图，它含蓄地封装了用户的行为模式和偏好信息。运用 GraphRAG
技术提取关键子图可以更好地解决电子商务平台数量的增多以及用户交互数据量的持续增长带来的问题。集成不同类型或具有不同参数的多个检索器以提取相关子图，随后对其进行编码以用于预测用户的时间行为。为了提升客户服务问答系统的模型性能，构建具有问题内和问题间关系的过去问题图。对于每一个给定的查询，检索类似过去问题的子图以提高系统的响应质量。

**三、金融知识图谱GraphRAG &DeepSeek实践 **

**  
**

目前，市场上关于金融类GraphRAG的应用较少，而我们认为二级投研市场由于涉及大量的上市公司、产品、供应链、上下游产业链等实体和关系，是高效实现LLM+GraphRAG的绝佳应用场景。为此，我们使用目前在多个测评数据集上排名靠前的DeepSeek-R1模型作为LLM，使用微软开源版本的GraphRAG进行知识图谱的构建，探究其实际应用效果。
**（一）金融知识图谱介绍**
金融知识图谱是一种以图结构表示金融领域知识的技术，通过节点和边展示金融实体及其关系。节点代表金融实体（如公司、产品、市场等），边则描述实体间的关联（如投资、交易、控股等）。它利用自然语言处理、数据挖掘等技术，从海量金融数据中提取信息，构建结构化的知识网络。可以用于以下多种用途：

1\.  风险控制：评估企业、个人的信用风险，识别实体之间的关联。

2\. 投资决策：分析企业、行业关系，发现潜在投资机会。

3\. 市场监管：实时监控市场动态，识别异常交易。

在Wang
etl(2021)中，构建了一个基于研报数据的中文金融知识图谱FP2KG。这个数据集来自于达观数据在CCKS2020（2020全国知识图谱与语义计算大会）所组织的金融研报知识图谱的自动化构建的评测任务。该FR2KG数据集有17,799实体，26,798关系三元组，1,328属性三元组，包括10个实体类型，19个关系类型和6种属性。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWbQtp4CYEHm0OWsp7JUC6IeyicNSst4cny6LVlUkzHEyBjyza9gCuxtQ/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWna0exzFTiczjbohnALibpkIbLskIDNe8avXHr6l5seic0VCV4Bf3sq8Kw/640?wx_fmt=png&from=appmsg)

通过类似上述图结构，可以帮助我们极大减轻投研工作中的负担。知识图谱可以将投研领域中常见的实体划分为：机构、产品、人物和行业等。而实体之间的关系也可以归纳为属于、投资、拥有、发布、采购买、任职于、采用等。最终将所需了解的领域中各类实体之间的复杂联系快速梳理出来，帮助我们进行下一步的投资决策。
**（二）GraphRAG部署流程**

此处我们直接使用微软开源的GraphRAG版本，将其部署到本地后结合DeepSeek大模型，以近期的研报作为输入文本数据，对比其构建知识图谱的整体效果。

1\. 首先安装该库：pip install graphrag。

2\. 在工作目录下新建空文件夹：mkdir -p ./ragtest/input。

3.下载官方提供的英文示例数据：curl https://www.gutenberg.org/cache/epub/24022/pg24022.txt -o
./ragtest/input/book.txt。

4\. 项目初始化：graphrag init --root
./ragtest。此时文件夹内会出现.env和settings.yaml两个文件。我们建议根据自己的需求选择合适的大模型，在settings中设置不同的API
Key和Base Url，其默认为OpenAI的GPT4模型。

5\. 正式构建知识图谱：graphrag index --root
./ragtest。此步骤运行时间较长，会完成上文中所述文本单元切分、实体和关系提取、图构建和社区总结等步骤。

6\. 尝试基于知识图谱提问搜索：graphrag query \

\--root ./ragtest \

\--method global \

\--query "What are the top themes in this story?"

此外，需要注意的是，由于原本框架的提示词、输入文本等均为英文，所获得部分输出结果（如实体关系表、图谱等）也均为英文。因此我们需要在每一步骤的提示词中将要求语言进行调整以确保最后结果的实用性。

而若希望将所需模型改为我们本地部署模型或其他渠道的模型，则需要对init后生成的settings.yaml中参数进行调整。主要涉及的参数包括：api_key,
api_base, type和model。需要设置为自己实际使用的模型api和来源厂商的请求地址。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWpNQ3icphMrVBhl1nGsHZkFzTVDQZF9s8LZE2MWicnRgRmVe9O2RSNXSg/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VW2bc385301Ht8Xs0vOe2TdTDrHx4wJmXWYicnKw50LT1elyRPtzBOa0Q/640?wx_fmt=png&from=appmsg)

该工具提供的搜索方式中，global更适用于针对整篇文本进行全局性的概括、理解性提问，而local更适合用于针对特定实体或与其他实体之间关系的提问。最终我们也可以使用Gephi等工具可视化呈现GraphRAG所构建的知识图谱。

**（三）基于研报的知识图谱搭建**

接下来，我们筛选若干篇行业研究研报，将其转为txt纯文本形式后，投喂给GraphRAG框架。

第一篇报告为广发证券传媒行业报告《传媒行业2025A股游戏板块前瞻：产品周期、AI赋能、并购扩张》。我们针对报告中内容测试如下问题：Take
Two都并购了哪些公司或游戏工作室？其中的哪家公司后来开发了《GTA》？

根据GraphRAG的输出结果，我们对比原文可以看出所列举名称均准确无误，无重复无遗漏，且能认识到原文中所提RockStar和2K
Games是公司自行设立，避免了将其纳入被并购公司的范畴。对于中间间隔一层关系的实体关联也能准确识别到BMG Interactive为《GTA》的开发者。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWps31eGUKzgZpCxEe5BFTPCpia3fEbrqQXp2ePEJiacNp0loVJ3TkITiaA/640?wx_fmt=png&from=appmsg)

A股游戏板块2025年有哪些潜在增长点，其分别的投资逻辑是什么？

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VW0qQHCOoHHxic24jFNEXO63T5g9Jcd8BR8iblKcEkDYicqtPYbhL1xtJxg/640?wx_fmt=png&from=appmsg)

笔者对比原文后发现，以上回答的准确性和完整性超出了原本预期，对于希望快速了解该板块投资逻辑的读者而言，阅读该回答回答已经超过了直接阅读原本研报摘要。

若我们希望能进一步探究研报背后的知识图谱，可以从outputs文件夹中读取相应的文件，其中的社区报告表是将知识图谱中的若干个强相关节点和边构建成一个社区（子图），并不断迭代直到不可再分。用户在针对社区相关内容提问时，系统会准备相应的社区摘要进行回答。

  

部分表格中的核心字段说明如下：

1\. 社区摘要：对该社区内容的进一步扩展描述，解释其主题或涵盖的主要内容。

2\. 排序：社区的排名或评分。

3\. 排序说明：对排名的解释。例如，“影响严重性从中等到高”。

4\. 大小：社区所包含内容数量。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWYqCee5JkdyHO4B4vgnnppAWEfjuwBYGrzmYmiaicxqib2zgwqQOKNtccQ/640?wx_fmt=png&from=appmsg)

另外，实体关系表和实体表可以将报告中所有涉及的各类实体和实体间联系通过结构化数据整理，方便后续构建图谱、做快速筛选和查找。在定位上下游产业链关系、股权结构关系等较为高效。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VW5aSPBC1EzhqeuAibEwWh7741TT0Wvl4S2JJ94ERSIpUOicfGqRHVhzQw/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VW6ibuvB4WsZMbXxUNN5WWWueC06rtUAcmSQMBv7f2w8CNLicWwBf7IbVw/640?wx_fmt=png&from=appmsg)

最终，我们可以将系统所输出的图谱进行可视化，直观观察其中主要实体间的关系和结构。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWwehRfK5NZIkqVQicicBf3UKd2EZanPu9rKfufM5VTTlsQas3r3pj8BJw/640?wx_fmt=png&from=appmsg)

第二篇研报为《中望软件(688083)：格局预期差叠加3D
CAD成熟有望驱动估值提升》，我们同样首先观察其主要内容的梳理概括准确程度：国产CAD领域近年来有哪些发展和变化？中望软件地位如何，都有哪些优势？

从下图回答内容可以看出，GraphRAG框架回答时较好地将整篇报告所描述投资逻辑拆分为技术创新、战略收购、市场拓展等，每一项均有准确的细节回答，相较于之前传统RAG模式大大提高了回答准确性的可信度。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWSgvpp0h0auWx5zWsePdZCHwWp9zibicSQbj0trVPf83GrVvPlneY3bibQ/640?wx_fmt=png&from=appmsg)

同样地，我们展示可视化的知识图谱和实体关系表：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWggzhibFWDnU6qMhkdqbaDfezPymBAbrEqVXDXh9VutBMWUJEpfQYfFA/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWdpEsv1H1JmgRuRxCEMgwjZO4lxsdO9ev22IyyW2g5ia4PSJKPafBlUA/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWIQrW5fOx7lib38t3TmekX0Z8y9997icI2SQjlg3qOnkxL64ibGULHXaicg/640?wx_fmt=png&from=appmsg)

第三篇研报为：《AIDC电源行业深度：海外数据中心需求高增
燃气轮机迎东风》，我们首先提问：AIDC的发展将如何影响燃气轮机的发展？产业链中哪些环节受益最明显？

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWPAa9apkKES13eCOdf5fiat8SzFsMaibIclgQsL7r51TYRM7rnXcFcxicQ/640?wx_fmt=png&from=appmsg)

进一步我们追问：目前国内都有哪些上市公司在燃气轮机相关产业链上有布局？分别有多少增长空间？

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWzl4QxewiavBpjr5EibHibWfhIic2WFpZVL1ZtzRl1A1pyg0N47jtO9mLibA/640?wx_fmt=png&from=appmsg)

回答标的均与原文匹配，准确度依然较高。以下为相应的实体关系表和知识图谱：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWV4qicypUPee4eM3DDJodiaAmfKWBHFhxorBGVXXlhAornc7yhKh3ltXQ/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWeqLj7cnBn2dVrGre0DV5VWKuzne2JZUdlsVjTqNoqWlcp4yianKv0xuxCibdQJiaiacXiabjxAfVeMXtw/640?wx_fmt=png&from=appmsg)

**四、风险提示**

**  
**

大语言模型基于上下文预测进行回答，不能保证回答准确性，由此可能产生误导影响用户判断。

GraphRAG或RAG框架的回答质量同样很大程度取决于用户所输入文本语料的内容质量，若文本本身具有误导性或重要信息遗漏，可能对投资决策判断产生重要影响。

市场若出现超出模型预期的变化，过往逻辑链条适用性下降可能会导致策略失效，需要动态对模型进行微调以修正偏差。

法律声明：  
本微信号推送内容仅供广发证券股份有限公司（下称“广发证券”）客户参考，其他的任何读者在订阅本微信号前，请自行评估接收相关推送内容的适当性，广发证券不会因订阅本微信号的行为或者收到、阅读本微信号推送内容而视相关人员为客户。  
完整的投资观点应以广发证券研究所发布的完整报告为准。完整报告所载资料的来源及观点的出处皆被广发证券认为可靠，但广发证券不对其准确性或完整性做出任何保证，报告内容亦仅供参考。  
在任何情况下，本微信号所推送信息或所表述的意见并不构成对任何人的投资建议。除非法律法规有明确规定，在任何情况下广发证券不对因使用本微信号的内容而引致的任何损失承担任何责任。读者不应以本微信号推送内容取代其独立判断或仅根据本微信号推送内容做出决策。  
本微信号推送内容仅反映广发证券研究人员于发出完整报告当日的判断，可随时更改且不予通告。  
本微信号及其推送内容的版权归广发证券所有，广发证券对本微信号及其推送内容保留一切法律权利。未经广发证券事先书面许可，任何机构或个人不得以任何形式翻版、复制、刊登、转载和引用，否则由此造成的一切不良后果及法律责任由私自翻版、复制、刊登、转载和引用者承担。

  

预览时标签不可点









****



****



****





__









