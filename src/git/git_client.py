from collections import OrderedDict
from git import Repo, Commit
from .git_helpers import (
    is_merge_commit,
    extract_target_branch_name,
    extract_source_branch_name,
    extract_issue_id_from_branch_name,
    extract_issue_id_from_commit_message,
)
from typing import List, Optional


class GitClient:
    """
    Клиент для работы с локальным Git-репозиторием.
    """

    def __init__(self, repo_path: str):
        """
        Инициализирует GitClient для указанного пути репозитория.

        Args:
            repo_path (str): Путь к локальному Git-репозиторию.
        """
        self.repo = Repo(repo_path)

    def __get_commits_from_range(self, commit_from: str, commit_to: str) -> List[Commit]:
        """
        Возвращает список коммитов в указанном диапазоне.

        Args:
            commit_from (str): Хеш или имя начального коммита.
            commit_to (str): Хеш или имя конечного коммита.

        Returns:
            List[Commit]: Список коммитов в порядке от старого к новому.
        """
        commits = list(self.repo.iter_commits(f"{commit_from}..{commit_to}"))
        return list(reversed(commits))  # Возвращает коммиты в порядке возрастания по дате.

    def get_issue_id_list_from_merge_commits(
        self, commit_from: str, commit_to: str, project_id: str, target_branch: Optional[str] = None
    ) -> List[str]:
        """
        Возвращает список идентификаторов задач (issue ID) из мерж-коммитов в указанном диапазоне.

        Args:
            commit_from (str): Хеш или имя начального коммита.
            commit_to (str): Хеш или имя конечного коммита.
            project_id (str): Префикс проекта для идентификации задач (например, 'PROJECT').
            target_branch (Optional[str], optional): Имя целевой ветки для фильтрации merge-коммитов.
                Если None, фильтрация по ветке не выполняется.

        Returns:
            List[str]: Список идентификаторов задач, связанных с мерж-коммитами в указанном диапазоне.
        """
        commits = self.__get_commits_from_range(commit_from, commit_to)
        issue_ids = OrderedDict()

        for commit in commits:
            if not is_merge_commit(commit):
                continue

            merge_commit_target_branch = extract_target_branch_name(commit.message)
            if target_branch is not None and target_branch != merge_commit_target_branch:
                continue

            merge_commit_source_branch = extract_source_branch_name(commit.message)
            if not merge_commit_source_branch:
                continue

            issue_id = extract_issue_id_from_branch_name(merge_commit_source_branch, project_id)
            if issue_id:
                issue_ids[issue_id] = None

        return list(issue_ids.keys())

    def get_issue_id_list_from_commit_messages(
        self, commit_from: str, commit_to: str, project_id: str, target_branch: Optional[str] = None
    ) -> List[str]:
        """
        Возвращает список идентификаторов задач (issue ID) из сообщений коммитов в указанном диапазоне.

        Args:
            commit_from (str): Хеш или имя начального коммита.
            commit_to (str): Хеш или имя конечного коммита.
            project_id (str): Префикс проекта для идентификации задач (например, 'PROJECT').

        Returns:
            List[str]: Список идентификаторов задач, найденных в сообщениях коммитов в указанном диапазоне.
        """
        commits = self.__get_commits_from_range(commit_from, commit_to)
        issue_ids = OrderedDict()

        for commit in commits:
            if is_merge_commit(commit):
                continue

            issue_id = extract_issue_id_from_commit_message(commit.message, project_id)
            if issue_id:
                issue_ids[issue_id] = None

        return list(issue_ids.keys())
