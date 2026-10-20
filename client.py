"""Git Commit Conventional Semantic Linter.
100% Python Standard Library.
"""
import re

class GitCommitConventionalSemanticLinter:
    """Conventional Commits 1.0.0 semantic linter and changelog grouping engine."""

    VALID_TYPES = {"feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"}
    COMMIT_REGEX = re.compile(r'^([a-zA-Z]+)(?:\(([a-zA-Z0-9_\-\./]+)\))?(!)?:\s+(.+)$')

    @classmethod
    def lint_commit(cls, message: str) -> dict:
        lines = message.strip().split("\n")
        header = lines[0].strip()

        match = cls.COMMIT_REGEX.match(header)
        violations = []

        if not match:
            return {
                "is_valid": False,
                "type": None,
                "scope": None,
                "is_breaking": False,
                "description": None,
                "violations": ["Header does not match Conventional Commits format '<type>(scope): description'"]
            }

        ctype, scope, breaking_bang, desc = match.groups()
        ctype = ctype.lower()

        if ctype not in cls.VALID_TYPES:
            violations.append(f"Invalid commit type '{ctype}'. Must be one of: {sorted(list(cls.VALID_TYPES))}")

        if len(desc) < 3:
            violations.append("Description is too short (minimum 3 characters)")

        if desc[0].isupper():
            violations.append("Description should start with a lowercase letter")

        if desc.endswith("."):
            violations.append("Description should not end with a period")

        is_breaking = bool(breaking_bang)
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        if "BREAKING CHANGE:" in body or "BREAKING-CHANGE:" in body:
            is_breaking = True

        issue_refs = re.findall(r'(?:Closes|Fixes|Resolves)\s+#(\d+)', body, re.IGNORECASE)

        return {
            "is_valid": len(violations) == 0,
            "type": ctype,
            "scope": scope,
            "is_breaking": is_breaking,
            "description": desc,
            "body": body,
            "issue_references": issue_refs,
            "violations": violations
        }
