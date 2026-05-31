![cover_image](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWfMsXibIK1NKUtth3ekK5ehfm9kjGB9dAnwY49ta0nnXA9SYiaLBQPfKfjUPAgmlTUKOp1njYWtX2yw/0?wx_fmt=jpeg)

#  【广发金融工程】基于SemiBeta的因子研究——多因子Alpha系列报告之(四十五)

原创  广发金融工程  广发金融工程  [ 广发金融工程研究 ](javascript:void\(0\);)

_2022年11月22日 11:28_ __ _ _ _ _ _ 上海  _

在小说阅读器读本章

去阅读

  
  
**摘 要**  
****

** 研究背景和理论基础  ** ** ：  **
传统Beta因子在A股市场蕴含的Alpha信息相对有限，并且因子忽略了投资者更在意资产的下行风险，这契合行为金融学中的有限理性投资者呈现出的“损失厌恶”（Loss
Aversion）特征。我们借鉴Bollerslev（2021）的研究思路，将传统Beta因子拆解为SemiBeta因子，并在A股市场实证检验。

** SemiBeta因子构建：  ** 基于个股收益和市场收益方向的不同，将传统Beta因子拆解为4个SemiBeta（  、  、  和
），同时分别采取20、60、120个交易日的回溯周期，分别以沪深300、中证500、中证1000和创业板指作为市场基准，合计构建了48个细分因子。

** A股实证分析：  **
全市场选股范围内，月频调仓频率下，fBeta_MN（市场基准收益为负，股票收益为正）系列因子，即反映市场下行时具备对冲特征的因子，整体表现较好。计算Beta因子滚动回溯的周期越短，回测总收益越高，但换手率也相对更高。以fBeta_MN_60_S399006为例，IC均值为-7.4%、多空收益信息比为（LS_IR）为1.88，IC_IR为-0.86，年化收益为128.7%，胜率为72.2%，平均换股比例为43.5%。

** 传统因子相关性分析：  ** SemiBeta系列因子和市值、短期动量因子的相关性相对较低，和波动率存在一定相关性。

** 指数增强策略构建：  **
综合考虑因子IC、换手率和长期收益等因素，筛选并保留了fBeta_MN_60_S399905、fBeta_MN_60_S000852和fBeta_MN_60_S399006作等权重配置，针对沪深300、中证500和中证1000指数，构建市值行业中性的指数增强策略。月度换仓频率下，2015年初至2022年11月，沪深300、中证500和中证1000增强策略分别实现约5%、10%和12%的年化超额收益。

  
  
  
**正 文**  
一、 传统市场因子（Beta）研究背景  
**1.1** 因子起源  

CAPM模型（Capital Asset Pricing
Model）于20世纪60年代问世，由Treynor（1961，1962）、Sharpe（1964）等多位学者分别独立提出，该模型首次清晰地刻画了风险和收益率之间的线性关系，指出了风险资产的预期超额收益是由市场整体的预期超额收益和该资产对市场风险的暴露水平共同决定，为后续大量线性多因子定价模型的研究奠定基石。根据该模型，资产i的预期收益率由以下线性模型表达：

是风险资产i的预期收益率；  是无风险收益率；  是市场整体的预期收益率；  是风险资产i与市场整体的系统性风险系数。其中
刻画了资产收益率对市场收益的敏感程度，即我们常说的市场（Beta，或β）因子。CAPM模型简单清晰，但是诸如完全竞争市场、同质性预期和理性投资者等假设相对严苛。早期的研究成果，诸如Markowitz（1959）、Hogan
and
Warren（1972，1974）均提出传统Beta因子的假设情形过于简单化。同样诸多研究也显示了单凭Beta因子较难以解释不同资产（如股票）收益的截面差异。

**1.2** A股实证检验  

对于传统Beta因子，我们在A股市场进行实证检验。我们以主要的宽基指数即沪深300、中证500和中证800，作为市场基准，滚动回溯过去20、60和120个交易日计算各股票换仓时点的传统Beta因子。回测结果显示，传统Beta因子较难稳定贡献Alpha收益，即高Beta个股并未带来稳定的超额收益。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrWxl0y3Qo8qFEdfhWz0hVrD8nAodgCNYa4Yc0xKVB5p61FicHQsicDyWw/640?wx_fmt=png)

综上所述，传统Beta因子存在一定局限性。一方面，后续研究朝多因子方向发展，即认为资产的收益率并非由单一的市场因子决定，如Ross（1976）提出APT（Arbitrage
Pricing Theory）理论。另一方面，部分研究针对Beta因子，进行更加深入细化的拆解。

  

**本报告将聚焦于后者** ** ，针对传统Beta因子的不足，参考Bollerslev（2021）构建SemiBeta因子，并在A股市场进行实证检验
** 。  

  

二、SemiBeta因子研究理论基础

行为金融学研究领域，Kahneman and Tversky（1979）提出“前景理论”（Prospect Theory）和“损失厌恶”（Loss
Aversion）概念，即认为完全理性投资者的假设不完全符合实际，现实中的投资者更多是呈现有限理性的特征，面对同样数量的收益和损失时，认为损失带来更多的负效用，表现为“损失厌恶”，而非“风险厌恶”（Risk
Aversion）的特征。因此面对盈利，投资者表现为风险厌恶，追求“落地为安”；面对亏损，投资者表现为风险偏好，追求“扭亏为盈”。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrHmJRnu0ozWQDxgX0qjs8HAyicBUtWDV2zQFicuibzF8Q5AJamXZbdPx3w/640?wx_fmt=png)

针对传统Beta因子，假设投资者只厌恶可能导致亏损的波动，那么相关的风险就应当只聚焦于负收益的部分。如果投资者只关注下行风险，那么个股和市场整体在上涨和下跌不同状态下的协方差则不应被均衡定价。

Ang等（2006）发现，相比于传统Beta因子，只聚焦于市场下跌状态下的Beta，即Downside
Beta，能更好地解释美股权益市场的截面差异。但Levi and Welch（2020）等人发现Downside
Beta并不能提供更好的预测能力。基于上述研究背景，Bollerslev（2021）提出SemiBeta概念，即基于个股收益和市场基准收益方向的不同，将传统Beta因子拆解为4部分。

其中  表示某风险资产收益率，  表示市场基准收益率，  、  、  、
分别对应4个不同的组成结构。N表示市场和风险资产均为负收益，P表示市场和风险资产均为正收益，M^+表示市场收益为正但风险资产为负，M^-表示市场收益为负但风险资产为正。而为了方便描述，参考原文，报告后续采取同样的设定，即：

按照上述方法，即将传统Beta拆解为了4个不同的SemiBeta。

为进一步更好地理解相应概念，以下图为例，我们假设有4个传统Beta均为1的不同的风险资产，但是其SemiBeta呈现差异化的特征。

如果基于传统CAPM模型，那么这4个资产应当有相同的预期收益率。

引入SemiBeta模型，Panel
A中的资产（后续称为资产A，其他资产采取类似处理）Beta保持稳定，而资产B的Beta在市场整体下跌时要低于市场整体上涨时的Beta，即
。那么基于相关理论，投资者仅厌恶下行风险，因此相应资产若能在下跌环境中提供预期相对稳定的收益，则愿意接受相对较低的预期收益率，即意味资产B的预期回报率要低于资产A。

相似的，资产C与资产B特征相反，则资产C要求相对高于资产A和资产B的预期回报率。而资产D相比于资产C有相对更好的对冲特性，因此资产D的预期回报率要低于资产C。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrY7TuCs76sRI6wGhsVmTr2C9VabKKCS3XgdkHygG2quCkt26CVY4Nfg/640?wx_fmt=png)

Bollerslev（2021）研究发现，对于美股市场，若基于日度数据计算月度的SemiBeta，  因子有相对明显的正溢价，
因子有相对明显的负溢价，其余两个SemiBeta因子特征不显著。我们参考相应的构造方法，将SemiBeta因子引入到A股市场进行实证研究。

**三、实证分析**  
**3.1** 数据说明 **** ** 选股范围：  ** 全市场；  
**股票预处理：** 剔除摘牌、涨跌停板、ST/*ST、上市未满180个交易日的股票；  
**因子预处理：** MAD去极值、Z-Score标准化；  
**回测区间：** 2010.01.01 – 2021.12.31；  
**分档方式：** 根据当期股票的因子值，从小到大分为十档 ；  
**调仓周期：** 月度，每个月最后一个交易日以收盘  价调仓。  
3.2  因子构建  
  
  

我们采取如下结构来构建SemiBeta因子：

表示股票i在第t期，回溯第  个交易日的日度收益率数据；  表示市场基准在第t期，回溯第  个交易日的日度收益率数据。其中以  为例：

为方便表述，针对A股构建的SemiBeta因子，我们以符号  、  、  、  表示  、  、  和
。每期回溯的时间区间，我们分别采取20、60、120个交易日，即对应1个月、3个月和半年；市场基准方面，我们分别以沪深300、中证500、中证1000和创业板指作为市场基准。

将4个SemiBeta原始结构、3类回溯时间、4个比较基准进行排列组合，合计构建了48个后续用于A股实证检验的SemiBeta因子。如fBeta_MN_120_S000852，表示以中证1000作为基准（s000852）,每期回溯120个交易日（120）构建的
（MN）因子，并用于全市场选股（fBeta）。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrXibIchs0GYeMZJhEOA8ibLlfNaZgb6aFrDlCSOJfVBnwYZ7g1WB5ib39Q/640?wx_fmt=png)

**3.3** 因子绩效表现  ** 1\. fBeta_MN系列因子  ** 多  数fBeta_M
N系列因子的覆盖度超过了90%，所有因子均表现出负IC的特征，其中综合较优的因子是fBeta_MN_60_S000852：
IC均值为-7.1%、多空收益信息比为（LS_IR）为2.13，IC_IR为-0.98，年化收益为121%，胜率为75.7%，平均换股比例为46.6%，因子覆盖度达95.5%。
其中关于年化收益，以沪深300作为市场基准时的长期年化收益不够理想，其他宽基指数作为基准的年化收益均相对较高。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrHVUBMaQslgLLwQ68ibUUsojjc1dJrfTaes2dU2T9t0nibbaQx0ySlTww/640?wx_fmt=png)

** 2\. fBeta_MP系列因子  **
多数fBeta_MP系列因子的覆盖度同样超过了90%，所有因子均表现出负IC的特征，其中综合较优的因子是fBeta_MP_20_S000852：IC均值为-6.6%、多空收益信息比为（LS_IR）为1.76，IC_IR为-0.71，年化收益为74.6%，胜率为69.4%，平均换股比例为82.4%，因子覆盖度达95.6%。  
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrtQ8IYsDkMsF67WaOm7aDTsnACj3KiczSZk306w1zvqptjicWXiavLs6nQ/640?wx_fmt=png)
**3. fBeta_N系列因子  **
fBeta_N系列因子的有效性相对较弱，IC绝对值回测结果未超过5%。Bollerslev（2021）在美股中的实证结果显示高Beta_N个股具备较高的风险溢价，和我们基于A股的实证结果存在差异。
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYr7ZlVOxU6mbVIUbw3BxXmD9LSEbxqARgjQaxibwibvibPA8cXqfT0US9LA/640?wx_fmt=png)
** 4\. fBeta_P系列因子  **  
fBeta_P系列因子在A股的实证结果来看，整体有效性并不显著。
![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrP5Y0Lk8B18CnicdUicIQTH1aicEibxQyuMoIpalD5mkJ66JcicjzPONjaIA/640?wx_fmt=png)
综上所述，整体而言，fBeta_MN系列因子的有效性相对较高，我们将进一步展示fBeta_MN因子以中证500、中证1000和创业板指作为基准的特征和表现。
**四、绩优因子详细表现** **4.1** fBeta_MN_120系列因子表现

对比其他MN系列因子，相对而言，fBeta_MN_120系列因子整体换手率相对较低，其中综合较优的因子是fBeta_MN_120_S000852：IC均值为-5.8%、多空收益信息比为（LS_IR）为1.64，IC_IR为-0.81，年化收益为76.5%，胜率为65.3%，平均换股比例为30.6%，因子覆盖度达95.4%。

** 1\. **fBeta_MN_120_S399905** **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrTpNJCYSGOoV35BNuib5AiaU10sGialvjqRRRk855M0FibCJ2XGvYfQ5mRw/640?wx_fmt=png)

  

**2.** fBeta_MN_120_S000852  ** ** ****

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrRgzWhDZJ4bqI1Vp8zbIdn0Bjpp8QcDAhUVF6zPMdhSHYtxZwdiaebpg/640?wx_fmt=png)

  

**3.** fBeta_MN_120_S ** 399006  ** ** ** ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYricAibgojGwSdWZaf9FjHLric1nX5eskcZlCU0orIaXMBnOoPxRibJBGunQ/640?wx_fmt=png)

**** ** **

**4.2** fBeta_MN_60系列因子表现

fBeta_MN_60系列因子整体换手率相对高于fBeta_MN_120，长期收益也有较明显的提升。以fBeta_MN_60_S399006为例：IC均值为-7.4%、多空收益信息比为（LS_IR）为1.88，IC_IR为-0.86，年化收益为128.7%，胜率为72.2%，平均换股比例为43.5%，因子覆盖度达90.0%。

1\.  ** fBeta_MN_60_S399905  **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYricDSLhaYHaAgHfdUhKdEnkxNJcDln83IpKzY2ZgjSics3qEGvooczEDA/640?wx_fmt=png)

  

** 2\.  ** fBeta_MN_60_S000852  ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYryCyHL508pmKOogicmUoGiblFhrAEzak2Eox0Zr3fqWYpY6ohJbp1xP8g/640?wx_fmt=png)

  

** ** 3\.  ** fBeta_MN_60_399006  ** ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYriaTX5jBZt4jqdo0TLrWuptjnhJn8WciacMwYQwtXcWwtB7oxctLwmdQw/640?wx_fmt=png)

**4.3** fBeta_MN_20系列因子表现

fBeta_MN_20系列因子整体换手率相比于fBeta_MN_60系列因子进一步提高，同时回测收益也相对较高。以fBeta_MN_20_S399006为例：IC均值为-6.7%、多空收益信息比为（LS_IR）为1.97，IC_IR为-0.85，年化收益为180.0%，胜率为71.5%，平均换股比例为80.4%，因子覆盖度达91.4%。

1\.  ** fBeta_MN_20_399905  **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrGvtL6qBffS8icZ4Aibhcp0nwO6n22aNb16bUDUfJNup3SL1dsiciaGGmxA/640?wx_fmt=png)

  

** 2\.  ** fBeta_MN_20_000852  ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrhFkrJsCZxz8Umqfmvw5r7E6WKU8CgSibBibJ6Z9KeT5RH3kccZ12wtLQ/640?wx_fmt=png)

**** ** ** ****  
** ** **** 3\.  ** fBeta_MN_20_399006  ** ** **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrxLviaKFcqQgmbiaOwPyYk6j88IcbdXgrdlqFUicqEoNeibqibh4rPal52ZQ/640?wx_fmt=png)

**** ** ** ** **  
**五、传统因子相关性分析**

我们将SemiBeta系列因子和常见的市值、动量、波动率等因子做相关性分析。整体而言，SemiBeta系列因子和市值、短期动量的相关性相对较低，和波动率存在一定相关性。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrma53LvtmleKicvLPicj2MFFfusBcw9bS8wcWB03BWic2CxGqleMGiclLTw/640?wx_fmt=jpeg)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrWOJGFXWDlDSjc2253xRK58o7vzbiaWYklB5u9fRS5WT4fTdYDCcyRpA/640?wx_fmt=png)

  
**六、指数增强策略构建**  
**6.1** 策略说明

基于上述SemiBeta测算结果，针对沪深300、中证500和中证1000指数，构建市值中性且行业中性的指数增强策略。  
因子筛选方面，综合考虑因子IC、换手率和长期收益等因素，我们筛选并保留了fBeta_MN_60_S399905、fBeta_MN_60_S000852和fBeta_MN_60_S399006作等权重配置。  
其他设置如下。  
**选股范围：** 全市场；  
**股票预处理：** 剔除摘牌、ST/*ST、上市未满180个交易日的股票；  
**因子预处理：** MAD去极值、Z-Score标准化、行业中性、市值中性；  
**回测区间：** 2010.01.01 – 2022.11.15；  
**调仓周期：** 月度，每个月最后一个交易日以收盘价调仓  
**个股权重上限：** 2%（沪深300增强）；1%（中证500增强和中证1000增强）；  
**交易费用：** 双边千分之三。

**6.2** 沪深300指数增强

SemiBeta沪深300增强策略，在2015年初至2022年11月中旬期间，累计实现6.2%的年化收益，约5%的年化超额收益。2022年初至今，已实现约7.2%的超额收益。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrToT4kNdaB2icMEmUH4IWKFwQYiabHYibrRBV1GGice6HTibr0QpSBOWYzfA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrz0AZWUevRwyX4hDNdsOsfFFLPPx37tnp6sJXib2xpwE9blbF1eMrwtg/640?wx_fmt=png)

**6.3** 中证500指数增强

SemiBeta中证500增强策略，在2015年初至2022年11月中旬期间，累计实现12.4%的年化收益，约10%的年化超额收益。2022年初至今，已实现约12%的超额收益。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrXc9Pico0fKQJDSKjVfXSTibqjiaFFC4LIVFnRIfXHugm5HfA8xZiaAg41g/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrEsdIQlpuAt8PaphIibXt7M3l2NCfBo3POaQ5sRRYLdlHWYaiabGr274w/640?wx_fmt=png)

**6.4** 中证1000指数增强

SemiBeta中证1000增强策略，在2015年初至2022年11月中旬期间，累计实现14.3%的年化收益，约12.8%的年化超额收益。2022年初至今，已实现约13.3%的超额收益。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYrZQoicMic2FlPDeYVydiafQKrs1hY7hG1kOHcZFNEgt6WY83Mr2GZpK0VA/640?wx_fmt=png)

  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWd253U0dzTgw1CW9ZdueeYr4cpPiaoBALtL9vbOIRKTpEibqmibU1lxnPrWrthCqhO89bXsvTgCTia5pA/640?wx_fmt=png)

**七、总结**

研究背景和理论基础：传统Beta因子在A股市场蕴含的Alpha信息相对有限，行为金融学提出损失厌恶”（Loss
Aversion）概念，即有限理性投资者认为等数量的损失的负效用高于收益的正效用，那么Beta因子的收益方向应纳入考量。本篇专题报告借鉴Bollerslev（2021）《Realized
semibetas: Disentangling “good” and “bad” downside
risks》的研究思路，对Beta因子进行深入细化拆分，构建SemiBeta因子，并在A股市场进行实证检验。  
SemiBeta因子构建：基于个股收益和市场基准收益方向的不同，将传统Beta因子拆解为4个SemiBeta，同时分别采取20、60、120个交易日的Beta计算回溯周期，分别以沪深300、中证500、中证1000和创业板指作为市场基准，合计构建了48个细分因子。  
A股实证分析：从整体表现来看，全市场选股范围内，月频调仓频率下，fBeta_MN系列因子表现较好，所有因子均表现出负IC的特征，计算Beta回溯周期越短，回测总收益越高，且和换手率呈现负相关。以fBeta_MN_60_S399006为例，IC均值为-7.4%、多空收益信息比为（LS_IR）为1.88，IC_IR为-0.86，年化收益为128.7%，胜率为72.2%，平均换股比例为43.5%，因子覆盖度达90.0%。  
传统因子相关性分析：SemiBeta系列因子和市值、短期动量的相关性相对较低，和波动率存在一定相关性。  
指数增强策略构建：综合考虑因子IC、换手率和长期收益等因素，我们筛选并保留了fBeta_MN_60_S399905、fBeta_MN_60_S000852和fBeta_MN_60_S399006作等权重配置，针对沪深300、中证500和中证1000指数，构建市值行业中性的指数增强策略。月度换仓频率下，
2015年初至2022年11月，SemiBeta沪深300增强策略实现约5%的年化超额收益，SemiBeta中证500增强策略实现约10%的年化超额收益，SemiBeta中证1000增强策略实现约12%的年化超额收益。

**八、风险提示**

本专题报告所述模型用量化方法通过历史数据统计、建模和测算完成，所得结论与规律在市场政策、环境变化时可能存在失效风险；本专题策略模型在市场结构及交易行为的改变时有可能存在策略失效风险。

**九、参考文献**

  1. Ang, A., Hodrick, R. J., Xing, Y., & Zhang, X. 2006. The cross‐section of volatility and expected returns. The journal of finance, 61(1), 259-299. 
  2. Bollerslev, T. , Patton, A. J. , & Quaedvlieg, R. . 2021. Realized semibetas: disentangling "good" and "bad" downside risks. Journal of Financial Economics(2). 
  3. Hogan, W.W., Warren, J.M., 1972. Computation of the efficient boundary in the ES portfolio selection model. J. Financ. Quant. Anal. 7 (4),1881–1896. 
  4. Hogan, W.W., Warren, J.M., 1974. Toward the development of an equilibrium capital-market model based on semivariance. J. Financ. Quant.Anal. 9 (1), 1–11. 
  5. Kahneman, D. and A. Tversky 1979. Prospect Theory: an analysis of decision under risk.Econometrica, Vol. 47(2), 263 – 292. 
  6. Levi, Y., & Welch, I. 2020. Symmetric and asymmetric market betas and downside risk. The Review of Financial Studies, 33(6), 2772-2795. 
  7. Markowitz, H., 1959. Portfolio Selection, Efficient Diversification of Investments. J. Wiley. 
  8. Parsons, C. A., Sabbatucci, R., & Titman, S. 2018. Geographic Lead-Lag Effects. Available at SSRN 2780139. 
  9. Ross, S. A. 1976. The arbitrage theory of capital asset pricing. Journal of Economic Theory, 13(3), 341-360. 
  10. Sharpe, W. F. 1964. Capital asset prices: A theory of market equilibrium under conditions of risk. The journal of finance, 19(3), 425-442. 
  11. Treynor, J. L. 1961. Market value, time, and risk. Time, and Risk (August 8, 1961). 
  12. Treynor, J. L. 1961. Toward a theory of market value of risky assets. 

  
**详细研究内容请参见广发金工专题报告**  
  
《金融工程：基于SemiBeta的因子研究——多因子Alpha系列报告之(四十五)  》  
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









