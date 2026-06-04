![cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSv84EYU2244Ou6R92z2Cz2ibrkYDTaNBassM1CBwS4UmYn7ApNyUsib5A/0?wx_fmt=jpeg)

#  华泰金工 | LLMRouter-GRU：“舆情分诊台”赋能AI量价因子 

原创  林晓明 何康等  林晓明 何康等  [ 华泰证券金融工程 ](javascript:void\(0\);)

_2025年07月18日 08:29_ __ _ _ _ _ _ 北京  _

在小说阅读器读本章

去阅读

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYUGfd0mFlPV2D8aAfnYunCObDF0fp1BFibQuFw7b6iaQYxzI0RwVmvQeMib64ODbpxcfGjXsoUrSBP7g/640?wx_fmt=png)

本研究提出LLMRouter-
GRU神经网络，将大语言模型（LLM）对新闻舆情的情感分析能力引入AI量价模型，构建“舆情分诊台”。我们对基础GRU量价模型进行了关键性改进，引入混合专家模块（MoE）以实现分域建模。不同于传统MoE仅依赖内生路由机制，也区别于简单套用市值、风格因子等外生指标进行分域，我们将预训练LLM作为“智能分诊台”，使用新闻情感作为MoE的决策依据，通过对原有神经网络进行轻量级改造，即可实现“情绪分域，量价建模”。实证表明，该模型能有效融合另类舆情信息与量价数据，提升指数增强组合表现。在回测区间2022-12-30至2025-06-30内，300增强年化超额提升达3.0pct，信息比率与最大回撤也有明显改善。

  
** 核心观点  **  
人工智能94：大模型情绪路由赋能AI量价，300指增表现优异  本研究提出LLMRouter-
GRU神经网络，将大语言模型（LLM）对新闻舆情的情感分析能力引入AI量价模型，构建“舆情分诊台”。该结构通过对原有神经网络进行轻量级改造，基于市场情绪动态选择稀疏专家路由，实现了“情绪分域，量价建模”。实证表明，该模型能有效融合另类舆情信息与量价数据，提升指数增强组合表现。在回测区间2022-12-30至2025-06-30内，舆情覆盖度高的300增强年化超额提升达3.0pct，信息比率与最大回撤也有明显改善。  
LLM-News舆情因子：风格特征清晰，Alpha属性不强
新闻舆情是市场反馈最灵敏的另类数据源。本研究基于GLM-4-9B、Qwen2-7B、InternLM2-7B三组大模型构建LLM-
News舆情因子，通过高效提示词设计完成海量新闻情感标注。实验显示，该因子虽Alpha属性不强，但呈现清晰的风格特征。后续，我们将利用其清晰可辨的风格特征进行专家分域。此外，该因子在大市值股票池覆盖度更高，将为后续的大市值指增策略提供更为明显的增量信息。  
LLMRouter-GRU：“情绪分域，量价建模”  传统MoE-
GRU依赖内生路由，由于决策依据与量价信息同源，因此相较于外生路由，其Alpha增厚的空间可能有限。本研究借鉴LLMoE思想，将预训练LLM作为“智能分诊台”，使用舆情因子替代内生路由器。网络的关键创新在于采用稀疏路由（Sparse
Router）方案，通过情绪三分位离散化，仅激活单一专注该情绪风格的GRU专家。相比稠密路由，此设计可显著降低计算成本并避免过拟合风险，且仅需对原有专家网络进行轻量化改造。  
“舆情分诊台”策略可提升指数增强组合表现  LLMRouter-Sparse-
GRU相比于传统AI量价模型在五类指数增强场景均取得提升。在回测区间2022-12-30至2025-06-30内，相较于传统GRU，在300增强与500增强场景下，模型年化超额收益分别提升3.0pct与2.2pct，最大回撤同步改善；红利增强和成长增强则分别提升2.1pct和3.7pct；在1000增强提升稍逊，仅提升0.9pct。该策略在GRUa、GRUb两类基座模型上均验证有效，且稀疏路由显著优于稠密路由及简单特征拼接方案。  
** 正 文  **  

** 01  ** 导读

“  Creativity is just connecting things.  ”  ——Steve Jobs

  

在  DeepSeek  、  GPT-4  等顶尖大模型的技术白皮书里，“  MoE  ”一词频繁出现。  MoE  的全称为混合专家模型（
Mixture of Experts  ），它的核心思想类似于三甲医院的“  ** 分诊系统  ** ”：首先，模型被分割为多个小型神经网络（称为“  **
专家  ** ”），每个专家专注处理特定类型的数据模式；此外，每轮计算开始之前，一个轻量级“  ** 路由器  **
”将根据输入数据的特点，动态选择最相关的  1-2  个专家参与计算。

  

传统混合专家（  MoE
）架构以内生网络作为“路由器”的分诊依据。但在量化选股场景中，内生路由可能难以捕捉市场情绪等非结构化数据的隐含关联信息。笔者曾探索将  DeepSeek
的核心网络结构应用于  AI  量价选股，发现由于决策依据与量价信息同源，其  Alpha  增厚的空间似乎有限。据此，  Liu  （  2025
）等人提出了  ** LLMoE  ** ** （  LLM-Based Routing in Mixture of Experts  ** ** ）
** ，引入预训练  LLM  作为“智能分诊台”，以外生路由替代传统  MoE  的内生路由器，以更好地解析新闻  /  财报等非结构化信息。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSEOtEuEibC6KJsvuXfWx1BicZCIF1mkgK7xiaYz66l26aI1yuKLdm71NUA/640?wx_fmt=png&from=appmsg)

  

LLM
可处理的另类数据包括研报、电话会议、公告及舆情等类型。其中，研报、电话会议作为专业机构输出的信息观点，具备完整的逻辑链条与高信息密度；舆情数据呈碎片化、低信息密度特征，信息挖掘难度虽大，却是市场反馈最灵敏的数据源。本文选取新闻舆情数据作为研究对象，从中挖掘另类信息。直觉上，使用碎片化的新闻数据直接做出“另类
Alpha  ”是困难的，而以此做出另类风格特征是相对容易的。  ** LLMoE  ** **
的分域思想为另类风格特征提供了天然的成长土壤，基于这一解决方案，我们无需构造复杂的另类  Alpha  ** ** 因子，仅需对基础  AI  ** **
量价模块做轻量级改动，即可快速巧妙地将多模态信息融入神经网络。  **

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSIGwkCUTZWAvf7nicA1qEewdI5qkGQsibABibibnfibnUIiazEP09ibhS9hDFg/640?wx_fmt=png&from=appmsg)

  

本文基于  LLMoE  思想提出了  LLMRouter-GRU  神经网络。该网络对于传统的  GRU  量价模型进行了轻量化改造，加入混合专家模块（
MoE  ）来进行分域建模。与普通的  MoE
不同的是，我们利用了大模型对股票新闻情感的分析能力，构建“舆情分诊台”来提取其中蕴含的市场情绪信息，并以此为依据选择稀疏预测专家，得到融合市场情绪信息的
AI  量价融合因子。

  

本文针对沪深  300  、中证  500  、中证  1000  、中证红利与国证成长五类指数增强场景开展测试，实验结果表明，在回测区间
2022-12-30  至  2025-06-30  内，基于“舆情分诊台”构建的  AI  量价策略相较于普通  GRU  模型均有不同程度提升。以“
GRUb  ”模型基座为例，在舆情覆盖度较高的  300  增强、  500  增强、红利增强、成长增强场景下，模型年化超额分别提升  3.0pct  、
2.2pct  、  2.1pct  和  3.7pct  ，最大回撤明显改善；在舆情覆盖度较低的  1000  增强下，模型表现亦不劣于普通  GRU
，年化超额提升  0.9pct  。通过巧妙的“舆情分诊台”结构设计，我们可以在不改变  Alpha  基础预测算法的基础上，有效提升  AI
量价因子的预测表现。  ~~ ~~

  

** 02  ** 因子构建：LLM-News舆情因子

我们将使用快速、低推理成本的方案构造LLM-News简易舆情因子，为后续搭建“舆情分诊台”奠定数据基础。  

** 数据来源  
**
新闻舆情数据来源于大智慧财汇，数据库包含新闻基本信息表、新闻正文表及新闻关联机构表。新闻与证券资产之间的关联大致依靠新闻正文的关键词抓取，因此一条新闻可能对应多个证券资产。考虑到数据覆盖度、推理耗时等因素，我们选取
2017-01-01  至  2025-06-30  的舆情数据用于构造舆情因子。

  

由数据样例可见，并非每条新闻媒体数据都和资本市场强相关。本文暂未对舆情数据做任何粗筛提纯处理，实盘落地时可考虑通过大模型语义提取等方式，对新闻媒体信息做初步清洗、提炼。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nS8fbg6fibHiaZZalqP6vhkuw8nCrYRmjsKYb2icqhUKIbIu48krIU0928Q/640?wx_fmt=png&from=appmsg)

  

从每日舆情数量来看，年报、中报、三季报等财报季的新闻舆情数量明显高于平日。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nStChSAR3ibCLovfvX3Bz369icUhKtLiaHToN3icnaejuX324BqMPN6Opf5A/640?wx_fmt=png&from=appmsg)

** **

** 大模型推理  ** ** 方案比选  ** 下面列举LLM-
News舆情因子的两种构建思路。方案一以“单个预测日期+单只股票”作为最小推理单元，方案二以“单条新闻”作为最小推理单元，两种任务复杂度存在显著差异。  
![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSejPdDHOErhUgyE63iaCjnCGlFoRRdOlszxCkiaUtcWDPCUYzBSL48HRQ/640?wx_fmt=png&from=appmsg)  

** 方案一（多模态整体推理）：  **

构建“量价  \-  舆情”的多模态输入，对单一个股的某一预测截面，整合其滚动  N  日的  OLCHV
量价序列与全量舆情文本，通过大模型端到端输出“乐观”或“悲观”的两种情绪标签。此设计继承了“  LLMoE
”原论文的理想化落地范式，试图让大模型同时捕捉量价趋势的时序关联与舆情文本的语义信息，生成融合量价与市场利好利空情绪的多维度综合情绪因子。

  

** 方案二（舆情逐条推理）：  **

抽取单条新闻舆情数据，逐条输入大模型进行情绪分类，将新闻内容分类为“乐观”或“悲观”两种情绪标签。后续通过滚动时序衰减加权，将单条舆情的打分标签聚合得到整体舆情得分。不再将量价数据传入大模型。

  

本文作为对大模型舆情分析的初探，  ** 选择了方案二这一快速、低推理成本的解决思路。  **
后续，配合强大的另类数据源与成熟的语义提纯技术，方案一或可获得更好的分类打分效果。

  

大模型基座选择

为了提升实验结果的鲁棒性，我们选择了  ** GLM-4-9B  ** ** 、  Qwen2-7B  ** ** 、  InternLM2-7B  **
三组不同的大模型基座，后续实验中将对三组大模型的模型输出取平均得到最终值。  ** 从发布时间看，  ** 这三组大模型基座均发布于  2024  年  6
月底之前，可为我们提供长达一年的大模型样本外效果验证时间。  ** 从模型能力上看，  **
这三组模型在中文财经文本理解与长文本推理任务中均表现良好。在分析股票新闻舆情时，这些模型有能力处理包含较多专业数据和复杂逻辑的新闻信息，进而较为准确地提取关键信息辅助情绪判断。

  
![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSJoSyK5sibZiaCC2KRUCnsBxvzInarUB24a90H7oNZkwVPEEtdpfxNbTg/640?wx_fmt=png&from=appmsg)  

提示词设计

我们的提示词框架包含四个关键部分：

1  ）角色设定：将模型定位为专业财经新闻情感分析师；

2  ）核心任务：明确二分类目标；

3  ）分析指南：引导模型忽略表面措辞，聚焦核心事实与数据；

4  ）输出规范：限定输出仅为“乐观”或“悲观”，确保结果一致性；不设置“无情绪”情感状态，防止出现模型分类类别模糊性（  Class Ambiguity
）。

  

基于以上提示词，我们对  2017  年至  2025  年间的全量  A  股公司相关新闻进行了标注，积累了超过  1000
万条带情绪标签的新闻数据，为后续构建舆情因子奠定了基础。

  

舆情因子时序合成

方案二的最后一步是通过滚动  n  日平均得到  ** 滚动舆情因子  ** 。这一步骤的运算细节如下：

1  ）时序滚动区间为  30  个自然日。且周一盘前发出的调仓信号，应包含上周末的完整舆情信息。

2  ）加权权重随时间做指数衰减。

3  ）区别于“先日内平均、再日间平均”的两步平均法，本研究直接对原始舆情数据做逐条聚合平均。这是由于  **
日内的舆情数量、舆情密度也属于情绪强度的重要表征  **
。例如，某股突发并购利好传闻，单日正面舆情数量暴增，采取逐条聚合时，乐观得分的权重占比也会随之激增，这有利于模型捕捉“情绪爆发”信号；如某只股票单日仅有少量负面舆情（如
1-2  条媒体质疑），因总权重小，也不至于显著拉低得分，有效避免模型出现“单条噪音干扰”。

4  ）将滚动舆情因子通过线性变化映射至  0-1  区间内，方便后续构建情绪路由。

  

实验结果与讨论

新闻情绪的正负标签是否均衡？新闻舆情数据的覆盖度如何？如何控制大模型推理的随机性？下面进行分析讨论。

  

正负样本平衡统计

正负样本的均衡性是分类任务最核心的关注点。在推理过程中，如果无法精准地捕捉两类样本的核心差异，大模型会倾向于将这些“边缘样本”划分至乐观标签，造成正类样本过多。直觉上，推理能力越强的模型，越能更好地捕捉语义歧义、隐含逻辑、上下文关联信息，进而得到更均衡客观的分类结果。

  

下表展示了各个大模型对原始舆情的情感分类情况。总体来看，三种大模型已然展现出良好的分类效果。由于舆情原始数据本身可能就是“有偏”的，我们不能苛求其实现正负分类的严格平衡。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSico9ejmfTHuhXRj61eRLpFBcjaB5ZxjHjCTogENUyV87aGPUZYDfRfw/640?wx_fmt=jpeg)

  

不同股票池的舆情因子分布差异

舆情因子在不同股票池的分布具有显著差异。

1  ）大市值股票池的  ** 舆情覆盖度  ** 显著高于小市值股票；可以预见，在后续实验中，舆情覆盖度越高的股票池中，策略的边际提升将越明显。

2  ）市值越大，新闻舆情的  ** 乐观比例  ** 越高。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSxicLawIKibibERVVAia6K0rneBYOVbRrdJXK5GHjHNibsACiaQBDNqOSWRdw/640?wx_fmt=png&from=appmsg)

  

LLM  推理随机性讨论

大模型对同一指令的多次执行可能得到截然不同的输出结果，这使得许多人对  LLM  推理结果加入量化模型心存疑虑。我们通过合理调节  Top-K  、
Top-P  和  Temperature  三个参数，兼顾了大模型的高创造性和低随机性。我们选取了某个自然月的  15
万余条舆情数据进行多次运行，发现多次运行结果之间的差异率仅在  1.5%  以下，这一结论对三个大模型基座均成立。

  

舆情因子分层测试结果

最后展示舆情因子的分层测试结果。可见舆情因子本身的“  Alpha  ”能力并不强，虽然头部两组（  Layer1  、  Layer2
）具有一定的选股能力，但其整体呈现了风格因子的特性。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSZiahFAroibicp3kHAafenKeddCSeVbUYA1IialMqvGhYpial09yzlW14wkw/640?wx_fmt=png&from=appmsg)

  

三种大模型推理得到的舆情因子相关性较高，两两之间相关性均在  0.75  以上。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSH808Zfb9XaealUlbRCUlJVGia4q4Iw0Y9gLbzAUuwfbohAKrSSDIzMg/640?wx_fmt=png&from=appmsg)

  

** 03  ** 网络构建：LLMRouter-GRU“舆情分诊台”  

由于舆情因子呈现出一定的风格特性，将其使用线性加权、简单拼接等方式加入多因子模型，或难以带来稳定的超额提升。本文基于  LLMoE  架构，提出  **
“情绪分域，量价建模”  ** 的解决思路。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSn96jibeqVf9w3TslSYXerThiaLiaZk40CjgRiaO0ibfiaPk6iaEweUMUVtj6Q/640?wx_fmt=png&from=appmsg)

  

网络结构

混合专家（  MoE  ）的整体思想类似于三甲医院的“  ** 分诊系统  ** ”：首先，模型被分割为多个小型神经网络（称为“  ** 专家  **
”），每个专家专注处理特定类型的数据模式；此外，每轮计算开始之前，一个轻量级“  ** 路由器  ** ”将根据输入数据的特点，动态选择最相关的  1-2
个专家参与计算。本研究针对传统  MoE  做出了较多改进，下面展开详述。

  

从  MoE  到  LLMoE

传统混合专家（  MoE  ，如图  13
方案②）架构以内生网络作为“路由器”的分诊依据。但在量化选股场景中，内生路由因为决策依据与量价信息同源，故相较于外生路由，其难以捕捉市场情绪等非结构化数据的隐含关联信息，
Alpha  增厚的空间可能有限。并且笔者认为，内生路由拉高了网络参数量，对于时间序列预测这类小样本任务，可能会适得其反，导致过拟合。  Liu  （
2025  ）等人提出的  LLM-MoE
量化选股网络，创新性地将路由器模块重构为外部大模型情绪分类模块，本质上是将自训练路由变成了冻结参数的预训练路由。原始的  LLMoE
由于推理量大，仅可用于单只龙头股的收益预测。我们基于  LLMoE  的思想，拓展提出了“大模型情绪路由  \-  专家特征提取  -AI
量价因子合成”的全市场端到端架构（如图  13  方案③、④），称为  LLMRouter-GRU  “舆情分诊台”神经网络。

  

网络整体分为两大核心模块，模块一  “情绪分域”  ，模块二  “量价建模”  ：

  

** LLMRouter  ** ** —大模型情绪路由层  **

基于  LLM  （如  Qwen-LLM  ）构建舆情文本分析引擎，将新闻舆情、社交媒体文本等非结构化数据转化为舆情情绪因子，替代传统内生路由网络。

  

传统  MoE  的  Router  本质是输入到专家权重的映射函数，数学表达为：𝑔(𝑥)=𝑠𝑜𝑓𝑡𝑚𝑎𝑥(𝑊𝑥)  ，其中  𝑊
为线性路由层的网络参数。本文将其替换为大模型情绪分类器，具体实现路径已在“舆情因子”章节详述。  LLM-News
舆情因子为标量数据，我们可以将其简单地作为连续路由的权重，将预测任务分流至多组专家路径；也可作为离散路由的分诊依据，将预测任务分配给指定一名专家。

  

与传统内生路由相比，  LLM  路由可捕捉另类文本数据中的隐含情绪（如“政策利好”“业绩不及预期”等语义信息），且为多模态融合入  AI
量价提供了轻量级解决方案。此处的情绪路由输出不要求具有强烈的  Alpha  属性，甚至风格属性可能比  Alpha  属性能提供更多的分域增量信息。

  

** GRU Experts  ** ** —多专家特征提取层  **

专家网络采用同构设计，使用简单  GRU  构成的小型神经网络作为基础收益预测专家（  GRU Experts  ），相较于过往报告未做改动。在传统  AI
量价模型中，我们使用简单  GRU  直接得到因子输出。在“舆情分诊台”  LLMoE  结构中，我们对  GRU Experts  做多次堆叠，配合
LLMRouter  得到多个专注处理不同风格的  GRU  专家。

  

在本策略中，仅专家网络层的参数参与训练与反向传播；  LLM  参数则被固定，本质上可视为外生独立的计算过程。

  

稠密  vs  稀疏

经归一化后的舆情因子呈现为  [0,1]  区间的连续数值分布。基于该因子构造的“舆情分诊台”路由机制存在两种设计方案：

  

一种做法是使用  ** 稠密路由（  ** ** Dense Router  ** ** ）  **
，最大程度保留舆情强度信息，将连续型因子直接输入稠密路由层，通过权重分配机制激活全部专家模块。

  

另一种做法是  ** 稀疏路由（  ** ** Sparse Router  ** ** ）  **
，通过三分位离散化将舆情因子映射为乐观、悲观、中性三类情绪变量。每个训练样本仅激活  Top-k  的少量专家路由。  DeepSeek
在训练大模型基座时提倡采用此类稀疏式路由结构，该种方法可显著降低训练成本。本文设定  k=1  ，即每个训练样本仅开启一个专家路由。

  

后续实验中，我们将同时对两种路由方案展开测试。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nS3nFhnmD2PFnibicWQDjKPoiazx19oEokmAFMib9gIZ3xMBfTFZoZA8WUJg/640?wx_fmt=jpeg)

  

输出与损失函数

模型输出即为融合市场情绪的  AI  量价因子。损失函数为  IC
。注意涉及多个专家路由独立预测时，需将预测结果先平均（稠密路由）或拼接（稀疏路由），再统一计算  IC  损失函数，以保证不同专家输出间的量纲统一。

  

实验设计

我们设计了较为丰富的对比实验，通过多种网络结构、多种  GRU  基座来证实策略的可靠性。

  

网络结构对比

共对比四类网络结构，将舆情信息更换多种形式融入  GRU  网络，以证明“舆情分诊台”策略的可靠性。

  

1  ）纯量价输入：基线模型。普通  GRU  ，以  OLCHV  等数据作为输入，无舆情信息。

  

2  ）量价  & 舆情输入：在实验  1  的基础上，额外增加舆情因子作为  GRU  普通特征输入网络。

  

3  ）  LLMRouter-Dense  ：稠密型  MoE  ，模型中所有的“  GRU
专家”均被激活。“舆情分诊台”生成连续而非离散的权重，不同“专家科室”给予不同的加权权重。  GRU  本身仅接受量价数据作为输入。

  

4  ）  LLMRouter-Sparse  （推荐）：稀疏型  MoE  ，仅激活  Top-k  少量专家路由。  DeepSeek
在训练大模型基座时提倡采用此类稀疏式路由结构，该种方法可显著降低训练成本。本文设定  k=1  ，即“舆情分诊台”仅开启一个专家路由。

  

GRU  基座双重验证

为了证明策略对不同预测算法的通用适配性，我们专门设计了两类不同的  GRU  基座，称为  GRUa  与  GRUb  。其中，  GRUa
包含了复杂注意力机制，前期表现强势，但  2024  年  9  月以来遭遇了较大回撤；  GRUb  为简单  GRU  网络，表现稳健。这两种  GRU
基座完整涵盖了过拟合、欠拟合、适当拟合等情形。

  

** 后续实验中，我们将构造  4  ** ** ×  2=8  ** ** 项对比实验，同时证明“舆情分诊台”策略在两类  GRU  ** **
基座上的提升。  **

**  
**

其余参数设定

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSe6vO0xnB9d5nCOyxQ8NYpJL0rKTWY2KR8rjVjhLt9doZevU84TPeVw/640?wx_fmt=png&from=appmsg)

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSJn2pdMMq0sQ7Dw9c7VD45QdvXDxqALQcCazcQJIS677ZKaloqjwVXw/640?wx_fmt=jpeg)

  

实验结果

总体来看，我们推荐的  LLMRouter-Sparse  策略结合了  GRU  对量价因子的强提取能力与  LLM
根据新闻舆情选择稀疏专家的能力，借助轻量级的解决方案实现了另类数据与  AI  量价因子的融合。

  

因子表现

可见  AI  舆情融合因子改善主要体现在多头端。多头收益、多头端区分度都有显著提升。  RankIC  指标无明显改善。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSvaUMplBLZUSFXzVZ8wwJsU5hcdmQ0pKWXXW2kgvyavcudbzmXMSppg/640?wx_fmt=jpeg)

  

指数增强组合表现

整体结论：

1  ）本文主推的  GRU-LLMRouter-Sparse  因子，在不同  GRU  基座、不同指增组合上均有一定程度提升。  **
在舆情覆盖度较高的  ** ** 300  ** ** 增强、  500  ** ** 增强、红利增强、成长增强中提升较为明显  ** ；  1000
增强由于舆情覆盖度低，提升不太明显，但策略并未劣于  GRU  基座模型。

  

2  ）两种舆情分诊台结构中，  Sparse  （稀疏结构）显著优于  Dense
（稠密结构）。直觉上，稠密结构在拉高训练成本的同时，还可能给模型带来过拟合风险。

  

3  ）简单地将情绪因子作为普通特征传入  GRU  基本不奏效。

  

基于两组不同的  GRU  基座分别构建的四类沪深  300  指增策略净值与绩效如下：

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSib215Zhkej0kHQEgupue74ibU7IicXNYj2wOf8mJaEtO5kpUwsqCIqNiaA/640?wx_fmt=png&from=appmsg)

  

300  增强超额提升显著，相较于普通  GRU  ，  LLMRouter-Sparse  因子在基座  a  、基座  b  的年化超额收益均提升
3.0pct  ，分别达到  7.5%  与  9.5%  。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSoIuYMf7gH0qILKcrmOEgUJ5rH4r2a2kGkDyPVL1nGzko03Pszoj0yQ/640?wx_fmt=jpeg)

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSEvq629GXGjVsicHmyiaR12ic3SN5ELdRMa65gIUyZicpqnnONL3CKkVvNg/640?wx_fmt=jpeg)

  

基于两组不同的  GRU  基座分别构建的四类中证  500  指增策略净值与绩效如下：

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYX8yvByXja8aNqXEGttRK8ODviamKoDoaQT0FO9EqiapwmTwOUicyd6ic9Y9QxcRYC6kqnQT5nniax1fPA/640?wx_fmt=jpeg)

  

500  指增中，  LLMRouter-Sparse  提升幅度稍弱，相比传统  GRU  在基座  a  、基座  b  的年化超额收益分别提升
2.3pct  、  2.2pct  。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSiaA1NzLuNQiaU842GZx3OX9bXkY78XYAEIh27v9fHCJMxZcib2SLlT2dQ/640?wx_fmt=jpeg)

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nShtCJoD0mZKBnyfjrssVz38oV93UqGVEcLgawZ7Cr4fTylZ5icjKnzmA/640?wx_fmt=png&from=appmsg)

  

基于两组不同的  GRU  基座分别构建的四类中证  1000  指增策略净值与绩效如下：

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nS4V5DMYehUE7cOzicBJeEczuuQKdZIVXzlsicPcvPAfMbVbrPEb44oY1w/640?wx_fmt=jpeg)

  

由于舆情数据在小票覆盖度较低，模型在中证  1000  指增组合的提升较小，但同样未劣于传统  GRU  。  LLMRouter-Sparse
策略相较传统  GRU  在两类模型基座的年化超额收益率分别提升  1.3pct  、  0.9  pct  。

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSRnDFzhIzyf8Xdia54IQib6WpV0tJ6ecR5ubch5LSia5UMDibarTLGpwb0A/640?wx_fmt=jpeg)

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nStgf8VugjoAA26gv3y3pAhBrXDCQhsA4fuIvoeHOGAKSmcGria8DGibtA/640?wx_fmt=png&from=appmsg)

  

基于两组不同的  GRU  基座分别构建的四类中证红利指增策略净值与绩效如下：

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSwEygHx3kVFGOxIBM1ZY3xps9dfdu2LeVxOpcQfpxKoPpkRualagq2g/640?wx_fmt=jpeg)

  

红利增强策略同样提升明显。提升后的  GRUb-LLMRouter-Sparse  策略相对于中证红利全收益指数的年化超额达到  3.8%  。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSxyPRBdngnrD9rd0Y2gEn8NZYEhKzU4RcCIJTvHjCtbsvTKCZ7SeUPA/640?wx_fmt=png&from=appmsg)

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSe4FXWmEH7qttUA0OSmeUM5QBjTqDibDYh9x4K8jAgAJT9h7EZe1qFyg/640?wx_fmt=jpeg)

  

基于两组不同的  GRU  基座分别构建的四类国证成长指增策略净值与绩效如下：

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSiacQMdeJXqibjKpD3GEWDQIHX0UjnlmEdbtxqpYYzMTFkvXyQq2eFHibA/640?wx_fmt=jpeg)

  

成长增强超额提升明显，  LLMRouter-Sparse  策略相较传统  GRU  在两类模型基座中分别提升  1.9pct  、  3.7pct
，信息比率则分别提升  0.40  、  0.78  。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSsibN8TorWQEFhIxlnTUDsP0JNHictf3IffwZOlVG4GoxFJWoWBSrwWTg/640?wx_fmt=png&from=appmsg)

  

![](https://mmbiz.qpic.cn/mmbiz_jpg/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSXos9ZiaIEdOiam06CY66B4Vib6eWL1lia8C6OS4GRNL6rpmHDgA8OeKbCQ/640?wx_fmt=jpeg)

  

附加讨论：大模型发布前的回测区间是否会引入未来信息？

本文所使用  LLM  的最大参数规模为  9B
。通常来讲，该类中小模型的训练集以数学类、代码类及通用领域文本为主，直接涉及的新闻语料较少，财经新闻覆盖可能更为有限。且大模型在本文中仅用于新闻情绪分类任务，我们并未引导其建立与股价变动的直接关联。这在一定程度上构成了“信息防火墙”，使得“信息泄露”的风险相对可控。

  

由结果同样可见，大模型发布后各策略的超额提升幅度，并未显著弱于发布前区间。这代表大模型引入“未来信息”的风险是有限的。

  

![](https://mmbiz.qpic.cn/mmbiz_png/XqS3WcqWGYVGQJJPRpHibqmAsCSa8Y1nSmnmZawVAU8RGEicez4AFz4RJ8lrKrQicYLTUQEx0lJ1LWnJZicMK9pOPw/640?wx_fmt=png&from=appmsg)

  

** 04  ** 总结

本研究针对传统  AI  量价模型难以融合非结构化数据的痛点，提出了基于大模型专家路由的  LLMRouter-GRU  模型。该结构  将大语言模型（
LLM  ）对新闻舆情的情感分析能力引入  AI
量价模型，构建“舆情分诊台”。通过对原有神经网络进行轻量级改造，我们基于市场情绪动态选择稀疏专家路由，实现了“情绪分域，量价建模”，
为另类数据与量价因子的融合提供了高效的解决方案。

  

因子构造上，我们构建了低推理成本的  LLM-News  舆情因子，  通过高效提示词设计完成海量新闻情感标注。实验显示，该因子虽  Alpha
属性不强，但呈现清晰的风格特征。  LLMoE  的分域思想为另类风格特征提供了天然的成长土壤，基于这一解决方案，我们无需构造复杂的另类  Alpha
因子，仅需对基础  AI  量价模块做轻量级改动，即可快速巧妙地将多模态信息融入神经网络。

  

网络设计上，我们  对基础  GRU  量价模型进行了关键性改进，引入混合专家模块（  MoE  ）以实现分域建模。不同于传统  MoE
仅依赖内生路由机制，也区别于简单套用市值、风格因子等外生指标进行分域，  我们  将预训练  LLM  作为“智能分诊台”，使用舆情因子作为  MoE
的决策依据。网络采用稀疏路由（  Sparse Router  ）方案，通过情绪三分位离散化，激活专注特定情绪风格的  GRU
专家，从而构建出融合情绪感知机制的  LLMRouter-Sparse-GRU  策略。相较于稠密路由，稀疏路由可显著降低计算成本并避免过拟合风险。

  

实验结果上，  LLMRouter-Sparse-GRU  相比于传统  AI  量价模型在五类指数增强场景均取得提升。在回测区间  2022-12-30
至  2025-06-30  内，相较于传统  GRU  ，在舆情覆盖度较高的  300  增强与  500  增强场景下，模型年化超额收益分别提升
3.0pct  与  2.2pct  ，最大回撤同步改善；红利增强和成长增强则分别提升  2.1pct  和  3  .7pct  ；在  1000
增强提升稍逊，仅提升  0.9pct  。该策略在  GRUa  、  GRUb  两类基座模型上均验证有效，且稀疏路由显著优于稠密路由及简单特征拼接方案。

  

参考文献

Liu, K. M., & Lo, M. C. (2025). LLM-Based Routing in Mixture of Experts: A
Novel Framework for Trading. arXiv preprint arXiv:2501.09636.

  

风险提示

大模型基于海量数据训练而成。人工智能挖掘市场规律是对历史的总结，市场规律在未来可能失效。神经网络存在一定的过拟合风险。本文所采用的  GLM-4-9B  、
Qwen2-7B  、  InternLM2-7B  大模型训练截止日最晚为  2024  年  6  月底，因此样本外回测时间稍短。本报告不涉及标的推荐。

  

相关研报

研报：《  LLMRouter-GRU:“舆情分诊台”赋能AI量价因子  》2025年7月17日

分析师  ：  林晓明 S0570516010001 | BPY421  分析师：何康 S0570520080004 | BRB318  分析师：  徐特  S057  0523050005  联系人：孙浩  然  S0570124070018    

关注我们

  
** 华泰证券研究所国内站（研究Portal）  **

** https://inst.htsc.com/research  **

访问权限：国内机构客户

  
** 华泰证券研究所海外站  **

**** https://intl.inst.htsc.com/research  ** **

访问权限：美国及香港金控机构客户  添加权限请联系您的华泰对口客户经理

免责声明

▲向上滑动阅览

本公众号不是华泰证券股份有限公司（以下简称“华泰证券”）研究报告的发布平台，本公众号仅供华泰证券中国内地研究服务客户参考使用。其他任何读者在订阅本公众号前，请自行评估接收相关推送内容的适当性，且若使用本公众号所载内容，务必寻求专业投资顾问的指导及解读。华泰证券不因任何订阅本公众号的行为而将订阅者视为华泰证券的客户。

本公众号转发、摘编华泰证券向其客户已发布研究报告的部分内容及观点，完整的投资意见分析应以报告发布当日的完整研究报告内容为准。订阅者仅使用本公众号内容，可能会因缺乏对完整报告的了解或缺乏相关的解读而产生理解上的歧义。如需了解完整内容，请具体参见华泰证券所发布的完整报告。

本公众号内容基于华泰证券认为可靠的信息编制，但华泰证券对该等信息的准确性、完整性及时效性不作任何保证，也不对证券价格的涨跌或市场走势作确定性判断。本公众号所载的意见、评估及预测仅反映发布当日的观点和判断。在不同时期，华泰证券可能会发出与本公众号所载意见、评估及预测不一致的研究报告。

在任何情况下，本公众号中的信息或所表述的意见均不构成对任何人的投资建议。订阅者不应单独依靠本订阅号中的内容而取代自身独立的判断，应自主做出投资决策并自行承担投资风险。订阅者若使用本资料，有可能会因缺乏解读服务而对内容产生理解上的歧义，进而造成投资损失。对依据或者使用本公众号内容所造成的一切后果，华泰证券及作者均不承担任何法律责任。

本公众号版权仅为华泰证券所有，未经华泰证券书面许可，任何机构或个人不得以翻版、复制、发表、引用或再次分发他人等任何形式侵犯本公众号发布的所有内容的版权。如因侵权行为给华泰证券造成任何直接或间接的损失，华泰证券保留追究一切法律责任的权利。华泰证券具有中国证监会核准的“证券投资咨询”业务资格，经营许可证编号为：91320000704041011J。

  

预览时标签不可点









****



****



****





__









