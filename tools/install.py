"""Install the portable skills and their knowledge without overwriting local edits."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--project', type=Path)
    group.add_argument('--skills-dir', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    destination = ((args.project / '.agents' / 'skills') if args.project else args.skills_dir).resolve()
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    for entry in manifest:
        source = root / entry['path']
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
            raise SystemExit('Package hash mismatch: ' + entry['path'])
    plan = []
    for skill in sorted((root / 'skills').iterdir()):
        if not (skill / 'SKILL.md').is_file():
            continue
        for source in skill.rglob('*'):
            if source.is_file() and '__pycache__' not in source.parts:
                plan.append((source, destination / skill.name / source.relative_to(skill)))
        for source in (root / 'knowledge').glob('*.md'):
            plan.append((source, destination / skill.name / 'knowledge' / source.name))
    for source, target in plan:
        if target.exists() and (not target.is_file() or target.read_bytes() != source.read_bytes()):
            raise SystemExit('Existing different content; no files written: ' + str(target))
    for source, target in plan:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if source.read_bytes() != target.read_bytes():
            raise SystemExit('Copy verification failed: ' + str(target))
    print(json.dumps({'status': 'verified', 'files': len(plan), 'destination': str(destination)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
