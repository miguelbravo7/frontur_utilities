from setuptools import setup, find_namespace_packages

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    import re
    requirements = list(map(lambda string: re.sub('==.*', '', string), f.read().splitlines()))

print(requirements)

setup(
    name="fronTur_utilities",
    author="Miguel Bravo Arvelo",
    author_email="alu0101031538@ull.edu.es",
    description="Trabajo de fin de grado",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.5",
    packages=find_namespace_packages(
        where="src"
    ),
    package_dir={"": "src"},
    include_package_data=True,

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires='docutils' + requirements,

    keywords="TFG ULL ISTAC",
    url="http://example.com/HelloWorld/",   # project home page, if any
    project_urls={
        "Documentation": "https://github.com/miguelbravo7/df_utilities#df_utilities",
        "Source Code": "https://github.com/miguelbravo7/df_utilities",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    entry_points={
        "console_scripts": [
            "frontur_utilities = df_utilities.commands:cli"
        ]
    },
    python_requires='>=3.7'
)
