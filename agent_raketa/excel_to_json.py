import pandas as pd
import json

def excel_to_json(excel_file_path, json_file_path):
    try:
        df = pd.read_excel(excel_file_path)
        required_columns = ["Nomenclature", "GroupModificator", "Modificator"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"В Эксель остутсвует колонка: {col}")

        df = df.replace("<NULL>", None)
        grouped = df.groupby("Nomenclature")
        result = []
        for dish_name, dish_data in grouped:
            dish = {
                "name": dish_name,
                "modifiers": []
            }

            modifier_groups = dish_data.groupby("GroupModificator")
            for modifier_type, modifier_data in modifier_groups:
                modifier_options = modifier_data["Modificator"].dropna().tolist()
                if modifier_options:
                    modifier = {
                        "type": modifier_type,
                        "options": modifier_options
                    }
                    dish["modifiers"].append(modifier)
            result.append(dish)

        with open(json_file_path, 'w', encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"JSON файл успешно создан: {json_file_path}")
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {excel_file_path}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

excel_file = "C:/Users/neste/opt/test_gigachain/agent_raketa/menu1.xlsx"  # Замените на путь к вашему Excel файлу
json_file = "agent_raketa/output.json"  # Замените на желаемый путь для JSON файла
excel_to_json(excel_file, json_file)