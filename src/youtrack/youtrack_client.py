import aiohttp
from .youtrack_issue import Issue, convert_to_issue
from typing import List


class YouTrackClient:
    def __init__(self, base_url: str, token: str):
        """Инициализирует YouTrackClient.

        Аргументы:
            base_url (str): Базовый URL экземпляра YouTrack.
            token (str): Токен авторизации для доступа к API.
        """
        self.base_url = base_url.rstrip('/')
        self.token = token

    async def get_issues(self, issue_ids: List[str]) -> List[Issue]:
        """Получает детали нескольких задач из YouTrack в одном запросе.

        Аргументы:
            issue_ids (List[str]): Список ID задач для получения данных (например, ['TMOB-123', 'TMOB-1234']).

        Возвращает:
            List[Issue]: Список объектов Issue, содержащих ID задач, заголовки и состояния.

        Исключения:
            aiohttp.ClientResponseError: Если HTTP-запрос завершился с ошибкой.
        """
        url = f"{self.base_url}/api/issues"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        params = {
            "fields": "idReadable,summary,customFields(name,value(name))",
            "query": " OR ".join([f"issue id: {issue_id}" for issue_id in issue_ids])
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                data = await response.json()

        return [convert_to_issue(item) for item in data]
