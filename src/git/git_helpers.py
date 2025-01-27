import re
from typing import Optional
from git import Commit


def is_merge_commit(commit: Commit) -> bool:
    """
    Проверяет, является ли указанный коммит merge-коммитом.

    Args:
        commit (Commit): Объект коммита из библиотеки `git`.

    Returns:
        bool: True, если коммит является merge-коммитом (имеет более одного родителя), иначе False.
    """
    return len(commit.parents) > 1


def extract_target_branch_name(merge_commit_message: str) -> Optional[str]:
    """
    Извлекает имя целевой ветки из сообщения merge-коммита.

    Args:
        merge_commit_message (str): Текст сообщения merge-коммита.

    Returns:
        Optional[str]: Имя целевой ветки, если оно найдено, иначе None.
    """
    pattern = r"^Merge branch .* into ([\w\-.\/]+)$"
    match = re.search(pattern, merge_commit_message)
    return match.group(1) if match else None


def extract_source_branch_name(merge_commit_message: str) -> Optional[str]:
    """
    Извлекает имя исходной ветки из сообщения merge-коммита.

    Args:
        merge_commit_message (str): Текст сообщения merge-коммита.

    Returns:
        Optional[str]: Имя исходной ветки, если оно найдено, иначе None.
    """
    pattern = r"^Merge branch '([\w\-.\/]+)' into"
    match = re.search(pattern, merge_commit_message)
    return match.group(1) if match else None


def extract_issue_id_from_branch_name(branch_name: str, project_id: str) -> Optional[str]:
    """
    Извлекает идентификатор задачи из имени ветки.

    Args:
        branch_name (str): Имя ветки, из которой извлекается идентификатор задачи.
        project_id (str): Префикс проекта (например, 'PROJECT'), используемый для идентификации задачи.

    Returns:
        Optional[str]: Идентификатор задачи в формате '{project_id}-<число>', если он найден, иначе None.
    """
    pattern = rf"{project_id}-\d+"
    match = re.search(pattern, branch_name)
    return match.group(0) if match else None

def extract_issue_id_from_commit_message(commit_message: str, project_id: str) -> Optional[str]:
    """
    Извлекает идентификатор задачи из сообщения.

    Args:
        commit_message (str): Сообщение коммита, из которого извлекается идентификатор задачи.
        project_id (str): Префикс проекта (например, 'PROJECT'), используемый для идентификации задачи.

    Returns:
        Optional[str]: Идентификатор задачи в формате '{project_id}-<число>', если он найден, иначе None.
    """
    pattern = rf"{project_id}-\d+"
    match = re.search(pattern, commit_message)
    return match.group(0) if match else None
