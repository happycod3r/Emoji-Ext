## Documentation

Building the documentation with [Sphinx](https://www.sphinx-doc.org/):

```bash
git clone https://github.com/carpedm20/emoji.git
cd emoji/docs
python -m pip install -r requirements.txt
make html
```

Check for warnings:

```bash
make clean
sphinx-build -n -T -b html . _build
```

Test code in code blocks:

```bash
make doctest
```

Test coverage of documentation:

```bash
make coverage
```
