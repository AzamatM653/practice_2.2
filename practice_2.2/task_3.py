import requests
import json
import os


SAVE_FILE = "save.json"


def load_currency_data():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        data = response.json()
        return data['Valute']
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return None


def display_all_currencies(currencies):
    if not currencies:
        print("Нет данных для отображения.")
        return

    print("\n" + "=" * 80)
    print(f"{'Код':<6} {'Кол-во':<8} {'Название':<40} {'Курс (руб)':<15}")
    print("=" * 80)

    for code, info in currencies.items():
        name = info['Name']
        nominal = info['Nominal']
        value = info['Value']
        print(f"{code:<6} {nominal:<8} {name:<40} {value:<15.4f}")
    print("=" * 80)


def display_single_currency(currencies):
    code = input("Введите код валюты (например, USD, EUR): ").upper()
    if code in currencies:
        info = currencies[code]
        print(f"\n--- {info['Name']} ({code}) ---")
        print(f"{info['Nominal']} ед. = {info['Value']} руб.")
        print(f"Предыдущий курс: {info['Previous']} руб.")
    else:
        print(f"Валюта с кодом {code} не найдена.")


def load_groups():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_groups(groups):
    with open(SAVE_FILE, 'w') as f:
        json.dump(groups, f)


def create_group(groups, currencies):
    group_name = input("Введите название новой группы: ").strip()
    if not group_name:
        print("Название не может быть пустым.")
        return

    if group_name in groups:
        print(f"Группа '{group_name}' уже существует.")
        return

    groups[group_name] = []
    print(f"Группа '{group_name}' создана. Теперь добавьте в неё валюты.")
    add_to_group(groups, currencies, group_name)


def add_to_group(groups, currencies, group_name=None):
    if not group_name:
        view_groups(groups)
        group_name = input("Введите название группы для добавления: ").strip()

    if group_name not in groups:
        print(f"Группа '{group_name}' не найдена.")
        return

    code = input("Введите код валюты для добавления (например, USD): ").upper()
    if code not in currencies:
        print(f"Валюта {code} не найдена.")
        return

    if code in groups[group_name]:
        print(f"Валюта {code} уже есть в группе.")
    else:
        groups[group_name].append(code)
        print(f"Валюта {code} добавлена в группу '{group_name}'.")
        save_groups(groups)


def remove_from_group(groups, currencies):
    view_groups(groups)
    group_name = input("Введите название группы для удаления валюты: ").strip()

    if group_name not in groups:
        print(f"Группа '{group_name}' не найдена.")
        return

    if not groups[group_name]:
        print("В этой группе нет валют.")
        return

    print(f"Валюты в группе '{group_name}': {', '.join(groups[group_name])}")
    code = input("Введите код валюты для удаления: ").upper()

    if code in groups[group_name]:
        groups[group_name].remove(code)
        print(f"Валюта {code} удалена из группы '{group_name}'.")
        save_groups(groups)
    else:
        print(f"Валюты {code} нет в группе.")


def view_groups(groups):
    if not groups:
        print("Нет созданных групп.")
        return

    print("\n--- Список групп ---")
    for name, currencies in groups.items():
        print(f" {name}: {', '.join(currencies) if currencies else 'пусто'}")
    print("-" * 30)


def view_group_currencies(groups, currencies):
    view_groups(groups)
    group_name = input("Введите название группы для просмотра: ").strip()

    if group_name not in groups:
        print(f"Группа '{group_name}' не найдена.")
        return

    if not groups[group_name]:
        print(f"В группе '{group_name}' нет валют.")
        return

    print(f"\n--- Курсы валют группы '{group_name}' ---")
    for code in groups[group_name]:
        if code in currencies:
            info = currencies[code]
            print(f"{code}: {info['Nominal']} {info['Name']} = {info['Value']} руб.")
        else:
            print(f"{code}: данные не найдены (возможно, устаревший код)")


def main():
    groups = load_groups()

    while True:
        print("\n" + "=" * 50)
        print("Главное меню")
        print("=" * 50)
        print("1. Показать курсы всех валют")
        print("2. Найти валюту по коду")
        print("3. Создать группу валют")
        print("4. Показать все группы")
        print("5. Добавить валюту в группу")
        print("6. Удалить валюту из группы")
        print("7. Показать курсы валют группы")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice != '0':
            currencies = load_currency_data()
            if not currencies:
                print("Не удалось загрузить данные. Проверьте подключение к интернету.")
                continue

        if choice == '1':
            display_all_currencies(currencies)
        elif choice == '2':
            display_single_currency(currencies)
        elif choice == '3':
            create_group(groups, currencies)
        elif choice == '4':
            view_groups(groups)
        elif choice == '5':
            add_to_group(groups, currencies)
        elif choice == '6':
            remove_from_group(groups, currencies)
        elif choice == '7':
            view_group_currencies(groups, currencies)
        elif choice == '0':
            print("Программа завершена.")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 0 до 7.")

if __name__ == "__main__":
    main()