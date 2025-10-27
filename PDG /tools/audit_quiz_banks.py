#!/usr/bin/env python3
"""
Comprehensive audit of quiz banks to identify quality issues.
"""

import re
from pathlib import Path
from collections import defaultdict


def audit_quiz_bank(quiz_file: Path) -> dict:
    """Audit a single quiz bank for quality issues."""
    with open(quiz_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = {
        'duplicate_questions': [],
        'bad_distractors': [],
        'incomplete_questions': [],
        'metadata_questions': [],
        'vague_questions': [],
        'truncated_answers': [],
        'poor_references': []
    }
    
    # Extract all questions
    questions = re.findall(r'### (AFH1-C\d+-Q\d+) \| (\w+)\n\n\*\*Question:\*\* (.+?)\n\n(.+?)\n\n\*\*Answer:\*\* (.+?)\n\n\*\*Rationale:\*\* (.+?)\n\n\*\*Reference:\*\* (.+?)\n\n---', content, re.DOTALL)
    
    seen_prompts = defaultdict(list)
    
    for q_id, difficulty, prompt, choices, answer, rationale, reference in questions:
        # Check for duplicate prompts
        seen_prompts[prompt].append(q_id)
        
        # Check for metadata questions (AFH 1, AIRMAN date)
        if "AFH 1, AIRMAN 15 February" in prompt:
            issues['metadata_questions'].append({
                'id': q_id,
                'prompt': prompt[:100]
            })
        
        # Check for bad distractors (generic/useless)
        if "A temporary designation used only during wartime operations" in choices:
            issues['bad_distractors'].append({
                'id': q_id,
                'prompt': prompt[:100]
            })
        
        # Check for vague questions
        if "What does" in prompt and "refer to in the context" in prompt:
            issues['vague_questions'].append({
                'id': q_id,
                'prompt': prompt[:100]
            })
        
        # Check for truncated answers
        if "..." in choices and choices.count("...") > 2:
            issues['truncated_answers'].append({
                'id': q_id,
                'prompt': prompt[:100]
            })
        
        # Check for incomplete questions
        if prompt.endswith("___?") or "___" in prompt:
            # This is okay for fill-in questions, but check if it makes sense
            if prompt.count("___") > 1:
                issues['incomplete_questions'].append({
                    'id': q_id,
                    'prompt': prompt[:100]
                })
    
    # Find duplicates
    for prompt, ids in seen_prompts.items():
        if len(ids) > 1:
            issues['duplicate_questions'].append({
                'prompt': prompt[:100],
                'ids': ids
            })
    
    return issues, len(questions)


def main():
    quiz_dir = Path("/Users/dre/Desktop/PDG /quiz_banks")
    
    print("=" * 80)
    print("COMPREHENSIVE QUIZ BANK AUDIT")
    print("=" * 80)
    print()
    
    total_issues = defaultdict(int)
    chapter_reports = []
    
    for chapter_num in range(1, 25):
        quiz_file = quiz_dir / f"chapter{chapter_num:02d}_quiz_bank" / f"chapter{chapter_num:02d}_quiz.md"
        
        if not quiz_file.exists():
            continue
        
        issues, num_questions = audit_quiz_bank(quiz_file)
        
        chapter_issues = sum(len(v) for v in issues.values())
        total_issues['total'] += chapter_issues
        
        for issue_type, issue_list in issues.items():
            total_issues[issue_type] += len(issue_list)
        
        chapter_reports.append({
            'chapter': chapter_num,
            'questions': num_questions,
            'issues': chapter_issues,
            'details': issues
        })
        
        print(f"Chapter {chapter_num:02d}: {num_questions} questions, {chapter_issues} issues")
    
    print()
    print("=" * 80)
    print("ISSUE SUMMARY")
    print("=" * 80)
    print()
    
    for issue_type, count in sorted(total_issues.items()):
        if issue_type != 'total':
            print(f"  {issue_type.replace('_', ' ').title()}: {count}")
    
    print()
    print(f"TOTAL ISSUES: {total_issues['total']}")
    print()
    
    # Show examples of worst issues
    print("=" * 80)
    print("CRITICAL ISSUES TO FIX")
    print("=" * 80)
    print()
    
    for report in chapter_reports[:5]:  # First 5 chapters as examples
        if report['issues'] > 0:
            print(f"\nChapter {report['chapter']:02d}:")
            for issue_type, issue_list in report['details'].items():
                if issue_list:
                    print(f"  - {issue_type}: {len(issue_list)} instances")
                    if issue_list and len(issue_list) > 0:
                        print(f"    Example: {issue_list[0]}")


if __name__ == "__main__":
    main()

