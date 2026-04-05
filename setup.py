"""Setup script for financial-reporter."""

from setuptools import setup, find_packages

setup(
    name="financial-reporter",
    version="1.0.0",
    description="Production-grade financial report generator powered by local LLMs",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Financial Reporter Team",
    python_requires=">=3.10",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0",
        "rich>=13.0",
        "streamlit>=1.28",
        "requests>=2.28",
        "pyyaml>=6.0",
        "pandas>=2.0",
        "numpy>=1.24",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "financial-reporter=financial_reporter.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
