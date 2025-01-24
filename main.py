import os
import asyncio
from src import YouTrackClient


async def main(youtrack_token: str):
    client = YouTrackClient("https://yt.skbkontur.ru", youtrack_token)
    issues = await client.get_issues(["TMOB-166", "TMOB-167"])
    for issue in issues:
        print(f"ID: {issue.id}, Title: {issue.title}, State: {issue.state}")


if __name__ == "__main__":
    YOUTRACK_TOKEN = os.getenv("YOUTRACK_TOKEN")

    if not YOUTRACK_TOKEN:
        raise EnvironmentError("Переменная окружения YOUTRACK_TOKEN не установлена.")
    
    asyncio.run(main(YOUTRACK_TOKEN))
