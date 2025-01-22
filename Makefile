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
	@echo "  make install    - Установить или обновить зависимости"
	@echo "  make run        - Запустить main.py"
	@echo "  make add <libs> - Установить зависимости и обновить requirements.txt"
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

## Запустить main.py
run: install
	@$(PYTHON) main.py

## Добавить одну или несколько зависимостей и обновить requirements.txt
add: install
	@DEPENDENCIES=$(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS)); \
	if [ -z "$$DEPENDENCIES" ]; then \
		echo "Ошибка: Не указаны зависимости."; \
		exit 1; \
	fi; \
	echo "Устанавливаем зависимости: $$DEPENDENCIES..."; \
	$(PIP) install $$DEPENDENCIES; \
	$(PIP) freeze > $(REQUIREMENTS); \
	echo "Зависимости $$DEPENDENCIES добавлены в $(REQUIREMENTS)."

## Удалить виртуальное окружение и временные файлы
clean:
	rm -rf $(VENV) __pycache__ *.pyc *.pyo
	@echo "Очистка завершена."

## Паттерн для обработки всех других целей
%:
	@:
