# based on https://github.com/pypa/sampleproject
# MIT License

# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Extract version from cbsodata.py
for line in open(path.join("asreviewcontrib", "visualization", "__init__.py")):
    if line.startswith('__version__'):
        exec(line)
        break

setup(
    name='asreview-visualization',
    version=__version__,  # noqa
    description='Visualization tools for the ASReview project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/asreview/asreview-visualization',
    author='Utrecht University',
    author_email='asreview@uu.nl',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='asreview plot visualization',
    packages=find_namespace_packages(include=['asreviewcontrib.*']),
    install_requires=[
        "numpy", "matplotlib", "asreview",
    ],

    extras_require={
    },

    entry_points={
        "asreview.entry_points": [
            "plot = asreviewcontrib.visualization.entrypoint:PlotEntryPoint",
        ]
    },

    project_urls={
        'Bug Reports':
            "https://github.com/asreview/asreview-visualization/issues",
        'Source':
            "https://github.com/asreview/asreview-visualization",
    },
)
