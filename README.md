# Content Formatter Tool
## Caltech Library Blog Design System

This tool helps content editors format multiple types of content for the Caltech Library blog with consistent, accessible styling including book lists, events, resource links, and featured card layouts.

## Architecture
A standalone, single-file (index.html) client-side web app for editors to generate styled HTML snippets for SpringShare LibGuides/Blog Posts via CKEditor's source tab.                                         
                                                                                                                        
  - Pure JS/HTML/CSS. no build step, no backend, no framework
  - Single page with tab-based navigation (switchTab())                                                                 
  - External CSS in content-styles.css that is added to the SpringShare master css file
  - Web component in web component/card-layout.js (Card Layout tab, Shadow DOM)
  - All event times are normalized to Pacific Time (PST/PDT) on ICS import
  - ISBN import has a 10s timeout and falls back gracefully if Google Books fails                                       
  - Card Layout generates a <card-layout> web component loaded from Caltech Library's CDN                               
  - No external API keys required (Open Library, Microlink, and Google Books are public/free-tier)   

## Files in This Package

1. **index.html** - The main tabbed formatter tool (open in browser)
2. **help.html** - In-tool help and documentation page
3. **content-styles.css** - CSS to add to your blog stylesheet
4. **web component/** - Source files for the Three Card Layout web component

## How to Use the Tool

The tool has four tabs for different content types:

### 📚 Books Tab

**Use this for:** Creating formatted book lists from ISBNs

**Step 1: Choose Your Layout**
- **Vertical List** - Books displayed in a stacked list with cover on left, details on right
- **Horizontal Grid** - Books displayed in a grid with covers and titles

**Step 2: Enter Book Details**

**Quick Fill Option:**
1. Paste a list of ISBNs (comma-separated or one per line) into the text box
2. Click **"Fetch Book Details"**
3. The tool automatically fetches from Open Library:
   - Book title
   - Author(s)
   - Cover image
   - ISBN
   - Description (via Google Books, falls back to Open Library)
4. Review and edit the auto-filled information
5. Manually add Call Number if needed (optional)
6. Click **"Format Book List"**
7. *(Optional)* Click **"Preview Styled Output"** to see how it will look
8. Click **"Copy to Clipboard"**
9. Paste into your blog's Source Code view

**Manual Entry Option:**
1. Fill in the form fields for each book:
   - **Title** (required)
   - **Author** (optional)
   - **ISBN** (optional)
   - **Description** (optional) - brief summary of the book
   - **Cover Image URL** (optional)
   - **Cover Alt Text** (optional) - defaults to "Book cover of [Title] by [Author]"
   - **Call Number** (optional)
   - **URL/Permalink** (optional)
2. Click **"+ Add Another Book"** to add more books
3. Click **"Format Book List"** when done
4. *(Optional)* Click **"Preview Styled Output"**
5. Click **"Copy to Clipboard"**
6. Paste into your blog's Source Code view

**What it generates:**
- Book entries with cover images displayed on the left
- Book title, author, description, ISBN, and call number
- Alternating background colors for readability
- "View Book" button if URL is provided
- HTML comments marking the beginning and end of the book list

---

### 📅 Event Tab

**Use this for:** Creating styled event announcements

**Quick Fill Option:**
1. Upload an .ics calendar file using the file picker
2. The tool automatically fills in:
   - Event title
   - Date and time (always displayed in Pacific Time)
   - Location
   - Description
   - URL (if available)
3. Review and edit the auto-filled information
4. Click **"Format Event"**
5. *(Optional)* Click **"Preview Styled Output"**
6. Click **"Copy to Clipboard"**
7. Paste into your blog's Source Code view

**Manual Entry Option:**
1. Fill in the form:
   - **Event Title** (required)
   - **Date** (required) - use the date picker
   - **Time** (optional) - displayed in Pacific Time (PST or PDT depending on date)
   - **Location** (optional)
   - **Description** (required)
   - **Link** (optional) - registration or more info URL
   - **Link Text** (optional) - defaults to "Learn More"
2. Click **"Format Event"**
3. *(Optional)* Click **"Preview Styled Output"**
4. Click **"Copy to Clipboard"**
5. Paste into your blog's Source Code view

**What it generates:**
- Calendar-style date box with day and month
- Event title, date, time (with PST/PDT label), and location
- Event description
- "Learn More" link button if URL provided
- HTML comments marking the beginning and end of the event

---

### 🔗 Links Tab

**Use this for:** Creating styled resource/link lists

**Quick Fill Option:**
1. Paste a list of URLs (one per line) into the text box
2. Click **"Fetch Link Details"**
3. The tool automatically fetches:
   - Page title
   - Page description (meta description)
4. Review and edit the auto-filled information
5. *(Optional)* Add a section title (e.g., "Related Resources")
6. Click **"Format Links"**
7. *(Optional)* Click **"Preview Styled Output"**
8. Click **"Copy to Clipboard"**
9. Paste into your blog's Source Code view

**Manual Entry Option:**
1. *(Optional)* Add a section title (e.g., "Related Resources")
2. For each link, fill in:
   - **Link Title** (required)
   - **URL** (required)
   - **Description** (optional)
3. Click **"+ Add Another Link"** to add more links
4. Click **"Format Links"** when done
5. *(Optional)* Click **"Preview Styled Output"**
6. Click **"Copy to Clipboard"**
7. Paste into your blog's Source Code view

**What it generates:**
- Styled link cards with hover effects
- Optional section title
- Link title, URL, and description for each link
- Links open in new tab
- HTML comments marking the beginning and end of the link section

---

### 🃏 Three Card Layout Tab

**Use this for:** Displaying three featured items side-by-side (or stacked), such as spotlighted resources, services, or announcements

**Step 1: Choose Your Layout**
- **Horizontal Row** - Three cards displayed side by side (stacks on mobile automatically)
- **Vertical Stack** - Three cards stacked with image on the left and content on the right

**Step 2: Enter Card Details**

Fill in the form for each of the three cards:
- **Title** (required)
- **Description** (optional) - brief text for the card body
- **Image URL** (optional) - displayed at the top (horizontal) or left (vertical) of the card
- **Image Alt Text** (optional) - defaults to the card title if not provided
- **Link URL** (optional) - if omitted, no link button appears on that card
- **Link Text** (optional) - defaults to "Read more"

Click **"Format Cards"** when all three cards are filled in.

**Step 3: Retrieve Formatted HTML**
1. *(Optional)* Click **"Preview Styled HTML"** to see how it will look
2. Click **"Copy to Clipboard"**
3. Paste into your blog's Source Code view

**What it generates:**
- A `<card-layout>` web component tag with all card content as attributes
- A `<script>` tag that loads the component from the Caltech Library CDN
- No additional CSS needed — styles are built into the component
- HTML comments marking the beginning and end of the card layout

**Note:** The card layout uses a web component with encapsulated styles (Shadow DOM). It does not depend on `content-styles.css` and will automatically receive style updates when new versions of the component are released.

---

## What the Styling Does

### Books:
- Book cover images displayed on the left (120px wide)
- Book information on the right (title, author, description, ISBN, etc.)
- Alternating background colors (light grey/white) for readability
- Green "View Book" button (when URL is provided)
- Clean spacing with bottom borders between entries

### Events:
- Calendar-style date box with colored background
- Event details laid out horizontally
- Date, time (with PST/PDT label), and location clearly formatted
- Event description with good readability
- Styled link button for registration/more info

### Links:
- Card-style layout with borders
- Hover effects on link items
- Optional section title with bottom border
- Link titles, URLs, and descriptions
- Links open in new tabs

### Three Card Layout:
- Responsive flexbox layout — horizontal row on desktop, stacks on mobile
- Vertical layout option with image left, content right
- Placeholder shown when no image is provided
- Link button hidden automatically if no URL is provided

---

## Troubleshooting

### Books Tab

**Problem:** Book details not fetching
- **Solution:** Check that ISBNs are valid and properly formatted (10 or 13 digits)
- **Solution:** Some books may not be in the Open Library database; fill in manually if needed

**Problem:** The styling doesn't show up on the blog
- **Solution:** Check that content-styles.css has been added to the blog's stylesheet

**Problem:** Cover images not showing
- **Solution:** Some books may not have cover images available; you can add a custom cover image URL

### Event Tab

**Problem:** Can't format event
- **Solution:** Make sure you've filled in all required fields (Title, Date, Description)

**Problem:** ICS file not uploading
- **Solution:** Make sure the file is a valid .ics calendar file

**Problem:** Time shows incorrectly after ICS import
- **Solution:** Times are always converted to Pacific Time. If the time looks wrong, check that the original event was saved with the correct time in LibCal and re-download the .ics file

### Links Tab

**Problem:** "Some links are incomplete"
- **Solution:** Each link needs both a title and URL. Fill in or remove incomplete links

**Problem:** URL fetch not working
- **Solution:** Some websites may block automated requests; fill in the title and description manually if needed

### Three Card Layout Tab

**Problem:** Cards not displaying on the blog
- **Solution:** Make sure the full output was copied, including the `<script>` tag at the bottom
- **Solution:** The web component requires a modern browser; it will not render in very old browsers

**Problem:** Card layout looks unstyled in preview
- **Solution:** The preview loads the component script from the Caltech Library CDN; make sure you have an internet connection when previewing

---

## Tips

1. **Use the preview** before copying - it shows exactly how content will look on the blog
2. **Use Quick Fill features** - ISBN, ICS, and URL imports save time and reduce errors
3. **Combine content types** - Format books, events, and links separately, then paste them all into one blog post
4. **HTML comments help identify sections** - Each formatted section includes comments like `<!-- BEGIN BOOK LIST -->` to help you find content in source code
5. **Keep the tool open** - You can switch between tabs without losing your work
6. **Clear between uses** - Use the "Clear" button to start fresh on each tab
7. **Edit after import** - Quick Fill auto-populates data, but you can always edit any field before formatting

---

## CSS Classes Reference

The Books, Events, and Links tabs use these CSS classes from `content-styles.css`. The Three Card Layout tab uses a web component with built-in styles and does not use these classes.

### Books:
- `.book-item` - Main container for each book
- `.book-item-odd` / `.book-item-even` - Alternating background colors
- `.book-content` - Flexbox container for cover and info
- `.book-cover` - Book cover image container
- `.book-cover-img` - Book cover image (120px wide)
- `.book-info` - Book information container
- `.book-main` - Title, author, and description container
- `.book-title` - Book title
- `.book-author` - Book author
- `.book-description` - Book description text
- `.book-meta` - Metadata container
- `.book-details` - ISBN, call number
- `.book-view-btn` - "View Book" button/link

### Events:
- `.event-item` - Main container
- `.event-date-box` - Calendar-style date box
- `.event-day` - Day number in date box
- `.event-month` - Month in date box
- `.event-content` - Event details container
- `.event-title` - Event title
- `.event-meta` - Date/time/location container
- `.event-meta-item` - Individual meta item (Date, Time, Location)
- `.event-description` - Event description
- `.event-link` - Call-to-action link

### Links:
- `.link-section` - Overall container
- `.link-section-title` - Section heading
- `.link-item` - Individual link container
- `.link-title` - Link title with anchor tag
- `.link-description` - Link description

---

## Support

If you encounter any issues or have questions, please contact Twila Smith.

---

**Last Updated:** February 2026
**Version:** 5.0 - Added Three Card Layout content type
