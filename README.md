# Simple Code Reviewer

A beginner-friendly Python tool that performs automated code reviews on Python functions.

## Features

- Checks code style and formatting
- Detects common bugs and anti-patterns
- Enforces naming conventions
- Analyzes code complexity
- Provides clear feedback with suggestions for improvement

## Usage

```python
from simple_code_reviewer import SimpleCodeReviewer

reviewer = SimpleCodeReviewer()
results = reviewer.review_code(your_code_here)
print(results)
