from setuptools import setup, find_namespace_packages

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    import re
    requirements = list(map(lambda string: re.sub('==.*', '', string), f.read().splitlines()))

print(requirements)

setup(
    # metadata to display on PyPI
    name="HelloWorld",
    author="Miguel Bravo Arvelo",
    author_email="alu0101031538@ull.edu.es",
    description="Trabajo de fin de grado",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1",
    packages=find_namespace_packages(
        where="src"
    ),
    package_dir={"":"src"},
    include_package_data=True,

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["docutils>=0.3"] + requirements,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "hello" package, too:
        "hello": ["*.msg"],
    },

    keywords="TFG ULL ISTAC",
    url="http://example.com/HelloWorld/",   # project home page, if any
    project_urls={
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://github.com/miguelbravo7/TFG-Seleccion_de_Vuelos",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Languaje :: Python',
        'Operating System :: OS Independent',
        'Topic :: Data Science :: Operational Research'
    ],
    entry_points='''
        frontur_cli=TFG_Seleccion_de_Vuelos.df_utilities.commands:cli
        frontur_gui=TFG_Seleccion_de_Vuelos.interface.commands:cli
        frontur_solver=TFG_Seleccion_de_Vuelos.df_solver.commands:cli
    '''
)