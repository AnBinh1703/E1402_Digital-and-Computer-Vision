#!/usr/bin/env python
"""
Refactor traffic sign detection notebook:
- Remove legacy CNN classifier sections
- Keep YOLO detection pipeline
- Add comprehensive EDA, validation, evaluation
- Improve modularity and logging
"""

import json
from pathlib import Path

def analyze_notebook():
    """Analyze current notebook structure"""
    nb_path = Path(r"d:\UMEF\E1402_Digital and Computer Vision\final-project\DuongBinhAn_Trafic_Sign_Detection.ipynb")
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    print("="*80)
    print("NOTEBOOK ANALYSIS")
    print("="*80)
    print(f"\nTotal cells: {len(nb['cells'])}\n")
    
    # Categorize cells
    sections = {}
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            src = ''.join(cell['source']).strip()
            if src.startswith('#'):
                title = src.split('\n')[0]
                sections[i] = ('markdown', title)
        else:
            src = ''.join(cell['source'])
            if 'SECTION' in src or '===' in src:
                lines = src.split('\n')
                for line in lines:
                    if 'SECTION' in line:
                        sections[i] = ('code', line.strip())
                        break
    
    print("MAIN SECTIONS:")
    for idx, (cell_type, title) in sorted(sections.items()):
        print(f"  Cell {idx+1:2d} [{cell_type:8s}]: {title[:70]}")
    
    # Check for legacy code
    legacy_markers = {'ResNet', 'Classifier', 'violation', 'tracking', 'CNN'}
    yolo_markers = {'YOLO', 'train_yolo', 'data.yaml'}
    
    legacy_count = 0
    yolo_count = 0
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            src = ''.join(cell['source'])
            if any(m in src for m in legacy_markers):
                legacy_count += 1
            if any(m in src for m in yolo_markers):
                yolo_count += 1
    
    print(f"\nCode cells with legacy markers: {legacy_count}")
    print(f"Code cells with YOLO markers: {yolo_count}")
    print("="*80 + "\n")

if __name__ == "__main__":
    analyze_notebook()
