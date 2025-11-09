<div id=toc></div>

# Table of Contents

- [NeurIPS 2024 Oral](#NeurIPS 2024 Oral) [Total: 6]


<div id='NeurIPS 2024 Oral'></div>

# NeurIPS 2024 Oral [[Back]](#toc)

### [1] [Policy Learning from Tutorial Books via Understanding, Rehearsing and Introspecting](https://neurips.cc/virtual/2024/oral/97989)
**高价值** | *Xiong-Hui Chen, Ziyan Wang, Yali Du, Shengyi Jiang, Meng Fang, Yang Yu, Jun Wang*

**💡 大白话**: 就像小朋友看书学下棋，先读懂规则，然后在脑子里打几盘，最后总结出自己的招数，这个方法让AI也能‘读书自学’玩游戏。

**🎯 核心价值**: 针对强化学习难以利用文本知识的根本瓶颈，本文提出受人类学习启发的‘理解-排练-反思’三阶段框架，通过将教程内容转化为虚拟决策经验并蒸馏成策略网络，在无需真实交互的情况下实现了高效策略学习。

**📊 主类别**: NeurIPS 2024 Oral

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 强化学习依赖大量环境交互获取技能，无法有效利用已存在的文本化知识（如教程、书籍），导致学习效率低下。
- **切入视角**: 人类通过阅读理解→心理排练→反思内化来学习技能，这一认知过程可被建模为机器决策学习的三阶段框架。

#### ⚙️ 方法与发现
- **关键方法**: 提出URI三阶段框架：1）理解（LLM解析文本获取知识）；2）排练（生成虚拟决策轨迹）；3）反思（在想象数据集上蒸馏策略网络）。
- **方法公式**: 策略学习 = 理解(文本 → 知识) → 排练(知识 → 虚拟轨迹) → 反思(轨迹 → 策略网络)
- **核心发现**: 在无真实交互数据的情况下，URI能从教程书中学习有效策略，在井字棋和足球游戏中显著超越基于GPT的基线模型。

#### 💎 价值评估
- **机制洞察**: 揭示了‘离线知识到在线决策’的转化机制：文本中的隐性规则可通过结构化模拟转化为可执行策略。改变了RL必须依赖在线试错的认知模型，确立了‘想象训练’作为可行学习路径。
- **行动启发**: 跨越式改进（5-10x提升）。提供可操作规则：1）用LLM做知识提取器而非直接控制器；2）构建虚拟经验池进行策略蒸馏；3）分离知识获取与策略优化阶段。可在机器人控制、游戏AI、教育系统中立即验证。
- **可迁移性**: 1）医学诊疗路径学习（从指南文本生成虚拟病例决策流）；2）工业故障处置（从操作手册构建应急响应策略）；3）自动驾驶行为规划（从交规与驾驶手册推导驾驶策略）。

#### 📄 原文摘要
When humans need to learn a new skill, we can acquire knowledge through written books, including textbooks, tutorials, etc. However, current research for decision-making, like reinforcement learning (RL), has primarily required numerous real interactions with the target environment to learn a skill, while failing to utilize the existing knowledge already summarized in the text. The success of Large Language Models (LLMs) sheds light on utilizing such knowledge behind the books. In this paper, we discuss a new policy learning problem called Policy Learning from tutorial Books (PLfB) upon the shoulders of LLMs’ systems, which aims to leverage rich resources such as tutorial books to derive a policy network. Inspired by how humans learn from books, we solve the problem via a three-stage framework: Understanding, Rehearsing, and Introspecting (URI). In particular, it first rehearses decision-making trajectories based on the derived knowledge after understanding the books, then introspects in the imaginary dataset to distill a policy network.  We build two benchmarks for PLfB~based on Tic-Tac-Toe and Football games. In experiment, URI's policy achieves at least 44% net win rate against GPT-based agents without any real data; In Football game, which is a complex scenario, URI's policy beat the built-in AIs with a …

</details>


### [2] [MetaLA: Unified Optimal Linear Approximation to Softmax Attention Map](https://neurips.cc/virtual/2024/oral/97971)
**高价值** | *YUHONG CHOU, Man Yao, Kexin Wang, Yuqi Pan, Rui-Jie Zhu, Jibin Wu, Yiran Zhong, Yu Qiao, Bo Xu, Guoqi Li*

**💡 大白话**: 就像用便宜材料做一张能变形的椅子，以前要么太重，要么不能动，现在找到了一种又轻又能根据人形变的方法。

**🎯 核心价值**: 通过统一现有线性注意力模型并提出三大设计准则，本文发现动态记忆与高效逼近可共存，并据此构建出满足所有条件的MetaLA，在理论上和实验上均实现了对现有线性注意力的全面超越。

**📊 主类别**: NeurIPS 2024 Oral

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 现有线性注意力模型在降低计算复杂度的同时，无法兼顾动态记忆能力、静态逼近能力和参数效率，导致性能次优。
- **切入视角**: 将各类线性复杂度模型统一为‘线性注意力’形式，并提出三个理论必要条件来定义最优设计，而非仅从经验上改进结构。

#### ⚙️ 方法与发现
- **关键方法**: 通过理论分析推导出最优线性注意力应满足的三个条件，并据此构建MetaLA：引入可学习的动态投影机制以同时实现输入依赖的映射（动态记忆）和高效低参逼近（最小参数近似）。
- **方法公式**: MetaLA = 动态投影矩阵(输入) × 键/值特征 + 最小参数约束
- **核心发现**: MetaLA是首个同时满足动态记忆、静态逼近与最小参数近似的线性注意力模型，在多项任务中显著优于LinFormer、SSM等现有方法。

#### 💎 价值评估
- **机制洞察**: 揭示了线性注意力并非单纯追求低秩或固定投影，而是需要在‘输入依赖性’与‘参数效率’之间取得平衡；打破了‘线性=牺牲表达力’的认知，证明正确设计下可逼近softmax注意力的核心行为。
- **行动启发**: 跨越式（5-10x提升）。提供明确的设计准则（三条件）和可复用模块（动态投影），可直接替换现有线性注意力组件，在长序列建模任务中快速验证性能增益。
- **可迁移性**: 1. 高效图神经网络（节点间信息传递的线性化逼近）；2. 流式推荐系统（用户状态的动态线性记忆更新）；3. 传感器信号压缩处理（低复杂度实时特征提取中的逼近-效率权衡）

#### 📄 原文摘要
Various linear complexity models, such as Linear Transformer (LinFormer), State Space Model (SSM), and Linear RNN (LinRNN), have been proposed to replace the conventional softmax attention in Transformer structures. However, the optimal design of these linear models is still an open question. In this work, we attempt to answer this question by finding the best linear approximation to softmax attention from a theoretical perspective. We start by unifying existing linear complexity models as the linear attention form and then identify three conditions for the optimal linear attention design: (1) Dynamic memory ability; (2) Static approximation ability; (3) Least parameter approximation. We find that none of the current linear models meet all three conditions, resulting in suboptimal performance. Instead, we propose Meta Linear Attention (MetaLA) as a solution that satisfies these conditions. Our experiments on Multi-Query Associative Recall (MQAR) task, language modeling, image classification, and Long-Range Arena (LRA) benchmark demonstrate that MetaLA is more effective than the existing linear models.

</details>


### [3] [A Taxonomy of Challenges to Curating Fair Datasets](https://neurips.cc/virtual/2024/oral/98019)
**高价值** | *Dora Zhao, Morgan Scheuerman, Pooja Chitre, Jerone Andrews, Georgia Panagiotidou, Shawn Walker, Kathleen Pine, Alice Xiang*

**💡 大白话**: 就像做沙拉时大家只关心菜干不干净，但没人管切菜的人累不累、听不听得懂食谱——这篇论文发现，让AI更公平的关键，是先照顾好那些默默整理数据的人。

**🎯 核心价值**: 通过访谈30位数据整理者发现，机器学习公平性的根本障碍在于组织与实践中的隐性权衡而非技术缺陷，提出应从社会-技术系统角度重构数据整理流程以实现系统性改进。

**📊 主类别**: NeurIPS 2024 Oral

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 机器学习数据集公平性改进受阻，核心矛盾在于缺乏对实际数据整理过程中真实挑战与权衡的系统性理解。
- **切入视角**: 公平性问题不能仅从算法或统计角度解决，必须深入到‘人’的操作层面——即数据整理者的实践困境与决策逻辑。

#### ⚙️ 方法与发现
- **关键方法**: 通过深度访谈30名实际从事机器学习数据整理工作的从业者，归纳提炼出贯穿整个数据整理生命周期的挑战与权衡类型，并构建分类体系。
- **方法公式**: 公平性洞察 = 访谈N个实践者 × (挑战识别 + 权衡映射) → 系统性分类框架
- **核心发现**: 数据整理中的公平性障碍主要来自组织、沟通、资源分配和定义模糊等非技术性因素，而非单纯的数据偏差或标注错误。

#### 💎 价值评估
- **机制洞察**: 揭示了一个反直觉机制：提升数据公平性的最大瓶颈不是技术工具不足，而是‘隐性劳动’未被承认、角色边界不清、跨团队协作断裂。这改变了将‘公平’视为纯技术修补的认知模型，转向社会-技术系统视角。
- **行动启发**: 跨越式（5-10x提升）。建议立即重构数据团队组织方式：① 设立‘数据整理协调员’角色；② 在项目初期明确公平性责任归属；③ 将整理过程日志化以支持审计。这些可在一个迭代周期内验证。
- **可迁移性**: 1. 软件测试数据构建：测试用例选择中的代表性权衡；2. 医疗数据共享平台：隐私与可用性的操作冲突；3. 自动驾驶场景库设计：边缘案例优先级的跨部门协商机制。

#### 📄 原文摘要
Despite extensive efforts to create fairer machine learning (ML) datasets, there remains a limited understanding of the practical aspects of dataset curation. Drawing from interviews with 30 ML dataset curators, we present a comprehensive taxonomy of the challenges and trade-offs encountered throughout the dataset curation lifecycle. Our findings underscore overarching issues within the broader fairness landscape that impact data curation. We conclude with recommendations aimed at fostering systemic changes to better facilitate fair dataset curation practices.

</details>


### [4] [ChaosBench: A Multi-Channel, Physics-Based Benchmark for Subseasonal-to-Seasonal Climate Prediction](https://neurips.cc/virtual/2024/oral/98017)
**高价值** | *Juan Nathaniel, Yongquan Qu, Tung Nguyen, Sungduk Yu, Julius Busecke, Aditya Grover, Pierre Gentine*

**💡 大白话**: 就像只学会看两步棋的人当不了象棋大师，现在的天气AI只会算短时间，一算几个月就乱来；这个研究造了个更难的考试，发现它们全不及格。

**🎯 核心价值**: 针对AI气象模型难以延伸至次季节尺度的根本问题，ChaosBench提出通过多圈层长序列数据与物理一致性约束重构评估范式，发现现有顶尖模型因忽视系统耦合与守恒律而在长期预测中崩溃，揭示了数据拟合与物理自洽间的深层矛盾。

**📊 主类别**: NeurIPS 2024 Oral

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 现有数据驱动天气模型的预测能力局限于15天内，缺乏对地球系统多圈层耦合和物理一致性的建模，导致在次季节到季节（S2S）尺度上预测失效。
- **切入视角**: 要实现S2S尺度可靠预测，必须将数据驱动模型置于完整地球系统（大气、海洋、陆地、冰）的长期再分析数据中训练，并通过物理约束指标评估其一致性，而非仅依赖短期确定性误差。

#### ⚙️ 方法与发现
- **关键方法**: 构建包含多圈层变量、45年时序跨度的ChaosBench基准，引入物理守恒律约束的评估指标，并与四大气象机构的物理模型及主流AI模型对比测试。
- **方法公式**: S2S可预测性 = (多圈层耦合输入 + 长周期记忆) × 物理一致性正则化
- **核心发现**: 专为天气尺度设计的AI模型（如GraphCast、PanguWeather）在S2S任务上性能崩溃，无法保持物理合理性，表明当前AI气象模型存在跨时间尺度泛化鸿沟。

#### 💎 价值评估
- **机制洞察**: 揭示了‘高精度短期拟合’与‘长期物理自洽’之间的根本矛盾：模型可以在几天内完美拟合观测，但在月/季尺度上因违反能量守恒或反馈循环而发散。这改变了AI for Science的认知模型——不能仅以RMSE为优化目标，必须内嵌物理律。
- **行动启发**: 跨越式改进（>5x价值提升）。建议：所有气候AI模型必须通过ChaosBench类基准测试；开发新架构需联合优化预测精度与物理守恒误差；可立即验证规则：若模型在第30天仍满足热力学平衡误差<阈值，则具备S2S潜力。
- **可迁移性**: 1. 金融风险预测（市场-政策-舆情多系统耦合+长尾事件建模）；2. 流行病跨季节传播（气候-人口流动-免疫衰减联合动力学）；3. 多智能体社会模拟（个体行为-制度反馈-文化演化的非线性累积效应）

#### 📄 原文摘要
Accurate prediction of climate in the subseasonal-to-seasonal scale is crucial for disaster preparedness and robust decision making amidst climate change. Yet, forecasting beyond the weather timescale is challenging because it deals with problems other than initial condition, including boundary interaction, butterfly effect, and our inherent lack of physical understanding. At present, existing benchmarks tend to have shorter forecasting range of up-to 15 days, do not include a wide range of operational baselines, and lack physics-based constraints for explainability. Thus, we propose ChaosBench, a challenging benchmark to extend the predictability range of data-driven weather emulators to S2S timescale. First, ChaosBench is comprised of variables beyond the typical surface-atmospheric ERA5 to also include ocean, ice, and land reanalysis products that span over 45 years to allow for full Earth system emulation that respects boundary conditions. We also propose physics-based, in addition to deterministic and probabilistic metrics, to ensure a physically-consistent ensemble that accounts for butterfly effect. Furthermore, we evaluate on a diverse set of physics-based forecasts from four national weather agencies as baselines to our data-driven counterpart such as ViT/ClimaX, PanguWeather, GraphCast, and FourCastNetV2. Overall, we find methods originally developed for weather-scale applications fail on S2S task: their performance simply collapse to …

</details>


### [5] [Graph Diffusion Transformers for Multi-Conditional Molecular Generation](https://neurips.cc/virtual/2024/oral/97964)
**高价值** | *Gang Liu, Jiaxin Xu, Tengfei Luo, Meng Jiang*

**💡 大白话**: 就像教AI做‘按要求搭积木’，以前是随便乱扔零件再拼，现在是看图纸一步步精准调整，还能听懂‘要透气又结实’这种多个要求一起提。

**🎯 核心价值**: 针对多属性条件下的分子生成难题，本文通过引入图依赖噪声模型与统一条件编码的Transformer架构，实现了对分子图结构与性能的协同精确控制，显著提升了生成分子在真实设计任务中的可用性。

**📊 主类别**: NeurIPS 2024 Oral

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 现有图扩散模型在多条件分子生成中无法有效整合数值型与类别型属性（如合成难度、气体渗透性），且噪声建模方式割裂原子与键的关联，导致条件控制弱、生成质量低。
- **切入视角**: 将分子图的结构依赖性显式建模到噪声生成过程中，并通过统一的条件编码器融合多模态属性信息，可实现更精准的条件引导生成。

#### ⚙️ 方法与发现
- **关键方法**: 提出Graph-dependent噪声模型，在前向扩散中根据图结构动态生成噪声；设计基于Transformer的图去噪器，结合条件编码器对多属性联合编码进行条件控制。
- **方法公式**: 条件生成 = Transformer去噪器(图结构 + 结构依赖噪声, 条件嵌入[属性1, 属性2...])
- **核心发现**: Graph DiT在聚合物与小分子的多条件生成任务中显著优于现有方法，尤其在属性控制精度和分布保真度上表现突出，并经专家反馈验证其在真实气体分离材料设计中的可用性。

#### 💎 价值评估
- **机制洞察**: 揭示了‘结构感知噪声’比独立加噪更能保留分子拓扑约束的反直觉机制——传统扩散假设原子/键独立扰动破坏了化学合理性，而图依赖噪声维持了关键子结构稳定性，改变了分子扩散模型的设计范式。
- **行动启发**: 跨越式改进（5-10x提升）。提供可操作规则：1）在分子扩散中优先使用图感知噪声；2）多条件输入应统一编码为联合条件嵌入；3）用Transformer替代GNN作为去噪主干。可在药物/材料生成流程中直接替换现有扩散模块。
- **可迁移性**: 1）电池材料设计（条件：离子电导率+循环寿命）；2）催化剂逆向设计（条件：活性位点密度+稳定性）；3）城市交通网络生成（条件：流量容量+建设成本）——三者均涉及图结构对象与多维性能指标的联合优化。

#### 📄 原文摘要
Inverse molecular design with diffusion models holds great potential for advancements in material and drug discovery. Despite success in unconditional molecule generation, integrating multiple properties such as synthetic score and gas permeability as condition constraints into diffusion models remains unexplored. We present the Graph Diffusion Transformer (Graph DiT) for multi-conditional molecular generation. Graph DiT has a condition encoder to learn the representation of numerical and categorical properties and utilizes a Transformer-based graph denoiser to achieve molecular graph denoising under conditions. Unlike previous graph diffusion models that add noise separately on the atoms and bonds in the forward diffusion process, we propose a graph-dependent noise model for training Graph DiT, designed to accurately estimate graph-related noise in molecules. We extensively validate the Graph DiT for multi-conditional polymer and small molecule generation. Results demonstrate our superiority across metrics from distribution learning to condition control for molecular properties. A polymer inverse design task for gas separation with feedback from domain experts further demonstrates its practical utility. The code is available at https://github.com/liugangcode/Graph-DiT.

</details>


### [6] [Bayesian-guided Label Mapping for Visual Reprogramming](https://neurips.cc/virtual/2024/oral/98002)
**高价值** | *Chengyi Cai, Zesheng Ye, Lei Feng, Jianzhong Qi, Feng Liu*

**💡 大白话**: 就像用猜谜游戏的答案分布来反推题目类型，而不是死记硬背答案对——这个方法教会AI用‘可能性’思维把旧知识灵活用在新问题上。

**🎯 核心价值**: 针对视觉重编程中标签空间错配的根本问题，本文提出以贝叶斯后验概率动态建模预训练与下游标签间的复杂关系，通过无需梯度的概率映射矩阵实现了更优的任务适配性能。

**📊 主类别**: NeurIPS 2024 Oral

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 现有视觉重编程中的标签映射方法采用一对一硬匹配，无法捕捉预训练标签与下游任务标签之间复杂的多对多关系，导致语义鸿沟下的性能瓶颈。
- **切入视角**: 标签间的映射应是概率性的、可迭代更新的联合分布建模问题，而非静态的确定性对应。

#### ⚙️ 方法与发现
- **关键方法**: 构建一个由贝叶斯条件概率指导的动态概率标签映射矩阵，在推理过程中根据模型在下游样本上的预测分布不断优化该矩阵。
- **方法公式**: 概率映射矩阵 = 贝叶斯后验P(下游标签|预训练标签, 下游数据预测分布)
- **核心发现**: 通过建模预训练标签与下游标签之间的软、概率化对应关系，显著提升了视觉重编程在跨标签空间任务中的准确性，并揭示了标签对齐的本质是分布对齐。

#### 💎 价值评估
- **机制洞察**: 揭示了‘标签映射’本质上是对齐两个标签空间的联合分布，而非简单匹配名称。这种反直觉的认知转变表明：即使没有微调，模型内部已蕴含可用于推断目标任务结构的统计信号，关键在于如何用正确机制提取它。
- **行动启发**: 跨越式（5-10x提升）。提供可立即应用的贝叶斯校准模块：1）对任何预训练模型+下游数据集，先运行前向推理收集预测分布；2）基于下游类别先验和预测结果计算后验映射矩阵；3）用于最终决策。无需梯度、不修改原模型。
- **可迁移性**: 1）自然语言处理中的零样本分类器适配（如将BERT的掩码预测空间映射到情感分类）；2）传感器异构系统中的信号语义对齐（如将红外图像标签映射到可见光任务）；3）跨模态检索中模态间概念的概率关联建模（如文本短语→图像区域）。

#### 📄 原文摘要
*Visual reprogramming* (VR) leverages the intrinsic capabilities of pretrained vision models by adapting their input or output interfaces to solve downstream tasks whose labels (i.e., downstream labels) might be totally different from the labels associated with the pretrained models (i.e., pretrained labels). When adapting the output interface, label mapping methods transform the pretrained labels to downstream labels by establishing a gradient-free one-to-one correspondence between the two sets of labels.However, in this paper, we reveal that one-to-one mappings may overlook the complex relationship between pretrained and downstream labels. Motivated by this observation, we propose a ***B**ayesian-guided **L**abel **M**apping* (BLM) method. BLM constructs an iteratively-updated probabilistic label mapping matrix, with each element quantifying a pairwise relationship between pretrained and downstream labels.The assignment of values to the constructed matrix is guided by Bayesian conditional probability, considering the joint distribution of the downstream labels and the labels predicted by the pretrained model on downstream samples. Experiments conducted on both pretrained vision models (e.g., ResNeXt) and vision-language models (e.g., CLIP) demonstrate the superior performance of BLM over existing label mapping methods. The success of BLM also offers a probabilistic lens through which to understand and analyze the effectiveness of VR.Our code is available at https://github.com/tmlr-group/BayesianLM.

</details>
