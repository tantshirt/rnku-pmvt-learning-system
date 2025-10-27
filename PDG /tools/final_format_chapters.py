#!/usr/bin/env python3
"""
Apply the exact formatting from chapter01.md to all chapters 02-24
"""

import re
from pathlib import Path

def get_chapter_title(chapter_num: int) -> str:
    """Get the proper chapter title"""
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

def apply_chapter01_formatting(content: str, chapter_num: int) -> str:
    """Apply the exact formatting pattern from chapter01.md"""

    lines = content.split('\n')
    processed_lines = []
    chapter_title = get_chapter_title(chapter_num)

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Chapter title
        if line.startswith('# Chapter'):
            processed_lines.append(f'# Chapter {chapter_num} — {chapter_title}')
            processed_lines.append('')  # Empty line after title
            i += 1
            continue

        # Section headers - convert to proper format
        if line.startswith('Section ') and '—' in line:
            section_match = re.match(r'Section (\w+)—(.+)', line)
            if section_match:
                section_code = section_match.group(1)
                section_title = section_match.group(2).strip()

                # Skip if this section header is immediately followed by the comprehension header
                # (meaning it's already properly formatted)
                if (i + 1 < len(lines) and 'Required Level' in lines[i + 1] and
                    i + 2 < len(lines) and lines[i + 2].strip().startswith('**REQUIRED')):
                    # This section is already formatted, skip it
                    i += 1
                    continue

                processed_lines.append(f'## Section {section_code} — {section_title}')
                processed_lines.append('')  # Empty line after section header

                # Add the bold header and rank table after section header
                processed_lines.append('**REQUIRED LEVEL OF COMPREHENSION FOR DEVELOPMENT AND PROMOTION**')
                processed_lines.append(f'Chapter {chapter_num}—{chapter_title.upper()} SSgt TSgt MSgt SMSgt CMSgt')

                # Look for rank levels in the next few lines
                rank_levels = []
                temp_i = i + 1
                while temp_i < len(lines) and lines[temp_i].strip() in ['A', 'B', 'C']:
                    rank_levels.append(lines[temp_i].strip())
                    temp_i += 1

                if rank_levels:
                    rank_line = ' '.join(rank_levels)
                    processed_lines.append(f'Section {section_code}—{section_title} {rank_line}')
                    i = temp_i  # Skip the processed rank lines
                else:
                    processed_lines.append(f'Section {section_code}—{section_title} B B C C C')
                    i += 1  # Skip the original line

                continue

        # Skip existing comprehension headers (already formatted)
        if line.startswith('**REQUIRED LEVEL OF COMPREHENSION'):
            i += 1
            continue

        # Skip existing rank headers (already formatted)
        if line.startswith('Chapter ') and 'SSgt' in line:
            i += 1
            continue

        # Subsection headers
        if re.match(r'^\d+\.\d+\.\s+', line):
            # Convert to ### format
            parts = line.split('.', 2)
            if len(parts) >= 3:
                section_num = f"{parts[0]}.{parts[1]}"
                title = parts[2].strip()
                processed_lines.append(f'### {section_num}. {title}')
                processed_lines.append('')  # Empty line after subsection header
                i += 1
                continue

        # Sub-subsection headers
        if re.match(r'^\d+\.\d+\.\d+\.\s+', line):
            # Convert to #### format
            parts = line.split('.', 3)
            if len(parts) >= 4:
                section_num = f"{parts[0]}.{parts[1]}.{parts[2]}"
                title = parts[3].strip()
                processed_lines.append(f'#### {section_num}. {title}')
                processed_lines.append('')  # Empty line after sub-subsection header
                i += 1
                continue

        # Bold subheadings (lines that end with .** or are short titles)
        if (line.endswith('**') or
            (len(line.split()) <= 8 and line.endswith('.') and not line.startswith(('•', '-', '*', '1.', '2.', '3.')) and
             not line[0].isdigit() and line[0].isupper() and not line.startswith('#'))):
            if not line.startswith('**'):
                line = f'**{line}**'
            processed_lines.append(line)
            processed_lines.append('')  # Empty line after bold subheading
            i += 1
            continue

        # Handle list items
        if line.startswith(('- ', '* ', '1. ', '2. ', '3. ')):
            processed_lines.append(line)
            i += 1
            continue

        # Handle page markers
        if line.startswith('<!-- Page'):
            processed_lines.append(line)
            i += 1
            continue

        # Regular content
        if line:
            processed_lines.append(line)
        elif processed_lines and processed_lines[-1] != '':  # Only add empty line if previous line wasn't empty
            processed_lines.append('')

        i += 1

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
    """Reformat a single chapter file with chapter01.md formatting"""

    chapter_num = int(filepath.stem.replace('chapter', ''))

    print(f"Applying chapter01.md formatting to Chapter {chapter_num}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply the exact formatting from chapter01.md
    formatted_content = apply_chapter01_formatting(content, chapter_num)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(formatted_content)

    print(f"Chapter {chapter_num}: {len(formatted_content.split())} words")

def main():
    chapters_dir = Path('./chapters')

    # Process chapters 02-24 (skip chapter 01 as it's already formatted)
    for chapter_num in range(2, 25):
        filename = f"chapter{chapter_num:02d}.md"
        filepath = chapters_dir / filename

        if filepath.exists():
            reformat_chapter_file(filepath)
        else:
            print(f"Warning: {filename} not found")

    print("\nAll chapters reformatted to match chapter01.md formatting!")

if __name__ == '__main__':
    main()
