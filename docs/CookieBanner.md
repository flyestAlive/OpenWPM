# Cookie Banner Interactions

This example shows how a site can be crawled multiple times while selecting different
options on a cookie banner at the start of each visit. The commands are implemented in
`openwpm/commands/cookie_banner_commands.py` and demonstrate how to locate banner
buttons by their visible text.

`CookieBannerSelectionCommand` clicks a button whose text matches the provided string.
`LogCookieBannerOptionsCommand` prints all detected option texts to the log which can be
helpful when preparing your crawl.  The demo script enables the same instrumentation
as `demo.py` (HTTP requests, cookies, navigation, JavaScript and DNS logging) so each
consent choice produces a full crawl record.

To run the demo:

```bash
python cookie_banner_demo.py https://example.com "Alle akzeptieren" "Nur funktional" --headless
```

This will visit `https://example.com` twice, once clicking the button with the text
`"Alle akzeptieren"` and once clicking `"Nur funktional"`. Each visit is stored in the
result database like any other crawl allowing you to compare requests or loaded scripts
for different consent choices.
