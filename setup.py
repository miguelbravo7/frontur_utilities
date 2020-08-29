from setuptools import setup, find_namespace_packages

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    requirements = f.read().splitlines()

setup(
    name="fronTur_utilities",
    author="Miguel Bravo Arvelo",
    author_email="alu0101031538@ull.edu.es",
    description="Trabajo de fin de grado",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.1",
    packages=find_namespace_packages(),
    include_package_data=True,

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils'] + requirements,

    keywords="TFG ULL ISTAC",
    url="http://example.com/HelloWorld/",
    project_urls={
        "Documentation": "https://github.com/miguelbravo7/frontur_utilities/docs/frontur_utilities",
        "Source Code": "https://github.com/miguelbravo7/frontur_utilities",
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
            "frontur_utilities = frontur_utilities.commands:cli"
        ]
    },
    python_requires='>=3.7'
)
