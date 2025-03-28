from setuptools import setup, find_packages

setup(
    name="ClaudeMCP",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.5.3",
    ],
    author="Mehrdad Mohamadali",
    author_email="your.email@example.com",
    description="Claude MCP Revit Integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mehrdadmo/MCPServer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 