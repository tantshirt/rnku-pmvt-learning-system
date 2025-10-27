#!/usr/bin/env python3
"""
Reformat all chapter markdown files with clean markdown styling
"""

import re
import os
from pathlib import Path

def get_chapter_title(chapter_num: int) -> str:
    """Get the proper chapter title from TOC"""
    titles = {
        1: "Professionalism",
        2: "Aviation History",
        3: "USAF Heritage",
        4: "Air and Cyberpower",
        5: "Military Organization and Command",
        6: "Doctrine and Joint Force",
        7: "Enlisted Force Development",
        8: "Assessments and Recognition",
        9: "Enlisted Promotions",
        10: "Assignments and Occupational Codes",
        11: "Personnel Programs and Benefits",
        12: "Finance, Manpower and Resources",
        13: "Developing Organizations",
        14: "Developing Others",
        15: "Developing Self",
        16: "Developing Ideas",
        17: "Emergency Management",
        18: "Security",
        19: "Standards of Conduct",
        20: "Enforcing Military Standards",
        21: "Military Justice",
        22: "Fitness and Readiness",
        23: "Dress and Appearance",
        24: "Military Customs and Courtesies"
    }
    return titles.get(chapter_num, f"Chapter {chapter_num}")

def clean_chapter_content(content: str, chapter_num: int) -> str:
    """Apply the same cleaning logic used for chapter01.md"""

    lines = content.split('\n')
    processed_lines = []
    skip_next_duplicate = False

    chapter_title = get_chapter_title(chapter_num)

    for i, line in enumerate(lines):
        original_line = line.strip()

        # Skip empty lines at the start
        if not processed_lines and not original_line:
            continue

        # Handle chapter title - use proper title
        if original_line.startswith('# Chapter'):
            processed_lines.append(f'# Chapter {chapter_num} — {chapter_title}')
            continue

        # Skip duplicate section headers that appear right after the main header
        if skip_next_duplicate and original_line.startswith('Chapter ') and 'SECTION' in original_line.upper():
            skip_next_duplicate = False
            continue

        if original_line.startswith('## Section'):
            processed_lines.append(line)
            skip_next_duplicate = True  # Next line might be duplicate
            continue

        # Skip lines that are just "Section X" after we've already processed "## Section X"
        if original_line.startswith('Section ') and processed_lines and processed_lines[-1].startswith('## Section'):
            continue

        # Skip duplicate chapter titles and standalone titles
        if original_line.startswith('Chapter ') and processed_lines and processed_lines[0].startswith('# Chapter'):
            continue

        # Skip standalone chapter titles that appear after the main header
        if (original_line and not original_line.startswith('#') and not original_line.startswith('##') and
            not original_line.startswith('Section') and processed_lines and processed_lines[0].startswith('# Chapter') and
            len(processed_lines) < 4 and not original_line.startswith('**') and not original_line.startswith('<!--')):
            continue

        # Skip duplicate section titles that appear after comprehension headers
        if (original_line.startswith('Section ') and processed_lines and
            processed_lines[-1].startswith('## Required Level')):
            continue

        # Handle comprehension level headers
        if 'REQUIRED LEVEL OF COMPREHENSION' in original_line:
            processed_lines.append('')
            processed_lines.append('**REQUIRED LEVEL OF COMPREHENSION FOR DEVELOPMENT AND PROMOTION**')
            continue

        # Handle the main rank header line
        if ('SSgt' in original_line and 'TSgt' in original_line and
            any(rank in original_line for rank in ['MSgt', 'SMSgt', 'CMSgt'])):
            # This is the main rank header line - clean it
            cleaned = re.sub(r'Chapter \d+—', '', original_line)
            processed_lines.append(f'Chapter {chapter_num}—{cleaned.strip()}')
            continue

        # Handle individual rank levels (single letters)
        if original_line.strip() in ['A', 'B', 'C'] and processed_lines and 'Chapter ' in processed_lines[-1]:
            processed_lines.append(original_line.strip())
            continue

        # Convert numbered subsections to markdown headers
        section_match = re.match(r'^(\d+(?:\.\d+)*\.?)\s+(.+)$', original_line)
        if section_match:
            section_num = section_match.group(1).rstrip('.')
            title = section_match.group(2)

            # Determine header level based on dots
            dot_count = section_num.count('.')
            if dot_count == 1:  # X.Y format -> ###
                processed_lines.append(f'### {section_num}. {title}')
            elif dot_count == 2:  # X.Y.Z format -> ####
                processed_lines.append(f'#### {section_num}. {title}')
            else:  # Other formats
                processed_lines.append(f'### {section_num}. {title}')
            continue

        # Handle bullet points and lists - preserve existing markdown
        if original_line.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
            processed_lines.append(line)
            continue

        # Convert certain standalone titles to bold
        if (len(original_line.split()) <= 10 and
            original_line.endswith('.') and
            not original_line.startswith(('•', '-', '*')) and
            not original_line[0].isdigit() and
            original_line[0].isupper()):
            # Likely a subsection title
            processed_lines.append(f'**{original_line}**')
            processed_lines.append('')
            continue

        # Handle page markers and other special content
        if original_line.startswith('<!--') or original_line.startswith('**CMSAF'):
            processed_lines.append(line)
            continue

        # Regular content - clean up spacing
        if original_line:
            # Normalize multiple spaces
            cleaned = re.sub(r'\s+', ' ', original_line)
            processed_lines.append(cleaned)
        else:
            # Preserve single empty lines for paragraph breaks
            if processed_lines and processed_lines[-1] != '':
                processed_lines.append('')

    # Clean up excessive empty lines
    final_lines = []
    prev_empty = False

    for line in processed_lines:
        is_empty = line == ''

        if is_empty and prev_empty:
            continue

        final_lines.append(line)
        prev_empty = is_empty

    return '\n'.join(final_lines).strip()

def reformat_chapter_file(filepath: Path) -> None:
    """Reformat a single chapter file"""
    chapter_num = int(filepath.stem.replace('chapter', ''))

    print(f"Reformatting Chapter {chapter_num}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply cleaning
    cleaned_content = clean_chapter_content(content, chapter_num)

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
            reformat_chapter_file(filepath)
        else:
            print(f"Warning: {filename} not found")

    print("\nAll chapters reformatted!")

    # Clean up any remaining old files
    old_files = list(Path('.').glob('Chapter_*.md'))
    if old_files:
        print(f"\nRemoving {len(old_files)} old chapter files...")
        for old_file in old_files:
            old_file.unlink()
        print("Old files removed!")

if __name__ == '__main__':
    main()
