#!/usr/bin/env python3
"""Validate technical research skill or document."""
import sys
import re
from pathlib import Path


def validate_skill(skill_path: Path):
    errors = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        return False, ["Missing SKILL.md"]
    
    content = skill_md.read_text(encoding='utf-8')
    
    # Check frontmatter
    if not content.startswith('---'):
        errors.append("Missing YAML frontmatter")
    else:
        parts = content.split('---', 2)
        if len(parts) >= 2:
            fm_text = parts[1]
            if 'name:' not in fm_text:
                errors.append("Missing field: name")
            if 'description:' not in fm_text:
                errors.append("Missing field: description")
    
    return len(errors) == 0, errors


def validate_doc(doc_path: Path):
    errors = []
    content = doc_path.read_text(encoding='utf-8')
    
    if not content.startswith('---'):
        errors.append("Missing YAML frontmatter")
    else:
        parts = content.split('---', 2)
        if len(parts) >= 2:
            fm_text = parts[1]
            for field in ['title:', 'date:', 'topic:', 'tags:', 'status:']:
                if field not in fm_text:
                    errors.append(f"Missing field: {field.rstrip(':')}")
    
    return len(errors) == 0, errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py <path>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    if path.is_dir() or path.name == "SKILL.md":
        valid, issues = validate_skill(path if path.is_dir() else path.parent)
        title = "Skill"
    else:
        valid, issues = validate_doc(path)
        title = "Document"
    
    print(f"{'✅ PASS' if valid else '❌ FAIL'} - {title}")
    for issue in issues:
        print(f"  - {issue}")
    sys.exit(0 if valid else 1)s