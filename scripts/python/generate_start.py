import os

print("Генерация скрипта запуска...")
WORKDIR = os.path.abspath(os.path.join(".", os.pardir))

try:
    if not os.path.isdir("./generated"):
        os.mkdir("./generated")
    with open('./templates/start.bat') as f:
        start_template = f.read()
        start_bat = start_template.replace("{$WORK_PATH}", WORKDIR)
    with open('./generated/start.bat', 'w') as f:
        f.write(start_bat)
    print("Успешно сгенерирован скрипта запуска")

except Exception as e:
    print("Ошибка: ", e)
