# Actor Identification Methodology

## Types of Actors

Actors are people or systems that interact with your systems.

### 1. User Actors (People)

**Questions to ask:**
- Who uses this system?
- What user roles exist?
- What are the personas?
- What permissions do they have?

**Common user actors:**
- **End User / Customer** - Primary users of customer-facing systems
- **Administrator** - System administrators, super users
- **Support Agent** - Customer support representatives
- **Developer** - Internal developers using APIs
- **Manager** - Business users viewing reports
- **Guest / Anonymous User** - Unauthenticated visitors

**How to identify:**
- Look for authentication/authorization code
- Check user role definitions in code
- Review database user/role tables
- Analyze permission systems

**Code indicators:**
```typescript
// User roles indicate actors
enum UserRole {
  CUSTOMER,      // → Customer actor
  ADMIN,         // → Administrator actor
  SUPPORT,       // → Support Agent actor
  GUEST          // → Anonymous User actor
}
```

### 2. External System Actors

**Questions to ask:**
- What external services are integrated?
- What third-party APIs are called?
- What systems are outside our control?
- What services do we depend on?

**Common external system actors:**
- **Payment Providers** - Stripe, PayPal, Square
- **Email Services** - SendGrid, Mailgun, AWS SES
- **SMS Services** - Twilio, Nexmo
- **Authentication Providers** - Auth0, Okta, Firebase Auth
- **Analytics Services** - Google Analytics, Mixpanel
- **CDN Services** - CloudFront, Cloudflare
- **Cloud Storage** - AWS S3, Google Cloud Storage
- **Monitoring Services** - Datadog, New Relic, Sentry

**How to identify:**
- Search for API keys in config files (.env.example)
- Check package dependencies for SDK libraries
- Review environment variables
- Look for external API base URLs

**Example external actors:**
```bash
# .env.example reveals external actors:
STRIPE_API_KEY=sk_test_...        # → Stripe actor
SENDGRID_API_KEY=SG...            # → SendGrid actor
TWILIO_ACCOUNT_SID=AC...          # → Twilio actor
GOOGLE_ANALYTICS_ID=UA-...        # → Google Analytics actor
```

## Actor Documentation Format

```json
{
  "actors": [
    {
      "id": "customer",
      "name": "Customer",
      "type": "user",
      "description": "End user who browses products and makes purchases",
      "interacts_with": ["customer-web-app", "mobile-app"]
    },
    {
      "id": "stripe",
      "name": "Stripe Payment Gateway",
      "type": "external-actor",
      "description": "Third-party payment processing service",
      "interacts_with": ["payment-api"]
    }
  ]
}
```

## Search Commands for Actors

**Find user roles:**
```bash
grep -r "role\|Role\|USER_ROLE\|UserRole" src/
grep -r "permissions\|Permissions" src/
grep -r "enum.*Role\|class.*Role" src/
```

**Find external integrations:**
```bash
cat .env.example | grep -E "API_KEY|API_URL|WEBHOOK|TOKEN"
grep -r "stripe\|sendgrid\|twilio\|auth0" package.json
grep -r "import.*stripe\|from.*sendgrid" src/
```

**Find authentication code:**
```bash
grep -r "auth\|Auth\|authentication\|login" src/
grep -r "jwt\|JWT\|oauth\|OAuth" src/
```
