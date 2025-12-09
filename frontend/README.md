# Temple Dashboard

**Temporal Pattern Engine** - Frontend UI for detecting and visualizing stock price patterns.

## Overview

This is the web-based dashboard for Temple, providing an intuitive interface for:
- **Pattern Builder**: Visually create temporal patterns without code
- **Scanner**: Find stocks matching your patterns across markets
- **Dashboard**: Monitor pattern performance and market insights
- **Analytics**: View pattern confidence scores and historical data

## Tech Stack

- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Fast build tool
- **Temple REST API** - Backend integration

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

The dashboard communicates with the Temple REST API:

```
Frontend (React) ←→ Temple REST API (FastAPI) ←→ Temple Components
                    └── /api/v1/patterns/match
                    └── /api/v1/patterns/examples
                    └── /api/v1/scanner/scan
                    └── /api/v1/scanner/universes
```

### API Configuration

Set the API URL in `.env`:

```bash
VITE_API_URL=http://localhost:8000
```

### API Endpoints

- `POST /api/v1/patterns/match` - Match pattern against a stock
- `GET /api/v1/patterns/examples` - Get example patterns
- `POST /api/v1/scanner/scan` - Scan multiple stocks or universes
- `GET /api/v1/scanner/universes` - List available stock universes
- `GET /api/v1/scanner/health` - Check API health

### Running with Backend

1. Start the backend API:
   ```bash
   python -m uvicorn api.main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the dashboard at `http://localhost:5173`

The frontend will automatically connect to the API and fetch real data.

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

## API Service Layer

The frontend includes TypeScript services for API integration:

- `services/templeApi.ts` - Main API service class
- `hooks/useTempleApi.ts` - React hooks for API calls
- `types/api.ts` - TypeScript types for API requests/responses

### Example Usage

```typescript
import { usePatternMatch, useScanStocks } from './hooks/useTempleApi';

function MyComponent() {
  const { data, loading, matchPattern } = usePatternMatch();
  const { scanStocks } = useScanStocks();

  // Match a pattern
  await matchPattern('AAPL', myPattern, 365);

  // Scan stocks
  await scanStocks({ symbols: ['AAPL', 'MSFT'] }, myPattern, 0.7);
}
```

## Notes

- Fully integrated with Temple REST API
- Real-time data from backend when API is running
- Falls back to mock mode when API is unavailable
- Pattern definitions compatible with Temple's schema
- TypeScript ensures type safety across API boundaries

---

Built for Temple - Temporal Pattern Engine
