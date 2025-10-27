# Syn Songs - GitHub Pages Player

A simple GitHub Pages site that plays songs when navigating to document URLs.

## Setup

1. Push this repository to GitHub
2. Go to your repository settings → Pages
3. Enable GitHub Pages (source: main branch, /root)
4. The site will be available at `https://YOUR_USERNAME.github.io/synSongs/`

## Usage

To play a song for a specific document URL:

```
https://YOUR_USERNAME.github.io/synSongs/?doc=DOCUMENT_URL
```

Example:
```
https://YOUR_USERNAME.github.io/synSongs/?doc=https://help.synapse.org/docs/About-Synapse.2058846607.html
```

## How It Works

The page:
1. Loads the `songz.csv` file
2. Looks up the document URL in the CSV
3. Embeds the corresponding Suno.com song player (if available)
4. Displays the document content in an embedded iframe
5. Allows you to browse documentation while music plays

**Note:** The document is embedded within the GitHub Pages site, so clicking links within the document stays within the iframe context.

## Files

- `index.html` - Main page with song player
- `songz.csv` - CSV file mapping document URLs to song URLs
- `README.md` - This file
