<div align="center">

<!-- TODO: add banner -->

[![PyPI](https://img.shields.io/pypi/v/outlify)](https://pypi.org/project/outlify/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/outlify)
![Build](https://github.com/k1shk1n/outlify/actions/workflows/checks.yaml/badge.svg)
![Repo Size](https://img.shields.io/github/repo-size/k1shk1n/outlify)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


# outlify
Structured cli output — beautifully, simply, and dependency-free.

[Overview](#overview) •
[Install](#install) •
[Usage](#usage) •
[License](#license)

</div>

# Overview
**Outlify** is designed with a focus on streamlined log output, making it perfect for cli tools.
It emphasizes lightweight operation and minimal dependencies, ensuring smooth integration
into any project. The second key aspect of **Outlify** is its beautiful and user-friendly
log formatting, designed to enhance readability and provide a pleasant experience
for developers and their users.

## Install
**Outlify** is available as a Python package and can be easily installed via `pip` from [PyPI](https://pypi.org/project/outlify/). 
To install, simply run:
```bash
pip install outlify
```
This will automatically install the latest version of **Outlify**.

## Usage
### Panels
<details>
    <summary><kbd>demo</kbd></summary>

   To display demo use:
   ```bash
   python -m ourlify.panel
   ```
</details>

To highlight the importance of the text, you can display it in the panel. Try this:
```python
from outlify.panel import Panel

print(Panel('A very important text', title='Warning'))
```

## License
Licensed under the [MIT License, Copyright (c) 2025 Vladislav Kishkin](LICENSE)