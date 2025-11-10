#!/usr/bin/env python3
"""
🔄 DIFF TOOL - Порівняння реалізацій

Цей інструмент показує детальні відмінності між еталонною
та розробницькою реалізаціями на рівні коду.

Використання:
    python diff_tool.py field.py              # Порівняння field.py
    python diff_tool.py contact.py            # Порівняння contact.py
    python diff_tool.py --side-by-side        # Бік-о-бік порівняння
"""

import argparse
import difflib
from pathlib import Path
from typing import List, Tuple

def read_file_safely(file_path: Path) -> List[str]:
    """Безпечно прочитати файл."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return [f"# Файл не знайдено: {file_path}\n"]
    except Exception as e:
        return [f"# Помилка читання файла: {e}\n"]

def get_file_paths(filename: str) -> Tuple[Path, Path]:
    """Отримати шляхи до еталонного та розробницького файлів."""
    project_root = Path(__file__).parent.parent.parent
    
    # Еталонний файл
    if filename == "field.py":
        ref_path = project_root / "personal_assistant" / "models" / "field.py"
    elif filename == "contact.py":
        ref_path = project_root / "personal_assistant" / "models" / "contact.py"
    else:
        ref_path = project_root / "personal_assistant" / filename
    
    # Розробницький файл
    dev_path = project_root / "dev_implementation" / "models" / filename
    
    return ref_path, dev_path

def show_unified_diff(ref_lines: List[str], dev_lines: List[str], ref_path: Path, dev_path: Path):
    """Показати unified diff."""
    print("📋 UNIFIED DIFF")
    print("=" * 70)
    
    diff = difflib.unified_diff(
        ref_lines,
        dev_lines,
        fromfile=f"Еталон: {ref_path.name}",
        tofile=f"Розробка: {dev_path.name}",
        lineterm=""
    )
    
    diff_lines = list(diff)
    if not diff_lines:
        print("✅ Файли ідентичні!")
        return
    
    for line in diff_lines:
        if line.startswith('+++'):
            print(f"🟢 {line}")
        elif line.startswith('---'):
            print(f"🔴 {line}")
        elif line.startswith('@@'):
            print(f"🔵 {line}")
        elif line.startswith('+'):
            print(f"🟩 {line}")
        elif line.startswith('-'):
            print(f"🟥 {line}")
        else:
            print(f"   {line}")

def show_side_by_side_diff(ref_lines: List[str], dev_lines: List[str], ref_path: Path, dev_path: Path):
    """Показати side-by-side diff."""
    print("📋 SIDE-BY-SIDE COMPARISON")
    print("=" * 120)
    
    # Заголовки колонок
    print(f"{'ЕТАЛОН':<58} | {'РОЗРОБКА':<58}")
    print("-" * 58 + " | " + "-" * 58)
    
    max_lines = max(len(ref_lines), len(dev_lines))
    
    for i in range(max_lines):
        ref_line = ref_lines[i].rstrip() if i < len(ref_lines) else ""
        dev_line = dev_lines[i].rstrip() if i < len(dev_lines) else ""
        
        # Обрізати довгі лінії
        ref_display = (ref_line[:55] + "...") if len(ref_line) > 55 else ref_line
        dev_display = (dev_line[:55] + "...") if len(dev_line) > 55 else dev_line
        
        # Позначити відмінності
        marker = "🔸" if ref_line != dev_line else "  "
        
        print(f"{ref_display:<58} {marker} {dev_display}")

def analyze_structure_diff(ref_lines: List[str], dev_lines: List[str]):
    """Аналіз структурних відмінностей."""
    print("\n🔍 СТРУКТУРНИЙ АНАЛІЗ")
    print("=" * 70)
    
    # Пошук класів
    ref_classes = []
    dev_classes = []
    
    for line in ref_lines:
        if line.strip().startswith("class "):
            class_name = line.strip().split()[1].split("(")[0].rstrip(":")
            ref_classes.append(class_name)
    
    for line in dev_lines:
        if line.strip().startswith("class "):
            class_name = line.strip().split()[1].split("(")[0].rstrip(":")
            dev_classes.append(class_name)
    
    print("📚 Класи:")
    print(f"   Еталон: {', '.join(ref_classes) if ref_classes else 'Не знайдено'}")
    print(f"   Розробка: {', '.join(dev_classes) if dev_classes else 'Не знайдено'}")
    
    # Відсутні класи
    missing_in_dev = set(ref_classes) - set(dev_classes)
    extra_in_dev = set(dev_classes) - set(ref_classes)
    
    if missing_in_dev:
        print(f"❌ Відсутні класи в розробці: {', '.join(missing_in_dev)}")
    if extra_in_dev:
        print(f"➕ Додаткові класи в розробці: {', '.join(extra_in_dev)}")
    
    # Пошук методів
    ref_methods = []
    dev_methods = []
    
    for line in ref_lines:
        if line.strip().startswith("def "):
            method_name = line.strip().split()[1].split("(")[0]
            ref_methods.append(method_name)
    
    for line in dev_lines:
        if line.strip().startswith("def "):
            method_name = line.strip().split()[1].split("(")[0]
            dev_methods.append(method_name)
    
    print(f"\n🔧 Методи (загалом):")
    print(f"   Еталон: {len(ref_methods)} методів")
    print(f"   Розробка: {len(dev_methods)} методів")
    
    # Відсутні методи
    missing_methods = set(ref_methods) - set(dev_methods)
    if missing_methods:
        print(f"❌ Відсутні методи: {', '.join(missing_methods)}")

def show_statistics(ref_lines: List[str], dev_lines: List[str]):
    """Показати статистику файлів."""
    print("\n📊 СТАТИСТИКА")
    print("=" * 70)
    
    # Базова статистика
    ref_total = len(ref_lines)
    dev_total = len(dev_lines)
    
    ref_code = sum(1 for line in ref_lines if line.strip() and not line.strip().startswith('#'))
    dev_code = sum(1 for line in dev_lines if line.strip() and not line.strip().startswith('#'))
    
    ref_comments = sum(1 for line in ref_lines if line.strip().startswith('#'))
    dev_comments = sum(1 for line in dev_lines if line.strip().startswith('#'))
    
    ref_empty = sum(1 for line in ref_lines if not line.strip())
    dev_empty = sum(1 for line in dev_lines if not line.strip())
    
    print(f"📏 Рядки:")
    print(f"   Еталон: {ref_total} загалом ({ref_code} код, {ref_comments} коментарі, {ref_empty} пусті)")
    print(f"   Розробка: {dev_total} загалом ({dev_code} код, {dev_comments} коментарі, {dev_empty} пусті)")
    
    # Відсоток готовності
    if ref_code > 0:
        completeness = (dev_code / ref_code) * 100
        print(f"\n📈 Готовність коду: {completeness:.1f}%")
        
        if completeness < 50:
            print("🔴 Потребує значної роботи")
        elif completeness < 80:
            print("🟡 Частково готово")
        else:
            print("🟢 Майже готово")

def main():
    parser = argparse.ArgumentParser(description='Порівняння файлів з еталоном')
    parser.add_argument('filename', help='Ім\'я файлу для порівняння (field.py, contact.py)')
    parser.add_argument('--side-by-side', '-s', action='store_true', 
                       help='Показати side-by-side порівняння')
    parser.add_argument('--analysis', '-a', action='store_true',
                       help='Показати структурний аналіз')
    
    args = parser.parse_args()
    
    ref_path, dev_path = get_file_paths(args.filename)
    
    print(f"🔍 ПОРІВНЯННЯ ФАЙЛУ: {args.filename}")
    print("=" * 70)
    print(f"Еталон: {ref_path}")
    print(f"Розробка: {dev_path}")
    
    # Читання файлів
    ref_lines = read_file_safely(ref_path)
    dev_lines = read_file_safely(dev_path)
    
    # Показати відповідний тип порівняння
    if args.side_by_side:
        show_side_by_side_diff(ref_lines, dev_lines, ref_path, dev_path)
    else:
        show_unified_diff(ref_lines, dev_lines, ref_path, dev_path)
    
    # Додатковий аналіз
    if args.analysis or args.side_by_side:
        analyze_structure_diff(ref_lines, dev_lines)
        show_statistics(ref_lines, dev_lines)

if __name__ == "__main__":
    main()