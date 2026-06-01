![cover_image](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWe5dTteKibtejpjgxCumB4DQ6dHU2vuibm1KkaT32fNY6vl6D416rZQhHGibD90wicia7diaBbQq7iaK8iaDA/0?wx_fmt=jpeg)

#  【广发金融工程】再谈SemiBeta因子：高频测算——多因子Alpha系列报告之(四十七)

原创  罗军安宁宁张钰东  罗军安宁宁张钰东  [ 广发金融工程研究 ](javascript:void\(0\);)

_2023年04月07日 11:27_ __ _ _ _ _ _ 上海  _

在小说阅读器读本章

去阅读

  

**摘要**

Abstract

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8h7Tm4XybFWMq6lNibbqTE2icSBeoV1W686rAenqzdqKMDHR0UXqAqJwiaw/640?wx_fmt=gif)

  * ** 研究背景：  ** 传统Beta因子在A股市场蕴含的Alpha信息相对有限，并且因子忽略了投资者更在意资产下行风险的潜在影响。我们借鉴Bollerslev（2021）的研究思路，将传统Beta因子拆解为SemiBeta因子。《基于SemiBeta的因子研究——多因子Alpha系列报告之(四十五)》报告中，我们基于日频数据构建因子进行测算，本报告进一步落脚到A股市场的日内高频数据，进行相对更高频数据维度的实证检验。 
  * ** SemiBeta因子构建：  ** 基于个股收益和市场收益方向的不同，将传统Beta因子拆解为4个SemiBeta（  ![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByDhwiaFlPaziavQqibrYBtbD0YK7nJVibStOPDmq2dDIOicTq7JXupa7qOPg/640?wx_fmt=jpeg) ）。参数设置方面，我们分别基于月频和周频的换仓频率进行检验，以沪深300、中证500、中证1000和创业板指等作为市场基准，以及尝试1分钟级和5分钟级等不同数据频率等内容。 
  * ** A股实证分析：  ** 周频调仓频率下，全市场选股范围内，所有因子均表现出负IC的特征，对比MN、MP、N和P各大类因子，MN系列因子表现较好。如5avg_fBeta_MN_HF_S000300均值为-5.3%，年化ICIR为-4.75，多空年化收益为29.4%，多头年化收益为18.5%，多空单期换股比例均值为60.9%。将选股范围限定到如沪深300、中证500和中证1000指数成分股等不同的选股池内，因子有效性呈现一定程度的下降。 
  * 月频调仓频率下，全市场选股范围内，N因子和P因子的因子表现较好。semi_beta_P_SH000852因子的IC均值为-6.4%，多空年化收益为14.8%。限定选股池后，中证500指数成分股范围内的因子效果相对较好。 
  * ** 因子相关性分析：  ** 反馈相似收益方向组合的因子相关性相对较高，即N因子和P因子之间相关性较高，MN因子和MP因子的相关性较高。高频SemiBeta因子内部之间的相关性高于低频SemiBeta因子内部。低频的P因子和高频的N、P因子存在一定相关性。 

  
**风险提示：**
1.本报告中所述模型用量化方法通过历史数据统计、建模和测算完成，所得出的结论与规律在政策、市场环境发生变化时可能存在失效的风险。2.本报告中所述模型在市场结构及交易行为改变时有可能存在策略失效风险。  
  
  
  
![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

**一、研究背景**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)  
市场（ _Beta_ ，或β）因子刻画了资产收益率对市场收益的敏感程度。早期的研究成果，诸如Markowitz（1959）、Hogan and
Warren（1972，1974）均提出传统Beta因子的假设情形过于简单化，同样诸多研究也显示了单凭Beta因子较难以解释不同资产（如股票）收益的截面差异。
对于传统Beta因子，我们在A股市场进行实证检验。我们以主要的宽基指数，即沪深300、中证500和中证800，作为市场基准，滚动回溯过去20、60和120个交易日计算各股票换仓时点的传统Beta因子。
**回测结果显示，传统Beta因子较难稳定贡献Alpha收益，即高Beta个股并未带来稳定的超额收益。**
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBymr8ID4x5KnDibbdrfzzBYTghic4XbIQx0wYsPcguC329jEczclTxp3KQ/640?wx_fmt=png)
我们在《基于SemiBeta的因子研究——多因子Alpha系列报告之(四十五)》报告中，借鉴Bollerslev（2021）的研究思路，基于个股收益和市场收益方向的不同，将传统Beta因子拆解为4个SemiBeta。
**回测结果显示，月频调仓频率下，基于日度收益计算的fBeta_MN（市场基准收益为负，股票收益为正）系列因子，整体表现较好。**
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBy1XJyBoRQVaVg9qcsEayOwGGEvDy0Q7XXkibN2OJDzdpm50LVmVZQBCA/640?wx_fmt=png)
近年来，由于因子拥挤等因素影响，低频因子的增量信息成果放缓，日内高频价量信息的挖掘逐渐成为市场的关注重点。因此，针对SemiBeta的因子研究，本报告将进一步基于A股市场的日内高频数据，
**进行相对更高频维度的实证检验。**  
  
![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

**二、 _** SemiBeta  ** _ ** 因子研究理论基础  ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)  
Bollerslev（2021）提出SemiBeta概念，即基于个股收益和市场基准收益方向的不同，将传统Beta因子拆解为4部分。
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByKSdHVGIeAfH6DxPNOE5uwmt87kzwh9RVicESicM1O0urmVeBChvvQwGg/640?wx_fmt=jpeg)
其中  _Ri_ 表示某风险资产收益率，  _Rm_ 表示市场基准收益率，  _N_ 、  _P_ 、  _M+_ 、  _M-_ 分别对
应4个不同的组成结构。  _N_ 表示市场和风险资产均为负收益，  _P_ 表示市场和风险资产均为正收益，  _M+_ 表示市场收益为正但风险资产为负，
_M-_ 表示市场收益为负但风险资产为正。  而为了方便描述，参考原文，报告后续采取同样的设定，即：
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByxPJZ1XMtlr4VZB2RhyHYmzARjOlVl2w6zVK8ehM0wVn01ur0SyyyjQ/640?wx_fmt=jpeg)
按照上述方法，即将传统Beta拆解为了4个不同的SemiBeta。
为进一步更好地理解相应概念，以下图为例，我们假设有4个传统Beta均为1的不同的风险资产，但是其SemiBeta呈现差异化的特征。  如  果基于
传统CAPM模型，那么这4个资产应当有相同的预期收益率。  引入SemiBeta模型，Panel
A中的资产（后续称为资产A，其他资产采取类似处理）Beta保持稳定，而资产B的Beta在市场整体下跌时要低于市场整体上涨时的Beta，即
![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBynXHJUDkVagzibuTHL2FFaDOtzd8Xww2uspmqUich25bwmWxEjqicciaiaqA/640?wx_fmt=jpeg)
，那么基于相关理论，投资者仅厌恶下行风险，因此相应资产若能在下跌环境中提供预期相对稳定的收益，则  愿意接受相对较低的预期收益率，即意味资产  B
的预期回报率要低于资产  A  。  相似的，资产C与资产B特征相反，则资产C要求相对高于资产A和资产B的预期回报率。
而资产D相比于资产C有相对更好的对冲特性，因此资产D的预期回报率要低于资产C。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBywicvDvxgyxRiaicNaFd1v3DSnVhicUTvElsCx3j4nyQ8ldM6jAW1gMhFdg/640?wx_fmt=png)

Bollerslev（2021）研究发现，对于美股市场，若基于日度数据计算月度的SemiBeta，因子有相对明显的正溢价，因子有相对明显的负溢价，其余两个SemiBeta因子特征不显著。我们参考相应的构造方法，将SemiBeta因子引入到A股市场进行实证研究。

  

  

  

  

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

**三、** 实证分析：月频全市场选股  ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

  

**3.1**

**数据说明**

选股范围：全市场；

股票预处理：剔除摘牌、涨跌停板、ST/*ST、上市未满180个交易日的股票；

因子预处理：MAD去极值、Z-Score标准化；  回测区间：2010.01.01 – 2021.12.31；
分档方式：根据当期股票的因子值，从小到大分为十档 ；  调仓周期：月度，每个月最后一个交易日以收盘价调仓。

  

**3.2**

**因子构建**

因子构建的逻辑和我们在《基于SemiBeta的因子研究——多因子Alpha系列报告之(四十五)》中的方案保持一致，同样涉及4个SemiBeta原始结构，详情请参考对应报告。

针对高频数据，在参数设置方面，主要包括以下几个方面的内容：

1\. 市场基准：沪深300、中证500、中证1000和创业板指；  2\. 日内数据频率：1分钟级和5分钟级；  3\.
是否平滑：（部分）采取滚动10日均值进行平滑。  最终构建了64个高频数据级别的细化的SemiBeta因子，应用于全市场选股。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBy2cug4b8xzqiaUj5w8EI9ozANJHQoAjpic6wzImrbV1oy21MY12qibKdIw/640?wx_fmt=png)

  

**3.3**

**因子实证结果**

本小节中，主要将对各类SemiBeta因子在IC、多空策略、胜率以及换手率方面的回测表现进行整体展示。

月频全市场选股方式下，所有因子均表现出负IC的特征，即因子值相对较小的个股样本内的后续收益表现相对较好。对比MN、MP、N和P各大类因子，总体而言，N因子和P因子的IC均值绝对值相对较高。

N因子中，semi_beta_N_SH000852和semi_beta_N_SZ399300_ma10因子的总体效果相对较好，其中semi_beta_N_SH000852因子的IC均值为-6.1%，多空年化收益为12.6%。semi_beta_N_SZ399300_ma10因子的IC均值为-7.1%，多空年化收益为12.7%。

P因子中，semi_beta_P_SH000852和semi_beta_P_SZ399300因子的总体效果相对较好，其中semi_beta_P_SH000852因子的IC均值为-6.4%，多空年化收益为14.8%。semi_beta_P_SZ399300因子的IC均值为-6.0%，多空年化收益为13.0%。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByCqicPU8vtF29bT3KfU0cgN7SsIGPDyphcRbeHibib22dZkgzv7VAxxQ9A/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBy40ObzlN8W6DGHCRZar1Hp2KWIm06K9QJ5uC1L8M1K572mF425xerUg/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByOTjSyhFWLFwrMZCecKHw6GX7nYTaJbHxia8oicCej6Uu0cXjkEq6B2bw/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByaqBRafa9ibXIpniafyFIOTs3PvTjz9tCCEe6Xzib7bqXhGaur9lYmRY4A/640?wx_fmt=png)

**3.4**

**因子实证结果补充**

** 1.N因子  **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByia1dKKpB5GIVnI2ae7Zp81JYGfw0A7fHYaHv7E2FhCKav7Ffd5xenZg/640?wx_fmt=png)
** 2.P因子  **  
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByrXUDr0dnjK2ror8NmpBXh6xQOriag4Wc0nWj8QTAckCjqHqWcMWKPzA/640?wx_fmt=png)

  

**3.5**

**相关性分析**

本部分针对高频SemiBeta因子，以及报告《基于SemiBeta的因子研究——多因子Alpha系列报告之(四十五)》中的低频SemiBeta因子进行相关性分析。相应的因子均以中证1000作为基准。

低频因子方面，反馈相似收益方向组合的因子相关性相对较高，即N因子和P因子之间相关性为54%，MN因子和MP因子的相关性为47.5%；而反馈不同收益方向组合的因子之间相关性相对较低，如N因子和MP因子的相关性为-0.5%。
高频因子方面，相关性特征和低频因子内部基本相似，但总体相关性进一步上升。N因子和P因子之间相关性为70.7%，MN因子和MP因子的相关性为58.7%；反馈不同收益方向组合的因子之间相关性也有提高，如N因子和MP因子的相关性为37.6%。
高频因子和低频因子之间来看，总体相关性相对较小，其中低频的P因子和高频的N、P因子存在一定相关性。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByJ6JIbSYZX5VmXKe50MslaTynk3fqtB4ModJviahbGOjIt2V0j8YhlYQ/640?wx_fmt=png)

  

  

  

  

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

**四、** 实证分析：月频限定股票池  ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

我们进一步将选股范围限定到如沪深300、中证500和中证1000指数成分股等不同的选股池内，以此检验不同股票池的高频Semi Beta因子的选股效果。

**4.1**

**因子实证结果：沪深300指数成分股**

对于沪深300指数成分股，回测结果来看，相对于全市场选股，整体IC均值的绝对值有一定程度下滑，即使部分IC均值绝对值相对较高的个股，其长期收益也不够理想。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBylHjLcKX6GEyQf1G5FzBTRfYfAvxAWPuQ4yAuvrbzicOB7v54g6rECmA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByKEdiaDFibnypic9YZjH5JSus4LCw8Th9yzSiaIwIZH1wiaicc7BLVuC7j4xQ/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByavb4YFAa6k3ic6qUFbDXwII3sY6xbFXr5cUOqrk0kM0Ep5fSCsjOxQA/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByZcvicSH0Boxt7V3sVkuiaic2gqROrRP2Dj2nvCwib2E33KOsChsvsrqy9g/640?wx_fmt=png)

  

**4.2**

**因子实证结果：中证500指数成分股**

对于中证500指数成分股，回测结果来看，N因子和P因子整体的IC均值的绝对值相对较高，但回测的长期收益不够理想。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByzoTQCUic7SDU82lvrRAAUnPYGbK5q7GXCbhjCOj82zOibTCib8mnEhibcA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBylwYIyEAUgZNcdsrG4MpaxjqbH4V6lywjgicHHCMMV1XWlxLdAWs9xCg/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByQr9UHChf5um5CGmBBjuKtUBq2OdiaKV135AmQM286dMrUsI6TArFXQA/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByLRUKBTqc3FZQX6uZOOCQ28eCibR2yF1oCpNPcMtt1X5BMISauq8dW5g/640?wx_fmt=png)

  

**4.3**

**因子实证结果：中证1000指数成分股**

对于中
证1000指数成分股，回测结果来看，MN因子总体的效果相对较好，其中semi_beta_MN_SZ399006_5m_ma10因子的IC均值为-6.3%，多空年化收益为18.9%，semi_beta_MN_SZ399905_5m_ma10因子的IC均值为-5.8%，多空年化收益为15.8%
。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByIAtKhzWGPJ9AtpHe0uSffxcfoaLoXQ1cib7PexKaRV24Nn4gBBDGQcw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBy8s0niazKp5j8XMRcMuUQ1OM6oqdZ48hePD8K03sazGAXuet4z46hW5w/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByvZR9P1bwmbcpgVjiaSpQbqkRP3XlbZOgC30FeXDE373xIac9XcqS4lw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByF2h6nib1iaibYnQHE0xGjmbbzZCWv9CCOr3DVqaowspibRvgu8VbGr8Cicw/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

**五、实证分析：周频换仓全市场选股**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hfeDnewI2QF7QWUjhIqLcR8957DtUA3N2Cq2c3gBEtCibPorHkuMRSHA/640?wx_fmt=gif)

  

我们进一步基于周度换仓频率进行回测检验。

  

**5.1**

**数据说明**

选股范围：全市场；

股票预处理：剔除摘牌、涨跌停板、ST/*ST、上市未满1年的股票；

因子预处理：MAD去极值、Z-Score标准化、行业市值中性化；

回测区间：2007.02.01 – 2022.11.30；

分档方式：根据当期股票的因子值，从小到大分为十档 ；

调仓周期：周度。

  

**5.2**

**因子构建**

针对周度高频数据，在参数设置方面，主要包括以下几个方面的内容：  

1\. 市场基准：同样以沪深300、中证500、中证1000和创业板指；

2\. 日内数据频率：1分钟级；

3\. 平滑：滚动计算过去5个交易日的日内高频数据的因子均值。

最终构建了16个应用于周频换仓的细化的SemiBeta因子。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByR4eujOksytiaDkibP8bwOPK4UU4ZZWBnAlfMPP0lyqEfY8BqrF4v7ozA/640?wx_fmt=png)

**5.3**

**因子实证结果**

本部分将分别回溯采取全市场选股，以及限定选股池在沪深300、中证500和中证1000指数成分股的选股结果。

全市场选股维度，整体来看MN因子效果相对较好。如5avg_fBeta_MN_HF_S000905均值为-5.0%，多空年化收益为26.8%，多头年化收益为17.0%；5avg_fBeta_MN_HF_S000300均值为-5.3%，多空年化收益为29.4%，多头年化收益为18.5%。

限定选股池之后，总体来看因子有效性呈现一定程度的下降。相对而言，中证500指数成分股的选股池的因子效果相对较好。区分因子细分类型，MN因子效果相对较好，如5avg_fBeta_MN_HF_S000300均值为-3.8%，多空年化收益为17.1%，多头年化收益为11.8%。
** 1.全市场选股  **
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByRPggKbA6LIhiab80I5UuubdSCXibZRZJZjmxLMH72jIC0kF1AZZtHEfA/640?wx_fmt=png)
** 2.沪深300指数成分股选股  **
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBy6n6ZYfDtf9tBGbmF2rFJxbyibY60DMKhtoy6n4cw6x6mcX1s2j4ibDKA/640?wx_fmt=png)
** 3.中证500指数成分股选股  **
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHBySwYVPH0Zln26ib7iaVribmNWicRmXkgicUR5F1ibOib7p0nWbLnP7Qa6p6lsQ/640?wx_fmt=png)
** 3.中证1000指数成分股选股  **
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWdkuoAicH7icusEGyHNYZQHByL7BIMf6SibXOTMTX43DuyYlGftI8e1Kw0BgTP1t2P3sdVdibR6UpUVLA/640?wx_fmt=png)

**总结**

Summary

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8h7Tm4XybFWMq6lNibbqTE2icSBeoV1W686rAenqzdqKMDHR0UXqAqJwiaw/640?wx_fmt=gif)

** 研究背景：  ** 借鉴Bollerslev（2021）《Realized semibetas: Disentangling “good” and
“bad” downside
risks》的研究思路，对Beta因子进行深入细化拆分，构建SemiBeta因子。本报告进一步基于A股市场的日内高频数据，进行相对更高频维度的实证检验。

** SemiBeta因子构建：  **
基于个股收益和市场基准收益方向的不同，将传统Beta因子拆解为4个SemiBeta。参数设置方面，涉及月频和周频的换仓频率，以沪深300、中证500、中证1000和创业板指等作为市场基准，以及1分钟级和5分钟级等不同数据频率等内容。

** A股实证分析：  **
周频调仓频率下，全市场选股范围内，所有因子均表现出负IC的特征，对比MN、MP、N和P各大类因子，MN系列因子表现较好。如5avg_fBeta_MN_HF_S000300均值为-5.3%，年化ICIR为-4.75，多空年化收益为29.4%，多头年化收益为18.5%，多空单期换股比例均值为60.9%。将选股范围限定到如沪深300、中证500和中证1000指数成分股等不同的选股池内，因子有效性呈现一定程度的下降。
月频调仓频率下，全市场选股方式下，N因子和P因子的因子相对表现较好。semi_beta_P_SH000852因子的IC均值为-6.4%，多空年化收益为14.8%。限定选股池后，中证500指数成分股范围内的因子效果相对较好。
** 因子相关性分析：  **
反馈相似收益方向组合的因子相关性相对较高，即N因子和P因子之间相关性较高，MN因子和MP因子的相关性较高。高频SemiBeta因子内部之间的相关性高于低频SemiBeta因子内部。高频因子和低频因子之间来看，总体相关性相对较小，其中低频的P因子和高频的N、P因子存在一定相关性。

  

**参考文献**

Summary

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8h7Tm4XybFWMq6lNibbqTE2icSBeoV1W686rAenqzdqKMDHR0UXqAqJwiaw/640?wx_fmt=gif)

1\. Ang, A., Hodrick, R. J., Xing, Y., & Zhang, X. 2006. The cross‐section of
volatility and expected returns. The journal of finance, 61(1), 259-299.

2\. Bollerslev, T. , Patton, A. J. , & Quaedvlieg, R. . 2021. Realized
semibetas: disentangling "good" and "bad" downside risks. Journal of Financial
Economics(2).

3\. Hogan, W.W., Warren, J.M., 1972. Computation of the efficient boundary in
the ES portfolio selection model. J. Financ. Quant. Anal. 7 (4),1881–1896.

4\. Hogan, W.W., Warren, J.M., 1974. Toward the development of an equilibrium
capital-market model based on semivariance. J. Financ. Quant.Anal. 9 (1),
1–11.

5\. Kahneman, D. and A. Tversky 1979. Prospect Theory: an analysis of decision
under risk.Econometrica, Vol. 47(2), 263 – 292.

6\. Levi, Y., & Welch, I. 2020. Symmetric and asymmetric market betas and
downside risk. The Review of Financial Studies, 33(6), 2772-2795.

7\. Markowitz, H., 1959. Portfolio Selection, Efficient Diversification of
Investments. J. Wiley.

8\. Parsons, C. A., Sabbatucci, R., & Titman, S. 2018. Geographic Lead-Lag
Effects. Available at SSRN 2780139.

9\. Ross, S. A. 1976. The arbitrage theory of capital asset pricing. Journal
of Economic Theory, 13(3), 341-360.

10\. Sharpe, W. F. 1964. Capital asset prices: A theory of market equilibrium
under conditions of risk. The journal of finance, 19(3), 425-442.

11\. Treynor, J. L. 1961. Market value, time, and risk. Time, and Risk (August
8, 1961).

12\. Treynor, J. L. 1961. Toward a theory of market value of risky assets.

**风险提示**

1\. 本报告中所述模型用量化方法通过历史数据统计、建模和测算完成，所得出的结论与规律在政策、市场环境发生变化时可能存在失效的风险。  2\.
本报告中所述模型在市场结构及交易行为改变时有可能存在策略失效风险。

  

**历史报告**  

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8hzmicN3iamnq1UIzlLic7vFEjetCW6D7deFiaqErDHko3ZtibxmibIqjUpiaVg/640?wx_fmt=gif)

多因子Alpha研究系列

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8h7Tm4XybFWMq6lNibbqTE2icSBeoV1W686rAenqzdqKMDHR0UXqAqJwiaw/640?wx_fmt=gif)

再谈股价跳跃因子研究:多因子Alpha系列报告之(四十六）

基于SemiBeta的因子研究:多因子Alpha系列报告之(四十五)

  

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









