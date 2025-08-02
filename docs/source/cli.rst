Command Line Interface
=====================

The Markdown Converter provides a comprehensive command-line interface for converting documents to markdown.

Basic Commands
-------------

Convert a single file:

.. code-block:: bash

   markdown-converter convert input.docx output.md

Convert a directory of files:

.. code-block:: bash

   markdown-converter batch input_directory output_directory

Show supported formats:

.. code-block:: bash

   markdown-converter formats

Show system information:

.. code-block:: bash

   markdown-converter info

Command Options
--------------

Convert Command
~~~~~~~~~~~~~~

.. code-block:: bash

   markdown-converter convert [OPTIONS] INPUT_FILE [OUTPUT_FILE]

Options:
- --verbose, -v: Enable verbose output
- --quiet, -q: Suppress output
- --config: Path to configuration file
- --help: Show help message

Batch Command
~~~~~~~~~~~~

.. code-block:: bash

   markdown-converter batch [OPTIONS] INPUT_DIR [OUTPUT_DIR]

Options:
- --recursive, -r: Process subdirectories recursively
- --parallel, -p: Number of parallel processes
- --verbose, -v: Enable verbose output
- --quiet, -q: Suppress output
- --config: Path to configuration file
- --help: Show help message

Environment Variables
-------------------

The following environment variables can be used to configure the tool:

- MDC_LOG_LEVEL: Set logging level (DEBUG, INFO, WARNING, ERROR)
- MDC_CONFIG_FILE: Path to configuration file
- MDC_TEMP_DIR: Directory for temporary files
- MDC_CACHE_DIR: Directory for caching
- MDC_MAX_WORKERS: Maximum number of parallel workers 