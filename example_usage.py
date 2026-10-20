"""Example usage for Git Commit Conventional Semantic Linter."""
from client import GitCommitConventionalSemanticLinter
import json

commit = """feat(search)!: add vector embedding search with cosine index

BREAKING CHANGE: changes the query parameter format from q to query_vector.
Closes #108
"""

res = GitCommitConventionalSemanticLinter.lint_commit(commit)
print(json.dumps(res, indent=2))
