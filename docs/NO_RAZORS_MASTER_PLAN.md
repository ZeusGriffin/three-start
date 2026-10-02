# No Razors / FLOSS — Master Product Plan

> Source of truth for the No Razors roadmap. Preserve existing working code and extend incrementally.

## Product
- **Name:** No Razors
- **Design system:** FLOSS
- **Creator mark:** ZEU — Made by Zeus
- **Core idea:** fast, minimal operating system for independent barbers and barbershops.
- **Brand statement:** OLD SCHOOL ROOTS. NEW SCHOOL POWER.
- **Product rule:** the software is modern; the soul is old-school.

## Design Lock
- Black, white, and grey interface only.
- No colored status indicators or colorful gradients.
- Editorial/industrial presentation with old-school barbershop culture.
- Large editorial typography, generous negative space, strong grids, small technical metadata.
- Photography: authentic vintage barber chairs, mirrors, chrome, clippers, combs, scissors, straight razors, leather strops, appointment books, cash registers, storefronts, checkerboard floors, wood cabinetry, waiting chairs, framed photographs, and barbers working.
- Photography should generally be black-and-white/grayscale, high contrast, archival/cinematic, with optional subtle grain.
- Avoid generic/cheesy barbershop clip art.
- Design for one-handed, glanceable use while a barber is working.
- State must be communicated without relying on color.
- Motion: deliberate fades, slides, expanding cards, image reveals, gentle scale, typography transitions; usually 150–300ms.

### Color tokens
```css
--black: #0B0B0B;
--white: #F8F8F6;
--paper: #EFEDE8;
--gray-100: #E7E7E7;
--gray-200: #D2D2D2;
--gray-400: #8C8C8C;
--gray-700: #3C3C3C;
```

## Current MVP
- Splash
- Home
- Bookings
- Clients
- Money
- Settings
- Add/edit/reschedule/cancel/complete appointment
- Add/search/manage clients
- Services with duration, price, deposit, active/inactive
- Local persistence
- 2-hour default cancellation window
- 20% default late-cancellation fee
- Barber override
- Revenue/tax/service metrics
- Today's revenue and appointment count
- Next appointment and today's schedule
- Cancellation alerts and open chair/time slots

## Booking + Scheduling
- Smart scheduling
- Smart rescheduling
- Real-time availability
- Recurring appointments
- Waitlist
- Walk-in mode
- Open chair/time slots
- Confirmation links
- Reschedule links
- Cancellation links
- Rebooking
- Calendar sync
- Live ETA / client-on-the-way status
- Service selection
- Client selection
- Barber-defined availability

## Payments
- Fixed-dollar deposits
- Percentage deposits
- Optional full prepayment
- Cash
- Card
- Apple Pay
- Google Pay
- Cancellation fees
- Refunds
- Payout tracking
- Invoices
- Receipts
- Barber-configurable payment/cancellation rules

## Client CRM
- Name and phone
- Preferred cuts
- Haircut/client notes
- Appointment history
- Cancellation history
- No-show history
- Lifetime spend
- Preferred appointment times
- Optional reference photos
- Retention tracking
- Regular-client reminders
- No-show prediction
- Fast rebooking

## Barber Operations
- Daily schedule
- Walk-ins
- Chair utilization
- Revenue per hour
- Expense tracking
- Cancellation-loss tracking
- Tax estimates
- Earnings heatmaps
- Service popularity
- Peak hours / peak days
- Shop/team management
- Multi-barber
- Multi-location
- Inventory

## Money + Analytics
- Today / Week / Month / Year
- Gross revenue
- Net estimate
- Cash/card
- Deposits
- Cancellation fees
- Refunds
- Estimated taxes
- Average ticket
- Revenue per hour
- Service revenue
- Repeat clients
- Retention
- Cancellation rate
- No-show rate
- Peak hours/days
- Client lifetime value

## Customer Experience
- Public barber booking page
- Customer booking flow/app
- Barber discovery
- Local marketplace
- Portfolio pages
- Wallet pass / wallet card
- NFC check-in
- Live ETA
- Booking reminders
- Payment confirmations

## AI
- AI booking assistant
- AI rescheduling assistant
- FAQ replies
- Open-slot suggestions
- Daily briefing
- Revenue summaries
- Pricing insights
- Retention alerts
- Schedule optimization
- No-show prediction
- AI-assisted portfolio/profile pages
- AI should remain invisible until useful and never complicate the basic workflow.

## Platform Roadmap
- Barber app
- Customer app
- Shop-owner dashboard
- Admin portal
- Public booking website
- API
- Authentication/login
- Barber onboarding
- Shop/team onboarding
- Supabase backend
- Stripe payments
- SMS
- Email
- Push notifications
- Analytics / PostHog
- PWA
- iOS app
- Android app
- Widgets
- Live Activities
- App Store deployment
- Google Play deployment

## Architecture
Current MVP:
- React
- Vite
- JavaScript/TypeScript
- CSS
- Lucide icons
- localStorage

Prepare for:
- Supabase
- Stripe
- push notifications
- SMS
- email

Keep reusable:
- components/
- pages/
- hooks/
- services/
- utils/
- data/
- styles/
- assets/

Avoid giant components and duplicated logic. Keep business logic separate from presentation.

## Core Data Model
Prepare for:
- users
- barbers
- shops
- clients
- services
- appointments
- payments
- availability
- notifications
- settings

Appointment fields:
- id
- shopId
- barberId
- clientId
- serviceId
- date
- startTime
- duration
- price
- deposit
- status
- paymentStatus
- cancellationFee
- createdAt
- updatedAt

## Default Cancellation Logic
Default cancellation window: **2 hours**.
Default late cancellation fee: **20%** of appointment price.
Record cancellation time, fee, appointment, client, and payment status.
Barber can override the charge. Both defaults must eventually be configurable.

## Development Rules
1. Inspect the existing repository before modifying anything.
2. Preserve working functionality.
3. Modify only necessary files.
4. Reuse existing components and patterns.
5. Refactor only when structurally necessary.
6. Never silently remove features.
7. Preserve the FLOSS design system.
8. Keep the app responsive and iPhone-first.
9. Test affected flows.
10. Fix build/runtime errors before calling work complete.
11. Keep a working preview available whenever possible.
12. Do not rebuild from scratch unless explicitly instructed: **REBUILD NO RAZORS**.
13. Build the smallest working version of each feature first; do not expand scope until it is inspectable and passes acceptance checks.

## GitHub / Deployment
- Canonical repository: `ZeusGriffin/three-start`
- Do not create a separate No Razors repository unless explicitly requested.
- Preserve existing files and history.
- Use GitHub Actions for build/deploy verification when applicable.
- Treat deployment failures as blockers to resolve, not ignore.

## Current Build Goal
Build and maintain a complete working MVP from the existing repository. Navigation, booking, client management, appointment completion, cancellation logic, money calculations, and persistence must be functional. Keep the interface responsive for iPhone first. Do not stop at mockups or pseudocode.
