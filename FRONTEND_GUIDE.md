# Frontend Dashboard - Complete Implementation

## Overview

The AI Kubernetes Agent frontend is a modern, responsive Next.js dashboard that provides real-time Kubernetes troubleshooting with AI-powered analysis.

## Architecture

### Technology Stack

- **Framework:** Next.js 14.2.5
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 3.4
- **State Management:** React Query v5 + React Hooks
- **HTTP Client:** Axios with 5-minute timeout
- **UI Pattern:** Component-based with separation of concerns

### Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with providers
│   ├── page.tsx            # Main dashboard page
│   ├── globals.css         # Tailwind imports
│   └── providers.tsx       # Query client provider
├── components/
│   ├── AuthProvider.tsx    # Login wrapper component
│   ├── InvestigationProgress.tsx  # Progress tracker
│   ├── DiagnosisCard.tsx   # Results display
│   └── InvestigationHistory.tsx   # Past analyses
├── hooks/
│   └── useAuth.ts          # Auth state management
├── services/
│   └── api.ts              # HTTP client and endpoints
├── types/
│   └── index.ts            # TypeScript definitions
├── public/                 # Static assets
├── next.config.mjs         # Next.js configuration
├── tsconfig.json           # TypeScript config
├── tailwind.config.ts      # Tailwind CSS config
└── package.json            # Dependencies
```

## Components Deep Dive

### 1. InvestigationProgress

**Purpose:** Visual representation of investigation steps with real-time completion tracking.

**Props:**
```typescript
interface InvestigationProgressProps {
  steps: Array<{ name: string; completed: boolean }>;
  isInvestigating: boolean;
}
```

**Features:**
- 7-step progress indicator
- Animated step completion
- Checkmarks for completed steps
- Color coding (cyan for active, slate for pending)

**Usage:**
```tsx
<InvestigationProgress steps={steps} isInvestigating={isPending} />
```

### 2. DiagnosisCard

**Purpose:** Display AI analysis results in a structured, professional format.

**Props:**
```typescript
interface DiagnosisCardProps {
  diagnosis: {
    root_cause: string;
    explanation: string;
    fix: string;
    kubectl_command: string;
    prevention: string;
    confidence: number;
  };
}
```

**Features:**
- Root cause highlighting
- Explanation section
- Fix recommendations
- kubectl command with code block
- Prevention tips
- Confidence percentage display

**Styling:**
- Dark background (slate-900)
- Cyan accents for section headers
- Professional typography
- Responsive padding

### 3. InvestigationHistory

**Purpose:** Display previous investigation results for reference and comparison.

**Props:**
```typescript
interface HistoryProps {
  investigations: Array<{
    timestamp: string;
    root_cause: string;
    namespace: string;
    confidence: number;
    status: "success" | "failed";
  }>;
}
```

**Features:**
- Sortable history list
- Timestamp display
- Root cause summary
- Confidence badges
- Status indicators
- Empty state message

### 4. AuthProvider

**Purpose:** Login interface for user authentication.

**Features:**
- Email/password inputs
- Submit button
- Simple, clean form
- Conditional rendering

**Note:** MVP implementation; extend for full auth features

## Custom Hooks

### useAuth

**Purpose:** Manage user authentication state and provide login/logout functions.

**API:**
```typescript
const {
  user,           // Current user or null
  isLoading,      // Initial auth check loading
  error,          // Auth error message
  login,          // async (email, password) => Promise
  logout          // async () => Promise
} = useAuth();
```

**Implementation:**
- Checks `/api/auth/me` on component mount
- Handles login via `/api/auth/login`
- Manages loading and error states
- Provides logout function

## Main Dashboard (page.tsx)

### Features

#### 1. Investigation Trigger
```tsx
<button onClick={() => mutation.mutate()}>
  Investigate Cluster
</button>
```
- Disabled during investigation
- Shows "Investigating..." text while running
- Cyan button with hover effects

#### 2. Real-time Progress Tracking
```tsx
const mutation = useMutation<InvestigationResult, Error>({
  mutationFn: runInvestigation,
  onMutate: () => {
    // Setup progress animation
    const interval = setInterval(() => {
      // Update steps
    }, 400);
  },
  onSuccess: (data) => {
    // Mark all steps complete
    // Add to history
  }
});
```

- Animation interval: 400ms per step
- Auto-completes all steps on success
- Shows error on failure

#### 3. Responsive Layout
```tsx
<div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
  <div className="lg:col-span-1">
    {/* Progress + History */}
  </div>
  <div className="lg:col-span-2">
    {/* Diagnosis */}
  </div>
</div>
```

- Single column on mobile
- 3-column grid on desktop
- 1/3 width for progress, 2/3 for diagnosis
- Responsive gap and padding

#### 4. State Management
```tsx
const [steps, setSteps] = useState<InvestigationStep[]>(INITIAL_STEPS);
const [historyItems, setHistoryItems] = useState<any[]>([]);

const { data: healthData } = useQuery({...});
const { data: historyData } = useQuery({...});
const mutation = useMutation({...});
```

- React Query for server state (health, history)
- Local state for UI (steps, history items)
- Mutation for investigation trigger

## API Integration

### Endpoints Used

#### fetchHealth
```typescript
GET /health
Returns: { status: "ok", timestamp: "..." }
```

#### runInvestigation
```typescript
POST /investigate
Returns: {
  status: "success",
  investigation: {...},
  diagnosis: {...}
}
Timeout: 5 minutes (300000ms)
```

#### fetchInvestigationHistory
```typescript
GET /history
Returns: {
  status: "success",
  investigations: [...],
  total: number
}
```

#### Authentication Endpoints
```typescript
POST /api/auth/login
POST /api/auth/logout
GET /api/auth/me
```

## Styling & Theme

### Color Scheme

- **Background:** slate-950 (dark)
- **Surfaces:** slate-900 (cards, containers)
- **Borders:** slate-800 (dividers)
- **Text:** slate-100, slate-400, slate-300
- **Accent:** cyan-500 (primary actions)
- **Success:** green (implicit in components)
- **Error:** rose-700, rose-950

### Responsive Design

**Mobile (0-768px)**
- Single column layout
- Full-width components
- Smaller padding (px-6 py-16)

**Tablet (768px-1024px)**
- Grid adjusts
- Moderate spacing

**Desktop (1024px+)**
- 3-column layout
- Full spacing
- Optimized readability

## Performance Optimizations

1. **React Query Caching**
   - Health check cached automatically
   - History data refreshed on demand
   - Stale time: 5 minutes

2. **Lazy Loading**
   - Components are "use client" (client-side only)
   - No server-side rendering for interactive features

3. **Debouncing**
   - Progress animation runs on fixed 400ms interval
   - Prevents rapid re-renders

## Error Handling

### Investigation Failures

```tsx
{mutation.isError && (
  <div className="rounded-2xl border border-rose-700 bg-rose-950/80 p-6 text-rose-200">
    <h2 className="text-lg font-semibold">Investigation Failed</h2>
    <p className="mt-2 text-sm">
      Unable to complete investigation. Please check the backend logs.
    </p>
  </div>
)}
```

### Empty States

```tsx
{!isPending && !mutation.data && (
  <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
    <h2 className="text-lg font-semibold text-white">
      Click Investigate to Begin
    </h2>
  </div>
)}
```

## Future Enhancements

### Short Term
- [ ] Real-time progress updates via WebSocket
- [ ] Investigation filtering (by namespace, status)
- [ ] Export diagnosis as JSON/PDF
- [ ] Dark/light theme toggle

### Medium Term
- [ ] Multi-cluster support
- [ ] Advanced authentication (InsForge)
- [ ] Investigation comparison
- [ ] Custom prompt builder UI
- [ ] Webhook notifications

### Long Term
- [ ] Investigation analytics dashboard
- [ ] Trend analysis over time
- [ ] Predictive troubleshooting
- [ ] Integration with monitoring tools
- [ ] Mobile app (React Native)

## Development Workflow

### Local Development

```bash
cd frontend
npm install
npm run dev
```

Runs on http://localhost:3000 with hot reload.

### Building for Production

```bash
npm run build
npm start
```

### Type Checking

```bash
npx tsc --noEmit
```

### Linting

```bash
npm run lint
```

## Testing the Dashboard

### Manual Test Checklist

- [ ] Click "Investigate Cluster" button
- [ ] Watch progress steps complete in sequence
- [ ] Verify diagnosis card displays all sections
- [ ] Check history updates after investigation
- [ ] Verify error handling (if backend is down)
- [ ] Test responsive design (resize window)
- [ ] Check authentication (if implemented)
- [ ] Verify API timeouts (let request run 5+ min)

### API Integration Test

```bash
# Terminal 1: Start backend
cd backend && python main.py

# Terminal 2: Start frontend
cd frontend && npm run dev

# Terminal 3: Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/investigate
```

## Browser Compatibility

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari 15+
- ✅ Mobile browsers

## Accessibility

- Semantic HTML elements
- ARIA labels on buttons
- Keyboard navigation support
- High contrast colors (WCAG AA)
- Readable font sizes

## Notes

- Built with minimal dependencies
- No external CSS frameworks beyond Tailwind
- All components are client-side
- Designed for ease of understanding and modification
- Comments explain key logic sections
