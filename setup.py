import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="journyio-sdk",
    version="0.0.1",
    author="journy.io",
    author_email="hello@journy.io",
    description="This is the official Python SDK for journy.io.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/journy-io/python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)