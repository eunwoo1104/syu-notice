from asyncio import AbstractEventLoop, sleep
import logging
from io import StringIO
from traceback import format_exc

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, text
from aiosqlite import connect, Connection, Row
from aiohttp import ClientSession
from discord import Webhook, Embed, File

from config import Config
from parsers import available_parsers, BaseParser, RequestError, URLNotProvided, Notice

logger = logging.getLogger('syu')
logging.basicConfig(level=logging.INFO)  # DEBUG/INFO/WARNING/ERROR/CRITICAL
handler = logging.FileHandler(filename=f'syu.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

app = Sanic(__name__)
loaded_parsers: dict[str, BaseParser] = {}
db: Connection
parser_session: ClientSession
webhook_session: ClientSession
LOGO_URL = "https://eunwoo.dev/asset/로고(+한글명).png"
error_webhook: Webhook


async def publish_to_discord(notices: list[Notice], parser_id):
    tgt = await db.execute_fetchall("""SELECT webhook, mention FROM discord_sub WHERE sub LIKE ?""", (f"%{parser_id}%",))
    for webhook_url, mention in map(lambda x: (x["webhook"], x["mention"]), tgt):
        webhook = Webhook.from_url(webhook_url, session=webhook_session)
        buf = []
        for notice in notices:
            embed = Embed(title=notice["name"], url=notice["url"], color=0x001f99)
            embed.set_author(name=notice["author"])
            embed.set_footer(text=notice["date"])
            buf.append(embed)
            if len(buf) == 10:
                await webhook.send(content=f"<@&{mention}>" if mention else None, embeds=buf, username=f"삼육대학교 {loaded_parsers[parser_id].NAME}", avatar_url=LOGO_URL)
                buf.clear()
                
        if buf:
            await webhook.send(content=f"<@&{mention}>" if mention else None, embeds=buf, username=f"삼육대학교 {loaded_parsers[parser_id].NAME}", avatar_url=LOGO_URL)


async def parsing_task():
    while not parser_session.closed:
        errs = []
        for parser_id, parser in loaded_parsers.items():
            try:
                res = await parser.get_notices()
            except RequestError:
                logger.error(f"Unable to parse from parser {parser_id}.")
            except URLNotProvided:
                logger.warning(f"Invalid parser {parser_id}, removing...")
                errs.append(parser_id)
            except Exception as ex:
                logger.exception("Error occurred while parsing!")
                content = format_exc()
                traceback = File(StringIO(content), filename="traceback.py")
                await error_webhook.send(files=[traceback])
            else:
                logger.info(f"Parsed from {parser_id} parser.")

                from_db = [await db.execute_fetchall(f"SELECT url FROM {pid}") for pid in loaded_parsers.keys()]

                existing = set()

                for db_res in from_db:
                    for x in db_res:
                        existing.add(x["url"])

                # 처음 가져오는 경우는 스킵
                if existing:
                    filtered = [x for x in res if x["url"] not in existing and x["name"]]
                    if filtered:
                        await publish_to_discord(filtered, parser_id)

                await db.executemany(
                    f"INSERT INTO {parser_id} SELECT ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM {parser_id} WHERE url=?)",
                    ((x["url"], x["name"], x["author"], x["date"], x["url"]) for x in res if x["name"]))
                await db.commit()

        for err in errs:
            loaded_parsers.pop(err, None)

        await sleep(60)  # 60초 간격


@app.before_server_start
async def init_all(app: Sanic, loop: AbstractEventLoop):
    global db, parser_session, webhook_session, error_webhook

    db = await connect("database.db")
    db.row_factory = Row

    parser_session = ClientSession()
    webhook_session = ClientSession()

    for parser_id, parser_class in available_parsers.items():
        loaded_parsers[parser_id] = parser_class(parser_session)
        await db.execute(f"""CREATE TABLE IF NOT EXISTS {parser_id} (
        url TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        author TEXT NOT NULL,
        date TEXT NOT NULL
        )""")
        await db.commit()

    await db.execute("""CREATE TABLE IF NOT EXISTS discord_sub (
    webhook TEXT PRIMARY KEY,
    sub TEXT NOT NULL DEFAULT 'academic',
    mention TEXT DEFAULT NULL
    )""")

    error_webhook = Webhook.from_url(Config.ERROR_WEBHOOK_URL, session=webhook_session)

    await db.commit()


@app.after_server_start
async def start_task(app: Sanic, loop: AbstractEventLoop):
    app.add_task(parsing_task())


@app.after_server_stop
async def close_all(app: Sanic, loop: AbstractEventLoop):
    await parser_session.close()
    await db.close()


@app.get("/")
async def hello(request: Request) -> HTTPResponse:
    return text("Hello, World!")


if __name__ == "__main__":
    app.run(Config.HOST, Config.PORT)
