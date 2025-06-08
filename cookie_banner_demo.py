import argparse
from pathlib import Path
from typing import List, Literal

from custom_command import LinkCountingCommand

from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager

from openwpm.commands.cookie_banner_commands import (
    CookieBannerSelectionCommand,
    LogCookieBannerOptionsCommand,
)


def run(site: str, options: List[str], headless: bool) -> None:
    display_mode: Literal["native", "headless", "xvfb"] = "native"
    if headless:
        display_mode = "headless"

    manager_params = ManagerParams(num_browsers=1)
    browser_params = [BrowserParams(display_mode=display_mode)]

    for bp in browser_params:
        bp.http_instrument = True
        bp.cookie_instrument = True
        bp.navigation_instrument = True
        bp.js_instrument = True
        bp.dns_instrument = True
        bp.maximum_profile_size = 50 * (10 ** 20)

    manager_params.data_directory = Path("./datadir/")
    manager_params.log_path = Path("./datadir/openwpm.log")

    with TaskManager(
        manager_params,
        browser_params,
        SQLiteStorageProvider(Path("./datadir/crawl-data.sqlite")),
        None,
    ) as manager:
        for idx, option in enumerate(options):
            def callback(success: bool, val: str = option) -> None:
                print(
                    f"CommandSequence for option '{val}' ran "
                    f"{'successfully' if success else 'unsuccessfully'}"
                )

            cs = CommandSequence(site, site_rank=idx, callback=callback)
            cs.append_command(GetCommand(url=site, sleep=3), timeout=60)
            cs.append_command(LogCookieBannerOptionsCommand())
            cs.append_command(CookieBannerSelectionCommand(option))
            cs.append_command(LinkCountingCommand())
            manager.execute_command_sequence(cs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl a site with different cookie banner selections")
    parser.add_argument("site", help="URL of the site to crawl")
    parser.add_argument("options", nargs="+", help="Button texts to select")
    parser.add_argument("--headless", action="store_true", help="Run browser headless")
    args = parser.parse_args()
    run(args.site, args.options, args.headless)
