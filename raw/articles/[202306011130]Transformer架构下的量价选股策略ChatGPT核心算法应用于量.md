![cover_image](https://mmbiz.qpic.cn/sz_mmbiz_jpg/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1rHyF7aoz62ogWgd7uBwicZ8tEyf5cJz3Il5Bogefb6F7tzrziahG9iaKQ/0?wx_fmt=jpeg)

#  Transformer架构下的量价选股策略：ChatGPT核心算法应用于量化投资

原创  张超  张超  [ 广发金融工程研究 ](javascript:void\(0\);)

_2023年06月01日 11:30_ __ _ _ _ _ _ 广东  _

在小说阅读器读本章

去阅读

**摘要**

Abstract

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/8PaHf53BAWcKoBj1U9OhXh95xic301m8h7Tm4XybFWMq6lNibbqTE2icSBeoV1W686rAenqzdqKMDHR0UXqAqJwiaw/640?wx_fmt=gif&wxfrom=5&wx_lazy=1&wx_co=1)

**1. ChatGPT的广泛应用  ： **

ChatGPT是基于GPT模型的大型对话式语言模型，具有高质量文本生成、代码编写等多项功能。随着ChatGPT被广泛关注，GPT模型逐渐成为人工智能领域的研究热点，并开始应用于其他领域。本篇报告将其核心算法Transformer应用于量化投资策略。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1C7HbRrhTN2TiaU5l6hQ3RGsQx6MREr7iadLf44dJZicZHOOdTUROlPDmQ/640?wx_fmt=png)

**  
**

**2. 自注意力机制  ： **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1Q3OuuJfZDUXpPvj7qvVKp0f9iax9nJZOibMHllUpNCibhgIwjvdKplF7A/640?wx_fmt=png)

****

自注意力机制是NLP的一种数据处理方法，能够有效捕捉输入序列各位置之间的关系。自注意力机制通过计算query向量与key向量的相关性来加权平均value矩阵，得到输出结果；而多头注意力机制则利用并行计算和拆分矩阵为多个头的方式，在自注意力机制的基础上进一步提高模型训练效率。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1akVVCD2Flxa3R8YOiaGd9zf54NQ0rXGNhNiakDT3yQWDqk4Q2BLtqdFg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1XjkLHT1dvVcV5TvCm5Et0ckqiaFDjOWU9GIG5JpGFjn3U6iaBuB23bfw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1wSDJMcTYwUZxUDUItEXEarZKh1B3JdrvkaFoeYud93SweJiaCIskZKw/640?wx_fmt=png)

**  
**

**3. Transformer架构  ： **

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1ZRDibFqD58ZFJ9qM8Z5lcsWCpcYgV3FibhXKOV0akmUjxT4lAtbYCqzw/640?wx_fmt=png)

****

Transformer架构是一种采用自注意力机制的神经网络模型，由位置编码、编码层和解码层组成。位置编码使用正弦和余弦函数计算单词位置信息，编码器将序列中各位置之间关系的信息进行编码并输出，解码器则使用编码器输出的序列信息逐个预测输出。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1YKJyJXmrrD2nZ3w749J2FIlLlfjgFia5AG6TLgicibaHMDKsJlYv82SuA/640?wx_fmt=png)

模型同时具备并行计算和高效捕捉关系的能力，被广泛应用于自然语言处理、图像生成等领域。

  

**4. 基于Transformer架构的选股策略  ： **  

本报告将Transformer模型应用于股票涨跌预测中，选取个股涨跌幅和换手率作为面板数据输入，通过输出股票未来涨跌概率进行分类。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1StUJ1LBicyPwEXE0lq4SXXGyM3aAeGKzcAqGciavwL0nt9QXt4xXgfqA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1HXh3XVkrlKP3IZhiajXMTUowTQg3nAtJpypbHialCWatwqKpdlNGdvgA/640?wx_fmt=png)

在月度调仓策略中，中证500、沪深300和全市场选股自2020年以来均获得良好的相对收益与较强的回撤控制能力。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1FHXaBxZAibXiaLI0UDQ2KYZlRJZIkI7XTJXoD7DbRRria1WXRxQRKoDxQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1tr7y31cWdaENg4mttAuZfNOsicAE2utmzWoZicke0MdIUnPAmLyxxcBA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/sz_mmbiz_png/8PaHf53BAWezlVESq44Ly0wBTMvdbyJ1v2lxwpgY7rwohmFblx11Z0spHJL4u19UZbZNYxnOibMgUDhHEEJTvHw/640?wx_fmt=png)

**5.相对于传统神经网络的优势：**

（1）处理长期记忆；（2）变长输入序列；（3）并行计算效率；（4）预训练模型提高泛化能力。  

  

详细内容参考近期研报《Transformer架构下的量价选股策略》  

  

**风险提示**

策略模型并非百分百有效，市场结构及交易行为的改变以及类似交易参与者的增多有可能使得策略失效。本篇报告通过历史数据进行建模，但由于市场具有不确定性，模型仅在统计意义下有望获得较好投资业绩。另外，本报告不构成任何投资建议。

  

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









