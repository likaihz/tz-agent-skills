#!/usr/bin/env python3
"""
Skill Validator - Validates a skill folder structure and content

Usage:
    python validate_skill.py <path/to/skill-folder>

Example:
    python validate_skill.py skills/public/my-skill
    python validate_skill.py .
"""

import sys
from pathlib import Path

# Add script directory to path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))
from quick_validate import validate_skill as quick_validate


def validate_skill_verbose(skill_path):
    """
    Validate a skill folder with detailed output.

    Args:
        skill_path: Path to the skill folder

    Returns:
        True if valid, False otherwise
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"[x] Error: Skill folder not found: {skill_path}")
        return False

    if not skill_path.is_dir():
        print(f"[x] Error: Path is not a directory: {skill_path}")
        return False

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[x] Error: SKILL.md not found in {skill_path}")
        return False

    # Run validation
    print(f"Validating skill: {skill_path.name}")
    print(f"  Location: {skill_path}")
    print()

    valid, message = quick_validate(skill_path)

    if not valid:
        print(f"[x] Validation failed: {message}")
        return False

    print(f"[OK] {message}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py <path/to/skill-folder>")
        print("\nExample:")
        print("  python validate_skill.py skills/public/my-skill")
        print("  python validate_skill.py .")
        sys.exit(1)

    skill_path = sys.argv[1]

    result = validate_skill_verbose(skill_path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
