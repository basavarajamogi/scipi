# Personal Writing Portfolio

A minimal, winter-themed portfolio website for poems, prose, and quotes.
Built with HTML, CSS, and Vanilla JavaScript. Content is managed via distinct text files and parsed into JSON.

## 📂 Project Structure

```text
/
├── index.html          # Home Page
├── styles.css          # Main Styling (Winter Theme)
├── script.js           # Logic for loading content
├── parse_content.py    # Script to update content
├── CONTENT_GUIDE.md    # Instructions for formatting content
│
├── content_source/     # YOUR TEXT FILES GO HERE
│   └── poems.txt       # Example source file
│
├── content/
│   └── data.json       # Generated content data
│
├── poems/
│   └── index.html      # Poems Page
├── prose/
│   └── index.html      # Prose Page
└── quotes/
    └── index.html      # Quotes Page
```

## 🚀 How to Add Content

1.  Create a new text file inside `content_source/` (or use the existing `poems.txt` there).
2.  Add your new Poem, Prose, or Quote following the format in **[CONTENT_GUIDE.md](CONTENT_GUIDE.md)**.
3.  Run the update script:
    ```bash
    python3 parse_content.py
    ```
4.  Push your changes to GitHub (see below).

## 🌐 How to Deploy to GitHub

### First Time Setup
1.  Create a **New Repository** on GitHub (e.g., `my-portfolio`).
2.  Run these commands in your terminal:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/my-portfolio.git
    git push -u origin main
    ```
3.  Go to **Settings > Pages** on GitHub.
4.  Select `main` branch and click **Save**.
5.  Your site will be live at `https://YOUR_USERNAME.github.io/my-portfolio/`.

### Updating the Site
After adding new content and running the python script:
```bash
git add .
git commit -m "Added new poems"
git push
```
The site will update automatically within a few minutes.

## 🛠 Local Development
To preview the site on your computer (needed for dynamic content to load):
```bash
python3 -m http.server 8080
```
Then open `http://localhost:8080` in your browser.
