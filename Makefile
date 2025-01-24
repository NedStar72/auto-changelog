# Название виртуального окружения
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
REQUIREMENTS = requirements.txt

# Команда по умолчанию
.DEFAULT_GOAL := help

# Проверка на существование виртуального окружения
$(VENV)/bin/activate: 
	@echo "Создаём виртуальное окружение..."
	@python -m venv $(VENV)

# Правила
.PHONY: help venv install run clean

## Вывести список доступных команд
help:
	@echo "Доступные команды:"
	@echo "  make venv       - Создать виртуальное окружение (если отсутствует)"
	@echo "  make install    - Установить зависимости"
	@echo "  make freeze     - Обновить requirements.txt
	@echo "  make run        - Запустить main.py"
	@echo "  make test       - Запустить юнит-тесты"
	@echo "  make clean      - Удалить виртуальное окружение и временные файлы"

## Создать виртуальное окружение (если отсутствует)
venv: $(VENV)/bin/activate

## Установить или обновить зависимости
install: venv
	@$(PIP) freeze > .installed.txt || touch .installed.txt
	@diff --suppress-common-lines -y $(REQUIREMENTS) .installed.txt > /dev/null || ( \
		echo "Устанавливаем зависимости..."; \
		$(PIP) install -r $(REQUIREMENTS); \
	)
	@rm -f .installed.txt

## Обновить requirements.txt
freeze: install
	@$(PIP) freeze > $(REQUIREMENTS); \
	echo "Зависимости сохранены в $(REQUIREMENTS)."

## Запустить main.py
run: install
	@$(PYTHON) main.py

## Запустить юнит-тесты
test: install
	@pytest -s src/

## Удалить виртуальное окружение и временные файлы
clean:
	rm -rf $(VENV) __pycache__ *.pyc *.pyo
	@echo "Очистка завершена."
