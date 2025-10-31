# scraper.py
import json, time, requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def copy_cookies_to_session(driver, session):
    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain"), path=cookie.get("path", "/"))

def fetch_json(session, url, params=None):
    resp = session.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def clean_html(raw):
    if not raw: return ""
    soup = BeautifulSoup(raw, "html.parser")
    return soup.get_text(separator="\n").strip()

def scrape_canvas_data(driver, base_url):
    session = requests.Session()
    copy_cookies_to_session(driver, session)

    profile_url = urljoin(base_url, "/api/v1/users/self/profile")
    try:
        profile = fetch_json(session, profile_url)
        print("✅ Logged in as", profile.get("name"))
    except Exception as e:
        print("❌ Not logged in or cookie expired", e)
        return None

    courses = fetch_json(session, f"{base_url}/api/v1/courses", params={"enrollment_state": "active", "per_page": 100})
    output = []
    for c in courses:
        cid, cname = c.get("id"), c.get("name")
        print("Fetching", cname)
        obj = {"id": cid, "name": cname, "assignments": [], "pages": [], "discussions": []}

        # assignments
        try:
            assigns = fetch_json(session, f"{base_url}/api/v1/courses/{cid}/assignments", params={"per_page": 100})
            for a in assigns:
                obj["assignments"].append({
                    "id": a.get("id"),
                    "name": a.get("name"),
                    "due_at": a.get("due_at"),
                    "description": clean_html(a.get("description", ""))
                })
        except Exception: pass

        # pages
        try:
            pages = fetch_json(session, f"{base_url}/api/v1/courses/{cid}/pages", params={"per_page": 100})
            for p in pages:
                pdata = fetch_json(session, f"{base_url}/api/v1/courses/{cid}/pages/{p.get('url')}")
                obj["pages"].append({
                    "title": p.get("title"),
                    "url": p.get("url"),
                    "body": clean_html(pdata.get("body", ""))
                })
        except Exception: pass

        # discussions
        try:
            discussions = fetch_json(session, f"{base_url}/api/v1/courses/{cid}/discussion_topics", params={"per_page": 100})
            for d in discussions:
                obj["discussions"].append({
                    "id": d.get("id"),
                    "title": d.get("title"),
                    "message": clean_html(d.get("message", ""))
                })
        except Exception: pass

        output.append(obj)
        time.sleep(0.3)

    filename = "canvas_data.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    return filename
