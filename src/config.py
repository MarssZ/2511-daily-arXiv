"""配置管理"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """全局配置管理"""

    def __init__(self):
        # 加载 .env 文件
        load_dotenv()

        # API 配置
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

        # arXiv 配置
        self.arxiv_categories = os.getenv("ARXIV_CATEGORIES", "cs.AI").split(",")
        self.max_papers_per_category = int(os.getenv("MAX_PAPERS_PER_CATEGORY", "50"))

        # 输出配置
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
        self.output_language = os.getenv("OUTPUT_LANGUAGE", "zh")

        # 研究母题
        self.research_topics = self._load_research_topics()

    def _load_research_topics(self) -> list[str]:
        """从 config/research_topics.txt 加载研究母题"""
        topics_file = Path("config/research_topics.txt")
        if not topics_file.exists():
            raise FileNotFoundError(
                "未找到 config/research_topics.txt，请先创建该文件并添加研究母题"
            )

        topics = []
        with open(topics_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 忽略空行和注释
                if line and not line.startswith("#"):
                    topics.append(line)

        if not topics:
            raise ValueError(
                "研究母题列表为空，请在 config/research_topics.txt 中添加至少一个母题"
            )

        return topics

    def validate(self):
        """验证配置完整性"""
        if not self.api_key:
            raise ValueError("未找到 API 密钥，请在 .env 文件中设置 OPENAI_API_KEY")

        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "archive").mkdir(exist_ok=True)
