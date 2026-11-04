# Sanooj & Sneja — Wedding Invitation Website

An invitation website for the wedding of **Sanooj & Sneja**.

## 🌟 Features Included

- **Interactive Entrance Gate**: Silk curtain slide animation with `S & S` monogram, "Enter the Celebration" trigger, and flower petal burst effect.
- **Background Music**: Autoplays on opening the gate with an ambient music toggle button in the bottom right corner.
- **Hero Section**: Elegant Cormorant Garamond typography and subtle parallax background effects.
- **Couple & Love Story**: Tap-to-reveal photo interaction and full-width gallery image strips.
- **Live Countdown Timer**: Flip countdown animation ticking down to the wedding ceremony (December 28, 2026, 11:45 AM IST).
- **Ceremony & Reception Event Cards**:
  - **Wedding Ceremony**: Monday, December 28, 2026 (1202 Dhanu 12), Muhurtham: 11:45 AM – 12:30 PM at Sree Sundareswara Temple, Talap, Kannur.
  - **Wedding Reception**: Tuesday, December 29, 2026, 5:00 PM – 9:00 PM at Vallath House, Nadapuram Road, Madappally College, Vatakara.
  - Interactive 3D tilt cards with direct Google Maps location directions.
- **Family Blessings Section**: Parents' names and residence details for both groom and bride.
- **Fully Responsive**: Optimized for mobile devices, tablets, and desktop displays.

---

## 🚀 How to Run Locally

```bash
# Start a local static server
python3 -m http.server 8001
```
Then open [http://localhost:8001](http://localhost:8001) in your browser.

---

## 📁 File Structure

```text
.
├── index.html          # Main HTML document containing all styling and interactivity
├── og.jpg              # Open Graph social sharing preview image
├── assets/
│   ├── hero.jpg        # Hero banner photo
│   ├── gallery-1.jpg   # Photo banner above family section
│   ├── gallery-2.jpg   # Photo strip after date section
│   ├── gallery-3.jpg   # Photo strip after countdown section
│   ├── gallery-4.jpg   # Couple reveal photo
│   ├── soft-bg.jpg     # Closing section background
│   └── music.mp3       # Background song
└── README.md
```

---

## 🖼️ Replacing Photos & Music

To use your own photos and music track, simply replace the corresponding files inside the `assets/` directory (keeping the same filenames, or updating paths in `index.html`):

- `assets/hero.jpg` — Main hero background image
- `assets/gallery-4.jpg` — Couple tap-to-reveal photo
- `assets/gallery-1.jpg`, `gallery-2.jpg`, `gallery-3.jpg` — Gallery & divider photos
- `assets/music.mp3` — Wedding background instrumental song
