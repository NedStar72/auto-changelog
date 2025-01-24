from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Issue:
    id: str
    title: str
    state: Optional[str]


def convert_to_issue(data: Dict[str, Any]) -> Issue:
    """Преобразует данные задачи из формата YouTrack в объект Issue.

    Аргументы:
        data (Dict[str, Any]): Словарь с данными задачи из YouTrack.

    Возвращает:
        Issue: Объект задачи.
    """
    state = next(
        (
            field.get("value", {}).get("name")
            for field in data.get("customFields", [])
            if field.get("name") == "State"
        ),
        None
    )

    return Issue(
        id=data["idReadable"],
        title=data["summary"], # Решил, что title очевиднее summary
        state=state
    )
