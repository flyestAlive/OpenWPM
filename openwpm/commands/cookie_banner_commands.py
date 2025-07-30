import logging
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from openwpm.commands.types import BaseCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.socket_interface import ClientSocket


class CookieBannerSelectionCommand(BaseCommand):
    """Selects a cookie banner option with the given button text."""

    def __init__(self, button_text: str) -> None:
        self.button_text = button_text
        self.logger = logging.getLogger("openwpm")

    def __repr__(self) -> str:
        return f"CookieBannerSelectionCommand({self.button_text})"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        script = """
        const text = arguments[0].toLowerCase();
        const banners = Array.from(document.querySelectorAll('[id*="cookie" i], [class*="cookie" i]'));
        let buttons = [];
        for (const banner of banners) {
            buttons = buttons.concat(Array.from(banner.querySelectorAll('button, input[type="button"], input[type="submit"]')));
        }
        for (const b of buttons) {
            const btext = (b.innerText || b.value || '').trim().toLowerCase();
            if (btext.includes(text)) {
                b.click();
                return true;
            }
        }
        return false;
        """
        try:
            clicked = webdriver.execute_script(script, self.button_text)
            if clicked:
                self.logger.info("Clicked cookie banner option '%s'", self.button_text)
            else:
                self.logger.info("Cookie banner option '%s' not found", self.button_text)
        except Exception as exc:
            self.logger.error("Cookie banner selection failed: %s", exc)


class LogCookieBannerOptionsCommand(BaseCommand):
    """Logs available cookie banner option texts"""

    def __init__(self) -> None:
        self.logger = logging.getLogger("openwpm")

    def __repr__(self) -> str:
        return "LogCookieBannerOptionsCommand"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        script = """
        const banner = document.querySelector('[id*="cookie" i], [class*="cookie" i]');
        if (!banner) { return []; }
        const btns = banner.querySelectorAll('button, input[type="button"], input[type="submit"]');
        return Array.from(btns).map(b => (b.innerText || b.value || '').trim()).filter(t => t);
        """
        try:
            options = webdriver.execute_script(script)
            self.logger.info("Cookie banner options: %s", options)
        except Exception as exc:
            self.logger.error("Failed to extract cookie banner options: %s", exc)


class CookieBannerToggleCommand(BaseCommand):
    """Toggles a checkbox or switch matching the given label text."""

    def __init__(self, label_text: str) -> None:
        self.label_text = label_text
        self.logger = logging.getLogger("openwpm")

    def __repr__(self) -> str:
        return f"CookieBannerToggleCommand({self.label_text})"

    def execute(
        self,
        webdriver: Firefox,
        browser_params: BrowserParams,
        manager_params: ManagerParams,
        extension_socket: ClientSocket,
    ) -> None:
        script = """
        const text = arguments[0].toLowerCase();
        const banners = Array.from(document.querySelectorAll('[id*="cookie" i], [class*="cookie" i]'));
        let toggles = [];
        for (const banner of banners) {
            toggles = toggles.concat(Array.from(banner.querySelectorAll('input[type="checkbox"], input[type="radio"], [role="switch"]')));
        }
        for (const t of toggles) {
            let label = '';
            if (t.labels && t.labels.length) {
                label = Array.from(t.labels).map(l => (l.innerText || '').trim()).join(' ').toLowerCase();
            }
            if (!label && t.getAttribute('aria-label')) {
                label = t.getAttribute('aria-label').trim().toLowerCase();
            }
            if (!label && t.parentElement) {
                label = (t.parentElement.innerText || '').trim().toLowerCase();
            }
            if (label.includes(text)) {
                t.click();
                return true;
            }
        }
        return false;
        """
        try:
            clicked = webdriver.execute_script(script, self.label_text)
            if clicked:
                self.logger.info("Toggled cookie banner option '%s'", self.label_text)
            else:
                self.logger.info("Cookie banner toggle '%s' not found", self.label_text)
        except Exception as exc:
            self.logger.error("Cookie banner toggle failed: %s", exc)

