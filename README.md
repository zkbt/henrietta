# henrietta
Tools for the Fall 2018 semester of ASTR3400: Research Methods (The Henrietta Project). The documentation for using these tools, along with some examples and exercises, are located over at [zkbt.github.io/henrietta/docs](http://zkbt.github.io/henrietta/docs).

## Installation
If you're working on the `scorpius` computers at SBO, you should be able to access these tools simply by running `source henrietta` from a UNIX prompt.

If you're working on your own computer, you should be able to install this by running
```
pip install henrietta
```
from a UNIX prompt. As we add more code to this package, you may need to upgrade the version that is installed on your computer. To upgrade, run
```
pip install henrietta --upgrade
```
instead. That will make sure it always grabs the latest version of the code.

If you want to be able to modify the code yourself, please also feel free to fork/clone this repository onto your own computer and install directly from that editable package. For example, this might look like:
```
git clone https://github.com/zkbt/henrietta.git
cd henrietta/
pip install -e .
```
This will link the installed version of the `henrietta` package to your local repository. Changes you make to the code in the repository should be reflected in the version Python sees when it tries to `import henrietta`.

## Contributors

This package was written by [Zach Berta-Thompson](https://github.com/zkbt), [Will Waalkes](https://github.com/waalkesw), and [Jessica Roberts](https://github.com/jessicaeroberts).
