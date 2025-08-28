# Python Project Structure & Imports Guide

This guide explains the standard best practice for managing imports and file access within a structured Python project like this one, specifically addressing how to handle the "project root".

## The Challenge: Importing from a Parent Directory

In a project with a nested structure (e.g., a script at `scripts/generate_flashcards.py` needing to import a module from `common/secrets.py`), a common problem arises. By default, a Python script can only import modules from its own directory or subdirectories. It cannot "see" parent or sibling directories like `common/`.

## The Solution: Programmatically Adding the Project Root to `sys.path`

The most robust and standard solution is to programmatically add the project's root directory to Python's `sys.path`. This is a list of directories that the Python interpreter searches when you try to import a module. By adding the project root to this path, you make all top-level folders (like `common`, `Services`, etc.) importable from any script within the project.

### Step-by-Step Code Example

You can add the following code snippet to the very top of any Python script to make it aware of the project's root directory. This exact code is used in `scripts/generate_flashcards.py`.

```python
import os
import sys

# 1. Get the absolute path of the directory where the current script is located.
#    e.g., /path/to/your/project/scripts
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Navigate "up" one level to find the project's root directory.
#    e.g., /path/to/your/project/
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# 3. Add the project root to the system path if it's not already there.
#    This tells Python to look for modules in this directory.
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now, you can reliably import modules from the root of your project
# from any script, no matter where it's located.
# For example:
from common.secrets import get_secret

print("Successfully imported a module from the common directory!")
```

This technique makes your scripts portable, reliable, and independent of where you execute them from, which is essential for professional software development.
