#!/usr/bin/env python3
"""
AFH1 PDF Chapter Extractor

Extracts chapters from AFH1.pdf and writes them as separate Markdown files.
Handles TOC parsing, text cleaning, and Markdown formatting.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import time

try:
    from pdfminer.high_level import extract_pages, extract_text
    from pdfminer.layout import LTTextContainer, LTChar, LAParams
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
    PDFMINER_AVAILABLE = True
except ImportError:
    PDFMINER_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PyPDF2 = None
    PYPDF2_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


class PDFChapterExtractor:
    """Extract chapters from PDF and convert to Markdown"""

    def __init__(self, pdf_path: str, output_dir: str, num_chapters: int = 24):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.num_chapters = num_chapters
        self.split_index = {}

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Chapter detection patterns
        self.chapter_patterns = [
            re.compile(r'^\s*CHAPTER\s+(\d{1,2})\b', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^\s*Chapter\s+(\d{1,2})\b', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^\s*CHAPTER\s+(\d{1,2})\s*[—:-]', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^\s*Chapter\s+(\d{1,2})\s*[—:-]', re.IGNORECASE | re.MULTILINE),
        ]

        # Heading patterns for Markdown conversion
        self.heading_patterns = [
            # Chapter titles (already handled separately)
            # Section headings (1.1, 1.1.1, etc.)
            re.compile(r'^\s*(\d+(?:\.\d+)+)\s+(.+)$', re.MULTILINE),
            # Subsection headings
            re.compile(r'^\s*([A-Z][^.!?]*)$', re.MULTILINE),  # All caps lines
        ]

        # List patterns
        self.list_patterns = [
            re.compile(r'^\s*(\d+)\.\s+(.+)$', re.MULTILINE),  # Numbered lists
            re.compile(r'^\s*([a-zA-Z])\.\s+(.+)$', re.MULTILINE),  # Lettered lists
            re.compile(r'^\s*(•|\*|-)\s+(.+)$', re.MULTILINE),  # Bullet points
        ]

    def check_dependencies(self):
        """Check and install required dependencies"""
        missing_deps = []

        if not PDFMINER_AVAILABLE:
            missing_deps.append('pdfminer.six')
        if not PYPDF2_AVAILABLE:
            missing_deps.append('PyPDF2')
        if not PDFPLUMBER_AVAILABLE:
            missing_deps.append('pdfplumber')

        if missing_deps:
            print(f"Installing missing dependencies: {', '.join(missing_deps)}")
            import subprocess
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--user'
                ] + missing_deps)
                print("Dependencies installed successfully. Please restart the script.")
                sys.exit(0)
            except subprocess.CalledProcessError as e:
                print(f"Failed to install dependencies: {e}")
                print("Please install manually: pip install pdfminer.six PyPDF2 pdfplumber")
                sys.exit(1)

    def get_page_count(self) -> int:
        """Get total number of pages in PDF"""
        global PYPDF2_AVAILABLE

        if PYPDF2_AVAILABLE:
            try:
                reader = PyPDF2.PdfReader(self.pdf_path)
                return len(reader.pages)
            except Exception as e:
                print(f"PyPDF2 failed: {e}, trying manual count")
                PYPDF2_AVAILABLE = False

        # Fallback: count pages manually
        try:
            with open(self.pdf_path, 'rb') as f:
                count = 0
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if b'/Type /Page' in line:
                        count += 1
                return count
        except Exception as e:
            print(f"Manual page count failed: {e}")
            return 0

    def extract_text_from_page(self, page_num: int, use_plumber: bool = False) -> str:
        """Extract text from a single page"""
        try:
            if use_plumber and PDFPLUMBER_AVAILABLE:
                with pdfplumber.open(self.pdf_path) as pdf:
                    page = pdf.pages[page_num - 1]  # 0-indexed
                    return page.extract_text() or ""
            else:
                # Use pdfminer.six
                laparams = LAParams()
                with open(self.pdf_path, 'rb') as f:
                    for page in PDFPage.get_pages(f, [page_num - 1], caching=True, check_extractable=True):
                        resource_manager = PDFResourceManager()
                        device = PDFPageAggregator(resource_manager, laparams=laparams)
                        interpreter = PDFPageInterpreter(resource_manager, device)
                        interpreter.process_page(page)

                        layout = device.get_result()
                        text_parts = []

                        def extract_text_from_layout(layout_obj):
                            if isinstance(layout_obj, LTTextContainer):
                                for text_line in layout_obj:
                                    if isinstance(text_line, LTTextContainer):
                                        text_parts.append(text_line.get_text())
                            elif hasattr(layout_obj, '_objs'):
                                for child in layout_obj._objs:
                                    extract_text_from_layout(child)

                        extract_text_from_layout(layout)
                        return '\n'.join(text_parts)
        except Exception as e:
            print(f"Warning: Failed to extract text from page {page_num}: {e}")
            # Try with pdfplumber as fallback
            if not use_plumber and PDFPLUMBER_AVAILABLE:
                return self.extract_text_from_page(page_num, use_plumber=True)
            return ""

    def find_chapter_boundaries(self) -> Dict[int, Tuple[int, int]]:
        """Find chapter start and end page boundaries"""
        print("Analyzing PDF structure to find chapter boundaries...")

        total_pages = self.get_page_count()
        print(f"PDF has {total_pages} pages")

        # Try TOC first if available
        toc_boundaries = self._find_chapters_from_toc()
        if toc_boundaries:
            print(f"Found {len(toc_boundaries)} chapters from TOC")
            return toc_boundaries

        # Fallback: scan for chapter headers
        print("TOC not available, scanning for chapter headers...")
        return self._find_chapters_from_headers(total_pages)

    def _find_chapters_from_toc(self) -> Dict[int, Tuple[int, int]]:
        """Try to extract chapter boundaries from PDF TOC"""
        global PYPDF2_AVAILABLE

        if not PYPDF2_AVAILABLE:
            return {}

        try:
            reader = PyPDF2.PdfReader(self.pdf_path)

            # Try to get outline - API might be different in v3.x
            outline = None
            if hasattr(reader, 'outline'):
                outline = reader.outline
            elif hasattr(reader, 'getOutlines'):
                outline = reader.getOutlines()

            if not outline:
                return {}

            boundaries = {}
            def process_outline_item(item):
                if isinstance(item, list):
                    for subitem in item:
                        process_outline_item(subitem)
                else:
                    # Handle different outline item formats
                    if hasattr(item, 'title'):
                        title = item.title
                    else:
                        title = str(item)

                    # Get page number - this might be tricky in v3.x
                    page_num = None
                    if hasattr(item, 'page'):
                        # Try to get page number from page object
                        page_obj = item.page
                        if hasattr(page_obj, 'page_number'):
                            page_num = page_obj.page_number
                        elif hasattr(reader, 'get_destination_page_number'):
                            try:
                                page_num = reader.get_destination_page_number(item) + 1  # 0-indexed
                            except:
                                pass

                    if page_num is None:
                        return

                    # Extract chapter number
                    for pattern in self.chapter_patterns:
                        match = pattern.search(title)
                        if match:
                            chapter_num = int(match.group(1))
                            if 1 <= chapter_num <= self.num_chapters:
                                boundaries[chapter_num] = (page_num, None)  # Start page, end to be determined
                            break

            for item in outline:
                process_outline_item(item)

            # Set end pages
            if boundaries:
                chapters = sorted(boundaries.keys())
                for i, chapter in enumerate(chapters):
                    start_page = boundaries[chapter][0]
                    if i < len(chapters) - 1:
                        end_page = boundaries[chapters[i + 1]][0] - 1
                    else:
                        end_page = self.get_page_count()
                    boundaries[chapter] = (start_page, end_page)

            return boundaries

        except Exception as e:
            print(f"TOC extraction failed: {e}")
            return {}

    def _find_chapters_from_headers(self, total_pages: int) -> Dict[int, Tuple[int, int]]:
        """Parse TOC pages to find chapter boundaries"""
        boundaries = {}

        # Parse TOC from pages 5-8 (based on what we saw)
        toc_pages = [5, 6, 7, 8]
        toc_text = ""

        for page_num in toc_pages:
            page_text = self.extract_text_from_page(page_num)
            toc_text += page_text + "\n"

        # Extract chapter entries using regex
        # Pattern: Chapter X CHAPTER_TITLE ........................................................ PAGE_NUM
        chapter_pattern = re.compile(r'Chapter\s+(\d+)\s+[^.]*\.{10,}\s*(\d+)', re.MULTILINE | re.IGNORECASE)

        matches = chapter_pattern.findall(toc_text)

        for match in matches:
            chapter_num = int(match[0])
            page_num = int(match[1])

            if 1 <= chapter_num <= self.num_chapters:
                boundaries[chapter_num] = (page_num, None)  # Start page, end to be determined

        # Set end pages
        if boundaries:
            chapters = sorted(boundaries.keys())
            for i, chapter in enumerate(chapters):
                start_page = boundaries[chapter][0]
                if i < len(chapters) - 1:
                    end_page = boundaries[chapters[i + 1]][0] - 1
                else:
                    end_page = total_pages
                boundaries[chapter] = (start_page, end_page)

        return boundaries

    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""

        # Fix broken hyphenations at line ends
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)

        # Normalize whitespace
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double
        text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)  # Remove leading whitespace per line

        # Remove excessive spaces around punctuation
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        text = re.sub(r'([,.!?;:])\s+', r'\1 ', text)

        return text.strip()

    def detect_headings(self, text: str) -> str:
        """Convert detected headings to Markdown format"""
        lines = text.split('\n')
        processed_lines = []

        for line in lines:
            original_line = line.strip()
            if not original_line:
                processed_lines.append('')
                continue

            # Skip if already has markdown heading
            if original_line.startswith('#'):
                processed_lines.append(line)
                continue

            # Check for section numbers (1.1., 1.1.1., etc.)
            section_match = re.match(r'^(\d+(?:\.\d+)*\.?)\s+(.+)$', original_line)
            if section_match:
                section_num = section_match.group(1).rstrip('.')  # Remove trailing dot
                heading_text = section_match.group(2)
                # Determine heading level based on section number depth
                level = len(section_num.split('.')) + 1  # 1. -> ##, 1.1. -> ###
                processed_lines.append('#' * level + ' ' + heading_text)
                continue

            # Check for all-caps headings (likely section headers)
            if (len(original_line.split()) <= 10 and
                original_line.isupper() and
                not original_line.endswith('.') and
                not re.search(r'\d', original_line)):  # No numbers
                # This might be a heading, but let's be conservative
                # Only convert if it looks like a section title
                if len(original_line) > 20 or any(word in original_line.lower() for word in
                    ['introduction', 'summary', 'overview', 'conclusion', 'purpose', 'scope']):
                    processed_lines.append('## ' + original_line.title())
                    continue

            processed_lines.append(line)

        return '\n'.join(processed_lines)

    def detect_lists(self, text: str) -> str:
        """Convert detected lists to Markdown format"""
        lines = text.split('\n')
        processed_lines = []
        in_list = False

        for i, line in enumerate(lines):
            original_line = line.strip()
            if not original_line:
                processed_lines.append('')
                continue

            # Check for numbered lists
            num_match = re.match(r'^(\d+)\.\s+(.+)$', original_line)
            if num_match:
                processed_lines.append(f"{num_match.group(1)}. {num_match.group(2)}")
                continue

            # Check for lettered lists
            letter_match = re.match(r'^([a-zA-Z])\.\s+(.+)$', original_line)
            if letter_match:
                processed_lines.append(f"{letter_match.group(1).lower()}. {letter_match.group(2)}")
                continue

            # Check for bullet points
            bullet_match = re.match(r'^([•\*\-])\s+(.+)$', original_line)
            if bullet_match:
                processed_lines.append(f"- {bullet_match.group(2)}")
                continue

            processed_lines.append(line)

        return '\n'.join(processed_lines)

    def process_chapter_text(self, chapter_text: str, chapter_num: int) -> str:
        """Process raw chapter text into Markdown format"""
        # Clean the text
        cleaned_text = self.clean_text(chapter_text)

        # Extract and format chapter title
        lines = cleaned_text.split('\n')
        chapter_title = f"# Chapter {chapter_num}"

        # Look for the actual chapter title in the first few lines
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            if line and not line.startswith(('Page', 'page', 'PAGE')):
                # Check if it matches chapter pattern
                for pattern in self.chapter_patterns:
                    if pattern.search(line):
                        # Extract title part after chapter number
                        match = pattern.search(line)
                        title_part = line[match.end():].strip()
                        if title_part.startswith(('—', ':', '-')):
                            title_part = title_part[1:].strip()
                        if title_part:
                            chapter_title = f"# Chapter {chapter_num} — {title_part}"
                        break
                break

        # Remove the title line from content if found
        content_lines = []
        title_found = False
        for line in lines:
            if not title_found:
                for pattern in self.chapter_patterns:
                    if pattern.search(line.strip()):
                        title_found = True
                        continue
            if title_found or not line.strip():
                content_lines.append(line)

        content = '\n'.join(content_lines)

        # Apply formatting
        content = self.detect_headings(content)
        content = self.detect_lists(content)

        # Combine title and content
        return f"{chapter_title}\n\n{content}"

    def extract_chapter(self, chapter_num: int, start_page: int, end_page: int) -> Tuple[str, List[int]]:
        """Extract a single chapter from PDF"""
        print(f"Extracting Chapter {chapter_num} (pages {start_page}-{end_page})...")

        chapter_text = []
        processed_pages = []

        for page_num in range(start_page, end_page + 1):
            text = self.extract_text_from_page(page_num)
            if text:
                # Add page marker
                chapter_text.append(f"<!-- Page {page_num} -->")
                chapter_text.append(text)
                processed_pages.append(page_num)

        full_text = '\n\n'.join(chapter_text)
        markdown_text = self.process_chapter_text(full_text, chapter_num)

        return markdown_text, processed_pages

    def should_skip_chapter(self, chapter_file: Path, force: bool = False) -> bool:
        """Check if chapter should be skipped (already exists and is large enough)"""
        if force:
            return False

        if not chapter_file.exists():
            return False

        # Check file size (>50KB as specified)
        if chapter_file.stat().st_size > 50 * 1024:
            return True

        return False

    def save_chapter(self, chapter_num: int, content: str, pages: List[int]) -> Dict[str, Any]:
        """Save chapter to file and return stats"""
        filename = f"chapter{chapter_num:02d}.md"
        filepath = self.output_dir / filename

        # Skip if already exists and large enough
        if self.should_skip_chapter(filepath, getattr(self, 'force_mode', False)):
            print(f"Skipping Chapter {chapter_num} (already exists and >50KB)")
            return {
                'chapter': chapter_num,
                'filepath': str(filepath),
                'skipped': True,
                'size_bytes': filepath.stat().st_size,
                'pages': len(pages)
            }

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        size_bytes = len(content.encode('utf-8'))
        num_chars = len(content)

        # Extract first heading and last lines for verification
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        first_heading = ""
        for line in lines[:5]:
            if line.startswith('#'):
                first_heading = line
                break

        last_lines = lines[-2:] if len(lines) >= 2 else lines[-1:] if lines else []

        print(f"Chapter {chapter_num}: {size_bytes} bytes, {num_chars} chars")
        if first_heading:
            print(f"  First heading: {first_heading}")
        if last_lines:
            print(f"  Last lines: {' | '.join(last_lines[:2])}")

        return {
            'chapter': chapter_num,
            'filepath': str(filepath),
            'size_bytes': size_bytes,
            'num_chars': num_chars,
            'pages': pages,
            'first_heading': first_heading,
            'last_lines': last_lines,
            'skipped': False
        }

    def extract_all_chapters(self, force: bool = False) -> Dict[str, Any]:
        """Extract all chapters from PDF"""
        self.force_mode = force

        start_time = time.time()

        # Check dependencies
        self.check_dependencies()

        # Find chapter boundaries
        boundaries = self.find_chapter_boundaries()

        if not boundaries:
            raise ValueError("Could not find chapter boundaries in PDF")

        print(f"Found {len(boundaries)} chapters:")
        for chapter, (start, end) in boundaries.items():
            print(f"  Chapter {chapter}: pages {start}-{end}")

        # Extract each chapter
        results = []
        total_pages = 0

        for chapter_num in range(1, self.num_chapters + 1):
            if chapter_num not in boundaries:
                print(f"Warning: Chapter {chapter_num} not found, skipping")
                continue

            start_page, end_page = boundaries[chapter_num]
            content, pages = self.extract_chapter(chapter_num, start_page, end_page)

            result = self.save_chapter(chapter_num, content, pages)
            results.append(result)
            total_pages += len(pages)

        # Save split index
        split_index = {
            'pdf_path': str(self.pdf_path),
            'total_pages': self.get_page_count(),
            'chapters_found': len(boundaries),
            'chapters_extracted': len([r for r in results if not r.get('skipped', False)]),
            'chapter_boundaries': boundaries,
            'extraction_time_seconds': time.time() - start_time,
            'results': results
        }

        index_file = Path('.split_index.json')
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(split_index, f, indent=2, ensure_ascii=False)

        return split_index


def main():
    parser = argparse.ArgumentParser(description='Extract chapters from AFH1 PDF to Markdown')
    parser.add_argument('--pdf', default='./AFH 1.pdf', help='Path to PDF file')
    parser.add_argument('--out', default='./chapters', help='Output directory')
    parser.add_argument('--chapters', type=int, default=24, help='Number of chapters')
    parser.add_argument('--force', action='store_true', help='Force re-extraction even if files exist')

    args = parser.parse_args()

    # Check if PDF exists
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF file not found at {pdf_path}")
        print("Please specify the correct path with --pdf")
        sys.exit(1)

    # Create extractor and run
    extractor = PDFChapterExtractor(args.pdf, args.out, args.chapters)

    try:
        results = extractor.extract_all_chapters(force=args.force)

        # Print summary
        print("\n" + "="*60)
        print("EXTRACTION COMPLETE")
        print("="*60)
        print(f"PDF: {args.pdf}")
        print(f"Total pages: {results['total_pages']}")
        print(f"Chapters found: {results['chapters_found']}")
        print(f"Chapters extracted: {results['chapters_extracted']}")
        print(".3f")
        print(f"Output directory: {args.out}")
        print(f"Index file: .split_index.json")

        print("\nCHAPTER SUMMARY:")
        print("<5")
        print("-" * 70)

        for result in results['results']:
            status = "SKIPPED" if result.get('skipped') else "EXTRACTED"
            chapter = result['chapter']
            size_kb = result['size_bytes'] / 1024
            first_heading = result.get('first_heading', '')[:50]
            last_line = result.get('last_lines', [''])[-1][:50] if result.get('last_lines') else ''

            print("2d")

        # Verification
        print("\nVERIFICATION:")
        chapters_dir = Path(args.out)
        missing_chapters = []
        small_chapters = []

        for chapter_num in range(1, args.chapters + 1):
            chapter_file = chapters_dir / "02d"
            if not chapter_file.exists():
                missing_chapters.append(chapter_num)
            elif chapter_file.stat().st_size < 5 * 1024:  # Less than 5KB might be too small
                small_chapters.append((chapter_num, chapter_file.stat().st_size))

        if missing_chapters:
            print(f"Missing chapters: {missing_chapters}")
        else:
            print("All chapters extracted successfully!")

        if small_chapters:
            print("Small chapters (might need review):")
            for chapter_num, size_bytes in small_chapters:
                print(".1f")

    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
