"""Script to generate markdown API documentation from docstrings."""
from lazydocs import generate_docs

# The parameters of this function correspond to the CLI options
IGNORED_MODULES = []

generate_docs(["pyduino_sensor"],
              overview_file="readme.md",
              watermark=False,
              remove_package_prefix=False,
              ignored_modules=IGNORED_MODULES,
              include_toc=True)
