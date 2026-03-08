from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ghostlite",
    version="1.0.1",
    author="Praveen Kumar",
    description="A lightweight Python database with SQL, API, dashboard, and distributed mode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests"],
)