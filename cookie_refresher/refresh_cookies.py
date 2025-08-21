from playwright.sync_api import sync_playwright
import time

def refresh_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()
        page.goto("https://accounts.google.com/ServiceLogin")

        # ⚠️ First run requires manual login
        # Run this container locally without headless to login once:
        # docker run -it --rm --entrypoint bash cookie-refresher
        #   then run: python /app/refresh_cookies.py --no-headless

        page.goto("https://www.youtube.com")
        cookies = context.cookies()
        browser.close()

    with open("/app/cookies.txt", "w") as f:
        for c in cookies:
            f.write("\t".join([
                c["domain"],
                "TRUE" if c.get("secure") else "FALSE",
                c["path"],
                "TRUE" if c.get("httpOnly") else "FALSE",
                str(int(c.get("expires", time.time()+3600))),
                c["name"],
                c["value"],
            ]) + "\n")

if __name__ == "__main__":
    refresh_cookies()
