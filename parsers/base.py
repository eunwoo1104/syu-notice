from abc import ABC
from typing import TypedDict
from bs4 import BeautifulSoup

from aiohttp import ClientSession


class URLNotProvided(Exception):
    """URL이 입력되지 않았습니다. 대체 뭘 파싱하라는거죠.."""

    def __init__(self):
        super().__init__("Please provide URL! This is code-level error and should be fixed by parser's contributor.")


class RequestError(Exception):
    """공지를 가져오는데 문제가 있습니다. 나중에 다시 시도해주세요."""

    def __init__(self, status: int, body: str):
        super().__init__(f"Problem with request: {status} | {body}")


class Notice(TypedDict):
    name: str
    url: str
    author: str
    date: str


class BaseParser(ABC):
    URL: str = None
    NAME: str = None

    def __init__(self, session: ClientSession):
        self.session: ClientSession = session
        if not self.NAME:
            self.NAME = "알 수 없음"

    async def request(self) -> str:
        if not self.URL:
            raise URLNotProvided
        async with self.session.get(self.URL) as resp:
            if not 200 <= resp.status < 300:
                raise RequestError(resp.status, await resp.text())
            return await resp.text()

    def parse(self, body: str) -> list[Notice]:
        ret = []
        soup = BeautifulSoup(body, "html.parser")

        notice_box = soup.find("table", class_="md_notice_tbl").find("tbody")
        notice_titles = notice_box.find_all("tr")

        for notice in notice_titles:
            url = notice.find("td", class_="step2").find("a")
            title = notice.find("span", class_="tit")
            author = notice.find("td", class_="step3")
            date = notice.find("td", class_="step4")
            ret.append({"name": title.string, "url": url.attrs["href"], "author": author.string, "date": date.string})

        return ret

    async def get_notices(self) -> list[Notice]:
        body = await self.request()
        return self.parse(body)
