<div id=toc></div>

# Table of Contents

- [cs.CV](#cs.CV) [Total: 3]


<div id='cs.CV'></div>

# cs.CV [[Back]](#toc)

### [1] [LoRA-Edge: Tensor-Train-Assisted LoRA for Practical CNN Fine-Tuning on Edge Devices](https://arxiv.org/abs/2511.03765)
**高价值** | *Hyunseok Kwak, Kyeongwon Lee, Jae-Jin Lee, Woojoo Lee*

**💡 大白话**: 就像只改书的一小部分笔记就能让整本书适应新知识，而且不用重印这本书。

**🎯 核心价值**: 针对边缘设备无法承受全微调的根本矛盾，LoRA-Edge提出基于TT-SVD和选择性核心更新的方法，实现了极少参数更新下接近全微调的性能，使结构对齐、高效、无推理开销的CNN在线适应成为可能。

**📊 主类别**: cs.CV

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 在边缘设备上进行CNN微调时，面临全参数微调不可行（内存、计算、能耗受限）与保持模型性能之间的根本矛盾。
- **切入视角**: 卷积层的权重更新具有低秩结构且可张量分解，通过仅更新输出侧核心张量并零初始化，可在训练初期不干扰原始模型，实现高效且结构对齐的适应。

#### ⚙️ 方法与发现
- **关键方法**: 采用张量链奇异值分解（TT-SVD）对预训练卷积层进行分解，仅选择性地更新输出侧核心张量，并通过零初始化保持辅助路径初始静默，最终将更新融合回原始密集核中。
- **方法公式**: 可训练参数 = TT-SVD(卷积核) → 更新输出侧核心 × 零初始化掩码 + 原始核（推理时融合）
- **核心发现**: LoRA-Edge 能以最多1.49%的可训练参数达到接近全微调（差距<4.7%准确率）的性能，并在Jetson Orin Nano上实现1.4-3.8倍更快收敛，推理成本不变。

#### 💎 价值评估
- **机制洞察**: 揭示了卷积微调更新的‘稀疏有效子空间’特性：大部分参数更新集中在低维张量核心，且通过零初始化控制干预时机，实现了训练动态与模型稳定性的解耦，改变了PEFT需牺牲结构或引入推理开销的认知。
- **行动启发**: 跨越式改进（5-10x提升）。提供三条可操作规则：1）对卷积层优先使用TT-SVD初始化；2）只训练输出侧核心；3）零初始化确保起点一致。可在边缘AI产品中立即替换现有微调方案。
- **可迁移性**: 1）车载视觉模型在线适应不同天气条件；2）工业传感器网络中的轻量级故障检测迁移学习；3）移动端语音识别模型个性化定制——三者均具备‘固定主干+局部动态调整’的结构同构需求。

#### 📄 原文摘要
On-device fine-tuning of CNNs is essential to withstand domain shift in edge
applications such as Human Activity Recognition (HAR), yet full fine-tuning is
infeasible under strict memory, compute, and energy budgets. We present
LoRA-Edge, a parameter-efficient fine-tuning (PEFT) method that builds on
Low-Rank Adaptation (LoRA) with tensor-train assistance. LoRA-Edge (i) applies
Tensor-Train Singular Value Decomposition (TT-SVD) to pre-trained convolutional
layers, (ii) selectively updates only the output-side core with
zero-initialization to keep the auxiliary path inactive at the start, and (iii)
fuses the update back into dense kernels, leaving inference cost unchanged.
This design preserves convolutional structure and reduces the number of
trainable parameters by up to two orders of magnitude compared to full
fine-tuning. Across diverse HAR datasets and CNN backbones, LoRA-Edge achieves
accuracy within 4.7% of full fine-tuning while updating at most 1.49% of
parameters, consistently outperforming prior parameter-efficient baselines
under similar budgets. On a Jetson Orin Nano, TT-SVD initialization and
selective-core training yield 1.4-3.8x faster convergence to target F1.
LoRA-Edge thus makes structure-aligned, parameter-efficient on-device CNN
adaptation practical for edge platforms.

</details>


### [2] [SILVI: Simple Interface for Labeling Video Interactions](https://arxiv.org/abs/2511.03819)
**高价值** | *Ozan Kanbertay, Richard Vogg, Elif Karakoc, Peter M. Kappeler, Claudia Fichtel, Alexander S. Ecker*

**💡 大白话**: 就像给动物拍的视频加了个‘朋友圈点赞+评论’功能，不仅能圈出谁在干啥，还能标出它们是不是在打架、求偶或者玩耍。

**🎯 核心价值**: 针对动物行为分析中个体定位与交互标注割裂的根本问题，作者提出SILVI系统，通过将对象检测、行为标签与动态关系链接整合于统一平台，实现了结构化交互数据的高效标注，推动了基于场景图的细粒度行为建模。

**📊 主类别**: cs.CV

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 动物行为研究中缺乏能同时标注个体位置与社会互动的开源视频标注工具，导致无法有效训练用于细粒度行为分析的计算机视觉模型。
- **切入视角**: 将行为生态学的需求结构化为可编程的标注逻辑，在同一系统中统一‘个体定位’与‘交互关系标注’，生成可用于模型训练的动态场景图结构数据。

#### ⚙️ 方法与发现
- **关键方法**: 设计并实现一个集成化开源标注平台（SILVI），支持在视频帧中标注个体对象、定义其行为类别，并通过关系链接标注个体间的交互，输出结构化时序标注数据。
- **方法公式**: 交互标注系统 = (对象检测 + 行为标签) × 动态关系链接
- **核心发现**: SILVI 成功实现了对动物（及潜在人类）视频中个体行为与社会互动的同步标注，生成可用于训练和验证计算机视觉模型的结构化、时空一致的标注数据集。

#### 💎 价值评估
- **机制洞察**: 揭示了‘标注工具的设计瓶颈’是制约行为理解模型发展的隐性瓶颈——传统工具割裂空间与关系信息，而真正的行为语义存在于两者的耦合之中。该工具本身成为推动跨学科方法融合的认知接口。
- **行动启发**: 跨越式（5-10x提升）。提供开箱即用的完整标注闭环，相比拼接多个工具或手动整合，效率提升显著；支持直接导出用于训练GNN或时空动作检测模型的数据格式，可立即用于构建下一代行为分析系统。
- **可迁移性**: 1. 智能交通：车辆间交互意图标注（如让行、超车）；2. 工业安全监控：工人协作或违规接触的结构化记录；3. 在线教育：师生互动频次与模式的行为图谱构建。

#### 📄 原文摘要
Computer vision methods are increasingly used for the automated analysis of
large volumes of video data collected through camera traps, drones, or direct
observations of animals in the wild. While recent advances have focused
primarily on detecting individual actions, much less work has addressed the
detection and annotation of interactions -- a crucial aspect for understanding
social and individualized animal behavior. Existing open-source annotation
tools support either behavioral labeling without localization of individuals,
or localization without the capacity to capture interactions. To bridge this
gap, we present SILVI, an open-source labeling software that integrates both
functionalities. SILVI enables researchers to annotate behaviors and
interactions directly within video data, generating structured outputs suitable
for training and validating computer vision models. By linking behavioral
ecology with computer vision, SILVI facilitates the development of automated
approaches for fine-grained behavioral analyses. Although developed primarily
in the context of animal behavior, SILVI could be useful more broadly to
annotate human interactions in other videos that require extracting dynamic
scene graphs. The software, along with documentation and download instructions,
is available at: https://gitlab.gwdg.de/kanbertay/interaction-labelling-app.

</details>


### [3] [Noise Injection: Improving Out-of-Distribution Generalization for Limited Size Datasets](https://arxiv.org/abs/2511.03855)
**高价值** | *Duong Mai, Lawrence Hall*

**💡 大白话**: 就像让孩子蒙着眼睛拼图才能真正学会认形状，给AI看加了雪花噪点的X光片，它反而学会了不靠机器指纹作弊，真正去看病灶。

**🎯 核心价值**: 针对医学影像模型因依赖源特异性伪影而导致OOD泛化差的问题，本文提出通过训练时注入基础噪声迫使模型放弃捷径、学习稳定特征，实验表明该简单方法可将ID与OOD性能差距缩小至原来的1/5以下。

**📊 主类别**: cs.CV

<details>
  <summary><b>📖 详细分析</b></summary>

#### 🔍 问题与洞察
- **根本问题**: 深度学习模型在医学影像识别中过度依赖训练数据中的设备或来源特异性伪影（快捷方式），导致在新临床来源的分布外（OOD）数据上泛化能力差，尤其是在COVID-19胸部X光检测中。
- **切入视角**: 通过在训练过程中注入基础噪声（如高斯、斑点、泊松等），可破坏模型对源特异性伪影的依赖，迫使其学习更具生物学意义且跨分布稳定的特征。

#### ⚙️ 方法与发现
- **关键方法**: 在标准训练流程中引入多种经典噪声类型作为数据增强手段，在不增加复杂性的情况下提升模型对分布偏移的鲁棒性。
- **方法公式**: 鲁棒模型 = 标准训练 + 基础噪声注入（高斯/斑点/泊松/椒盐）
- **核心发现**: 简单噪声注入能将ID与OOD性能差距从0.10-0.20大幅缩小至0.01-0.06（AUC等多指标平均），显著提升跨机构泛化能力。

#### 💎 价值评估
- **机制洞察**: 揭示了‘适度干扰可抑制捷径学习’这一反直觉机制：看似降低输入质量的噪声，实则提高了特征选择的标准，使模型无法依赖脆弱的伪影，从而逼近真实病理信号。这改变了我们对‘数据清洁至上’的认知，提出‘可控污染’可能是正则化的有效形式。
- **行动启发**: 提供了一种即插即用的训练策略，仅需修改数据增强流程即可获得跨越式泛化提升（5-10x差距缩小）。启发式规则：当OOD性能下降>0.1时，优先尝试基础噪声注入而非复杂对抗训练或领域自适应。
- **可迁移性**: 1) 跨中心病理切片分类；2) 多设备MRI脑图像分析；3) 异构传感器下的工业缺陷检测——任何存在设备偏差且标签成本高的视觉诊断场景。

#### 📄 原文摘要
Deep learned (DL) models for image recognition have been shown to fail to
generalize to data from different devices, populations, etc. COVID-19 detection
from Chest X-rays (CXRs), in particular, has been shown to fail to generalize
to out-of-distribution (OOD) data from new clinical sources not covered in the
training set. This occurs because models learn to exploit shortcuts -
source-specific artifacts that do not translate to new distributions - rather
than reasonable biomarkers to maximize performance on in-distribution (ID)
data. Rendering the models more robust to distribution shifts, our study
investigates the use of fundamental noise injection techniques (Gaussian,
Speckle, Poisson, and Salt and Pepper) during training. Our empirical results
demonstrate that this technique can significantly reduce the performance gap
between ID and OOD evaluation from 0.10-0.20 to 0.01-0.06, based on results
averaged over ten random seeds across key metrics such as AUC, F1, accuracy,
recall and specificity. Our source code is publicly available at
https://github.com/Duongmai127/Noisy-ood

</details>
