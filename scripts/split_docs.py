#!/usr/bin/env python3
"""
Split CrewAI documentation into logical sections for the skill.
"""

def split_documentation(input_file, output_dir):
    """Split the large documentation file into logical sections."""

    # Define section mappings: (start_pattern, end_pattern, output_file)
    sections = {
        'getting-started.md': {
            'patterns': ['introduction', 'installation', 'quickstart'],
            'start_line': None,
            'end_line': None
        },
        'core-concepts.md': {
            'patterns': ['concepts/agents', 'concepts/tasks', 'concepts/crews', 'concepts/tools$'],
            'start_line': None,
            'end_line': None
        },
        'advanced-features.md': {
            'patterns': ['concepts/flows', 'concepts/processes', 'concepts/planning',
                        'concepts/reasoning', 'concepts/collaboration', 'concepts/memory',
                        'concepts/knowledge', 'concepts/event-listener'],
            'start_line': None,
            'end_line': None
        },
        'llms-and-integrations.md': {
            'patterns': ['concepts/llms', 'mcp/'],
            'start_line': None,
            'end_line': None
        },
        'tools-reference.md': {
            'patterns': ['tools/ai-ml/', 'tools/cloud-storage/', 'tools/database-data/',
                        'tools/file-document/', 'tools/search-research/', 'tools/web-scraping/',
                        'tools/automation/', 'tools/integration/'],
            'start_line': None,
            'end_line': None
        },
        'cli-testing-training.md': {
            'patterns': ['concepts/cli', 'concepts/testing', 'concepts/training'],
            'start_line': None,
            'end_line': None
        },
        'guides-best-practices.md': {
            'patterns': ['guides/advanced/', 'guides/agents/', 'guides/concepts/', 'guides/crews/', 'guides/flows/'],
            'start_line': None,
            'end_line': None
        },
        'examples-tutorials.md': {
            'patterns': ['learn/', 'examples/', 'observability/'],
            'start_line': None,
            'end_line': None
        }
    }

    # Read source lines and find section boundaries
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Map each line to a section
    line_sections = {}
    current_section = None

    for i, line in enumerate(lines):
        if line.startswith('Source: https://docs.crewai.com/'):
            url = line.strip()
            # Determine which section this belongs to
            matched = False
            for section_name, section_info in sections.items():
                for pattern in section_info['patterns']:
                    if pattern in url:
                        current_section = section_name
                        matched = True
                        break
                if matched:
                    break

            # If no match, set to None
            if not matched:
                current_section = None

        # Assign current line to current section
        if current_section:
            line_sections[i] = current_section

    # Write sections to files
    import os
    os.makedirs(output_dir, exist_ok=True)

    for section_name in sections.keys():
        output_path = os.path.join(output_dir, section_name)
        section_lines = []

        # Collect all lines for this section
        for line_num in sorted(line_sections.keys()):
            if line_sections[line_num] == section_name:
                section_lines.append(lines[line_num])

        if section_lines:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.writelines(section_lines)

            # Calculate size
            size_kb = len(''.join(section_lines).encode('utf-8')) / 1024
            print(f"✅ Created {section_name} ({size_kb:.1f} KB, {len(section_lines)} lines)")
        else:
            print(f"⚠️  Skipping {section_name} (no content found)")

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print("Usage: split_docs.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    split_documentation(input_file, output_dir)
    print("\n✅ Documentation split complete!")
