#!/usr/bin/env python3
"""
Generate PERFECT MCQ quiz banks for AFH1 chapters.
FINAL VERSION - Clean extraction, quality questions, no metadata.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import random
import hashlib


class QuizGenerator:
    def __init__(self, chapters_dir: str, output_dir: str):
        self.chapters_dir = Path(chapters_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.seen_questions = set()
        
    def read_chapter(self, chapter_num: int) -> Tuple[str, str]:
        """Read chapter content and extract title."""
        chapter_file = self.chapters_dir / f"chapter{chapter_num:02d}.md"
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Chapter {chapter_num}"
        
        return content, title
    
    def is_metadata(self, text: str) -> bool:
        """Check if text is metadata/formatting that should be excluded."""
        # Patterns to exclude
        exclude_patterns = [
            r'AFH 1, AIRMAN 15 February',
            r'REQUIRED LEVEL OF COMPREHENSION',
            r'Chapter \d+—[A-Z\s]+\s+[SBMT][Ss][Gg]t',  # Chapter X—TITLE SSgt TSgt...
            r'Section \d+[A-Z]—[^.]+\s+[BC\s]+$',  # Section XA—Title B B C C C
            r'^[SBMT][Ss][Gg]t\s+[SBMT][Ss][Gg]t',  # SSgt TSgt MSgt...
            r'^[BC\s]+$',  # Just "B B C C C" or "C C C C C"
            r'^\s*[SBMT][Ss][Gg]t\s*$',  # Just rank abbreviations
        ]
        
        for pattern in exclude_patterns:
            if re.search(pattern, text):
                return True
        
        # Exclude if it's just ranks
        if text.strip() in ['SSgt', 'TSgt', 'MSgt', 'SMSgt', 'CMSgt', 'B B C C C', 'C C C C C']:
            return True
        
        return False
    
    def clean_and_extract_sentences(self, content: str) -> List[Dict]:
        """Extract meaningful sentences, filtering ALL metadata."""
        # Remove page markers
        content = re.sub(r'<!-- Page \d+ -->', '', content)
        
        lines = content.split('\n')
        sentences = []
        
        current_section = None
        current_subsection = None
        
        for line in lines:
            line = line.strip()
            
            # Track section context
            if line.startswith('## '):
                current_section = line[3:].strip()
                current_subsection = None
                continue
            elif line.startswith('### '):
                current_subsection = line[4:].strip()
                continue
            elif line.startswith(('#', '####')):
                continue
            
            # Skip empty, very short, or metadata
            if not line or len(line) < 25:
                continue
            
            if self.is_metadata(line):
                continue
            
            # Skip markdown artifacts
            if line.startswith(('|', '---', '>', '```', '**REQUIRED')):
                continue
            
            # Split into sentences
            sent_parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', line)
            
            for sent in sent_parts:
                sent = sent.strip()
                
                if len(sent) < 25:
                    continue
                
                # Final metadata check
                if self.is_metadata(sent):
                    continue
                
                # Add period if missing
                if not sent.endswith(('.', '!', '?', ':')):
                    sent += '.'
                
                sentences.append({
                    'text': sent,
                    'section': current_section,
                    'subsection': current_subsection
                })
        
        return sentences
    
    def create_question_hash(self, prompt: str) -> str:
        """Create hash to detect duplicates."""
        return hashlib.md5(prompt.lower().strip().encode()).hexdigest()
    
    def create_mcq(self, sentence: Dict, all_sentences: List[Dict], chapter_num: int) -> Dict:
        """Create MCQ from sentence with intelligent strategies."""
        text = sentence['text']
        section = sentence['section']
        subsection = sentence['subsection']
        
        # Get clean similar sentences for distractors (no metadata)
        similar_sentences = [s for s in all_sentences 
                            if s.get('section') == section 
                            and s.get('text') != text
                            and len(s.get('text', '')) > 30
                            and not self.is_metadata(s.get('text', ''))]
        
        # STRATEGY 1: Year questions
        year_match = re.search(r'\b(1[89]\d{2}|20[0-2]\d)\b', text)
        if year_match:
            year = year_match.group(1)
            context = text.replace(year, '____', 1)
            
            prompt = f"What year completes this statement: {context}"
            correct = year
            
            base_year = int(year)
            distractors = [str(base_year - 1), str(base_year + 1), str(base_year + 2)]
            
            return {
                'prompt': prompt,
                'correct': correct,
                'distractors': distractors,
                'section': section,
                'subsection': subsection,
                'difficulty': 'Easy'
            }
        
        # STRATEGY 2: Number questions
        num_match = re.search(r'\b(\d+)\s*(percent|%|million|billion|thousand|hundred|years?|days?|months?|weeks?)\b', text, re.IGNORECASE)
        if num_match:
            number = num_match.group(0)
            context = text.replace(number, '____', 1)
            
            prompt = f"Complete this statement: {context}"
            correct = number
            
            try:
                base_num = int(re.search(r'\d+', number).group())
                unit = num_match.group(2) if num_match.group(2) else ""
                
                if base_num < 10:
                    distractors = [f"{base_num + 2} {unit}".strip(), f"{base_num - 1} {unit}".strip(), f"{base_num + 5} {unit}".strip()]
                else:
                    distractors = [f"{base_num + 10} {unit}".strip(), f"{base_num - 10} {unit}".strip(), f"{int(base_num * 1.5)} {unit}".strip()]
            except:
                distractors = ["5", "10", "20"]
            
            return {
                'prompt': prompt,
                'correct': correct,
                'distractors': distractors,
                'section': section,
                'subsection': subsection,
                'difficulty': 'Medium'
            }
        
        # STRATEGY 3: Named person questions
        person_match = re.search(r'((?:General|Colonel|Major|Captain|Lieutenant|President|Secretary|Chief|CMSAF)\s+[A-Z][a-z]+(?:\s+[A-Z]\.?)?\s*[A-Z][a-z]+)', text)
        if person_match:
            person = person_match.group(1)
            prompt = f"What does this chapter state about {person}?"
            correct = text
            
            if len(similar_sentences) >= 3:
                distractors = [s['text'] for s in similar_sentences[:3]]
            else:
                distractors = [
                    "This individual did not serve in the Air Force.",
                    "This person's contributions are not discussed in this chapter.",
                    "This information applies to a different time period."
                ]
            
            return {
                'prompt': prompt,
                'correct': correct,
                'distractors': distractors,
                'section': section,
                'subsection': subsection,
                'difficulty': 'Medium'
            }
        
        # STRATEGY 4: Acronym questions (excluding common words)
        acronym_match = re.search(r'\b([A-Z]{2,})\b', text)
        if acronym_match and len(text) > 50:
            acronym = acronym_match.group(1)
            # Skip common words
            if acronym not in ['THE', 'AND', 'FOR', 'NOT', 'ARE', 'WAS', 'BUT', 'CAN', 'ALL', 'ONE', 'TWO', 'USA', 'AIR']:
                prompt = f"According to this chapter, what is stated about {acronym}?"
                correct = text
                
                if len(similar_sentences) >= 3:
                    distractors = [s['text'] for s in similar_sentences[:3]]
                else:
                    distractors = [
                        "This acronym is not defined in this chapter.",
                        "This applies to a different organizational structure.",
                        "This term is used exclusively in other military branches."
                    ]
                
                return {
                    'prompt': prompt,
                    'correct': correct,
                    'distractors': distractors,
                    'section': section,
                    'subsection': subsection,
                    'difficulty': 'Medium'
                }
        
        # STRATEGY 5: Requirement questions
        if any(word in text.lower() for word in ['must', 'shall', 'required', 'responsible', 'obligated', 'ensures']):
            prompt = f"Which statement about requirements is accurate according to this chapter?"
            correct = text
            
            if len(similar_sentences) >= 3:
                distractors = [s['text'] for s in similar_sentences[:3]]
            else:
                distractors = [
                    "This is a recommended practice but not mandatory.",
                    "This requirement applies only to specific career fields.",
                    "This policy was superseded by more recent guidance."
                ]
            
            return {
                'prompt': prompt,
                'correct': correct,
                'distractors': distractors,
                'section': section,
                'subsection': subsection,
                'difficulty': 'Hard'
            }
        
        # STRATEGY 6: Definition questions
        if re.search(r'\b(is|are|means|refers to|defined as|consists of)\b', text, re.IGNORECASE):
            prompt = f"Which statement accurately describes a concept from this chapter?"
            correct = text
            
            if len(similar_sentences) >= 3:
                distractors = [s['text'] for s in similar_sentences[:3]]
            else:
                distractors = [
                    "This concept is not addressed in this chapter.",
                    "This definition applies to civilian organizations only.",
                    "This term has a different meaning in Air Force context."
                ]
            
            return {
                'prompt': prompt,
                'correct': correct,
                'distractors': distractors,
                'section': section,
                'subsection': subsection,
                'difficulty': 'Medium'
            }
        
        # STRATEGY 7: General fact questions
        if len(text) > 40:
            prompt = f"Which of the following statements from this chapter is accurate?"
            correct = text
            
            if len(similar_sentences) >= 3:
                distractors = [s['text'] for s in similar_sentences[:3]]
            else:
                distractors = [
                    "This information is not covered in this chapter.",
                    "This applies only to specific situations not described here.",
                    "This statement reflects outdated policy."
                ]
            
            return {
                'prompt': prompt,
                'correct': correct,
                'distractors': distractors,
                'section': section,
                'subsection': subsection,
                'difficulty': 'Medium'
            }
        
        return None
    
    def generate_questions(self, chapter_num: int, content: str) -> List[Dict]:
        """Generate comprehensive MCQ set from ALL clean sentences."""
        self.seen_questions.clear()
        questions = []
        
        # Extract sentences
        sentences = self.clean_and_extract_sentences(content)
        print(f"  Extracted {len(sentences)} sentences...", end=' ', flush=True)
        
        q_num = 1
        
        # Create question from every sentence
        for sentence in sentences:
            mcq = self.create_mcq(sentence, sentences, chapter_num)
            
            if mcq:
                # Check for duplicates
                q_hash = self.create_question_hash(mcq['prompt'])
                if q_hash in self.seen_questions:
                    continue
                self.seen_questions.add(q_hash)
                
                # Shuffle choices
                choices = [mcq['correct']] + mcq['distractors']
                random.seed(chapter_num * 1000 + q_num)
                random.shuffle(choices)
                correct_letter = chr(65 + choices.index(mcq['correct']))
                
                questions.append({
                    'type': 'MCQ',
                    'id': f"AFH1-C{chapter_num:02d}-Q{q_num:04d}",
                    'difficulty': mcq['difficulty'],
                    'prompt': mcq['prompt'],
                    'choices': choices,
                    'answer': correct_letter,
                    'rationale': self._get_rationale(mcq['difficulty']),
                    'refs': self._get_section_ref(mcq['section'], mcq['subsection'])
                })
                
                q_num += 1
        
        print(f"Created {len(questions)} questions", flush=True)
        return questions
    
    def _get_rationale(self, difficulty: str) -> str:
        """Get rationale based on difficulty."""
        rationales = {
            'Easy': "Understanding key facts and dates is essential for Air Force knowledge.",
            'Medium': "This tests comprehension of important Air Force concepts and procedures.",
            'Hard': "This requires understanding of Air Force requirements and their application."
        }
        return rationales.get(difficulty, "This is important knowledge for Air Force personnel.")
    
    def _get_section_ref(self, section: str, subsection: str) -> str:
        """Format section reference."""
        if subsection:
            return f"[{section} — {subsection}]"
        elif section:
            return f"[{section}]"
        else:
            return "[Chapter content]"
    
    def write_quiz_bank(self, chapter_num: int, title: str, questions: List[Dict]):
        """Write quiz bank to markdown file."""
        quiz_folder = self.output_dir / f"chapter{chapter_num:02d}_quiz_bank"
        quiz_folder.mkdir(exist_ok=True)
        
        quiz_file = quiz_folder / f"chapter{chapter_num:02d}_quiz.md"
        today = datetime.now().strftime('%Y-%m-%d')
        
        with open(quiz_file, 'w', encoding='utf-8') as f:
            # Frontmatter
            f.write("---\n")
            f.write(f"chapter: {chapter_num}\n")
            f.write(f'title: "AFH1 Chapter {chapter_num} — Quiz Bank"\n')
            f.write(f"source: ../chapters/chapter{chapter_num:02d}.md\n")
            f.write(f"generated: {today}\n")
            f.write(f"items: {len(questions)}\n")
            f.write(f"format: Multiple Choice Only\n")
            f.write("---\n\n")
            
            # Header
            f.write(f"# AFH1 Chapter {chapter_num} — Quiz Bank\n\n")
            f.write(f"**{title}**\n\n")
            f.write("Comprehensive multiple-choice questions covering all key content from this chapter.\n\n")
            f.write("---\n\n")
            
            # Group by difficulty
            for difficulty in ['Easy', 'Medium', 'Hard']:
                difficulty_questions = [q for q in questions if q['difficulty'] == difficulty]
                
                if not difficulty_questions:
                    continue
                
                f.write(f"## {difficulty} Questions\n\n")
                
                for q in difficulty_questions:
                    f.write(f"### {q['id']} | {q['difficulty']}\n\n")
                    f.write(f"**Question:** {q['prompt']}\n\n")
                    
                    for i, choice in enumerate(q['choices']):
                        f.write(f"{chr(65+i)}. {choice}\n\n")
                    
                    f.write(f"**Answer:** {q['answer']}\n\n")
                    f.write(f"**Rationale:** {q['rationale']}\n\n")
                    f.write(f"**Reference:** {q['refs']}\n\n")
                    f.write("---\n\n")
        
        return quiz_file, len(questions)
    
    def generate_all_quizzes(self):
        """Generate quiz banks for all 24 chapters."""
        print("=" * 70)
        print("AFH1 PERFECT MCQ QUIZ BANK GENERATOR - FINAL")
        print("=" * 70)
        print()
        
        summary = []
        
        for chapter_num in range(1, 25):
            print(f"Chapter {chapter_num:02d}:", end=' ', flush=True)
            
            content, title = self.read_chapter(chapter_num)
            questions = self.generate_questions(chapter_num, content)
            quiz_file, num_questions = self.write_quiz_bank(chapter_num, title, questions)
            
            file_size = quiz_file.stat().st_size
            
            summary.append({
                'chapter': chapter_num,
                'title': title,
                'questions': num_questions,
                'size': file_size
            })
        
        print()
        print("=" * 70)
        print("GENERATION COMPLETE")
        print("=" * 70)
        print()
        print(f"{'Ch':<4} {'Questions':<10} {'Size':<12} {'Title':<40}")
        print("-" * 70)
        
        total_questions = 0
        for item in summary:
            print(f"{item['chapter']:02d}   {item['questions']:<10} {item['size']:>10,}B  {item['title'][:40]}")
            total_questions += item['questions']
        
        print()
        print(f"✅ Total: {len(summary)} quiz banks | {total_questions} MCQ questions")
        print()


def main():
    base_dir = Path(__file__).parent.parent
    chapters_dir = base_dir / "chapters"
    output_dir = base_dir / "quiz_banks"
    
    generator = QuizGenerator(chapters_dir, output_dir)
    generator.generate_all_quizzes()


if __name__ == "__main__":
    main()
