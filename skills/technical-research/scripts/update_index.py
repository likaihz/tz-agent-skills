#!/usr/bin/env python3
"""Auto-generate or update SUMMARY.md index for research documents."""
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict


TOPIC_LABELS = {
    "ai-llm": "AI/LLM",
    "frontend": "Frontend",
    "backend": "Backend",
    "database": "Database",
    "devops": "DevOps",
    "tools": "Tools",
    "security": "Security",
    "architecture": "Architecture",
}


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    fm_text = parts[1].strip()
    result = {}

    for line in fm_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Parse list values
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip("'\"") for v in value[1:-1].split(",")]
            elif value in ["draft", "complete", "archived"]:
                pass  # Keep as string
            else:
                value = value.strip("'\"")

            result[key] = value

    return result


def scan_research_docs(research_dir: Path) -> dict:
    """Scan all research documents and group by topic."""
    docs_by_topic = defaultdict(list)

    for md_file in research_dir.rglob("*.md"):
        if md_file.name == "SUMMARY.md":
            continue

        content = md_file.read_text(encoding="utf-8")
        fm = extract_frontmatter(content)

        if not fm:
            continue

        topic = fm.get("topic", "other")
        title = fm.get("title", md_file.stem)
        date = fm.get("date", "")
        status = fm.get("status", "")

        # Get relative path from research dir
        rel_path = md_file.relative_to(research_dir)

        docs_by_topic[topic].append({
            "title": title,
            "path": str(rel_path),
            "date": date,
            "status": status,
        })

    # Sort each topic by date (newest first)
    for topic in docs_by_topic:
        docs_by_topic[topic].sort(key=lambda x: x["date"], reverse=True)

    return docs_by_topic


def generate_summary(docs_by_topic: dict) -> str:
    """Generate SUMMARY.md content."""
    lines = ["# 技术调研索引\n"]
    lines.append("> 自动生成，请勿手动编辑。更新文档后运行 `python scripts/update_index.py research/`\n")
    lines.append("")

    # Sort topics by label
    sorted_topics = sorted(docs_by_topic.keys(), key=lambda t: TOPIC_LABELS.get(t, t))

    for topic in sorted_topics:
        label = TOPIC_LABELS.get(topic, topic.title())
        docs = docs_by_topic[topic]

        lines.append(f"## {label}\n")

        for doc in docs:
            status_icon = "" if doc["status"] == "complete" else "📝 "
            lines.append(f"- {status_icon}[{doc['title']}]({doc['path']}) - {doc['date']}")

        lines.append("")

    # Add stats
    total_docs = sum(len(docs) for docs in docs_by_topic.values())
    lines.append("---\n")
    lines.append(f"**总计**: {total_docs} 篇调研文档\n")
    lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    return "".join(lines)


def update_index(research_dir: Path) -> bool:
    """Update SUMMARY.md in the research directory."""
    if not research_dir.exists():
        print(f"Error: Research directory not found: {research_dir}")
        return False

    docs_by_topic = scan_research_docs(research_dir)

    if not docs_by_topic:
        print("Warning: No research documents found")
        return False

    summary_content = generate_summary(docs_by_topic)
    summary_path = research_dir / "SUMMARY.md"
    summary_path.write_text(summary_content, encoding="utf-8")

    total_docs = sum(len(docs) for docs in docs_by_topic.values())
    print(f"Updated {summary_path}")
    print(f"Indexed {total_docs} documents across {len(docs_by_topic)} topics")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_index.py <research_directory>")
        print("Example: python update_index.py research/")
        sys.exit(1)

    research_dir = Path(sys.argv[1])
    success = update_index(research_dir)
    sys.exit(0 if success else 1)