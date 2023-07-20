from setuptools import setup, find_packages

setup(
    name="GmoWrapper",
    version="0.2",
    packages=find_packages(),
    install_requires=["requests", "rich", "pytz"],
)
