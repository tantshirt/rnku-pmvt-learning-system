#!/usr/bin/env python3
"""
Clean up duplicate sections in chapter files
"""

from pathlib import Path
import re

def clean_duplicates(content: str) -> str:
    """Remove duplicate sections and clean up formatting"""

    lines = content.split('\n')
    processed_lines = []
    seen_headers = set()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Always keep chapter title
        if line.startswith('# Chapter'):
            processed_lines.append(lines[i])
            if i + 1 < len(lines) and lines[i + 1].strip() == '':
                processed_lines.append('')
                i += 1
            i += 1
            continue

        # Handle section headers - keep only the first occurrence
        if line.startswith('## Section'):
            section_key = line
            if section_key not in seen_headers:
                seen_headers.add(section_key)
                processed_lines.append(lines[i])
                # Add empty line after section header if not already there
                if i + 1 < len(lines) and lines[i + 1].strip() != '':
                    processed_lines.append('')
            i += 1
            continue

        # Skip duplicate comprehension headers
        if '**REQUIRED LEVEL OF COMPREHENSION FOR DEVELOPMENT AND PROMOTION**' in line:
            # Only keep if we haven't seen a comprehension header for this section recently
            if not processed_lines or not any('REQUIRED LEVEL' in prev_line for prev_line in processed_lines[-5:]):
                processed_lines.append(lines[i])
            i += 1
            continue

        # Skip duplicate rank headers
        if line.startswith('Chapter ') and 'SSgt' in line:
            if not processed_lines or not any('SSgt' in prev_line for prev_line in processed_lines[-3:]):
                processed_lines.append(lines[i])
            i += 1
            continue

        # Skip duplicate section rank lines - be more aggressive
        if line.startswith('Section ') and any(rank in line for rank in ['A', 'B', 'C']):
            # Check if we already have a rank line for this section
            section_name = line.split('—')[0].strip()
            has_rank_already = any(section_name in prev_line and any(r in prev_line for r in ['A', 'B', 'C'])
                                  for prev_line in processed_lines[-5:])

            if not has_rank_already:
                processed_lines.append(lines[i])
                # Add empty line after rank line
                if i + 1 < len(lines) and not lines[i + 1].strip():
                    processed_lines.append('')
                    i += 1
            i += 1
            continue

        # Skip lines that are just "## Section X — Title" if we already have one
        if line.startswith('## Section') and any('## Section' in prev_line for prev_line in processed_lines[-3:]):
            i += 1
            continue

        # Keep all other lines
        processed_lines.append(lines[i])
        i += 1

    # Clean up excessive empty lines
    final_lines = []
    prev_empty = False

    for line in processed_lines:
        is_empty = not line.strip()

        if is_empty and prev_empty:
            continue

        final_lines.append(line)
        prev_empty = is_empty

    return '\n'.join(final_lines).strip()

def clean_chapter_file(filepath: Path) -> None:
    """Clean duplicates in a chapter file"""

    chapter_num = int(filepath.stem.replace('chapter', ''))

    print(f"Cleaning Chapter {chapter_num}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean duplicates
    cleaned_content = clean_duplicates(content)

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
            clean_chapter_file(filepath)
        else:
            print(f"Warning: {filename} not found")

    print("\nAll chapters cleaned!")

if __name__ == '__main__':
    main()
