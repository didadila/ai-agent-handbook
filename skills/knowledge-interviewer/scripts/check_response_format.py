#!/usr/bin/env python3
"""Check the teaching/closing envelope, not semantic correctness."""
import argparse
import re
from pathlib import Path

HEADINGS = {'teach': ('结论', '机制', '验证'), 'close': ('状态', '记录', '入口')}
INTERNAL = re.compile(r'\b(?:agent|go|fe|py|alg|jvm|conc|mysql|redis|spring|mq|dist|sys)\.[a-z][\w.-]*\b|\bL[0-4]\b')


def check_flow(lines):
    """Validate a deliberately small Mermaid subset; not a rendering guarantee."""
    if len(lines) < 4 or lines[0] != '```mermaid' or lines[-1] != '```':
        return ['Flow must be one closed Mermaid fence']
    if lines[1].strip() not in ('flowchart TD', 'flowchart LR', 'graph TD', 'graph LR'):
        return ['Flow direction must be TD or LR']
    node = r'([A-Za-z][A-Za-z0-9_]*)(?:\[([^\[\]{}\n]+)\]|\{([^{}\[\]\n]+)\})?'
    declaration = re.compile(node)
    edge = re.compile(node + r'\s*-->(?:\|([^|\n]+)\|)?\s*' + node)
    nodes, defined, edges = set(), set(), 0

    def accept(groups):
        name, rectangle, diamond = groups
        nodes.add(name)
        label = rectangle or diamond
        if label:
            if len(label) > 60 or any(char in label for char in '<>;`'):
                return False
            defined.add(name)
        return True

    for line in lines[2:-1]:
        match = edge.fullmatch(line.strip())
        if match:
            groups = match.groups()
            if not accept(groups[:3]) or not accept(groups[4:]):
                return ['Flow labels must be short plain text']
            if groups[3] and (len(groups[3]) > 20 or any(c in groups[3] for c in '<>;`')):
                return ['Flow edge labels must be short plain text']
            edges += 1
        else:
            match = declaration.fullmatch(line.strip())
            if not match or not (match[2] or match[3]) or not accept(match.groups()):
                return ['Flow supports only one labeled node or directed edge per line']
    if not 2 <= len(nodes) <= 8 or not 1 <= edges <= 10:
        return ['Flow needs 2-8 nodes and 1-10 edges']
    if nodes != defined:
        return ['Every flow node needs an explicit explanatory label']
    return []


def visible_text(text):
    text = re.sub(r'```([^\n]*)\n(.*?)```',
                  lambda m: m[2] if m[1].strip() == 'mermaid' else '', text, flags=re.S)
    return re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)


def check_response(text: str, mode: str) -> list[str]:
    errors = []
    lines = text.strip().splitlines()
    headings, fenced = [], False
    for index, line in enumerate(lines):
        if line.startswith('```'):
            fenced = not fenced
        elif not fenced and re.match(r'^#{1,6}\s', line):
            headings.append((index, line))
    expected = ['### ' + name for name in HEADINGS[mode]]
    if [line for _, line in headings] != expected:
        errors.append('Exactly three ordered headings required: ' + ', '.join(expected))
        return errors
    if headings[0][0] != 0:
        errors.append('Introductory text before the first heading')
    sections = []
    for offset, (start, _) in enumerate(headings):
        stop = headings[offset + 1][0] if offset < 2 else len(lines)
        sections.append([line for line in lines[start + 1:stop] if line.strip()])
    if len(sections[0]) != 1:
        errors.append('Conclusion/status must occupy exactly one text line')
    middle = sections[1]
    is_table = bool(middle) and all(line.strip().startswith('|') and line.strip().endswith('|') for line in middle)
    if is_table:
        separators = [i for i, line in enumerate(middle)
                      if all(re.fullmatch(r':?-{3,}:?', cell.strip()) for cell in line.strip().strip('|').split('|'))]
        widths = {len(line.strip().strip('|').split('|')) for line in middle}
        if separators != [1] or not 3 <= len(middle) <= 6 or len(widths) != 1:
            errors.append('One table with a header and 1-4 content rows required')
    elif mode == 'teach' and middle and middle[0] == '```mermaid':
        errors.extend(check_flow(middle))
    elif mode == 'teach' and len(middle) == 1 and 2 <= len(middle[0].split('→')) <= 4:
        pass
    else:
        errors.append('Middle section must contain only one short table or allowed arrow chain')
    last = sections[2]
    if mode == 'teach' and last and last[0].startswith('```'):
        close = next((i for i in range(1, len(last)) if last[i] == '```'), None)
        if close is None or not 1 <= close - 1 <= 6:
            errors.append('Validation code must be one closed fence with 1-6 code lines')
        last = last[close + 1:] if close is not None else []
    if len(last) != 1 or last[0].startswith('```'):
        errors.append('Final section needs exactly one question/action line or one closing entry line')
    if INTERNAL.search(visible_text(text)):
        errors.append('Internal point ID or graph level exposed in learner-facing text')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=HEADINGS, required=True)
    parser.add_argument('file', type=Path)
    args = parser.parse_args()
    errors = check_response(args.file.read_text(), args.mode)
    for error in errors:
        print('ERROR:', error)
    print('Structure only; semantic accuracy, evidence and action count need rubric review.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
