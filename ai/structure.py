from pydantic import BaseModel, Field

class ValueAssessment(BaseModel):
    """价值评估子结构 - 实用主义视角的多维度评估"""
    mechanism_insight: str = Field(
        description="机制洞察：揭示了什么反直觉的机制、矛盾或底层规律？如何改变了我们对该领域的认知模型？"
    )
    action_value: str = Field(
        description="行动启发：改进是渐进式(1-3x提升)/跨越式(5-10x提升)/新范式（改变游戏规则）？提供可立即验证、可操作的启发式规则"
    )
    transferability: str = Field(
        description="可迁移性：这个模式/机制可以迁移应用到哪3个其他领域？（要求结构同构，而非表面类比）"
    )
    value_score: str = Field(
        description="价值评分：高价值（立即深度处理）/中等价值（有趣但不紧急）/低价值（可能跳过）"
    )

class Structure(BaseModel):
    """论文分析输出结构 - 工程视角的价值提炼"""
    core_problem: str = Field(
        description="根本问题：论文所针对的最关键的矛盾点或知识空白是什么？"
    )
    key_insight: str = Field(
        description="切入视角：作者采用了什么区别于他人的关键洞察或新假设？"
    )
    method: str = Field(
        description="关键方法：作者用于验证其视角并解决问题的核心机制是什么？"
    )
    method_formula: str = Field(
        description="方法公式化：将关键方法抽象提炼成一个简洁的文字公式，揭示其内在的逻辑或演算过程（例如：新算法 = (特征A + 特征B) * 权重C）"
    )
    core_finding: str = Field(
        description="核心发现：最终得出了什么新知识或答案？"
    )
    value: ValueAssessment = Field(
        description="价值解读：从实用主义视角评估这个发现的真实价值"
    )
    summary_core: str = Field(
        description="一句话总结（核心价值）：将问题、视角、方法和发现四个要素熔合成一个单一、连贯、通顺且凝练的句子"
    )
    summary_layman: str = Field(
        description="一句话总结（大白话版）：用一个10岁小孩都能听懂的比喻或说法，概括论文最核心的观点"
    )