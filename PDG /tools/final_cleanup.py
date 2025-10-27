#!/usr/bin/env python3
"""
Final cleanup of duplicate sections
"""

from pathlib import Path

def final_cleanup(content: str) -> str:
    """Remove all known duplicate patterns"""

    lines = content.split('\n')
    processed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Always keep chapter title
        if line.startswith('# Chapter'):
            processed_lines.append(lines[i])
            if i + 1 < len(lines) and lines[i + 1].strip() == '':
                processed_lines.append(lines[i + 1])
                i += 1
            i += 1
            continue

        # Keep first section header
        if line.startswith('## Section') and not any('## Section' in prev for prev in processed_lines[-2:]):
            processed_lines.append(lines[i])
            if i + 1 < len(lines) and lines[i + 1].strip() == '':
                processed_lines.append(lines[i + 1])
                i += 1
            i += 1
            continue

        # Keep first comprehension header after a section
        if '**REQUIRED LEVEL OF COMPREHENSION FOR DEVELOPMENT AND PROMOTION**' in line:
            if not any('REQUIRED LEVEL' in prev for prev in processed_lines[-3:]):
                processed_lines.append(lines[i])
                if i + 1 < len(lines) and lines[i + 1].strip() == '':
                    processed_lines.append(lines[i + 1])
                    i += 1
            i += 1
            continue

        # Keep first rank header
        if line.startswith('Chapter ') and 'SSgt' in line:
            if not any('SSgt' in prev for prev in processed_lines[-3:]):
                processed_lines.append(lines[i])
            i += 1
            continue

        # Keep first section rank line
        if line.startswith('## Section') and any(rank in line for rank in ['A', 'B', 'C']):
            if not any('## Section' in prev and any(r in prev for r in ['A', 'B', 'C']) for prev in processed_lines[-3:]):
                processed_lines.append(lines[i])
                if i + 1 < len(lines) and lines[i + 1].strip() == '':
                    processed_lines.append(lines[i + 1])
                    i += 1
            i += 1
            continue

        # Keep subsection headers
        if line.startswith('### ') or line.startswith('#### '):
            processed_lines.append(lines[i])
            if i + 1 < len(lines) and lines[i + 1].strip() == '':
                processed_lines.append(lines[i + 1])
                i += 1
            i += 1
            continue

        # Keep bold subheadings
        if line.startswith('**') and line.endswith('**'):
            processed_lines.append(lines[i])
            if i + 1 < len(lines) and lines[i + 1].strip() == '':
                processed_lines.append(lines[i + 1])
                i += 1
            i += 1
            continue

        # Keep page markers
        if line.startswith('<!-- Page'):
            processed_lines.append(lines[i])
            i += 1
            continue

        # Keep list items
        if line.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
            processed_lines.append(lines[i])
            i += 1
            continue

        # Keep regular content
        if line:
            processed_lines.append(lines[i])
        elif processed_lines and processed_lines[-1] != '':
            processed_lines.append(lines[i])

        i += 1

    # Final cleanup of excessive empty lines
    final_lines = []
    prev_empty = False

    for line in processed_lines:
        is_empty = not line.strip()

        if is_empty and prev_empty:
            continue

        final_lines.append(line)
        prev_empty = is_empty

    return '\n'.join(final_lines).strip()

def cleanup_chapter_file(filepath: Path) -> None:
    """Clean up a chapter file"""

    chapter_num = int(filepath.stem.replace('chapter', ''))

    print(f"Final cleanup Chapter {chapter_num}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Final cleanup
    cleaned_content = final_cleanup(content)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Chapter {chapter_num}: {len(cleaned_content.split())} words")

def main():
    chapters_dir = Path('./chapters')

    # Process chapters 02-24
    for chapter_num in range(2, 25):
        filename = f"chapter{chapter_num:02d}.md"
        filepath = chapters_dir / filename

        if filepath.exists():
            cleanup_chapter_file(filepath)
        else:
            print(f"Warning: {filename} not found")

    print("\nAll chapters cleaned up!")

if __name__ == '__main__':
    main()
