import re
import ast
from typing import Dict, List, Tuple

class SimpleCodeReviewer:
    """A beginner-friendly code review assistant that checks Python functions."""
    
    def __init__(self):
        # Define some basic coding standards
        self.max_line_length = 80
        self.max_function_length = 30  # lines
        self.naming_patterns = {
            'function': r'^[a-z][a-z0-9_]*$',  # snake_case
            'variable': r'^[a-z][a-z0-9_]*$',  # snake_case
            'constant': r'^[A-Z][A-Z0-9_]*$',  # UPPER_CASE
        }
    
    def review_code(self, code: str) -> Dict:
        """
        Review a piece of Python code and provide feedback.
        
        Args:
            code: String containing Python code to review
            
        Returns:
            Dictionary with review results
        """
        results = {
            'issues': [],
            'suggestions': [],
            'verdict': 'approve',
            'explanation': ''
        }
        
        # Check if code is valid Python
        try:
            ast.parse(code)
        except SyntaxError as e:
            results['issues'].append(f"Syntax error: {str(e)}")
            results['verdict'] = 'request changes'
            results['explanation'] = 'Code contains syntax errors that must be fixed'
            return results
            
        # Perform various checks
        self._check_line_length(code, results)
        self._check_function_length(code, results)
        self._check_naming_conventions(code, results)
        self._check_complexity(code, results)
        self._check_common_bugs(code, results)
        
        # Determine final verdict
        if results['issues']:
            results['verdict'] = 'request changes'
            results['explanation'] = 'Code has issues that should be addressed'
        else:
            results['explanation'] = 'Code looks good and follows best practices'
            
        return results
    
    def _check_line_length(self, code: str, results: Dict) -> None:
        """Check if any lines exceed the maximum length."""
        lines = code.split('\n')
        long_lines = []
        
        for i, line in enumerate(lines, 1):
            if len(line) > self.max_line_length:
                long_lines.append(i)
                
        if long_lines:
            results['issues'].append(
                f"Lines {', '.join(map(str, long_lines))} exceed {self.max_line_length} characters"
            )
            results['suggestions'].append(
                "Break long lines using line continuation or refactor into smaller chunks"
            )
    
    def _check_function_length(self, code: str, results: Dict) -> None:
        """Check if any function is too long."""
        lines = code.split('\n')
        if len(lines) > self.max_function_length:
            results['issues'].append(
                f"Function is {len(lines)} lines long (exceeds recommended {self.max_function_length})"
            )
            results['suggestions'].append(
                "Break this function into smaller, more focused functions"
            )
    
    def _check_naming_conventions(self, code: str, results: Dict) -> None:
        """Check if names follow standard conventions."""
        # Simple regex-based check for variable names
        try:
            tree = ast.parse(code)
            
            # Check function names
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not re.match(self.naming_patterns['function'], node.name):
                        results['issues'].append(
                            f"Function name '{node.name}' doesn't follow snake_case convention"
                        )
                        results['suggestions'].append(
                            f"Rename '{node.name}' to follow snake_case (lowercase with underscores)"
                        )
                
                # Check variable names in assignments
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            name = target.id
                            if name.isupper() and not re.match(self.naming_patterns['constant'], name):
                                results['issues'].append(
                                    f"Constant '{name}' doesn't follow UPPER_CASE convention"
                                )
                            elif not name.isupper() and not re.match(self.naming_patterns['variable'], name):
                                results['issues'].append(
                                    f"Variable '{name}' doesn't follow snake_case convention"
                                )
        except:
            # If parsing fails, we'll skip this check
            pass
    
    def _check_complexity(self, code: str, results: Dict) -> None:
        """Check for overly complex code patterns."""
        # Simple check for nested loops and conditions
        try:
            tree = ast.parse(code)
            self._find_deep_nesting(tree, results)
        except:
            # If parsing fails, we'll skip this check
            pass
    
    def _find_deep_nesting(self, node, results: Dict, depth: int = 0) -> None:
        """Recursively check for deeply nested structures."""
        # Check nesting level for loops and conditionals
        if isinstance(node, (ast.For, ast.While, ast.If)):
            depth += 1
            if depth > 3:  # More than 3 levels of nesting is complex
                results['issues'].append("Code contains deeply nested loops or conditionals")
                results['suggestions'].append(
                    "Consider refactoring to reduce nesting by extracting functions or simplifying logic"
                )
                return
        
        # Recursively check all child nodes
        for child in ast.iter_child_nodes(node):
            self._find_deep_nesting(child, results, depth)
    
    def _check_common_bugs(self, code: str, results: Dict) -> None:
        """Check for common programming bugs and anti-patterns."""
        # Simple checks for a few common issues
        
        # Check for empty except blocks
        if re.search(r'except\s*:', code):
            results['issues'].append("Code contains bare 'except:' statement")
            results['suggestions'].append(
                "Specify the exceptions you want to catch instead of using bare 'except:'"
            )
        
        # Check for mutable default arguments
        if re.search(r'def\s+\w+\([^)]*=\s*\[\s*\]', code) or re.search(r'def\s+\w+\([^)]*=\s*\{\s*\}', code):
            results['issues'].append("Function uses mutable default argument (list or dict)")
            results['suggestions'].append(
                "Use 'None' as default and initialize the mutable object inside the function"
            )

def main():
    """Demo function to show how to use the SimpleCodeReviewer."""
    reviewer = SimpleCodeReviewer()
    
    # Example code to review (with some issues)
    code_to_review = """def calculateSum(a, b=[]):
    # This function calculates the sum of a number and a list
    result = a
    for item in b:
        result = result + item
    return result
"""
    
    # Perform the review
    review_results = reviewer.review_code(code_to_review)
    
    # Display results in a user-friendly way
    print("===== CODE REVIEW RESULTS =====")
    print(f"Verdict: {review_results['verdict'].upper()}")
    print(f"Explanation: {review_results['explanation']}")
    
    if review_results['issues']:
        print("\nIssues Found:")
        for i, issue in enumerate(review_results['issues'], 1):
            print(f"{i}. {issue}")
    
    if review_results['suggestions']:
        print("\nSuggestions:")
        for i, suggestion in enumerate(review_results['suggestions'], 1):
            print(f"{i}. {suggestion}")

if __name__ == "__main__":
    main()
