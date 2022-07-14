ZnamoToBot
==========

.. start-badges
.. image:: https://img.shields.io/badge/stability-alpha-f4d03f.svg
    :target: https://github.com/b3b/znamotobot
    :alt: Stability
.. image:: https://img.shields.io/docker/v/herethere/znamotobot?color=%23FFD43B&label=Docker%20Image
   :target: https://hub.docker.com/r/herethere/znamotobot
   :alt: Docker Image Version (latest by date)
.. image:: https://github.com/b3b/znamotobot/workflows/tests/badge.svg?branch=main
     :target: https://github.com/b3b/znamotobot/actions?workflow=tests
     :alt: CI Status
.. image:: https://codecov.io/github/b3b/znamotobot/coverage.svg?branch=main
    :target: https://codecov.io/github/b3b/znamotobot?branch=main
    :alt: Code coverage Status
.. end-badges

Inline Telegram bot to show excerpts from `awesome lists <https://github.com/topics/awesome-list>`_,
to remind chat users about some topic that has been previously discussed 256x times.

The idea is that list of links to *Your Chat* important messages are stored in collaborative repository.
And chat users can easily insert sections from this list by calling `@YourAwesomeBotName`.


Usage
-----

Simply type the `@YourAwesomeBotName` in the message field in any chat,
then (optinally) type some text to filter sections.
The bot will offer you sections that you can send in one tap.

Bot must have `Inline mode <https://core.telegram.org/bots/inline>`_ enabled via @BotFather.

Usage demonstration
-------------------

.. image:: docs/usage.gif
  :alt: Bot usage demonstration


List example
------------

Lists are in Markdown format:

.. code-block::

    # Telegram news selection

    ## Stickers

    * [Stickers from video files](https://t.me/telegram/165)
    * [Premium stickers](https://t.me/telegram/181)
    * [@Stickers](https://t.me/telegram/10) — Bot which helps you create sticker packs from your pictures

    ## Usability features

    * [Chat folders](https://t.me/telegram/127) — Helps if you have *too many* chats
    * [Attachment menu](https://t.me/telegram/171)
      When selecting multiple media items, tap  ‘⋯ selected’
      to **preview the message** and **reorder media** before sending
    * [Inline bots](https://t.me/telegram/26)



Run bot with Docker
-------------------

Example command to start the Docker container::

    docker run \
           --rm \
           -e TELEGRAM_TOKEN='token from @BotFather' \
           -e INDEX_URL='https://raw.githubusercontent.com/b3b/znamotobot/main/tests/basic.md' \
           herethere/znamotobot

Setting **INDEX_URL** specifies the list location: local file to load, or URL to remote file to periodically download.

List of all available settings: `znamotobot/settings.py <znamotobot/settings.py>`_

Docker Compose configuration example: `docker-compose.yml <docker-compose.yml>`_


Development
-----------

Commands to run locally::

  pip install -r requirements/dev.txt
  make format
  make test
  python -m znamotobot.bot
