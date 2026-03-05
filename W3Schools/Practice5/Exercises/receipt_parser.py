import re
import json

def parse_receipt_simple(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    #1
    prices = re.findall(r'(\d+[.,]\d{2})', text)
    print(f"Все цены: {prices}")
    
    #2
    product_lines = re.findall(r'\d+\.\s*(.+)', text)
    print(f"Названия товаров: {product_lines}")
    
    #3
    total = re.search(r'ИТОГО:\s*([\d\s,]+)', text)
    if total:
        total_sum = total.group(1).replace(' ', '').replace(',', '.')
        print(f"Общая сумма: {total_sum}")
    
    #4
    date_time = re.search(r'Время:\s*(.+)', text)
    if date_time:
        print(f"Дата и время: {date_time.group(1)}")
    
    #5
    payment_match = re.search(r'(Банковская карта|Наличные)', text)
    if payment_match:
        payment = payment_match.group(1)
    else:
        payment = "Не найдено"
    print(f"Метод оплаты: {payment}")
    
    #6
    result = {
        "магазин": "EUROPHARMA Астана",
        "дата": date_time.group(1) if date_time else "не найдено",
        "товары": product_lines,
        "цены": prices[:len(product_lines)*2:2],
        "итого": total_sum if total else "не найдено",
        "оплата": payment
    }
    
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТ (JSON):")
    print("="*50)
    print(json.dumps(result, ensure_ascii=False, indent=2))

parse_receipt_simple(r"C:\Users\dania\PP2_Practice\W3Schools\Practice5\Exercises\raw.txt")