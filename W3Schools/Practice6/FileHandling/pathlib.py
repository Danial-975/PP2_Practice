from pathlib import Path

base_path = Path("Practice6")
file_path = base_path / "data" / "config.json"

print(f"Полный путь: {file_path}")
print(f"Имя файла: {file_path.name}")       
print(f"Только имя: {file_path.stem}")       
print(f"Расширение: {file_path.suffix}")