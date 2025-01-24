import os
import shutil
from git import Repo
from .git_client import GitClient


def test_get_issue_id_list_between_parent_and_child_branches():
    """
    Проверяем формирование списка задач между родительской и дочерней ветками.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Работаем с фича-веткой
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")

        # Сливаем фича-ветку в релиз
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0) Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\
    # | * (feature/TEST-1) TEST-1 message 1
    # |/
    # * (master, tag: v1.0.0) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.commit("master").hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST")
        expected_issues = ["TEST-1"]
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_between_ahead_parent_and_child_branches():
    """
    Проверяем формирование списка задач между ушедшей вперед родительской и дочерней ветками.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Работаем с фича-веткой
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")

        # Сливаем фича-ветку в релиз
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        # Сливаем другую фича-ветку напрямую в мастер
        repo.git.checkout("master")
        repo.git.checkout("-b", "feature/TEST-2")
        repo.index.commit("TEST-2 message 1")
        repo.git.checkout("master")
        repo.git.merge("feature/TEST-2", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> master) Merge branch 'feature/TEST-2'
    # |\  
    # | | * (release/v1.1.0) Merge branch 'feature/TEST-1' into release/v1.1.0
    # | |/| 
    # |/| | 
    # | * | (feature/TEST-2) TEST-2 message 1
    # |/ /  
    # | * (feature/TEST-1) TEST-1 message 1
    # |/  
    # * (tag: v1.0.0) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.commit("master").hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST")
        expected_issues = ["TEST-1"]
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_after_merging_two_branches():
    """
    Проверяем формирование списка задач после слияния двух дочерних веток в родительскую.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Создаем и работаем с фича-ветками
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")
        repo.git.checkout("release/v1.1.0")
        repo.git.checkout("-b", "feature/TEST-2")
        repo.index.commit("TEST-2 message 1")
        repo.git.checkout("feature/TEST-1")
        repo.index.commit("TEST-1 message 2")
        repo.git.checkout("feature/TEST-2")
        repo.index.commit("TEST-2 message 2")

        # Сливаем фича-ветки в релиз
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")
        repo.git.merge("feature/TEST-2", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0) Merge branch 'feature/TEST-2' into release/v1.1.0
    # |\  
    # * \ Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\ \  
    # | | * (feature/TEST-2) TEST-2 message 2
    # | * | (feature/TEST-1) TEST-1 message 2
    # | | * TEST-2 message 1
    # | |/  
    # |/|   
    # | * TEST-1 message 1
    # |/  
    # * (tag: v1.0.0, master) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.commit("master").hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST")
        expected_issues = ["TEST-1", "TEST-2"]
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_in_same_commit():
    """
    Проверяем формирование списка задач между одним и тем же коммитом.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Работаем с фича-веткой
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")

        # Сливаем фича-ветку в релиз
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0) Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\
    # | * (feature/TEST-1) TEST-1 message 1
    # |/
    # * (master, tag: v1.0.0) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.commit("release/v1.1.0").hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST")
        expected_issues = []
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_between_merge_commits_in_same_branch():
    """
    Проверяем формирование списка задач на ветке между двумя мерж-коммитами.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Работаем с первой фича-веткой
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        # Создаем тег 'v1.1.0-last-build'
        repo.create_tag("v1.1.0-last-build")

        # Работаем со второй фича-веткой
        repo.git.checkout("-b", "feature/TEST-2")
        repo.index.commit("TEST-2 message 1")
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-2", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0) Merge branch 'feature/TEST-2' into release/v1.1.0
    # |\  
    # | * (feature/TEST-2) TEST-2 message 1
    # |/  
    # * (tag: v1.1.0-last-build) Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\  
    # | * (feature/TEST-1) TEST-1 message 1
    # |/  
    # * (tag: v1.0.0, master) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.tag("v1.1.0-last-build").commit.hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST")
        expected_issues = ["TEST-2"]
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_between_merge_commits_in_same_branch_reversed():
    """
    Проверяем формирование списка задач на ветке между двумя мерж-коммитами в обратном порядке.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Работаем с первой фича-веткой
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        # Создаем тег 'outdated-commit'
        repo.create_tag("outdated-commit")

        # Работаем со второй фича-веткой
        repo.git.checkout("-b", "feature/TEST-2")
        repo.index.commit("TEST-2 message 1")
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-2", "--no-ff")

        # Создаем тег 'v1.1.0-last-build'
        repo.create_tag("v1.1.0-last-build")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0, tag: v1.1.0-last-build) Merge branch 'feature/TEST-2' into release/v1.1.0
    # |\  
    # | * (feature/TEST-2) TEST-2 message 1
    # |/  
    # * (tag: outdated-commit) Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\  
    # | * (feature/TEST-1) TEST-1 message 1
    # |/  
    # * (tag: v1.0.0, master) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.tag("v1.1.0-last-build").commit.hexsha
        commit_to = repo.tag("outdated-commit").commit.hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST")
        expected_issues = []
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_with_nested_merge_commits():
    """
    Проверяем формирование списка задач с вложенными мерж-коммитами.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Создаем и работаем с фича-ветками
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")
        repo.git.checkout("-b", "feature/TEST-2")
        repo.index.commit("TEST-2 message 1")
        repo.git.checkout("feature/TEST-1")
        repo.git.merge("feature/TEST-2", "--no-ff")
        repo.index.commit("TEST-1 message 2")

        # Сливаем фича-ветку в релиз
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0) Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\  
    # | * (feature/TEST-1) TEST-1 message 2
    # | * Merge branch 'feature/TEST-2' into feature/TEST-1
    # | |\  
    # | | * (feature/TEST-2) TEST-2 message 1
    # | |/  
    # | * TEST-1 message 1
    # |/  
    # * (tag: v1.0.0, master) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.commit("master").hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST")
        expected_issues = ["TEST-2", "TEST-1"]
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_after_merge_external_branch():
    """
    Проверяем формирование списка задач после влития внешней ветки.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Сливаем feature/TEST-1 в релизную ветку
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        # Создаем тег 'v1.1.0-last-build'
        repo.create_tag("v1.1.0-last-build")

        # Вносим изменения в мастер
        repo.git.checkout("master")
        repo.git.checkout("-b", "feature/TEST-3")
        repo.index.commit("TEST-3 message 1")
        repo.git.checkout("master")
        repo.git.merge("feature/TEST-3", "--no-ff")

        # Подливаем мастер в релизную ветку
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("master", "--no-ff")

        # Сливаем feature/TEST-2 в релизную ветку
        repo.git.checkout("-b", "feature/TEST-2")
        repo.index.commit("TEST-2 message 1")
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-2", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0) Merge branch 'feature/TEST-2' into release/v1.1.0
    # |\  
    # | * (feature/TEST-2) TEST-2 message 1
    # |/  
    # * Merge branch 'master' into release/v1.1.0
    # |\  
    # * \ (tag: v1.1.0-last-build) Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\ \  
    # | | * (master) Merge branch 'feature/TEST-3'
    # | |/| 
    # |/| | 
    # | * | (feature/TEST-1) TEST-1 message 1
    # |/ /  
    # | * (feature/TEST-3) TEST-3 message 1
    # |/  
    # * (tag: v1.0.0) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.tag("v1.1.0-last-build").commit.hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST", target_branch="release/v1.1.0")
        expected_issues = ["TEST-2"]
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)


def test_get_issue_id_list_with_nested_merge_commits_and_specified_target_branch():
    """
    Проверяем формирование списка задач с вложенными мерж-коммитами и указанной целевой веткой.
    """

    def create_test_repo(repo_dir: str):
        # Удаляем старый репозиторий, если он существует
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)

        repo = Repo.init(repo_dir)
        repo.git.branch("-m", "main", "master") # Переименовываем ветку main в master
        repo.index.commit("Initial commit") # Создаем коммит 'Initial commit'
        repo.create_tag("v1.0.0") # Создаем тег 'v1.0.0'
        repo.git.checkout("-b", "release/v1.1.0") # Создаем релизную ветку

        # Создаем и работаем с фича-ветками
        repo.git.checkout("-b", "feature/TEST-1")
        repo.index.commit("TEST-1 message 1")
        repo.git.checkout("-b", "feature/TEST-2")
        repo.index.commit("TEST-2 message 1")
        repo.git.checkout("feature/TEST-1")
        repo.git.merge("feature/TEST-2", "--no-ff")
        repo.index.commit("TEST-1 message 2")

        # Сливаем фича-ветку в релиз
        repo.git.checkout("release/v1.1.0")
        repo.git.merge("feature/TEST-1", "--no-ff")

        return repo

    # Визуализация графа репозитория:
    #
    # * (HEAD -> release/v1.1.0) Merge branch 'feature/TEST-1' into release/v1.1.0
    # |\  
    # | * (feature/TEST-1) TEST-1 message 2
    # | * Merge branch 'feature/TEST-2' into feature/TEST-1
    # | |\  
    # | | * (feature/TEST-2) TEST-2 message 1
    # | |/  
    # | * TEST-1 message 1
    # |/  
    # * (tag: v1.0.0, master) Initial commit

    try:
        # Создаем тестовый репозиторий
        repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_repo")
        repo = create_test_repo(repo_dir)
        client = GitClient(repo_dir)

        commit_from = repo.commit("master").hexsha
        commit_to = repo.commit("release/v1.1.0").hexsha

        issues = client.get_issue_id_list(commit_from, commit_to, project_id="TEST", target_branch="release/v1.1.0")
        expected_issues = ["TEST-1"]
        assert issues == expected_issues
    finally:
        # Удаляем репозиторий после теста
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)
