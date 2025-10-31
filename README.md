````markdown
# 🕸️ Canvas Web Scraper

## 📖 Overview
A local **web scraper** for Canvas LMS that runs in your own browser session.  
It lets you log in manually (no API tokens required), detect whether you’re logged in to Canvas, and then automatically extract all course data — including assignments, pages, and discussions — into a downloadable JSON file.

---

## 🚀 Features
- Detects whether you are logged in to Canvas
- Opens Canvas login page in your current browser tab if not logged in
- Scrapes:
  - Course list
  - Assignments (full descriptions and due dates)
  - Course pages (full text)
  - Discussion topics (titles and messages)
- Automatically downloads the scraped data as `canvas_data.json`

---

## ⚙️ Installation
```bash
git clone https://github.com/<yourname>/canvas-web-scraper.git
cd canvas-web-scraper
python3 -m venv canvasenv
source canvasenv/bin/activate
pip install -r requirements.txt
````

---

## ▶️ Usage

1. Run the Flask server:

   ```bash
   python3 app.py
   ```
2. Open your browser and visit:

   ```
   http://localhost:5000
   ```
3. Click **Start Scraping**

   * If not logged in, the Canvas login page will open in the same browser session.
   * Once logged in, click again to begin scraping.
4. The JSON file will automatically download once finished.

---

## 📂 Project Structure

```
canvas-web-scraper/
├── app.py               # Flask web server
├── scraper.py           # Scraping logic (requests + BeautifulSoup)
├── templates/
│   └── index.html       # Frontend UI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📦 Output Example

```json
[
  {
    "id": 12345,
    "name": "CS 438 - Communication Networks",
    "assignments": [
      {
        "id": 567,
        "name": "MP2: Transport Protocol",
        "due_at": "2024-10-25T23:59:00Z",
        "description": "In this lab you will implement a reliable data transfer protocol..."
      }
    ],
    "pages": [
      {
        "title": "Course Overview",
        "url": "course-overview",
        "body": "This course introduces fundamental concepts in network communication..."
      }
    ],
    "discussions": [
      {
        "id": 432,
        "title": "Welcome to CS438",
        "message": "Please introduce yourself and tell us why you're interested in this course..."
      }
    ]
  }
]
```

---

## 🧠 Technologies

| Component                  | Purpose                                            |
| -------------------------- | -------------------------------------------------- |
| **Flask**                  | Runs the local web server                          |
| **Selenium**               | Controls browser automation (login, page handling) |
| **Requests**               | Fetches Canvas API data                            |
| **BeautifulSoup4**         | Cleans HTML into readable text                     |
| **JavaScript (Fetch API)** | Controls scraping via front-end actions            |

---

## 🧩 Commands Summary

```bash
# Activate environment
source ~/canvasenv/bin/activate

# Run local server
python3 app.py

# Access web UI
open http://localhost:5000
```

---

