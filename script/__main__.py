import asyncio
import logging
from logging.handlers import QueueHandler, QueueListener
import random
from signal import signal, SIGPIPE, SIG_DFL
import sys
import queue
from uuid import UUID

from script.emotions import emotions
from script.users import username

signal(SIGPIPE, SIG_DFL)
random.seed(123)
_log = logging.getLogger(__name__)

SLEEP_FACTOR = 3
NUM_USERS = 1000
IGNORED_PERCENTAGE = 0.25
ERRORS = 8
RND = random.Random()

RND.seed(123)

async def main():
    _log.info("Handling %s users", NUM_USERS)
    await asyncio.gather(*(action(username()) for _ in range(NUM_USERS)))

async def sleep():
    await asyncio.sleep(random.random() * SLEEP_FACTOR)

async def action(user: str):
    action_id = UUID(int=RND.getrandbits(128), version=4)
    _log.info("[%s] Found %s", action_id, user)
    await sleep()

    if random.random() > IGNORED_PERCENTAGE:
        _log.info("[%s] %s needs fixing", action_id, user)
        _log.debug("[%s] Determining emotion", action_id)
        await sleep()
        emotion = random.choice(emotions)
        if user.startswith(emotion):
            _log.warning("[%s] Emotion hasn't changed", action_id)
        else:
            _log.debug("[%s] %s is now feeling '%s'", action_id, user, emotion)
            _log.info("[%s] Fixing emotion", action_id)
            await sleep()
            if random.random() < ERRORS / NUM_USERS * IGNORED_PERCENTAGE * 7:
                _log.error("[%s] %s stuck in machine!", action_id, user)
            else:
                _log.info("[%s] %s emotion successfully fixed", action_id, user)
    else:
        await sleep()
        _log.warning("[%s] Ignoring %s", action_id, user)


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


if __name__ == "__main__":
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(CustomFormatter())

    queue_listener = QueueListener(log_queue, stdout_handler)
    queue_listener.start()

    asyncio.run(main())
