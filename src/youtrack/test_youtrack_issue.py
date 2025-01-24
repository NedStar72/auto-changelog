import pytest
from .youtrack_issue import Issue, convert_to_issue


def test_convert_to_issue_full_data():
    data = {
        "idReadable": "TMOB-123",
        "summary": "Исправить баг с модулем",
        "customFields": [
            {
                "name": "State",
                "value": {"name": "Open"}
            }
        ]
    }

    expected = Issue(
        id="TMOB-123",
        title="Исправить баг с модулем",
        state="Open"
    )

    result = convert_to_issue(data)
    assert result == expected


def test_convert_to_issue_no_state():
    data = {
        "idReadable": "TMOB-123",
        "summary": "Добавить новый функционал",
        "customFields": []
    }

    expected = Issue(
        id="TMOB-123",
        title="Добавить новый функционал",
        state=None
    )

    result = convert_to_issue(data)
    assert result == expected


def test_convert_to_issue_missing_custom_fields():
    data = {
        "idReadable": "TMOB-123",
        "summary": "Обновить документацию"
        # customFields отсутствует
    }

    expected = Issue(
        id="TMOB-123",
        title="Обновить документацию",
        state=None
    )

    result = convert_to_issue(data)
    assert result == expected


def test_convert_to_issue_missing_summary():
    data = {
        "idReadable": "TMOB-123",
        "customFields": []
    }

    with pytest.raises(KeyError):
        convert_to_issue(data)


def test_convert_to_issue_missing_id():
    data = {
        "summary": "Протестировать исключение",
        "customFields": []
    }

    with pytest.raises(KeyError):
        convert_to_issue(data)
