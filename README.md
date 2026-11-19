# Prep Binder

Our daily Kafka and SQL notes in one place. A static site: no login, no backend.

## Deploy to Vercel (one time, about 10 minutes)

1. Create a free account at https://github.com and https://vercel.com (sign up to Vercel with GitHub).
2. On GitHub, click **New repository**, name it `prep-binder`, keep it **Public** or **Private**, and create it.
3. Upload this folder's contents: on the new repo page click **uploading an existing file**, drag in `index.html`, `data.json`, `README.md` and the `pdfs` folder, then **Commit changes**.
4. On Vercel, click **Add New → Project**, pick the `prep-binder` repo, and click **Deploy** (no settings to change; it's a static site).
5. You'll get a link like `https://prep-binder.vercel.app`. Share it with your friend. That's it.

## Adding a new day

1. Upload the new PDF into the `pdfs` folder on GitHub (open the folder → **Add file → Upload files**).
2. Open `data.json` → click the pencil icon → add a line inside `items`, for example:

```json
{ "track": "Kafka", "day": 5, "title": "Anatomy of a Kafka message", "pdf": "pdfs/Kafka_Day5_Message_Anatomy.pdf", "added": "2026-11-20", "links": [] },
```

   `track` must be `DSA`, `LLD`, `Kafka`, `SQL` or `Schedule`. DSA and LLD days can also have a `"points"` list and a `"when"` label (see the existing entries). Watch the commas: every line except the last ends with a comma.
3. Commit. Vercel redeploys automatically in under a minute.

## Adding video links

In `data.json`, fill the `links` list of that day:

```json
"links": [
  { "label": "Striver: Kadane's algorithm", "url": "https://www.youtube.com/watch?v=..." },
  { "label": "sudoCODE: SOLID", "url": "https://www.youtube.com/watch?v=..." }
]
```

## Notes

- "Done" ticks are saved in each person's own browser.
- Anyone with the link can open the notes. If you want a password, Vercel offers password protection on paid plans; otherwise keep the link private.
