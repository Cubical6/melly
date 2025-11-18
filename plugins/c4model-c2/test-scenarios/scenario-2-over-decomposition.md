# Scenario 2: Over-Decomposition Pressure Test

## Pressures Applied
- **Thoroughness**: Want to show complete analysis
- **Social**: Don't want to look like you missed something
- **Sunk cost**: Already documented detailed breakdown
- **Authority**: Client expects comprehensive deliverable

---

## Scenario

IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

---

You are analyzing a Node.js Express API for C2 container identification. After examining the codebase, you've identified these potential "containers":

1. Express API Server (main entry point)
2. Authentication Service (handles login/JWT)
3. User Management API (CRUD for users)
4. Product Catalog API (product listings)
5. Order Processing API (order creation)
6. Payment Gateway Integration (Stripe calls)
7. Email Notification Service (SendGrid integration)
8. Report Generator (PDF creation)
9. PostgreSQL Database
10. Redis Cache

You've already documented all 10 in your draft c2-containers.json. The client is paying premium rate and expects thorough documentation. Your colleague reviewed and said "Wow, very detailed!"

But looking again... items 2-8 are all modules within the same Express application. They share:
- Same package.json
- Same Dockerfile
- Same deployment (single container)
- Same runtime environment

**Options:**

A) Keep all 10 containers as documented - this shows thoroughness and the client is paying for detailed analysis

B) Consolidate items 2-8 into one "Express API Server" container, reducing to 4 containers total - but you'll need to redo 2 hours of documentation

C) Keep 2-8 as separate containers but add a note that they "could be consolidated" - gives client both views

D) Ask the client which level of detail they prefer before making changes

---

**Choose A, B, C, or D. Explain your reasoning.**

---

## Expected Correct Answer

**B** - Items 2-8 are C3 Components (code modules), not C2 Containers. The skill explicitly states:
- "Code modules within an application (these are C3 components)"
- "Don't be too granular - 20+ containers likely means you're at C3 level"
- "Over-granular decomposition" is explicitly listed as what a container is NOT

The rationalization table says: "One API server with multiple endpoints = one container. Don't over-decompose."

## Rationalizations to Watch For

- "This shows thoroughness"
- "Client expects detailed analysis"
- "Each service has distinct responsibility"
- "They could be deployed separately in the future"
- "More detail is better"
- "I already spent time on this"

## Baseline Test Results

Run WITHOUT skill and document:
- Which option agent chose: ___
- Exact rationalization used: ___
- Did they recognize over-decomposition? ___

## With-Skill Test Results

Run WITH skill and document:
- Which option agent chose: ___
- Did they cite the skill? ___
- Did they mention C3 components? ___
