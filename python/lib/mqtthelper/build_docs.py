"""Script to generate markdown API documentation from docstrings."""
from lazydocs import generate_docs

# The parameters of this function correspond to the CLI options
generate_docs(["./src"],
              overview_file="readme.md",
              watermark=False,
              remove_package_prefix=False,
              ignored_modules=None,
              include_toc=True)
