import pytest
from .git_helpers import (
    is_merge_commit,
    extract_target_branch_name,
    extract_source_branch_name,
    extract_issue_id,
)


class MockCommit:
    """Простой мок для объекта Commit."""
    def __init__(self, parents):
        self.parents = parents


# Тесты для is_merge_commit
def test_is_merge_commit_with_merge():
    """Проверяет, что is_merge_commit возвращает True для merge-коммита."""
    merge_commit = MockCommit(parents=[object(), object()])  # Два родителя
    assert is_merge_commit(merge_commit) is True


def test_is_merge_commit_with_regular():
    """Проверяет, что is_merge_commit возвращает False для обычного коммита."""
    regular_commit = MockCommit(parents=[object()])  # Один родитель
    assert is_merge_commit(regular_commit) is False


def test_is_merge_commit_with_no_parents():
    """Проверяет, что is_merge_commit возвращает False для коммита без родителей."""
    no_parents_commit = MockCommit(parents=[])  # Нуль родителей
    assert is_merge_commit(no_parents_commit) is False


# Тесты для extract_target_branch_name
@pytest.mark.parametrize(
    "message, expected_branch",
    [
        ("Some random message", None),
        ("Some random message with 'into master'", None),
        ("Merge branch 'release' into ", None),
        ("Merge branch 'master' into some-feature", "some-feature"),
        ("Merge branch 'master' into release/v1.0.0", "release/v1.0.0"),
        ("Merge branch 'master' into feature/PROJ-123", "feature/PROJ-123"),
        ("Merge branch 'master' into feature/PROJ-123-some-feature", "feature/PROJ-123-some-feature"),
        ("Merge branch 'master' into release/v1.0.0/feature/PROJ-123", "release/v1.0.0/feature/PROJ-123"),
        ("Merge branch 'master' into release/v1.0.0/feature/PROJ-123-some-feature", "release/v1.0.0/feature/PROJ-123-some-feature"),
    ]
)
def test_extract_target_branch_name(message, expected_branch):
    """Проверяет, что извлечение имени целевой ветки из сообщения коммита работает корректно."""
    assert extract_target_branch_name(message) == expected_branch


# Тесты для extract_source_branch_name
@pytest.mark.parametrize(
    "message, expected_branch",
    [
        ("Some random message", None),
        ("Some random message with 'Merge branch 'some-feature' into master'", None),
        ("Merge branch '' into master", None),
        ("Merge branch 'some-feature' into master", "some-feature"),
        ("Merge branch 'release/v1.0.0' into master", "release/v1.0.0"),
        ("Merge branch 'feature/PROJ-123' into master", "feature/PROJ-123"),
        ("Merge branch 'feature/PROJ-123-some-feature' into master", "feature/PROJ-123-some-feature"),
        ("Merge branch 'release/v1.0.0/feature/PROJ-789' into master", "release/v1.0.0/feature/PROJ-789"),
        ("Merge branch 'release/v1.0.0/feature/PROJ-789-new-feature' into master", "release/v1.0.0/feature/PROJ-789-new-feature"),
    ]
)
def test_extract_source_branch_name(message, expected_branch):
    """Проверяет, что извлечение имени исходной ветки из сообщения коммита работает корректно."""
    assert extract_source_branch_name(message) == expected_branch


# Тесты для extract_issue_id
@pytest.mark.parametrize(
    "branch_name, project_id, expected_issue_id",
    [
        ("", "PROJ", None),
        ("release/v1.0.0", "PROJ", None),
        ("feature/PROJ-123", "TEST", None),
        ("feature/PROJ-123", "PROJ", "PROJ-123"),
        ("feature/PROJ-123-some-feature", "PROJ", "PROJ-123"),
        ("release/v1.0.0/feature/PROJ-123", "PROJ", "PROJ-123"),
        ("release/v1.0.0/bugfix/PROJ-123-fix-something", "PROJ", "PROJ-123"),
    ]
)
def test_extract_issue_id(branch_name, project_id, expected_issue_id):
    """Проверяет, что извлечение ID задачи из имени ветки работает корректно."""
    assert extract_issue_id(branch_name, project_id) == expected_issue_id
