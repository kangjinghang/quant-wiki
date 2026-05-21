![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhTPJAplVS26HZp86o5cKrTNmpfNrNktmR93LqK59D2A0iaSQoEF1DATw/0?wx_fmt=jpeg)

#  【方正金工】资产配置研究系列之一：通过风险平价与Black-Litterman打造稳定收益组合

方正金工  方正金工  [ 金工严选 ](javascript:void\(0\);)

_2019年12月03日 15:52_ __ _ _ _ _

在小说阅读器读本章

去阅读

** 报告摘要  **

➢  **经典模型的扩展与融合**  

传统均值方差模型尽管能够充分利用资产的预期收益率和协方差信息，但由于收益率难以估计以及模型敏感性较高的问题，实际效果较为一般；
B-L模型通过对资产的先验权重反推出先验收益率，再结合新的观点形成后验收益率，有效解决了收益率难以预测以及敏感性高的问题；
风险配置类模型仅从资产的历史协方差来构建模型，虽然能够有效控制策略的波动，但相应的收益率却比较低。  我们在  B-L
模型的框架下，以风险平价策略权重作为先验权重，叠加短期动量作为观点，得到资产的后验收益率分布并进行均值方差最优化。
同时加入跟踪误差的约束来控制策略的波动。

  

**➢** **** 基于风险平价和Black-Litterman的资产配置策略  ** **

股债配置策略：

股债RPBL(1%)策略属于低波动策略，年化波动率3.12%，年化收益率5.74%，风险调整后收益1.84，相比股债风险平价有小幅提升；股债RPBL策略属于高波动策略，年化收益率10.13%，最大回撤仅为-6.86%。

股票、债券、商品、海外四资产配置策略：

四资产RPBL(1%)策略属于低波动策略，年化波动率3.53%，年化收益率6.59%，风险调整后收益1.87，相比四资产风险平价有大幅提升；四资产RPBL策略属于高波动策略，年化收益率14.67%，最大回撤仅为-6.82%。
** 从经典资产配置模型出发  ** **  
** **1**

Hallerbach(2015)在《Risk-Based and Factor
Investing》一书中提出了“资产配置决策倒金字塔”的概念。他指出，从经典资产配置模型中的简单等权策略到最大夏普比率策略，构建策略时所需要预测的信息不断增加。比如，在倒金字塔底部，如果构建等权策略，不需要掌握任何资产的收益率和协方差信息就可以实现。往上一层，如果想要通过波动率倒数加权策略适度分散风险，则需要对资产的波动率进行预测；再往上一层，如果还能够预测资产间的相关系数，即掌握完整的协方差矩阵，就可以构建最小波动率、最大分散化和风险平价策略。最后，如果能够同时预测资产的收益率和协方差矩阵，就可以利用这些信息来构建均值方差、最大夏普比率和Black-
Litterman等模型。
![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhgjal9pWnch25brkD7cedVPAeA9XVibXFI6OPwUibYu91BibiaUUkf5Icibg/640?wx_fmt=png)

根据这一思路，我们将经典资产配置模型分为两类。一类是需要同时掌握资产的收益率和协方差信息才能够构建的“均值方差类模型”；另一类是不需要预测收益率，完全从风险的角度进行配置的“风险配置类模型”。下面我们将分别对上述模型的特点进行分析。  

** **均值方差类模型分析** ** **  
** **2**

均值方差模型的本质是对下列目标函数进行最优化，通过最大化投资者效用求出各资产的最优投资比例：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhY8ib4cHFwl2AyVVQORkYTCaVpGOsN3uzGrrbT9M2hL9t3xA9LEXG00g/640?wx_fmt=png)

对于最大夏普比率策略，其目标函数变为：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhXJt73Jc4nrhNGEp36shpI8zicgkFPGpct425LZBia2pHRyGEnLUouexQ/640?wx_fmt=png)

其中，μ  表示各资产的期望收益率向量，Σ表示各资产的协方差矩阵，δ表示投资者的风险厌恶系数，ω则是各资产在投资组合中的配置权重。

均值方差类模型的优势在于能够充分利用资产的预期收益和协方差的信息来最大化组合的收益风险比或者投资者效用，但其缺陷同样明显。

** 2.1  资产的收益率难以预测 **  

在实际投资中，除了债券以外的其他资产的价格波幅较大。从2014年以来各类资产滚动过去十年的年化收益率来看，债券资产的年化收益率基本在3%到4%之间，黄金在5%到10%之间，而以中证800指数代表的A股和以标普500指数代表的美股的年化收益率波动幅度非常大。另外，如果站在当前分别计算各类资产过去6年到10年的年化收益率，除了债券资产的收益率比较稳定以外，其他资产在不同区间内的年化收益率的差异非常大。从这两个角度来看，资产的预期收益率难以估计。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhd8myibLXzzcwiagBxd9qbymfYibEVNVcAP5KyzrhGB4tw9mduc9TLJibpg/640?wx_fmt=png)

** 2.2  最优化过程对收益率较为敏感 ** ** **

同时，均值方差模型的最优化过程对期望收益率的预测非常敏感。Chopra和Ziemba（1993）的研究表明，对资产收益率的估计误差带来的效用损失远远高于协方差；风险厌恶水平越高，对收益率的估计误差越敏感，效用损失越大。举例来说，假设我们对各资产的预期收益率的估计为预期1，将其输入均值方差模型后可得到各资产的权重为配置1。如果我们对中证800和标普500的收益率估计分别下调2%和上调2%，输入均值方差模型后可以得到各资产的权重如配置2。我们发现，不仅中证800和标普500的权重发生了变化，连带债券和黄金资产的权重也同样改变了，但这种结果很难被投资者所接受。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhG0hR78iaIDQB9ZHkMbpb7DIldm9ibwMuBDhXAEO3nPC2mgKIFlQibB0eg/640?wx_fmt=png)

** 2.3  实际投资中难以分散风险 ** ** ** ** **

最后，均值方差模型得到的资产权重过度集中且调整幅度较大，在实际投资中难以达到风险分散的效果。在最优化过程中，模型容易算出极端大或极端小的权重。在无卖空限制条件下，模型经常导致在一些资产上有很大的空头头寸，但如果限制不能卖空和放杠杆，均值方差模型就会在部分资产上的权重为0，同时在另一些资产上的权重过大，导致资产配置过度集中的现象。因此，当市场发生大幅波动时，均值方差模型可能会面临较大回撤。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhKWm5rIvCIm8KDVrSHA9eqd2qTJxRoZAV88dEDyuCviadvnsBEj0rqzw/640?wx_fmt=png)  

** 2.4  Black-Litterman模型的改进 ** ** **

Black和Litterman在1992年提出了Black-
Litterman模型。与均值方差模型相比，B-L模型不需要直接预测资产的收益率，而是在贝叶斯框架下通过对先验收益率和观点收益率的分布进行合成得到后验收益率的分布，再将其输入均值方差模型来计算各类资产的权重。

B-L模型的第一步是计算资产的先验收益率。传统B-
L模型从市场供需出发，使用各类资产的市值占比作为其先验权重。假设资产收益率服从正态分布，在均值方差模型下就可以反推出各类资产的先验期望收益率：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjh1nm5xDEGI5WfKTJAADC1efI3Ka8OBsibFVdU3FMeP28JCRIULIESWsg/640?wx_fmt=png)

第二步是对资产收益率进行预测后形成新的观点，观点可以是对每类资产都有一个收益率的预测，也可以是对资产间的收益率之差进行预测。同样假设其服从正态分布，因此需要对观点的不确定性进行刻画。观点矩阵为：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhWMdCiaetFAzWHa8LgGx2vPK2uThuFXNSmL5aPNoib095BZHcDEU5em6A/640?wx_fmt=png)

其中P为观点系数矩阵，如果是对每一类资产都有一个预测，则P为对角阵；Q为观点的预测值。代表预测观点不确定性的矩阵为Ω，如果假设每个观点之间是独立的，则  Ω
为对角阵。  

第三步是根据贝叶斯公式计算后验收益率分布：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhKGDfjnKmjSuFNtibmWL6LMydicUZfF7OE9mfglE0JLoA1OmnMribCI2YQ/640?wx_fmt=png)

最后，把各资产的后验收益率分布输入均值方差模型计算各资产的配置比例。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjha8QYMnz0lMZWzsRjwickk4mjtIkxUXllZh0WQhrr3r9hKh82uAqS5jw/640?wx_fmt=png)

B-L模型从市场均衡配置出发，结合对资产的观点后形成了后验收益率分布，能够有效解决传统均值方差模型中资产收益率难以预测以及对收益率输入敏感性高的问题。在B-
L模型中，只有观点涉及到的资产权重才会发生变化，不涉及到的资产权重不会发生变化。不过，传统B-
L模型在计算先验权重时使用了资产的市值占比这一信息，考虑到A股总市值受市场表现的影响波动较大，而且新股频发扩充总市值，这一指标在国内金融市场中可能意义不大。可以考虑在B-
L模型的先验权重计算中充分利用资产的历史表现信息。

** **风险配置类模型分析** **  
**3**

由于均值方差类模型对收益率的预测过于敏感，开始有更多的投资者关注不需要对资产的收益率进行预测，而是完全基于资产的协方差就可以构造的风险配置类模型，包括风险平价策略、最大分散化策略和最小波动率策略等等。其中风险平价策略是实务中较为常见的配置策略之一
。

  * ** 最小波动率策略  **

最小波动率策略在有效前沿上具有唯一性，处于有效前沿的最左边，因此也被称为全局最小风险组合。最小波动率策略的目标函数为：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhF5RAkj3Jsyes7BBiaPjNciclhIibvkfcJncvzZZibtq9Uq00d6fnDVpiaXw/640?wx_fmt=png)

  * **最大分散化策略**

最大分散化策略主要是最大化资产收益率的不相关性，其目标函数是最大化分散比率：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjht0iaQPsEOK7JeaOAvFrqUUmGE8FIv2SHRInQwCYeCt2O3qFlZGTJ7VA/640?wx_fmt=png)

其中  σ  是各个资产的波动率，即协方差矩阵Σ的对角线元素的平方根。

  * **风险平价策略**

风险平价策略使各类资产对总风险的贡献相等，风险平价以风险为立足点，避免了对资产收益进行预测从而导致的不确定性。组合的波动率为

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjh2s8KyPy9Fc2w4s0qXiczsjJ8q79uhmLTIuJ8zLrciakFOqcZ9GR8jRag/640?wx_fmt=png)

可以推出每个资产对组合的风险贡献度RCi等于：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhMLPM6uPejJvRQh6gObMUibtQibnUbvNzsEBfE2boTw9xPCm6mAqYMPFQ/640?wx_fmt=png)

组合的总风险TRC等于：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhvVia3tt7gASWczHwponOjgu8HkBqcYTtUicP4rJWGnCELDzwjFAe9QnA/640?wx_fmt=png)

风险平价策略的目标是实现组合内所有资产对组合的风险贡献相同，也就是对任意两种资产i和j，都有：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhPEbQGDp7EIcEzAlicqO0RjbnXMZ0F0mdew7pFoORPP7Bu4CGBibiaXnjA/640?wx_fmt=png)

可以转化为对下列目标函数进行最优化：

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhM1uqZXBAlF7hjEpdgcjes7U2ujb4YAfwfeCsNtKqic7w0Dibgsk54k8w/640?wx_fmt=png)

在实际投资中，一般要求不能做空、放杠杆，且各资产的权重之和等于1。

** 3.1  资产的历史协方差相对稳定 ** ** **

对于上述三类模型，在最优化过程中仅需用到资产的协方差矩阵，而相对于资产的收益率而言，资产的协方差矩阵在时间序列上相对较为稳定。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhQSx6icGI2vTib1FcEHmBZiakcpeGjOrsFsIhjAxJ9iathnPshbkFKbWIBg/640?wx_fmt=png)

** 3.2  策略波动可控但收益较低 ** ** **

然而，由于风险配置类模型放弃了关于资产预期收益的全部信息，仅从风险的角度去构建组合，从资产权重分布和策略累计收益来看，各类基于风险的资产配置模型对债券指数的平均配置比例均超过70%，国内权益和海外权益类资产平均配置比例仅在10%上下。由于高配债券类资产，风险配置类模型虽然能够有效的控制波动，但其收益相对于等权组合明显更低
。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhP68zna1Wibicm1NvATXpvfGl1QKx3toeLzycZlJv4aJ9kmKHrLicncuLQ/640?wx_fmt=png)

** 3.3  融合各类资产配置模型的优势 **

通过对上述模型的分析，我们总结了各类模型的优劣势。传统均值方差模型尽管能够充分利用资产的预期收益率和协方差信息，但由于收益率难以估计以及模型敏感性较高的问题，实际效果较为一般；B-L模型通过对资产的先验权重反推出先验收益率，再结合新的观点形成后验收益率，有效解决了收益率难以预测以及敏感性高的问题；风险配置类模型避免预测资产的收益率带来的高误差，仅从资产的历史协方差来构建模型，虽然能够有效控制策略的波动，但相应的收益率却比较低。

因此，我们希望以B-L模型作为一个桥梁，将风险配置类模型和均值方差模型联接起来，充分发挥三类模型的优势。比如，作为对均值方差模型的改进，传统B-
L模型以各资产的市值权重作为先验权重并反推出资产的先验收益率，但这一指标在国内金融市场中可能意义不大，而且没有用到关于资产历史表现的信息。因此我们考虑以风险平价策略的权重作为B-
L模型中的先验权重，其意义在于可以有效分散组合的风险。

其次，从收益的角度，由于风险平价策略的累计收益较低，因此我们在B-
L模型中加入资产的短期动量作为观点，希望通过观点收益率的分布对先验收益率的权重进行调整，以期提高策略的收益表现。

最后，将得到的后验收益率分布输入到均值方差模型下，通过最优化来计算各类资产的权重。此外，我们还会构建一个包含跟踪误差约束的资产配置策略。这里的跟踪误差是指根据资产后验收益率分布进行最优化得到的权重与风险平价策略的权重的差异带来的额外波动率。假设约束跟踪误差不超过1%，就可以观察在风险平价策略的基础上承担一定的额外风险，策略获得的额外收益是否能够提升它的夏普比率。

** **基于风险平价和Black-Litterman的资产配置策略** ** **4** 在基于风险平价和B-
L模型的思路下，我们对包含股票、债券、商品和海外股票在内的四类资产构建无跟踪误差约束的资产配置策略（以下简称为RPBL策略）和约束跟踪误差不超过1%的资产配置策略（以下简称为RPBL(1%)策略）。我们使用不同的指数来代表各类资产，同时各指数均有费率低廉的指数产品可以进行配置，便于实际投资。上述指数可获得的数据均可追溯至2005年初，我们使用过去18个月的月收益率数据来估计资产的协方差矩阵，计算B-
L模型的先验权重；同时，我们用过去6个月的累计收益率作为B-L模型的观点。
![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjh3klADU6Oiapib38CW34w8LKNXvBkk62RajB0oB7QnUDiabDYdmsdFR4qg/640?wx_fmt=png)

** 4.1  股债配置策略的表现 **

首先，我们构建一个仅包含股票和债券两类资产的股债配置策略。由于历史数据中有18个月用来构建风险平价模型，因此策略的回测周期为2006年7月至2019年11月，每月月底进行调整。

  * 策略历史表现分析 

与股债风险平价策略相比，股债RPBL(1%)策略的年化波动率从2.80%上升到3.12%，提升幅度11%，而年化收益率从5.03%上升到5.75%，提升幅度14%，因此其风险调整后收益相比风险平价策略有小幅提高。在无跟踪误差约束下，股债RPBL策略的年化波动率为7.80%，年化收益率为10.14%，相比于等权和风险平价策略均大幅提升，体现出了高风险高收益的特征，但其最大回撤仅为-6.86%。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhmyEScXicicibRuxELjb5hPvAdqmNG5edHBIGRUlrqPGafIc0LAzWWhrpA/640?wx_fmt=png)

分年度来看，股债RPBL(1%)策略和股债RPBL策略在过去14年中有13年获得了正收益，仅在2013年小幅下跌，单年度表现较为稳健。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjh70MONSgoYqqvYo1045mZ5bYZgkjaAGlm3OibdLAkhRmR48rshqic5OFQ/640?wx_fmt=png)

  * 各资产业绩归因分析 

从各资产的权重变化来看，由于股债RPBL(1%)策略仅在股债风险平价策略的基础上对权重小幅优化，因此绝大部分仓位依旧配在债券资产上。股票资产的平均权重约为8%，对总收益的贡献比例约为34%，相当于年化收益率为1.94%；债券资产的平均权重约为92%，对总收益的贡献比例约为66%，相当于年化收益率为3.81%。

而股债RPBL策略对风险平价策略的权重的调整幅度较大。股票资产的平均权重为15%，对总收益的贡献比例约为62%，相当于年化收益率6.32%；债券资产的平均权重约为85%，对总收益的贡献比例约为38%，相当于年化收益率3.81%。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhmmfWKOYzq4hgopAoKs0OibrcL32xZ4mpb6BlJI2Cj7BXlJjd3Pfgibxw/640?wx_fmt=png)

  * 通过跟踪误差约束来调整策略的风险收益特征 

我们可以通过调整跟踪误差的约束比例来控制策略的波动率。我们分别测试跟踪误差约束为1%、2%、5%、8%和无约束五种情况下股债策略的表现。

随着跟踪误差约束比例的上升，股债策略的年化收益率和年化波动率均有所提升，但是波动率提升的幅度相比收益率更快，因此股债策略的年化夏普比率随跟踪误差约束的上升而下降。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjh1T35RApMiaYSnFLVyxW6TudYKWIEHQU7YWCyGLaVoaqKricKgQDLpmPw/640?wx_fmt=png)

  * 当前模型配置比例 

截止至2019年11月底，根据模型最新计算结果，在股债RPBL(1%)策略中，股票资产的权重为11.27%，债券资产的权重为88.73%；在股债RPBL策略中，股票资产的权重为14.62%，债券资产的权重为85.38%。

** 4.2  四资产配置策略的表现 **  

我们再构建一个包含四类资产的资产配置模型，策略的回测周期为2006年7月至2019年11月，每月月底进行调仓。

  * 策略历史表现分析 

与四资产风险平价策略相比，四资产RPBL(1%)策略的年化波动率从3.20%上升到3.53%，提升幅度10%，而年化收益率从5.42%上升到6.60%，提升幅度22%，因此其风险调整后收益相比四资产风险平价策略大幅提高。对于无跟踪误差约束的四资产RPBL策略，其年化波动率为10.42%，年化收益率为14.67%，相比于等权和风险平价策略均大幅提升，体现出了高风险高收益的特征，但其最大回撤仅为-6.82%。

  

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhguGp2mIibvOzE8jXPGTIjvoDORPBVsxw0hJnU2tSTsLaaP8UAHamSWg/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhtU36QcVHLebicOs20Ah6XO0eDibWbzGgavMwrM6bdKkmwYe3XJyjvEUQ/640?wx_fmt=png)

分年度来看，四资产RPBL(1%)策略和四资产RPBL策略在过去14年均获得了正收益，其中四资产RPBL策略的单年度收益波动幅度较小。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjh9p3xlrSLoAhoKgS9icicnxFiaF1nPRq7cPqIP8ZW5FlmXJrbeNK4TIrnw/640?wx_fmt=png)

  * 各资产业绩归因分析 

从各资产的权重变化来看，四资产RPBL(1%)策略中债券的权重仍较多。股票、债券、商品和海外股票的平均权重分别为5%、72%、9%和14%，对总收益的贡献比例分别为18%、45%、18%、19%，分别相当于年化收益率1.17%、2.98%、1.17%和1.28%。

而四资产RPBL策略的权重的调整幅度较大。股票、债券、商品和海外股票的平均权重分别为14%、48%、13%和25%，对总收益的贡献比例分别为49%、18%、14%、19%，分别相当于年化收益率7.13%、2.64%、2.13%和2.78%。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhHFbWrUibiboGcIrPXyATOTvUJLJjvHic3kGNTN8HKkTWQKbj3Ov1JLK2g/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhvINnxlfEgwey6E4nHicl9Fr5JENfQ7eGgziarHvmDsKVQR6mSqiaHA3MQ/640?wx_fmt=png)

  * 通过跟踪误差约束来调整策略的风险收益特征 

我们可以通过调整跟踪误差的约束比例来控制策略的波动率。我们分别测试跟踪误差约束为1%、2%、5%、8%和无约束五种情况下四资产策略的表现。

随着跟踪误差约束比例的上升，四资产策略的年化收益率和年化波动率均有所提升，但是波动率提升的幅度相比收益率更快，因此四资产策略的年化夏普比率随跟踪误差约束的上升而下降。

![](https://mmbiz.qpic.cn/mmbiz_png/B7b5jz5YD4SqxmytURb8gJkjpINzOhjhg60RpEtYf6PfnadFBFvqXprxqcsFSFChqicb7bLWws47fS8NgiahSjFw/640?wx_fmt=png)

  * 当前模型配置比例 

截止至2019年11月底，根据模型最新计算结果，在四资产RPBL(1%)策略中，股票资产的权重为0，债券资产的权重为74.41%，商品资产的权重为11.34%，海外股票资产的权重为14.24%；在四资产RPBL策略中，股票资产的权重为0，债券资产的权重为50.32%，商品资产的权重为20.20%，海外股票资产的权重为29.49%。

** ******风险提示** ** **  
**  
**5**

本文根据客观的模型对历史数据进行分析，存在模型误设风险与失效风险，模型的历史表现不代表未来。同时，如果流动性紧张引发“股债双杀”或海外金融市场发生风险事件，可能会导致模型产生较大亏损。

  
** ➢交流联系  **

宋家骥||微信:18019787292(注明机构+姓名)

严佳炜||微信:18502168861(注明机构+姓名)

[
](http://mp.weixin.qq.com/s?__biz=MzI2NjY1MzMxMw==&mid=2247483976&idx=1&sn=8573fe683dd3383f65b13cbc621d1b40&chksm=ea8b99a6ddfc10b06a472889a578d18c4bacd7152f01c8add6e37110c1af0d749632a4bcfd78&scene=21#wechat_redirect)

**研究报告**  

《  资产配置研究系列之一：通过风险平价与Black-Litterman打造稳定收益组合  》

2019.12.2 宋家骥、  严佳炜

**相关报告**

[ 《  基金研究系列之一：如何识别权益基金的投资目标  》
](http://mp.weixin.qq.com/s?__biz=MzI2NjY1MzMxMw==&mid=2247483976&idx=1&sn=8573fe683dd3383f65b13cbc621d1b40&chksm=ea8b99a6ddfc10b06a472889a578d18c4bacd7152f01c8add6e37110c1af0d749632a4bcfd78&scene=21#wechat_redirect)

**团队介绍**

严佳炜 团队负责人，首席分析师，选股、行业风格轮动、择时、基金研究 18502168861

宋家骥 分析师，基金研究，FOF选基，大类资产配置 18019787292

朱定豪 分析师，基金研究，SmartBeta，量价因子研究 18621880250

邱捷铭 分析师，因子选股、行业风格轮动、择时、大数据AI研究 18938852865

**关于本公众号**  

“金工严选”公众号记录 **方正证券研究所金融工程团队** 的研究成果，欢迎关注

![](https://mmbiz.qpic.cn/mmbiz_jpg/B7b5jz5YD4RkpAquNiacLHFY6C7sZ2dibpXtzjyuez8E84Zps8zxJs2QUO7NibYBq8mqg5tGaoAItbnicWJiaPrm0gg/640?wx_fmt=jpeg)  

分析师声明

作者具有中国证券业协会授予的证券投资咨询执业资格，保证报告所采用的数据和信息均来自公开合规渠道，分析逻辑基于作者的职业理解，本报告清晰准确地反映了作者的研究观点，力求独立、客观和公正，结论不受任何第三方的授意或影响。研究报告对所涉及的证券或发行人的评价是分析师本人通过财务分析预测、数量化方法、或行业比较分析所得出的结论，但使用以上信息和分析方法存在局限性。特此声明。

免责声明

方正证券股份有限公司（以下简称“本公司”）具备证券投资咨询业务资格。本报告仅供本公司客户使用。本报告仅在相关法律许可的情况下发
放，并仅为提供信息而发放，概不构成任何广告。

本报告的信息来源于已公开的资料，本公司对该等信息的准确性、完整性或可靠性不作任何保证。本报告所载的资料、意见及推测仅反映本公司于发布本报告当日的判断。在不同时期，本公司可发出与本报告所载资料、意见及推测不一致的报告。本公司不保证本报告所含信息保持在最新状态。同时，本公司对本报告所含信息可在不发出通知的情形下做出修改，投资者应当自行关注相应的更新或修改。

在任何情况下，本报告中的信息或所表述的意见均不构成对任何人的投资建议。在任何情况下，本公司、本公司员工或者关联机构不承诺投资者一定获利，不与投资者分享投资收益，也不对任何人因使用本报告中的任何内容所引致的任何损失负任何责任。投资者务必注意，其据此做出的任何投资决策与本公司、本公司员工或者关联机构无关。

本公司利用信息隔离制度控制内部一个或多个领域、部门或关联机构之间的信息流动。因此，投资者应注意，在法律许可的情况下，本公司及其所属关联机构可能会持有报告中提到的公司所发行的证券或期权并进行证券或期权交易，也可能为这些公司提供或者争取提供投资银行、财务顾问或者金融产品等相关服务。在法律许可的情况下，本公司的董事、高级职员或员工可能担任本报告所提到的公司的董事。

市场有风险，投资需谨慎。投资者不应将本报告为作出投资决策的惟一参考因素，亦不应认为本报告可以取代自己的判断。

本报告版权仅为本公司所有，未经书面许可，任何机构和个人不得以任何形式翻版、复制、发表或引用。如征得本公司同意进行引用、刊发的，需在允许的范围内使用，并注明出处为“方正证券研究所”，且不得对本报告进行任何有悖原意的引用、删节和修改。

公司投资评级的说明：

强烈推荐：分析师预测未来半年公司股价有20%以上的涨幅；

推荐：分析师预测未来半年公司股价有10%以上的涨幅；

中性：分析师预测未来半年公司股价在-10%和10%之间波动；

减持：分析师预测未来半年公司股价有10%以上的跌幅。

行业投资评级的说明：

推荐：分析师预测未来半年行业表现强于沪深300指数；

中性：分析师预测未来半年行业表现与沪深300指数持平；

减持：分析师预测未来半年行业表现弱于沪深300指数。

  
|  北京  |  上海  |  深圳  |  长沙   
---|---|---|---|---  
地址：  |  北京市西城区阜外大街甲34号方正证券大厦8楼（100037）  |  上海市浦东新区浦东南路360号新上海国际大厦36楼（200120）  |  深圳市福田区深南大道4013号兴业银行大厦201（418000）  |  长沙市芙蓉中路二段200号华侨国际大厦24楼（410015）   
网址：  |  http://www.foundersc.com  |  http://www.foundersc.com  |  http://www.foundersc.com  |  http://www.foundersc.com   
E-mail：  |  yjzx@foundersc.com  |  yjzx@foundersc.com  |  yjzx@foundersc.com  |  yjzx@foundersc.com    
  
  

  

预览时标签不可点









****



****



****





__









