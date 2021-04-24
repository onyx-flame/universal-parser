import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="universal-parser-onyx_flame",
    version="1.0.1",
    author="Vyacheslav Zakharchuk",
    author_email="sovenok997@gmail.com",
    description="Json/Pickle/Toml/Yaml parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onyx-flame/universal-parser",
    project_urls={
        "Bug Tracker": "https://github.com/onyx-flame/universal-parser/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['scripts/format_converter'],
    packages=setuptools.find_packages(),
    install_requires=['PyYaml', 'pytomlpp'],
    python_requires=">=3.6",
)
