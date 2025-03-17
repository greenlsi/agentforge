from setuptools import setup, find_packages

setup(
    name="agentforge-core",
    version="0.1.0",
    description="Framework modular para sistemas de agentes de IA",
    author="AgentForge Team",
    author_email="info@agentforge.dev",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "python-dotenv>=0.19.0",
        "tenacity>=8.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.5.0"],
        "groq": ["groq>=0.3.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=0.900",
        ],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.5.0",
            "groq>=0.3.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
