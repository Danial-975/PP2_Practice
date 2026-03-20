import shutil
from pathlib import Path

shutil.copy2('source.txt', 'backup_source.txt')

if not Path('project_backup').exists():
    shutil.copytree('my_project', 'project_backup')