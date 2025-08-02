Usage
=====

Basic Usage
----------

Convert a single file:

.. code-block:: bash

   markdown-converter convert input.docx output.md

Convert a directory of files:

.. code-block:: bash

   markdown-converter batch input_directory output_directory

Command Line Interface
---------------------

The tool provides a comprehensive CLI with various options:

.. code-block:: bash

   markdown-converter --help

Available commands:
- convert: Convert a single file
- batch: Convert multiple files in a directory
- info: Show system information
- formats: List supported formats

Python API
----------

You can also use the converter programmatically:

.. code-block:: python

   from markdown_converter import MainConverter
   
   converter = MainConverter()
   result = converter.convert_file("input.docx", "output.md")
   
   if result.success:
       print(f"Conversion successful: {result.output_file}")
   else:
       print(f"Conversion failed: {result.error_message}") 