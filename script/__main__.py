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

signal(SIGPIPE,SIG_DFL)
_log = logging.getLogger(__name__)
NUM_USERS = 314
random.seed(123)

rnd = random.Random()
rnd.seed(123)

async def main():
    _log.info("Handling %s users", NUM_USERS)
    for _ in range(NUM_USERS):
        await action(username())


async def action(user: str):
    action_id = UUID(int=rnd.getrandbits(128), version=4)
    _log.info("[%s] Found %s", action_id, user)
    if random.random() > 0.8:
        _log.info("[%s] %s needs fixing", action_id, user)
        _log.debug("[%s] Determining emotion", action_id)
        await asyncio.sleep(random.random() / 10)
        emotion = random.choice(emotions)
        if user.startswith(emotion):
            _log.warning("[%s] Emotion hasn't changed", action_id)
        else:
            _log.debug("[%s] %s is now feeling '%s'", action_id, user, emotion)
            _log.info("[%s] Fixing emotion", action_id)
            await asyncio.sleep(random.random() / 10)
            if random.random() > 0.2:
                _log.error("[%s] %s stuck in machine!", action_id, user)
            else:
                _log.info("[%s] %s emotion successfully fixed", action_id, user)
    else:
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
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(CustomFormatter())

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)
    # create console handler with a higher log level
    # ch = logging.StreamHandler()
    # ch.setFormatter(CustomFormatter())
    #
    # logger.addHandler(ch)
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    #     handlers=[queue_handler]
    # )
    queue_listener = QueueListener(log_queue, stdout_handler)
    queue_listener.start()
    asyncio.run(main())
