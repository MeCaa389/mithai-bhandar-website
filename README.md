# Retailer Website Template

Demo built for: **Shree Mithai Bhandar** (sweets & namkeen shop, Karnal) — swap content per client.

## Run it locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Leaves running on `http://localhost:5000`.

**Frontend:**
Just open `frontend/index.html` in a browser. No build step — it's plain HTML/CSS/JS.

## What's inside

```
retailer-template/
├── frontend/
│   ├── index.html    → all page content — swap text here per client
│   ├── style.css      → all colors/fonts — swap palette here per client
│   └── script.js       → handles the inquiry form
├── backend/
│   ├── app.py          → tiny API: receives inquiry form, logs to CSV
│   └── requirements.txt
└── README.md
```

## Reskinning for a new client (your actual workflow)

1. Copy this whole folder → rename to `clientname-website`
2. In `style.css`, change the 6 color tokens at the top (`--cream`, `--maroon`, etc.) to match their brand
3. In `index.html`, replace: shop name, tagline, story text, product/menu cards, phone number, address, hours
4. Swap `.media-1` / `.media-2` gradient placeholders for real photos (just change `background:` to `background-image: url(...)`)
5. Update the WhatsApp number in both `index.html` (two links) and keep `script.js` API_URL pointed at their deployed backend

Most retailers won't need the backend/database at all — for a pure "show info + WhatsApp me" site, you can skip Flask entirely and use a free form service like **Formspree** or **Web3Forms** instead of `backend/app.py`. Only build the real backend for clients who want inquiries logged/tracked.

## Going live (GitHub → Vercel/Render)

1. Push the client's folder to its own GitHub repo
2. **Frontend** → connect the repo to **Vercel** or **Netlify**, set root directory to `/frontend` → free `clientname.vercel.app` (or connect their paid domain later)
3. **Backend** (only if they need the inquiry form/database) → connect the same repo to **Render**, set root directory to `/backend`, start command `python app.py` → free `clientname-api.onrender.com`
4. In `script.js`, update `API_URL` to the live Render URL before final push
5. Done — every future `git push` auto-redeploys both

## Notes for pricing tiers

- **Basic (₹2500–3500):** this template, reskinned, static content, WhatsApp CTA, Formspree contact form. No backend needed.
- **Standard (₹4000–5000):** + this Flask backend for logged/tracked inquiries, custom domain setup.
- **Advanced (₹5000+):** + real database (Supabase/Firebase) for live product catalog, search, or inventory — scope this only when a client actually asks.
