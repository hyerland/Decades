---
hide:
  - navigation
  - toc
---
# Decades ⌚

!!! warning
    Decades is currently within development and has **NOT** reached **v1.0.0** release.

A CLI tool to save recovery snapshots of your projects or files. ⌚

## So... what is decades? 🤔

Decades *(in my words)* is a way to **locally** backup your projects or files **without a git repository** being present.
No matter if you have no internet connection, or if you don't have git installed, you can still use decades to save your projects or files.

Decades is designed to be...

- Easy to use 🧑
- Fast and Portable 📦 🚀
- Work with any OS 🐧
- and Secure 🛡️
- Local only[^1] 🌍

## Installation 📦

!!! note
    Check the PyPI page [here](https://pypi.org/project/decades/) for installation instructions for latest versions of Decades.

To install Decades, simply run the following command:

```bash
pip install decades
```

This will install the latest **stable** version of Decades from **PyPI repository** to your system.

## Quick Start 🚀

Using Decades is quite simple. Just run the following command to take a, 'snapshot' of your project or file:

```bash
decades snap
```

This will create a **snapshot** of your project or file in the directory, `.decades`, to be saved and reused later.

## License 🛡️

Decades is licensed under the **MIT License** which allows you, the developer, to use the software in any way you want.

[^1]: Decades does not store any data on servers in which you already have. (For example, GitHub projects and more)
