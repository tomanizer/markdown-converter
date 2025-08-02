Installation
===========

Installation Guide
-----------------

The Markdown Converter can be installed using pip:

.. code-block:: bash

   pip install markdown-converter

Or install from source:

.. code-block:: bash

   git clone https://github.com/tomanizer/markdown-converter.git
   cd markdown-converter
   pip install -e .

Development Installation
-----------------------

For development, install with development dependencies:

.. code-block:: bash

   make install-dev

This will install all development tools including:
- Testing framework (pytest)
- Code formatting (black, isort)
- Linting (flake8, mypy)
- Pre-commit hooks

Requirements
-----------

- Python 3.8+
- Pandoc (for document conversion)
- Various document parsing libraries (see requirements/base.txt) 