An example manual done while implementing CI/CD for https://github.com/cyberhexe/reverse-shell-generator

- https://packaging.python.org/en/latest/tutorials/packaging-projects/

## Creating the skeleton

Create the following file structure locally:

```text
revshell-generator/
  src/
    reverseshellgenerator/
      __init__.py
      generator.py
  README.md
  pyproject.toml
  setup.py
  .gitignore
```

`__init__.py` is required to import the directory as a package, and should be empty.


Configuring pyproject.toml:

`pyproject.toml` tells build tools (like pip and build) what is required to build your project.

```text
[build-system]
requires = [
    "setuptools>=42",
    "termcolor"
]
build-backend = "setuptools.build_meta"
```

## Configuring metadata

There are two types of metadata: static and dynamic.
• `Static metadata (setup.cfg):` guaranteed to be the same every time. This is simpler, easier to read, and avoids many common errors, like encoding errors.
• `Dynamic metadata (setup.py):` possibly non-deterministic. Any items that are dynamic or determined at install-time, as well as extension modules or extensions to `setuptools`, need to go into setup.py.

`setup.py` is the build script for setuptools. It tells `setuptools` about your package (such as the name and version) as well as which code files to include.

```python
#!/usr/bin/env python3

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='revshell-generator',  # Required
    version='1.0.0',  # Required
    description='Reverse shell commands generator',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/cyberhexe/revshell-generator',  # Optional
    author='a',  # Optional
    author_email='a@a.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',

        'License :: OSI Approved :: MIT License',

        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='pentest, red-team, shell',  # Optional
    package_dir={'': './src'},  # Optional
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.6, <4',
    install_requires=[
        'termcolor'
    ],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'revshell-generator=reverseshellgenerator.generator:main',
        ],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/cyberhexe/revshell-generator/issues',
        'Source': 'https://github.com/cyberhexe/revshell-generator',
    },
)
```

Also create the README.md file with content to be included on the PyPI web page of your package.

## Creating a LICENSE


It's important for every package uploaded to the Python Package Index to include a license. 
This tells users who install your package the terms under which theycan use your package. 

For help picking a license, see https://choosealicense.com/. 

```text
MIT:
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


## Generating distribution archives

Download the latest version of PyPA's build installed:

```bash
python3 -m pip install --upgrade build
```

Build the package:

```bash
python3 -m build
```

The `tar.gz` file is a source archive whereas the.whl file is a built distribution.
Newer pip versions preferentially install built distributions, but will fallback to source archives if needed.

PS: you may want to add `./build` and `./dist` folders to `.gitignore`.


## Uploading the distribution archives (to TestPyPI) 
 
To securely upload your project, you’ll need a PyPI API token. 

Create one at https://test.pypi.org/manage/account/#api-tokens, setting the "Scope" to "Entire account".

Install or upgrade twine:

```bash
python3 -m pip install --upgrade twine
```

Upload the package:

```bash
python3 -m twine upload --repository testpypi dist/*
```

Repeat with real PyPI afterwards.
```bash
python3 -m twine upload dist/*
```