# Temple Dashboard

**Temporal Pattern Engine** - Frontend UI for detecting and visualizing stock price patterns.

## Overview

This is the web-based dashboard for Temple, providing an intuitive interface for:
- **Pattern Builder**: Visually create temporal patterns without code
- **Scanner**: Find stocks matching your patterns across markets
- **Watchlists**: Monitor specific stocks for pattern occurrences
- **Analytics**: View pattern performance and confidence scores

## Tech Stack

- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Fast build tool
- **Lucide React** - Beautiful icons

## Features

### 1. Pattern Builder
Create custom temporal patterns using a visual interface:
- Define event sequences (crosses, touches, rises/falls)
- Set timing constraints between events
- Configure frequency requirements
- Test patterns on historical data

### 2. Stock Scanner
Scan multiple stocks for pattern matches:
- Select from watchlists or indices (S&P 500, NASDAQ, etc.)
- Filter by confidence threshold
- View ranked results with scores
- Export results to CSV/JSON

### 3. Pattern Library
Manage your saved patterns:
- Pre-built templates (Mean Reversion, Support Bounce, etc.)
- Custom user-defined patterns
- Edit and delete patterns
- Share patterns with community (future)

### 4. Interactive Charts
Visualize pattern occurrences:
- Price charts with pattern highlights
- Mark event timestamps
- Show confidence levels
- Historical pattern performance

### 5. Watchlists
Monitor stocks for real-time pattern matches:
- Create custom watchlists
- Set alerts for pattern occurrences
- View recent matches
- Track pattern frequency

## Quick Start

### Install Dependencies

```bash
npm install
```

### Development Server

```bash
npm run dev
```

Opens at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Outputs to `dist/` folder.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── dashboard/      # Main dashboard view
│   │   ├── builder/        # Pattern builder UI
│   │   ├── profile/        # User settings
│   │   └── layout/         # Nav and layout components
│   ├── App.tsx             # Main app component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── package.json
└── vite.config.ts
```

## Integration with Backend

The dashboard communicates with the Python backend (patterns + scanner layers) via REST API:

```
Frontend (React)  ←→  Backend API (FastAPI/Flask)  ←→  Temple (Python)
                       └── /api/patterns
                       └── /api/scan
                       └── /api/stocks
```

API endpoints (to be implemented in backend):
- `GET /api/patterns` - List saved patterns
- `POST /api/patterns` - Create new pattern
- `POST /api/scan` - Run pattern scan
- `GET /api/stocks/{symbol}/data` - Get OHLCV data
- `POST /api/patterns/test` - Test pattern on stock

## Customization

### Theme Colors

Edit `tailwind.config.js` to customize colors:

```js
colors: {
  accent: '#10b981',  // Primary accent color
  bg: '#030303',      // Background
  surface: '#0a0a0a', // Card surfaces
  // ...
}
```

### Animations

Animations are defined in `tailwind.config.js` and `index.css`. Keep existing ones to maintain the polished feel.

## Development Guidelines

1. **Keep styles consistent** - Use existing Tailwind utility classes
2. **Maintain animations** - Don't remove blur effects, gradients, or transitions
3. **Type safety** - Define proper TypeScript interfaces for data
4. **Component reusability** - Extract common patterns into reusable components

## Future Enhancements

- [ ] Real-time pattern monitoring with WebSockets
- [ ] Pattern backtesting interface
- [ ] Community pattern library
- [ ] Advanced charting with technical indicators
- [ ] Mobile responsive improvements
- [ ] Dark/light theme toggle
- [ ] Export reports to PDF

## Notes

- Currently runs standalone with mock data
- Backend integration pending (scanner + API layer)
- Charts will use real data once backend is connected
- Pattern builder generates JSON definitions compatible with Temple's schema

---

Built for Temple - Temporal Pattern Engine
