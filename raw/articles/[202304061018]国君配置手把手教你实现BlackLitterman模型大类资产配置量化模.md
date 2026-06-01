![cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9ldwQbjlFedvOx0s6yTV4ay2MvuTD1IJZr6EH5ISt7ZnwVPVSXWib1icg/0?wx_fmt=jpeg)

#  【国君配置】手把手教你实现Black-Litterman模型——大类资产配置量化模型研究系列之二

原创  廖静池配置团队  廖静池配置团队  [ 廖市无双 ](javascript:void\(0\);)

_2023年04月06日 10:18_ __ _ _ _ _ _ 广东  _

在小说阅读器读本章

去阅读

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9gzBBxpVm9icMP6ibiaflROE1ScxyCLIFyMIjHGZe7EsG8ZpHpeyAMMTGA/640?wx_fmt=png)

_作者：_ _廖静池、张雪杰_

_感谢实习生朱惠东对本文的贡献_

  

**导读**

**本报告作为入门文章，旨在介绍Black-
Litterman模型的基本原理和编程实现。首先，介绍BL模型的基础——MVO模型。然后，详细介绍BL模型的基本理论和计算过程；其中市场均衡收益、后验分布的计算是重点，主观观点的预测准确性是模型效果的关键。最后，将资产最近一个月收益率作为主观观点，构建一个简单的适用于“固收+”产品的资产配置策略；结果表明BL模型策略整体优于MVO和固定比例模型。**

  

**摘要**

▶ **均值-方差模型是现代投资组合理论的基石，是Black-Litterman模型的基础。** 1952年Harry
Markowitz提出了著名的“均值-方差模型”（Mean-Variance
Model），给出了刻画预期收益和风险的一套范式，开启了量化配置时代。MVO模型在理论上具有开创性意义，但在实践中遇到了诸多问题。BL模型对MVO模型进行改进，采用贝叶斯理论将主观观点与量化配置模型有机结合起来
。

**▶** **** **Black-Litterman模型的实现过程主要分为四步。**
（1）通过逆向优化从市场均衡条件出发得到关于资产预期收益的先验估计；（2）将投资者的主观观点作为新的信息，计算观点分布；（3）将先验收益分布和主观观点分布结合，使用贝叶斯方法计算得到资产预期收益的后验估计；（4）将后验收益和后验协方差矩阵输入均值-
方差模型中进行优化求解，得到具体的资产配置权重。其中，市场均衡收益、后验分布的计算是重点，参数设置的合理性、主观观点的预测准确性是模型效果的关键  。

▶ **BL模型效果整体优于MVO模型和固定比例模型。**
为了讲解模型的使用和编程实现，我们将资产一个月收益率作为主观观点，使用BL模型构建一个简单的适用于“固收+”产品的资产配置策略。策略业绩比较基准设定为10%股票+80%债券+10%商品。历史回测发现，给定的参数取值和约束条件下，2012年以来BL模型策略1的年化收益为6.58%，最大回撤为3.13%，收益回撤比为2.1；明显优于均值方差基准策略（年化收益5.82%、最大回撤3.86%、收益回撤比1.51）和固定权重基准策略（年化收益5.41%、最大回撤3.55%、收益回撤比1.52）。

▶ **风险提示：**
黑天鹅事件等可能导致大类资产相关性增加，资产配置组合表现不佳；量化模型基于历史数据构建，而历史规律存在失效风险；市场情况不满足模型假设，模型存在失效风险。

![](https://mmbiz.qpic.cn/mmbiz_gif/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9UevTaRn2hibicVfN9Uz3Uwl91llFCWBqcyt9WOV1coURicLvdtUbVFWCg/640?wx_fmt=gif)

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9WicGMJTty6lEaAmNyp2RFeyRIZwDpwEgle0ssMHrsWgudVLalMXUskQ/640?wx_fmt=png)

  

国泰君安量化配置团队专注于资产配置量化模型研究。我们在 [ **大类资产配置量化模型研究系列**
](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg5MzY1NTc0Ng==&action=getalbum&album_id=2850486121783689218#wechat_redirect)
第一篇《 [ **大类资产配置体系简析**
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507957&idx=1&sn=0bd82f2cc513709f51ac2d6fda688775&chksm=c0291058f75e994ed6f5e40a2eddbacdc7b3da77a56d148ef8ff105a0dea551dc43200fcd291&scene=21#wechat_redirect)
》中，简单介绍了大类资产配置基本概念，重点梳理了大类资产配置模型理论发展历程以及相关模型的构造方法。 **本篇报告是该系列第二篇报告，作为Black-
Litterman基本模型的入门文章，选取较通用的做法来介绍BL模型的基本理论、具体实现步骤。同时，为了讲解模型的使用和编程实现，实现了一个简单的适用于“固收+”产品的资产配置策略，并和固定权重模型、MVO模型的效果做了对比，验证了BL模型相对前两者的有效性。**

  

**01 Black-Litterman模型是均值-方差模型的改进  **

  

**1.1** **均值-方差模型开启了量化配置时代**

**  
**

马科维茨（Harry Markowitz）在1952年提出了著名的“均值-方差模型”（Mean-Variance Optimization
Model，MVO），创建了现代资产组合理论，将大类资产配置带入到量化配置时代。MVO模型是大类资产配置理论的重要基础，其突出贡献在于：（1）提出了“约束+最优解”的标准范式来研究资产配置问题；（2）采用均值和方差来刻画资产收益与风险，使得进行量化配置成为可能；（3）同时考虑风险与收益，指出最优的投资组合并非单纯追求最高收益或最小风险，而是在两者之间找到平衡。均值-
方差模型的输入值包括三部分：收益、风险、反映投资者风险偏好的参数。

  

**Markowitz提出的均值-方差模型基于以下几个假设：**

1) 投资者是理性的，其行为模式是为了在给定收入和资金水平下最大化其投资效用。

2) 投资者可以自由获得投资组合的收益和风险的信息。

3) 市场是非常有效的，对信息的反应是及时且准确的。

4) 投资者是风险厌恶的，并希望让投资组合风险最小，收益最大。

5) 投资者基于预期收益和收益的标准差或方差做出投资决策。

6) 在给定风险水平下，投资者更喜欢高收益的投资组合。

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9rQqXgNnNuVgJ7zHx377ShDlhicDyEzFWlhGucaTALRMXIMbicdaoLUmQ/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9N3RJFtn2f2bJicbMrkZ8ALYvlf5olQHSMxc8x873KLD1tYCM2I1oFOA/640?wx_fmt=png)

  

**1.2 风险厌恶系数与目标波动率存在一定对应关系**

**  
**

**理论中常用的风险厌恶系数不可见，实际投资中目标波动率体现了风险厌恶程度。事实上，风险厌恶系数与投资者可接受最大波动率存在一定的对应关系。**
下面我们以存在借贷约束的投资者为例进行说明，此处引用杨朝军
(2021)做法。对于我国资产管理者或投资者而言，流动性需求迫使其资金在使用时需将一部分资金放在无风险资产上，其投资组合的

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ93y0ia5sodjC1ia0IicdUxhibU4cUbEhicibvr8hhQCquG4qGmKfAXGu2sDHw/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ90icDgbRH210DkcFEDdqFAfnydicOH8PoX8mjAapapziag3ggiazliboWb6w/640?wx_fmt=png)

**  
**

**1.3 BL模型引入主观观点对MVO进行改进**

**  
**

**MVO模型在理论上具有开创性意义，但在实践中遇到了诸多问题。**
比如作为模型输入参数的资产期望收益率难以准确估计，实际应用效果大打折扣；模型计算结果对输入参数，尤其是预期收益率非常敏感，使得模型结果很不稳定；容易得到极端的结果，权重集中于少数或个别资产。为了解决这些缺陷，学界和业界不断提出新的理论和方法进行改进。

  

**BL模型是传统的均值-方差模型的改进。** 1990年，高盛的Fisher Black和Robert
Litterman对MVO进行改进，开发了Black-
Litterman模型（简称BL模型），并于1992年将其发表，后被业内广泛使用。BL模型采用贝叶斯理论将主观观点与量化配置模型有机结合起来，通过投资者对市场的分析预测资产收益，进而优化资产配置权重。BL模型有效地解决了均值-
方差模型对于预期收益敏感的问题，同时相较纯主观投资具有更高的容错性，为投资者持续提供高效的资产配置方案。

  

**02** ** Black-Litterman模型理论介绍  **

  

**Black-Litterman模型的具体实现过程主要分四步：**
（1）通过逆向优化从市场均衡条件出发得到关于资产预期收益的先验估计；（2）将投资者的主观观点作为新的信息，计算观点分布；（3）将先验收益分布和主观观点分布结合，使用贝叶斯方法计算得到资产预期收益的后验估计；（4）将后验收益和后验协方差矩阵输入均值-
方差模型中进行优化求解，得到具体的资产配置比例。其中，市场均衡收益、后验分布的计算是重点，参数设置的合理性、主观观点的预测准确性是模型效果的关键。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9X3kFO6xFBnbGknv6fcicQw8kjm49SEqqq0liaDJ6CQib5QaZcSq55tBSQ/640?wx_fmt=png)

**  
**

**2.1 模型理论准备**

**  
**

**2.1.1 资产收益建模**

  

无论是BL模型还是均值-方差模型，都需要先对资产收益、风险特征进行建模。均值-
方差模型采用均值与协方差矩阵实现对资产收益和风险的刻画；BL模型在此基础上更进一步，将投资者主观观点建模汇入模型之中。按照Walters
(2009)做法，我们从收益率的正态分布假设出发，构建一个有关资产收益的基础模型，为后续的BL模型的进一步理论推导做

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9vUpsVHPYwT3kzvEUY7FFxGvp0tqeia5339cFSbvsF3rgw6kibZfLfibrw/640?wx_fmt=png)

  

**2.1.2 贝叶斯公式**

  

贝叶斯公式是根据英国数学家贝叶斯的思想发展而来。贝叶斯思想源于一个简单的事实——人们会根据新的信息更新对于已有事物的观念。后人根据贝叶斯的思想创建了统计学中声名远扬的贝叶斯理论。贝叶斯理论与人们对事物的认知过程相吻合，为近现代的统计理论进步做出了卓越贡献。Black和Litterman正是利用了贝叶斯理论，把主观观点和对资产收益率的先验估计相结合，形成最终的对资产预期收益率的估计，即资产收益率的后验估计。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ91s0Fic46wLj1nN1slOLa2sVNI4fk00dg2lN4qE73wJsyU5cedXZEzkw/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9KotD0XagkjoBtpVsVrGVEYO5DicmwbMpBhRvwECZUgtWQYT9V2qZmow/640?wx_fmt=png)

**  
**

**2.2 第一步：CAPM框架下反解先验分布**  

****

在没有主观观点的情况下，我们将公式（14）中的 π
称为先验收益率。在BL模型中，资产的先验收益率实际上是由CAPM框架下市场均衡条件下的市场投资组合的权重与市场风险厌恶系数，通过逆优化反解(reverse
Optimization)而来。

  

在CAPM的框架下，当投资者观点中性或市场中投资者的观点相互抵消时，市场处于均衡状态，资产均衡收益的分布即贝叶斯公式中的先验分布；当投资者形成主观观点时（市场中出现了新的信息，并将逐渐反映到市场价格中），市场均衡出现了移动，市场均衡条件下的资产预期收益率理应发生偏离，其分布对应贝叶斯公式中的后验分布。CAPM给出了均衡状态下的市场组合权重、市场组合收益率和各个资产收益率之间的关系。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9oJLCN8gJWIgwBuZGknzesgvDgZj6fb1HM1Iz9Q5EmtmbTeVouXEVog/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9yAXOzoOOv7KibwZbsOZuqSm3CFalvav9ekdNX9OhBrtSzfILShaia0zw/640?wx_fmt=png)

**  
**

**2.3 第二步：投资者主观观点的数学表达**  

****

**BL模型将投资者关于资产收益率的主观观点作为输入变量，投资者的**

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9vfs2AelNOY3TibE3Tn4VY8zA2SWB1jqQzicghNyriayP50QUSRKq7gxjw/640?wx_fmt=png)

**  
**

**主观观点举例说明。** 我们假定投资者在当期对于沪深300、标普500、恒

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9kx15CLXZPFXvQdiahukr2ibMk6w2oNVZkHia8Ph8GCZ0fEgk3yk98Yg1g/640?wx_fmt=png)

**  
**

**2.4 第三步：将先验分布和主观观点结合得到后验分布**  

  

前面2.2和2.3两个小节介绍了如何在市场均衡条件下得到收益率的先验估计以及主观观点的数学表达形式。这一节着重介绍如何把先验估计

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9Ucajo3ibkv4tWIpue0SicGbwIGFRNalY18iaJ8eHx8Rym4BxvxdFNhGSg/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9WUDsJBeGjb6yfFmW1qiaibpiaVqKGRhBRIDhSMic8iaADyyNUAIm4UN6HNw/640?wx_fmt=png)

  

由上图可以看出，BL模型涉及的变量比较多。总结一下主要有以下变量：

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ91zCLu4IsWqLPEy8SBHTPJBjzcHxPS6dGJ0fr4XllTDMTRdoBV7797g/640?wx_fmt=png)

**  
**

**2.5 第四步：后验收益率和后验协方差代入最优化问题求解**

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ94SYZcCrrDKz7LUwQicS0B9cgqBjGFTeJjD8jWvyaUpMHJiaLCLrO9TXQ/640?wx_fmt=png)

资产比例限制等。在确定以上数据参数和约束条件后，再通过求解带约束的最优化问题得到各个资产的投资权重。

**  
**

**2.6 举例：BL模型与MVO模型单期结果对比**  

****

BL模型通过贝叶斯方法把主观观点对收益率融入收益率估计中，进而对资产配置权重产生影响。为了对这种影响有更加清晰的认识，我们这里进行一个简单的BL模型求解示例。表
1对于沪深300、标普500、恒生指数与日经225四种资产历史表现进行了统计。无风险利率为2%。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ92J6RlDExCjHoWxUFXM9LZEUg7bZXDXannnq2xsu47SBCN98BlYIU9A/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9NRSdJFyLTSBoan0OAMo7dRLk60tFJxEtTMRibyNqVFqWaltdPJXmwHA/640?wx_fmt=png)

估计的资产预期收益率。对有主观观点的资产，我们认为主观观点即为资产预期收益率；对没有主观观点的资产，我们采用历史收益率为资产预期收益率，沪深300与恒生指数采用主观估计收益率，标普500与日经225指数采用历史收益率。根据公式(39)与公式(40)，我们解得各个资产如图
3所示。  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9icAbuPmfuTSDdXH1oFDKic4qJm7NQvYThHkAI42xas5LjfuqkicXPPiaZA/640?wx_fmt=png)

从图中可以看出，如果我们对某个资产不形成任何主观观点，则BL模型中该资产权重与市场均衡权重相同。这表明BL模型下配置资产权重相较传统均值-
方差模型更稳定，收益率估计的变化对模型的影响更小。

  

**2.7 Black-Litterman模型的缺陷和学术上的改进**

****

**尽管Black-Litterman模型克服了传统均值-方差模型的诸多弊处，但实际应用中仍存在一些缺陷**
。首先，观点的准确性直接影响模型的效果，观点错误会给组合带来较大风险；其次，观点输入方式较为单一，往往需要投资者对于资产有较为具体的收益预测；再次，模型输入参数较多，个别参数取值没有统一的选取方式，也增加了实际使用难度；最后，模型假设收益率呈正态分布，与实际的尖峰厚尾分布有较大差别。针对这些问题，大量的学者对其进行了较为细致的研究并加以改进。

  

**为了解决这些问题，大量的学者对其进行了较为详细的研究。** 为了改变观点矩阵的输入方法，Edward Qian、Stephen Gorman在2001
年提出了新的模型（以下简称 QG 模型 ），将针对波动率和相关性的观点设计到了模型中；Robert Almgren、Neil
Chriss在2004年提出了将收益率排序观点进行融合的模型（以下简称AC模型）；Jacques Pezier在 2007年提出了在最小区别原则（Least
discrimination）下的相对熵模型（以下简称 P 模型）。前 KKR首席风险官Attilio Meucci提出的Entropy
Pooling模型(简称 EP 模型)在诸多模型基础上再做改进，计算方便快捷，是此类模型的集大成者。Meucci (2010) 将学术界对Black-
Litterman模型的改进进行了总结，具体见下表。我们后续会根据需要进行相应研究，本篇报告仅聚焦实现BL的原始基本模型。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9QEiboAPWkvftMqLR1n10YUbxtVRDZanOJTpEy0g9duz0tPolJX3Th2A/640?wx_fmt=png)

  

**03 Black-Litterman模型的实现  **

  

本部分介绍Black-
Litterman模型的基本实现过程。首先，我们需要对BL模型的各种参数选取、主观观点进行设定。然后，编程上主要使用python的开源包PyPortfolioOpt
1  实现Black-
Litterman模型，构建一个简单的适用于“固收+”产品的资产配置策略，并和固定权重模型、MVO模型的配置效果做了对比，验证了BL相对前两者的有效性。

  

[1] PyPortfolioOpt包主要实现了MVO、Black-Litterman模型、Hierarchical Risk
Parity模型和常用的协方差矩阵估计方法。

  

** 3.1 模型参数的设定  **

  

BL模型涉及的参数很多，而且参数的取值不同学者有多种方式。模型能否有效运作的关键在于主观观点的准确性、参数设置的合理性。但较为准确的主观观点和适当的参数设置是比较困难的。本报告作为原始基本模型的介绍文章，选取较通用的做法来讲解BL模型的构建和实现。

  

**3.1.1 设定主观观点P和Q**

  

对于常规的主观观点，由于缺乏连续的历史数据，同时很难避免上帝视角，一般来讲很难回测。本报告为了介绍BL模型的实现，这里简单
**选用资产最近一个月的资产收益率作为各大类资产的主观观点收益** ，考察

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9JTzRSBAPt6MPeoHS4phuIqg9h2HZhUIv623ibsrFpDxn4XLzzNY680w/640?wx_fmt=png)

  

**3.1.2 设定主观观点信心水平Ω**

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9mDQVQ1dXvMRj3ns5uHibrtOAqrpx6StbZPpERYibmsz0a8ribugJG2eUA/640?wx_fmt=png)

**本篇报告我们采用做法1，设定观点信心水平矩阵Ω与各个资产协方差矩阵成正比。**

**  
**

[2] 其中，第1、4种做法在PyPortfolioOpt包都有实现，可直接调用相关函数default_omega()或idzorek_method()。

  

**3.1.3 设定风险厌恶系数λ**

**  
**

对于风险厌恶系数的设定，不同学者做法不一样:

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9TLukPuxOaL9XvZEhsyWCYg7mqs5UVsaLhpEod9qMiaQZ0wsI1xianVgQ/640?wx_fmt=png)

  

** 3.2 Black-Litterman模型搭建  **

  

我们将各资产最近一个月收益作为主观观点，使用BL模型构建一个简单月度资产配置策略，来讲解模型的具体实现过程。
**策略的收益风险目标设定为：年化收益6%左右、回撤4%左右的固收+策略，其业绩比较基准为10%股票+80%债券+10%商品。**
具体编程实现上，主要使用PyPortfolioOpt包计算大类资产先验分布、观点分布和后验分布；然后使用凸优化求解Cvxopt包求解二次优化问题。

  

**3.2.1 BL模型资产配置策略**

  

**3.2.1.1.大类资产选取**

  

我们选取的投资标的为沪深300、标普500、恒生指数、中债-国债总财富（总值）指数、中债-
企业债总财富（总值）指数和南华商品指数，分别来自股票、债券和商品三种大类资产。由于中债-
企业债总财富(总值)指数数据自2006年11月20日始，故采用的数据区间为2006年11月20日至2023年1月31日。简单起见，无风险利率设定为2%。我们每月末使用BL模型、MVO模型对大类资产权重进行求解，构建相应的资产配置组合。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9b3DE9R5ic2ozaHpY72fQWKGChfogpsd9SpnQKV5fZ8YfuLicic1TnAHUQ/640?wx_fmt=png)

  

**3.2.1.2 先验预期收益Π、协方差矩阵的计算方法**

****

**（1）先验预期收益Π**

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9ibDhg7PibBjZcYhGx0KiahechMFFIVVSKRwuLrwrZ4Rpe9RlyCckCvEWA/640?wx_fmt=png)

指定（基准）权重组合的波动率为该投资者目标波动率或最大可承受的波动率。

  

**（2）协方差矩阵计算**

  

**我们使用过去五年的日收益率样本协方差作为协方差 3  的先验估计。 **
我们也对比了采用不同频率（日频、周频、月频）、不同窗口期（过去五年、三年和一年）的收益率计算的协方差矩阵，发现使用时间越长、频率越高计算的协方差矩阵估计，最终得到的资产组合效果越好。

  

[3] 除了样本协方差，PyPortfolioOpt包的risk_models模块还提供了指数加权协方差、收缩协方差（Ledoit-Wolf等）多种选择。

  

**3.2.1.3 基准策略组合和BL模型策略组合说明**

  

**两个基准策略组合。** 为了对比BL模型与传统配置模型的效果差异，我们这里构建两个基准策略：

**1) 固定权重基准策略。**
固定权重基准策略采用每月末固定各个资产类别权重的做法（80%债券、10%股票和10%商品），对单资产类别下的各个资产进行等权处理，计算策略收益。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9RZC0eNcr4UeyQDDOibcP83xlf8WRQgcSgUiartMnOuQZr4NSGGiaBgUlw/640?wx_fmt=png)

**2) BL模型策略2**
：设定在市场均衡状态下，人为给定股票、债券和商品的市场的比例(1:8:1)；在某个资产类别下我们对各个细分资产进行等权处理。根据公式(25)，我们可以反解出对于当前市场权重的风险厌恶系数，进而进行BL模型计算。当投资者的目标波动率（最大可承受的波动率）和市场组合的波动率一致时，投资者的风险厌恶系数和市场权重隐含的风险厌恶系数一致。如果投资者目标波动率小于市场组合波动率，其风险厌恶系数值会大于市场组合隐含的λ。

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9Gv6UcKuHbVZVyBxJP19U2XZqyamvCxorGb01j2rRIakPUwVwO5a3ibw/640?wx_fmt=png)

  

**3.2.1.4 特定约束下的组合优化问题**

****

我们以“固收+”
产品为例，选取80%债券、10%股票和10%商品固定权重组合作为比较基准。每月末构建资产组合时，自然的设置股票和商品类别资产上限不得超过10%的投资限制。同时，为了防止单次调仓幅度过大，我们施加了资产双边换手率不超过60%的限制。相应的最优化问题如下：

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9AL1cThMEswdiaFJeiaB2b9tOyOo2fkJpR1J9ZnxUiaFkIj2zRHHf8l93Q/640?wx_fmt=png)

  

**3.2.1.5 四个配置策略组合的结果对比**

****

历史回测发现， **两个BL模型策略在年化收益、最大回撤均优于均值-方差基准模型策略和固定权重基准策略。** 具体见下图4。整体上看，
**2012年以来BL模型策略1的年化收益为6.58%，最大回撤为3.13%，收益回撤比为2.10；BL模型策略2的年化收益为6.59%，最大回撤为2.96%，收益回撤比为2.23。**
均值方差基准策略的年化收益为5.82%，最大回撤为3.86%，收益回撤比为1.51；固定权重基准策略的年化收益为5.41%，最大回撤为3.55%，收益回撤比为1.52。分年来看，两种BL模型策略在各年均录得了正向收益，且在某些权益市场表现较好年份搏击超额收益的能力较强；在2020年、2022年基准组合出现较大回撤（-2.5%~-3.9%）时，两个BL模型策略的最大回撤（-1.2%~-1.4%）均较小，具体见下表5和表6。

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9Py5ibbFVFdE2GOfRhOy7ib7uO8sIl2TItRuEcro3JxyEAII3Elk1otew/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9kobm55Dm8btGUaJFhrY4y4l5noOUwVBd810U3x0pibYBQD3jE69dyWg/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9FtL9J4RT0z6Jrye2ew2DFJtPT6icKicMoVasic2Ce3TSemmp2JpEPYryA/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9Z3m4LeS8QNKDJfDIrPicS0fKkKt0gVrNnOiaXLPBxN9Hbp7J7mctsn3g/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9k5R9XSqrYIiaCIzfnbpFONmnxDV3RKNjeowAfCPkib075EM4HKGQcCCg/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9R02zU4dPseia4wcZa9ZsyacnN1rQatBUOzeBmTS6xCLECJQEZdE2ugQ/640?wx_fmt=png)

  

**3.2.2 不同参数取值对模型策略结果的影响**

****

下面我们展示不同参数取值对模型策略结果的影响。对于BL模型策略1，不同的参数取值（双边换手率限制、资产权重约束、风险厌恶系数）对于模型策略表现的影响；对于BL模型策略2，不同的参数取值（市场均衡权重、资产权重约束）对于模型策略表现的影响。

  

**3.2.2.1 不同的参数取值对于BL模型策略1的影响**

****

**（1）不同双边换手率限制对BL模型策略1的影响**

****

我们前面设定了双边换手率限制在60%，旨在限制BL模型和均值-方差模型在进行资产配置时出现大幅度调仓。
**下面考察不同双边换手率限制对BL模型策略1的影响。**
我们固定风险厌恶系数为10，设置股票权重上限和商品权重上限分别为10%，分别计算双边换手率为20%、40%、60%、80%、100%和无双边换手率限制时BL模型的策略表现，具体见下图8。

  

由下表7可知，当我们将双边换手限制设置较低时，由于BL模型可调仓空间较小，模型整体配置能力受到限制，BL模型策略走势与传统均值-
方差模型表现差异较小，年化收益也较低； **当双边换手率限制放宽时，BL模型策略的年化收益相应提升**
；当双边换手率无限制时时，BL模型策略充分发挥主观观点的配置效果，其回撤水平与年化收益也较为稳定。

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ93OkFLic8IlUOFxFHTofa1Vv81xQdhpfWKxWMrBAS1LnDunUDRHQ2sYQ/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ99aWpY8xo9EypKt7Z2r5KBB4iaDGCoLKjlw5ibhClJ5sHoHH1Umx7Z2QA/640?wx_fmt=png)

  

**（2）不同的资产权重约束、不同市场风险厌恶系数对BL模型策略1的影响**

  

我们前面设定了资产权重约束限制在10%。下面考察不同资产权重约束限制对BL模型策略1的影响。我们固定风险厌恶系数为10，统一设置双边换手率限制为60%。分别计算股票权重上限和商品权重上限为5%、10%、15%、20%限制时BL模型策略1的策略表现，见图9。由表7可知，结论和双边换手限制结论类似，
**股票和商品的约束上限提高为投资组合带来了更多收益的机会，但在整体上同时带来了更大的回撤和波动。**

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9owPJeAJ5iaicRDaa4YmTibRT3Izw3f96j4AOwwbx6GaVuFGBpctnjWU6g/640?wx_fmt=png)

  

风险厌恶系数体现了此时投资者对于投资组合的风险敏感程度。考察不同风险厌恶系数条件下BL模型策略1的表现情况，这里统一设置双边换手率限制为60%，见图10。由下表8可知，
**随着风险厌恶系数的提高，模型的年化波动率减小，这与1.2的结论一致。**

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9ns9NibGsH85kdiapQRC7Ux3BlfggFLqfrYrxcibLicmISricfcEQYkw2cicw/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9ZG5kORictB9l9JSfxRb7ZtJqkibgLicsVibyibYYryuibZsOZTtFx6vYCENQ/640?wx_fmt=png)

  

**3.2.2.2 不同的参数取值对于BL模型策略2的影响**

****

**（1）不同股票商品权重上限、不同市场均衡权重对BL模型2的影响**

  

根据公式(24)与公式(25)，我们尝试从给定市场均衡条件下的各个资产权重出发，反解出市场当前风险厌恶系数进行BL模型搭建，进而观察市场均衡权重对BL模型的影响。其中，公式(25)的市场无风险利率统一设置为2%。

  

**首先，考察不同资产权重约束限制对BL模型策略2的影响。**
我们固定风险厌恶系数为10，统一设置双边换手率限制为60%。分别计算股票权重上限和商品权重上限为5%、10%、15%、20%限制时BL模型策略2的策略表现，见下图11。由表9可知，结论和BL模型策略1类似，
**股票和商品的约束上限提高为投资组合带来了更多收益的机会，但在整体上同时带来了更大的回撤和波动。**

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9tPxOicSfKjI02bprMQXqy8gupyZAhDKNmgwa6MoJUeCVYbN0Y8UUicicg/640?wx_fmt=png)

  

**然后，考察不同市场均衡权重对BL模型策略2的影响。**
我们首先设定股票、债券和商品三种类别资产之间的比例。然后，在具体某个资产类别下我们对各个细分资产进行等权处理，最终得到各个资产的市场均衡权重。股债商三种类别资产的市值权重比例分别取（1:8:1）、（1.5:7:1.5）、（2:6:2）、（2.5:5:2.5）。由表8可知，如果我们预设市场均衡条件下高波动资产所占比例越高，此时对应的市场的风险厌恶系数越低，进而策略的波动性增大；反之，若降低市场均衡条件下的高波动资产所占比例，则策略的最大回撤和年化波动都能得到较好的控制。

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9r4Oh1pY4IViccBbSsHR8Jic2hicL28hx1cm7Zvothjh55jnicbayYx4LIg/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9ox0mcbwxu27kYfOvd4xTN2ox1hGvHBqxkCfiaeaNHIXib8UjISSU3akw/640?wx_fmt=png)

  

**总的来看，我们使用大类资产最近一个月收益作为主观观点构建的BL模型策略，相对于传统的MVO模型策略和固定权重策略表现较好。**
BL模型策略不仅年化收益有所提高，最大回撤与波动率都有明显降低。采用最近一个月的资产收益率作为主观观点具有一定的局限性，
**如果使用者的预测能力较高、能给出更好的主观观点，或者有更好的大类资产收益预测方法作为主观观点，BL模型的配置能力可以得到更好的展现。**

  

**04 总结  **

  

**  
**

**本篇报告作为入门文章，主要介绍了资产配置领域的经典模型——Black-Litterman模型的基本理论和计算步骤。**
首先介绍了BL模型的基础——均值方差模型，重点指出风险厌恶系数与投资者可接受最大波动率存在一定的对应关系。然后，详细介绍了BL模型的基本理论和计算过程。其中，市场均衡收益、后验分布的计算是重点，参数设置的合理性、主观观点的预测准确性是模型效果的关键。最后，将一个月动量作为主观观点，使用BL模型编程实现了一个简单的资产配置策略。历史回测表明，BL模型效果整体优于MVO模型和固定权重模型。
**其中,2012年以来BL模型策略1的年化收益为6.58%，最大回撤为3.13%；明显好于均值方差基准策略（年化收益5.82%、最大回撤3.86%）和固定权重基准策略（年化收益5.41%、最大回撤3.55%）。**

  

**本文不足之处在于**
，我们仅采用最近一个月的资产收益率作为主观观点具有一定的局限性。倘若主观观点的预测能力提升，或者有更好的大类资产收益预测量化方法作为主观观点，BL模型的配置能力可以得到更好的展现。此外，学术界对Black-
Litterman模型的改进暂时没有涉及，我们后续会根据需要进行相应研究。

  

**未来研究计划上**
，除了提高大类资产上观点（主观观点、量化观点）的准确性改进BL模型效果，也会考察模型在行业配置、因子配置上的效果。此外，我们将继续研究风险平价/预算模型、宏观因子配置等模型在国内市场上的应用。大类资产收益预测、风险（协方差矩阵）估计、股债轮动等方向也会有相关研究发布。

  

**05 参考文献  **

  

  

[1]Andrew Bevan,Kurt Winkelmann.(1998).Using the Black-Litterman Global Asset
Allocation Model: Three Years of Practical Experience. Goldman Sachs Fixed
Income Research.

[2] Black, F., & Litterman, R. (1990). Asset allocation: combining investor
views with market equilibrium. Goldman Sachs Fixed Income Research, 115(1),
7-18.

[3] Black, F., & Litterman, R. (1992). Global portfolio optimization.
Financial analysts journal, 48(5), 28-43.

[4] CVXOPT文档.http://cvxopt.org/.

[5] Idzorek, T. (2007). A step-by-step guide to the Black-Litterman model:
Incorporating user-specified confidence levels. In Forecasting expected
returns in the financial markets (pp. 17-38). Academic Press.

[6] Litterman, R., & He, G. (1999). The intuition behind black-litterman model
portfolios. Goldman Sachs Investment Management Research.

[7] Meucci, A. (2005). Risk and asset allocation (Vol. 1). New York: Springer.

[8] Meucci (2006). Beyond Black-Litterman in Practice: A Five-Step Recipe to
Input Views on non-Normal Markets, Attilio Meucci, Working paper

[9] Meucci, A. (2010). The black-litterman approach: Original model and
extensions. Shorter version in, THE ENCYCLOPEDIA OF QUANTITATIVE FINANCE,
Wiley.

[10] PyPortfolioOpt文档. https://pyportfolioopt.readthedocs.io/en/latest/.

[11] Satchell, S., & Scowcroft, A. (2000). A demystification of the
Black–Litterman model: Managing quantitative and traditional portfolio
construction. Journal of Asset Management, 1, 138-150.

[12] Walters (2009). The Black-Litterman model in detail. Available at SSRN
1314585.

[13]Yoram Lustig. (2016).资产配置投资实践.电子工业出版社.

[14] 杨朝军,周仕盈,崔彬哲.(2021).资产配置理论与实证前沿问题研究.经济管理出版社.

[15]周仕盈. (2019).长短期资产配置理论与实证问题研究.上海交通大学.

  

**06 附录  **

  

  

** 6.1 均值-方差模型效用函数的等价性推导  **

  

根据效用函数(6)，我们对其进行求导，在不对w进行限制时，我们有

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9EdJkbQ9JMMo6kqmPwwxloTrE4CVOqoEDvx7w5Kx25TFaia6jQPwvRwg/640?wx_fmt=png)

** 6.2 Idzorek方法确定主观观点信心水平Ω  **

  

Idzorek(2005)方法具体见《A step-by-step guide to the Black-Litterman
model》，大致可以分为以下几步：

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9tNHPqnVeDEmVia2YnNnVVwyIvuloGVmZvlOypwk8iaDjVibPyAml4MicYA/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9diazoD7DdoFgeZCyXFw0PRzmMJvuytV9FKcmQUZBamME1vwib7wibicLNQ/640?wx_fmt=png)

  

** 6.3 应用贝叶斯公式得到收益率后验估计  **

  

根据前面的公式(27)和公式(29)，我们可以得到先验预期收益率和主观观点的概率密度函数：

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ97icqcxckAjmGmicXHRZvQNCjBVvDpVvZY5dXOibeawNJkropR0NO8ndfA/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkS0UlcIyoNBlyFcoSiaJoNZ9QNzjX2SyQS32Xka9m88VJib4viafeaLXdsuPlibQdc0szkGcfIiahicjx0A/640?wx_fmt=png)

**07 风险提示  **

  

  

黑天鹅事件等可能导致大类资产相关性增加，资产配置组合表现不佳；量化模型基于历史数据构建，而历史规律存在失效风险；市场情况不满足模型假设，模型存在失效风险。

  

![](https://mmbiz.qpic.cn/mmbiz_gif/RJvI2iblLnkRLBoMILBNnwMPQYUkkdJdzZ9ibZF8nnic9M5piclPy81TsH67ltibg4tvjNrRFjTmdF1DwJzUs3fwW8g/640?wx_fmt=gif)

  

相关报告（点击文字可查看原文）

** 量化配置专题报告：  **

1、《 [ 出奇辅正，奇正兼修——国君量化配置团队之“研究世界观”
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247504146&idx=1&sn=0919cdb8a2d7761244bcd369e17bf9a6&chksm=c0291ebff75e97a9582bbecc01330bf7ed47d6e1c1e497a76edbefc1942d01475790e277b56e&scene=21#wechat_redirect)
》 [ （20221205）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247497158&idx=1&sn=1017dda0bbfc2168a6ffb9c2777c5098&chksm=c0293a6bf75eb37dffdc186e05e0e02f32fc5731bc4a0b645137253ce83d3078d40d08a730af&scene=21#wechat_redirect)

2、《 [ 欲速则不达，周线级回踩后方为配置良机——基于筹码分布和同位对比的视角
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247498654&idx=1&sn=0e9af2c97be8326970a87cf3e2d86a13&chksm=c0293433f75ebd25772e0f69236a3c203ff9f0ec833c9eeb2ec006ba4bf855f198ab1c2dd543&scene=21#wechat_redirect)
》 [ （20220730）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247497158&idx=1&sn=1017dda0bbfc2168a6ffb9c2777c5098&chksm=c0293a6bf75eb37dffdc186e05e0e02f32fc5731bc4a0b645137253ce83d3078d40d08a730af&scene=21#wechat_redirect)

[ 3、《从春季行情“爽约”到强力反弹“未料而至”——2022年A股中场全景式回顾与展望》（20220627）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247497158&idx=1&sn=1017dda0bbfc2168a6ffb9c2777c5098&chksm=c0293a6bf75eb37dffdc186e05e0e02f32fc5731bc4a0b645137253ce83d3078d40d08a730af&scene=21#wechat_redirect)

4、《 [ 行稳致远，做好以“拉锯战”获得最终胜利的准备
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493541&idx=1&sn=3fec346a162c0f1d8c7513ce40954a8d&chksm=c0292808f75ea11eec23ba13cdcfc3039ec54361ddcdc136b9c0e40464ddb36dfc1b09382be2&scene=21#wechat_redirect)
》（20220506）

5、 [ 《基金重仓股当前“三重困境”深度解析》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247492879&idx=1&sn=6a7515ebc285d0ad9886e74c3a916169&chksm=c0292aa2f75ea3b43d124f0036e48eec48a2bcfa853ca32331eae5e9d26f02fdbfb6c37c4468&scene=21#wechat_redirect)
（20220419）

6、 [ 《观象析理：“政策底”后的“市场底”需季度级别的等待》（20220408）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247492370&idx=1&sn=0bf03017d4f0d0a62cc595c63a5c8edc&chksm=c0292cbff75ea5a9fe91cf27f7534c5f310628b054291d16c266bee897074780ba55dfe13a05&scene=21#wechat_redirect)

7、《 [ 无悲无喜，不忌多空，市场进入战略相持期——A股市场中期走势推演
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247491294&idx=1&sn=153c243ed36053bc7f23e9363eec796d&chksm=c02ad173f75d5865ffd772b151505492b3026fc318140c8bde89a825adefcd8d933abdc2e405&scene=21#wechat_redirect)
》（20220315）

8  [ 、《俄乌局势紧张，对大类资产影响几何
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490276&idx=1&sn=d4b771a113b0bfb4c8c44c55cb2b562e&chksm=c02ad549f75d5c5f5d052df02ad957c54e051ce7992b009c0d7f75c8c492dc024da2b73ca4dd&scene=21#wechat_redirect)
[ 》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490276&idx=1&sn=d4b771a113b0bfb4c8c44c55cb2b562e&chksm=c02ad549f75d5c5f5d052df02ad957c54e051ce7992b009c0d7f75c8c492dc024da2b73ca4dd&scene=21#wechat_redirect)
（20220213）

9、 [ 《短期阳光普照，中线扑朔迷离
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490170&idx=1&sn=f46a8ae7dea9c5a0f123939ef4b7b004&chksm=c02ad5d7f75d5cc170304cb0ea28d13129fb452895eee670133bef503cc61cb021370ce218bc&scene=21#wechat_redirect)
[ 》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490170&idx=1&sn=f46a8ae7dea9c5a0f123939ef4b7b004&chksm=c02ad5d7f75d5cc170304cb0ea28d13129fb452895eee670133bef503cc61cb021370ce218bc&scene=21#wechat_redirect)
（20220207）  

10 [ 、《二次探底：中概互联板块配置机会再现
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490041&idx=1&sn=36361da4b4cf564e5ae42a8d0e70f520&chksm=c02ad654f75d5f426b8e076b93af5d12f61e63c9a0e0519ee164ff6bb73d24768388e72be05c&scene=21#wechat_redirect)
[ 》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490041&idx=1&sn=36361da4b4cf564e5ae42a8d0e70f520&chksm=c02ad654f75d5f426b8e076b93af5d12f61e63c9a0e0519ee164ff6bb73d24768388e72be05c&scene=21#wechat_redirect)
（20220202）

11、《 [ 上证50进入“二次探底”阶段，配置价值再度显现
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247489876&idx=1&sn=fd430b9f843767d9db88bb25344feeca&chksm=c02ad6f9f75d5fefdefab1aa98ffa873a6e1cb669d5474fedb3b75eb3d6e2b1bf6e15e2db8af&scene=21#wechat_redirect)
》（20220127）

12、《 [ 一念之间：上证指数正处于技术上的关键节点》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247489511&idx=1&sn=e1198f4a8d0c46d40f10ee409245a4a5&chksm=c02ad84af75d515c0e47675eab9a13c6bb133527644964d6d826d4c1d4fc517c8966d6bdcf8b&scene=21#wechat_redirect)
（20220117）  

13、《 [ 否极泰来：中概互联板块配置价值逐渐显现
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247488769&idx=1&sn=345becafb1713df1c18c99afd284df97&chksm=c02adaacf75d53ba64d79c34f4f972cef00ab4896a13d46b2c85ccd7514e1889cddf1f6cd14d&scene=21#wechat_redirect)
》（20211224）

14、《 [ 周期股配置逻辑：反弹还是反转
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247488750&idx=1&sn=623370b9f45abec2850e576d84f1e3a6&chksm=c02adb43f75d525590c8a853e01c162c2237d61ed91910488c817c97580d50cc372f1b5a2f21&scene=21#wechat_redirect)
》（20211222）

15、《 [ A股战场形势变化，胜利天平逐渐转向多头
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247487822&idx=1&sn=95d4b9d54d967a0d858f8be9dbe9296a&chksm=c02adee3f75d57f5aee0d28a1fd4fd800ed4caee103d96b0e99a57c7674c8c2ab9807068e88b&scene=21#wechat_redirect)
》（20211207）

16  [ 、《上证50配置时点渐行渐近》（20211120）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247486849&idx=1&sn=4dd5ee487bd780a1a7a947e165bc177c&chksm=c02ac22cf75d4b3ad64ddf9ea28ef9e7a7e2981a9af9e0a2374111ee7939fccb0054302cca97&scene=21#wechat_redirect)

17、 [ 《券商板块将成为跨年行情的胜负手》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247486738&idx=1&sn=c5b33743ffa25e35a7049c665a3fb99f&chksm=c02ac2bff75d4ba9e5f79a5592e12b97404efd1fa2cbf0aedf08701e1458a48cb37883e510e9&scene=21#wechat_redirect)
（20211119）

18、 [ 《投资者适当性门槛下降，北交所微观结构大幅改善》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247486046&idx=1&sn=314921e52b830fa04c7e38fd154c8a8c&chksm=c02ac5f3f75d4ce5a11bb3ad25abd957596838cd2b2ebda28664564bfdfa49fa31446bc939cd&scene=21#wechat_redirect)
（20211021）  

19、 [ 《论两次“3700点回调”的不同之处》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247485311&idx=1&sn=f7f6db52fc59d0a3131d8181ac2a5c80&chksm=c02ac8d2f75d41c49fb572577057f71c6a29adc862484ff7525eca8fbc1426117c0c5e3dcae1&scene=21#wechat_redirect)
（20211005）  

20、 [ 《三论券商配置逻辑——基于交易和量化视角》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247485067&idx=1&sn=e62b881e838f691d2fdcdaff08a674e7&chksm=c02ac926f75d4030572dafebcf1bc7a6f287154fce98db2832412390c9095da955d0dadac7ac&scene=21#wechat_redirect)
（20210921）  

21  、  [ 《再论券商配置逻辑》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247484728&idx=1&sn=9c2ff8d50a748ef06b1d4e230e998e2c&chksm=c02aca95f75d4383152acd8fa68066f93a14ebb23013bacd075a5400dc8e1fd2a6ba3273e127&scene=21#wechat_redirect)
（20210905）

22、《  [ 风从虎，云从龙，券商配置正当时
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247484140&idx=1&sn=609cefd82c2b31a1daa228cfa89ca6f5&chksm=c02acd41f75d4457e66a2fccc24a27ace6af74f740caed810e3426e196930caa237bad1d6bab&scene=21#wechat_redirect)
》（20210813）

  

** A股市场运行周报：  **

1、《 [ 市场遭遇“低气压带”，保持耐心“两手准备”——72
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247508425&idx=1&sn=556591c3aa278e540d0f56b5d2c9dd75&chksm=c0296e64f75ee7720d255ea86170ddb0fc9a74ca2cb84de34fe90281d161a17ae89b37a17934&scene=21#wechat_redirect)
》  （20230401  ）

2、《 [ 大盘如期止跌回稳，后续关注反弹节奏——71
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247508241&idx=1&sn=86c905720e4ef14c1fa6c9972d3efb49&chksm=c0296ebcf75ee7aa50f1ad383fe72cbb0df04f93c25d707181cd38932961d33aab49d2c8ce4b&scene=21#wechat_redirect)
》  （20230325  ）

3、《 [ 权重指数逐步企稳，有望护航大盘开启反弹——70
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507744&idx=1&sn=36d84b287e891213c16c1ae856f7dfeb&chksm=c029108df75e999b9b85236803822436d9e81649dd692262be32bb4da00a0e4aeb1acc49b6ed&scene=21#wechat_redirect)
》  （20230318  ）

4、《 [ “预期偏差”导致向下变盘，不急不过应对调整——69
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507479&idx=1&sn=7ddd94cdbbf37d0a1da7b546bac39dee&chksm=c02911baf75e98ac8c2fd659899de70f93fd9ad606516154a18cad8b73cf59105b1e3f38b99b&scene=21#wechat_redirect)
》  （20230312  ）

5、《 [ “兔子”出现成功“撒鹰”，持仓静待后续变化——68
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507065&idx=1&sn=eda28b188e2924df442e920bad5a6d6e&chksm=c02913d4f75e9ac2c6f4df32a5d583d75d13d1fe128705dd74fb5b43d2c181532d4cadb1383c&scene=21#wechat_redirect)
》  （20230304  ）

  

**国君配置QIA-Timing模拟策略：**

1、《 [ 关注消费、新能源等板块的配置机会——（202303）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507286&idx=1&sn=174bca154c7554fe85d5a3a5522aa52b&chksm=c02912fbf75e9bed608da5e87d178666be03ebf1bc22c7baa98f1c416fa377b50755bd240bf1&scene=21#wechat_redirect)
》（20230307）

2、《 [ 关注消费、新能源等板块的配置机会——（202302
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505732&idx=1&sn=c543cba9e78efce2d0c6192dbf85f9eb&chksm=c02918e9f75e91ff177a541835ec99c39ef069a8b1c5e38fcea650473dea68a46df6ae603e21&scene=21#wechat_redirect)
）》（20230202）

3、  《  关注消费、新能源等板块的配置机会——03  》（20230105）

  

** 大类资产 [ 配置研究系列
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)
：  **

[ 1、《大类资产配置体系简析——之一》（20230322）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507957&idx=1&sn=0bd82f2cc513709f51ac2d6fda688775&chksm=c0291058f75e994ed6f5e40a2eddbacdc7b3da77a56d148ef8ff105a0dea551dc43200fcd291&scene=21#wechat_redirect)

  

** 量化择时  ** ** [ 研究系列
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)
：  **

1、  ** 《  ** [ 宽基指数如何择时：通过估值、流动性和拥挤度构建量化择时策略——01
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247508702&idx=1&sn=82226c13e3768ddd886662e994793f5f&chksm=c0296d73f75ee465f3055f21f13881d24672155a8de662593b256dbf72716e6f14de6e867aa4&scene=21#wechat_redirect)
** [
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247508702&idx=1&sn=82226c13e3768ddd886662e994793f5f&chksm=c0296d73f75ee465f3055f21f13881d24672155a8de662593b256dbf72716e6f14de6e867aa4&scene=21#wechat_redirect)
》 [
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507957&idx=1&sn=0bd82f2cc513709f51ac2d6fda688775&chksm=c0291058f75e994ed6f5e40a2eddbacdc7b3da77a56d148ef8ff105a0dea551dc43200fcd291&scene=21#wechat_redirect)
** [ （20230405）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507957&idx=1&sn=0bd82f2cc513709f51ac2d6fda688775&chksm=c0291058f75e994ed6f5e40a2eddbacdc7b3da77a56d148ef8ff105a0dea551dc43200fcd291&scene=21#wechat_redirect)

  

** [ 行业配置研究系列
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)
：  **

[ 1、《基金持仓还原在行业轮动上的应用——07》（20221125）  **  
**
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247503847&idx=1&sn=dc8af71773b25d7c49d03fe9a28a12f6&chksm=c029004af75e895caa30be11a2e3d7e5f74641f41782a3d00048436182ce9066a065de77822d&scene=21#wechat_redirect)

[ 2、《如何基于分析师预测数据构建行业轮动策略——06》（20221011）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247502192&idx=1&sn=feb14f8f5f16116f75c3d0ec41f0d41e&chksm=c02906ddf75e8fcb19dc63b85617b9516056c7f5db07ffa91c7114ce2384b74e9c3b68f819bb&scene=21#wechat_redirect)

3、《 [ 如何规避交易拥挤行业：通过拥挤度构建行业轮动策略——05
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247501615&idx=1&sn=27149134f26a64ae630241e07949c19b&chksm=c0290882f75e81941d8dabf377d3d4ea723c5718bf61f5764820fee307028171e887af6e19f1&scene=21#wechat_redirect)
》 [ （20220919）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)

4、《 [ 如何使用业绩预告和业绩快报改进景气度行业轮动模型——04
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247495978&idx=1&sn=3495988ac0ff4d5c493c6eb5bb08eb4f&chksm=c0293e87f75eb791835bde4da01fae93e4c44fc73fa7459f2cbfa65bac3686eda9db7a605c5d&scene=21#wechat_redirect)
》 [ （20220614）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)

[ 5、《
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247495391&idx=1&sn=3d11645bf38bce019898196d2f27fd46&chksm=c0292172f75ea86432b272e6d91168f40507c3dbc7a85e8c682b5f9281a879d014caaa7bb452&scene=21#wechat_redirect)
[ 如何基于北向资金构建行业轮动策略——03
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247495391&idx=1&sn=3d11645bf38bce019898196d2f27fd46&chksm=c0292172f75ea86432b272e6d91168f40507c3dbc7a85e8c682b5f9281a879d014caaa7bb452&scene=21#wechat_redirect)
[ 》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247495391&idx=1&sn=3d11645bf38bce019898196d2f27fd46&chksm=c0292172f75ea86432b272e6d91168f40507c3dbc7a85e8c682b5f9281a879d014caaa7bb452&scene=21#wechat_redirect)
[ （20220610）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)

[ 6、《如何基于PEAD超预期因子构建行业轮动策略——02》（20220426）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)

7 [ 、《如何基于景气度构建行业轮动策略——01》（20220412）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247492606&idx=1&sn=a718dbed9361373e255dda20f25f2674&chksm=c0292c53f75ea545257ffcbe8feb0f3b393dd3139bee319d55936ed0f7ab52e624063cfe7fa6&scene=21#wechat_redirect)

  

** 量化行业配置月报：  **

[ 1、  《2月电新板块拖累组合表现，商贸零售板块两次触发交易拥挤信号  ——9  》  （20230302）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507026&idx=1&sn=05eec13ce86d5d8a9db8eba4f3166ef2&chksm=c02913fff75e9ae9ab4f0c9636653d14e36543422d633ee821377fb8fac0097af4305cedba6a&scene=21#wechat_redirect)

2、《 [ 行业轮动景气度模型1月超额1.27%，消费者服务板块触发交易拥挤信号——8
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505732&idx=2&sn=23258ca650f4f25b37169361516268fe&chksm=c02918e9f75e91ff27901b9e1452bd80df8b26965e34135ce58ec3506b1d389a3b79cef16fec&scene=21#wechat_redirect)
》  （20230201）

3、  [ 《  12月行业轮动景气度模型表现较好，超额收益2.71%——7  》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505127&idx=2&sn=8808b88546c2735adac8a426ff038fb9&chksm=c0291b4af75e925c1a244e6a813680e6a02286087ee970159e7541c13d3aa09711cde3a308a6&scene=21#wechat_redirect)
（20230103）

** **

  

** [ 权益配置因子研究系列
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)
：  **

** 1、《  ** ** [ 使用基本面因子构建中证500指数增强策略初探——02
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247497923&idx=1&sn=cb920338a0844f9f969d5e21e663dbf2&chksm=c029376ef75ebe78187452a46d46231e9f8f09f7328ad859e2702715fe3a5848e9b73e5a79c3&scene=21#wechat_redirect)
》  ** ** （20220721）  **

2、《 [ 基于PEAD效应的超预期因子选股效果如何——01
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247494566&idx=2&sn=8bdbb5c1ac102325b4e274f0b47d0f81&chksm=c029240bf75ead1d5602a56bd176fa62691a65f7102dfe7a5fef109b48e3119580f2255567e7&scene=21#wechat_redirect)
》  [ （20220601）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493072&idx=1&sn=42cd70a2d992f4a75dae6639b2342242&chksm=c0292a7df75ea36bf7484f6b586d2cbfc8565f66b677fa55eaeeccc1f7cafd7f7b104e9e3617&scene=21#wechat_redirect)

  

**配置模型与方法系列：**  

1、《  [ 论指数的“价值守恒律”
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247494065&idx=1&sn=ebfac19f2f81a66070e2590211676160&chksm=c029261cf75eaf0a4edc718c6619b19e9ada647e9d728e693616908dd1f8987758825a321c1b&scene=21#wechat_redirect)
》（20220524）

2、  [ 《如何使用换手率进行大盘“顶底识别”》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247484887&idx=1&sn=4b9049120b79ce5f95627014323982e2&chksm=c02aca7af75d436cb718b4a1cd9e9d40bb57c2663e7af67d1c6e91ce6f4c48d4d3a6fe754139&scene=21#wechat_redirect)
（20210911）

  

** 权益因子观察周报：  **

[ 1
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505089&idx=1&sn=21ceff40301137cc5b4e11ae35409166&chksm=c0291b6cf75e927a9eef9aca08ac648ed58cf1efbb1efb557c7a930096ef4e81ac92531cbc1c&scene=21#wechat_redirect)
、《 [ 北向因子效果较好，小市值因子回撤较大——44
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247508569&idx=1&sn=91b9a9de10659f9e858737397f8fc6c7&chksm=c0296df4f75ee4e2209ca7b7ba4750797671b3f8a5facea5b41a9cdfd075cc44228b1921fd36&scene=21#wechat_redirect)
》  （  20230403  ）

2、《 [ 价量、分析师因子表现较好，成长类因子效果不佳——43
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247508402&idx=2&sn=9710483ad60641fad2db3c9c96c283fc&chksm=c0296e1ff75ee70925e800ea921ece09b4f01720e9caefa1b8605e894d26c6684120893ed4bb&scene=21#wechat_redirect)
》  （  20230328  ）

3、《 [ 估值、价量因子表现较好，基本面因子效果不佳——42
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507922&idx=2&sn=71fce79c32876143def8fe83a4e3d059&chksm=c029107ff75e9969cd6776ce7e8d7282cd3197216a52f37e75fe42173f5a74bd040916ccb272&scene=21#wechat_redirect)
》  （  20230320  ）

  

** 资产相对吸引力月报：  **

[ 1、  《2月权益指数分化，配对交易机会初现  ——2023年2月  》  （20230303）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507043&idx=2&sn=11bf00764763d05d6bb79e73f0b5521c&chksm=c02913cef75e9ad868bc6339b5d01753495b30db87b2eb759fba0396d0969d2d1517b290517f&scene=21#wechat_redirect)

2、《 [ 1 月权益全面反弹，市值偏好切换初现——2023年1月
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505732&idx=3&sn=5950be3b4f9d814e133b9c91833b059a&chksm=c02918e9f75e91ff1e86769ba9f4cf329dd9fa6d62c6f1beb5c73ab3bfc8f632eb2334b3da2d&scene=21#wechat_redirect)
》 [ （20230202）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505127&idx=3&sn=6b2be5c20e4e1918dfe1592f024f1c70&chksm=c0291b4af75e925cf978d3e7a3840a3664daab89bd4d65eceeda7452821fae61b1d7b4d9c00c&scene=21#wechat_redirect)
**  
**

3 [ 、《  12月商品领涨大类资产，复苏板块优势明显——2022年12月》（20230103）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505127&idx=3&sn=6b2be5c20e4e1918dfe1592f024f1c70&chksm=c0291b4af75e925cf978d3e7a3840a3664daab89bd4d65eceeda7452821fae61b1d7b4d9c00c&scene=21#wechat_redirect)

  

** 市场点评：  **

[ 1、《市场估值已进入底部区间，勿要过度恐慌——4月25日》（20220425）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247492985&idx=1&sn=34373da6a305447df8bf2a3126b02953&chksm=c0292ad4f75ea3c2df391dd430edb1bea616e28b369bc23ee8a491c62017b4c1e736ab844b10&scene=21#wechat_redirect)

[ 2、《“政策底”信号已现，“市场底”未来可期——3月16日》（20220317）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247491330&idx=1&sn=af9024012696b951830bf810f9778f96&chksm=c02ad0aff75d59b9049e1c557c5ffbdb863761d1b73a1bb6148f9869d3940db3c7e464c41f53&scene=21#wechat_redirect)

3、《 [ 风物长宜放眼量，静待中概互联价值回归——3月10日
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247491139&idx=1&sn=34f523f078c2b68c2e7b20c75d36fe76&chksm=c02ad1eef75d58f87db1aeb01247c2dedb390d4bac1f768dc78c276b5708f18eb794dc7ea1f9&scene=21#wechat_redirect)
》（20220310）

[ 4、《情绪低迷下“多杀多”不可取，建议就地卧倒等待反弹——3月9日》（20220309）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247491069&idx=1&sn=7a6e2f8e3d77a47cc75a8c9868029338&chksm=c02ad250f75d5b4614d80c8b91a5b8a65c540122a404513412b54de9e240d8409345016231e7&scene=21#wechat_redirect)

5 [ 、《“深蹲”正是配置时——2月14日》（20220215）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490345&idx=1&sn=ef8de8a9097bf10820137b7aa2206613&chksm=c02ad484f75d5d92f04f5bcebcc3316adab20d750634e5dde22c976d7720db9968b890d5a983&scene=21#wechat_redirect)

  

** 大类资产配置展望报告：  **

[ 1、《市场遭遇“低气压带”，保持耐心“两手准备”——2023年4月》（20230404）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247508574&idx=1&sn=afd31f729d711a54f7366f728bae0e01&chksm=c0296df3f75ee4e5ca36cc47bebd8faad4b9089981d1ce389d5650a2dc5bbf570df956a89447&scene=21#wechat_redirect)

2、《 [ 不悲不喜，变盘节点做好应对——2023年3月
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247507177&idx=1&sn=b8d2fe902f08075b1a5bc76d14ff809c&chksm=c0291344f75e9a52c7fa9069afcc1a5b02d850450c24960f500477eab8cccab76161e464dd8a&scene=21#wechat_redirect)
》 [ （20230305）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505127&idx=3&sn=6b2be5c20e4e1918dfe1592f024f1c70&chksm=c0291b4af75e925cf978d3e7a3840a3664daab89bd4d65eceeda7452821fae61b1d7b4d9c00c&scene=21#wechat_redirect)

3、《 [ 节奏为王——2023年春季大类资产走势展望
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505997&idx=1&sn=2dc1b55fe97351c32efaf9aa0377b276&chksm=c02917e0f75e9ef6245a2c5496d07581068eaa03ea7d0ee2ebcca264e0d9c85c1b1424130728&scene=21#wechat_redirect)
》 [ （20230206）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247505127&idx=3&sn=6b2be5c20e4e1918dfe1592f024f1c70&chksm=c0291b4af75e925cf978d3e7a3840a3664daab89bd4d65eceeda7452821fae61b1d7b4d9c00c&scene=21#wechat_redirect)

4、《 [ 前路已定，而今迈步从头越——2023年大类资产走势展望
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247504201&idx=1&sn=eee4c2e34ab44a5a60a8e981ec468740&chksm=c0291ee4f75e97f21b92fbcde548944299c5fa22ae4045f94c8f8b5b044a76a58d888b7635c5&scene=21#wechat_redirect)
》 [ （20221207）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247500819&idx=1&sn=dc03dd55c5fcdbb86f5bd75abd8bef40&chksm=c0290bbef75e82a86a6a599d512ea6e0bb76704a75100334e0b6f987097e7d6e363ac77e8922&scene=21#wechat_redirect)

5、《 [ 权重指数艰难筑底，仓轻觅机、仓重等待——2022年10月
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247502174&idx=1&sn=7701f8309c3911b697edc65a314fd498&chksm=c02906f3f75e8fe54c3850b5f55d0c7276fd6aa30b883d6e1e8df14adc62e091c3644346c38b&scene=21#wechat_redirect)
》 [ （20221010）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247500819&idx=1&sn=dc03dd55c5fcdbb86f5bd75abd8bef40&chksm=c0290bbef75e82a86a6a599d512ea6e0bb76704a75100334e0b6f987097e7d6e363ac77e8922&scene=21#wechat_redirect)

6、 [ 《两手打算、以守为主，做好回调上车准备——2022年9月》  （20220831）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247500819&idx=1&sn=dc03dd55c5fcdbb86f5bd75abd8bef40&chksm=c0290bbef75e82a86a6a599d512ea6e0bb76704a75100334e0b6f987097e7d6e363ac77e8922&scene=21#wechat_redirect)

7、 [ 《攻防两端短兵相接，调仓换股做好准备——2022年8月》（20220801）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247499023&idx=1&sn=a4867f6f6101aa0deff09fe6996148f7&chksm=c02932a2f75ebbb43a605b07da007a03e13729cc5d50c5cc25b3733b2f2f30dedad1359b2957&scene=21#wechat_redirect)

8  、《  [ 反弹后段注重节奏，行一观三未雨绸缪——2022年7月
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247497386&idx=1&sn=0606c50a050e34af601d8380a57f33f3&chksm=c0293907f75eb011b7d33ede9c58f1ec79062ccfd710bff84d5d0cbc944bc0e4db4566fc9bc4&scene=21#wechat_redirect)
》（20220704）

9 [ 、《反弹半渡莫要追高，借机优化行业配置——2022年年中展望》（20220613）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247495836&idx=1&sn=276e1302683df5d0bbf3e9fa39a24ff0&chksm=c0293f31f75eb62722f680cf95f3b1f866e0501ccf8daa4edf5eef16447e03262fa9a54b97dc&scene=21#wechat_redirect)

10、 **《** [ 反弹半渡莫要贪胜，借机优化行业配置——2022年6月 **》**
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247494448&idx=1&sn=bf64854707c3b15bdb2209309dc4d5a0&chksm=c029249df75ead8b12f336672bd6ffb3a2d285da98cbdefdfd9757f1a55939459bd155b2ee71&scene=21#wechat_redirect)
（20220531）

[ 11、《坚信长期向上趋势，做好中期“拉锯战”准备——2022年5月
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247493506&idx=1&sn=8c73f468054f532ca4aee5b474b6eb86&chksm=c029282ff75ea139fbd4b9f8db522683d7e32a8502d25027fb49116102035b52273cf4af7962&scene=21#wechat_redirect)
》（20220505）  

12、 [ 《战略相持——2022年夏季展望》（20220401）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247491943&idx=1&sn=ebe088039cf80b800ebc54be7cf9f591&chksm=c0292ecaf75ea7dc8c5031a7a14ed28ddfd019d3379092e61377d12ddba8b767122599790ba2&scene=21#wechat_redirect)

13、《 [ 两会预期利于短期反弹，中线受损仍需二次探底——2022年3月
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247490832&idx=1&sn=b08f3dbc8b6d05ab56ca1fce16908e67&chksm=c02ad2bdf75d5bab7d836300eea1864e963f31794aa6f63cd3c68c7b0b005d9217ff884d34c4&scene=21#wechat_redirect)
》（20220301）

14 [ 、《人心齐，泰山移，春季行情一触即发——2022年
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247489002&idx=1&sn=b8d6a16355c350f0a1e59d3133315f00&chksm=c02ada47f75d53516bd27b6eebba362f1687de2fcb2672b44e3750f4e31a4e3ade53aa5d83f6&scene=21#wechat_redirect)
春季展望》  （20220103）

15 [ 、《开往春天的列车将至，机会在于前半程——2022年年度展望》（20211125）
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247487095&idx=1&sn=f0b085a17f893ff9d89a763b1882fa5f&chksm=c02ac1daf75d48cc5981743df793a5781b10df9a71c4bcf119caefa519d8b6c1319c011b26c0&scene=21#wechat_redirect)  

16、 [ 《短期上攻受阻，市场年底前或保持震荡整理格局——2021年11月》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247486227&idx=1&sn=5c1eb6fab65f22f2dfc42d13def836df&chksm=c02ac4bef75d4da87219272ce2987e38c6de8935f6590aeb54bea997612f62325f28c0bcb7d1&scene=21#wechat_redirect)
（20211030）

17、 [ 《不惧短期调整，继续看好四季度A股行情——2021年10月》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247485447&idx=1&sn=bb1ebf70f2883ec7714985b2409c4441&chksm=c02ac7aaf75d4ebc1e213ee32ce10b09a09a2656f554421d9ff4c1f073a237b04ccc242c29d1&scene=21#wechat_redirect)
（20211007）

18、 [ 《A股渐入佳境，9月起有望开启新一轮攻势——2021年9月》
](http://mp.weixin.qq.com/s?__biz=Mzg5MzY1NTc0Ng==&mid=2247484502&idx=1&sn=6d11dcecad15a5a22deaf8ea7a10a936&chksm=c02acbfbf75d42ed26db767cf24cfd5be9803da9f1605297a5fcbc5fc0cf11350c7dfdcae7e8&scene=21#wechat_redirect)
（20210901）

  

![](https://mmbiz.qpic.cn/mmbiz_png/RJvI2iblLnkRaqFAUlmPOVQsxLDicnc02KpJgTVoXJbGd4YS5RtlEQeoS1rUvg8BPanbs77EsAjAJf1NVZvN99Kg/640?wx_fmt=png)

**  
**

**法律声明：**

  

本公众订阅号(微信号:
ljcasset)为国泰君安证券研究所量化配置研究团队依法设立并运营的微信公众订阅号。本团队负责人廖静池具备证券投资咨询（分析师）执业资格，资格证书编号为
S0880522090003  。

  

本订阅号不是国泰君安证券研究报告发布平台。本订阅号所载内容均来自于国泰君安证券研究所已正式发布的研究报告，如需了解详细的证券研究信息，请具体参见国泰君安证券研究所发布的完整报告。本订阅号推送的信息仅限完整报告发布当日有效，发布日后推送的信息受限于相关因素的更新而不再准确或者失效的，本订阅号不承担更新推送信息或另行通知义务，后续更新信息以国泰君安证券研究所正式发布的研究报告为准。

  

本订阅号所载内容仅面向国泰君安证券研究服务签约客户。因本资料暂时无法设置访问限制，根据《证券期货投资者适当性管理办法》的要求，若您并非国泰君安证券研究服务签约客户，为控制投资风险，还请取消关注，请勿订阅、接收或使用本订阅号中的任何信息。如有不便，敬请谅解。

  

市场有风险，投资需谨慎。在任何情况下，本订阅号中信息或所表述的意见均不构成对任何人的投资建议。在决定投资前，如有需要，投资者务必向专业人士咨询并谨慎决策。国泰君安证券及本订阅号运营团队不对任何人因使用本订阅号所载任何内容所引致的任何损失负任何责任。

  

本订阅号所载内容版权仅为国泰君安证券所有。任何机构和个人未经书面许可不得以任何形式翻版、复制、转载、刊登、发表、篡改或者引用，如因侵权行为给国泰君安证券研究所造成任何直接或间接的损失，国泰君安证券研究所保留追究一切法律责任的权利。

  

  

  

预览时标签不可点









****



****



****





__









