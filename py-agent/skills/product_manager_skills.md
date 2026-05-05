# Product Manager Skills

## Requirements Analysis

- **Stakeholder Interviews**: Structured questioning techniques (5 Whys, MoSCoW, INVEST criteria) to surface real needs from stated desires.
- **Workshop Facilitation**: Running discovery workshops, event storming sessions, and user journey mapping with mixed stakeholder groups.
- **Observation & Contextual Inquiry**: Analysing how users currently solve a problem (workarounds, spreadsheets, manual steps) to identify pain points.
- **Document Analysis**: Extracting requirements from existing systems, legacy documentation, and competitor product analysis.

## Epic & Story Creation

- **Epics → Stories → Tasks**: Decomposing business goals into Epics, then breaking Epics into sprint-sized Stories with clear acceptance criteria.
- **INVEST Criteria**: Independent, Negotiable, Valuable, Estimable, Small, Testable — applied to every story before it enters the backlog.
- **Story Mapping**: Building user journey maps that reveal gaps and ensure end-to-end coverage of the user experience.
- **Splitting Techniques**: Breaking down large stories by workflow step, data variation, business rule, interface type, or performance tier.
- **Personas**: Creating lightweight user personas (role, goals, pain points, technical literacy) to ground stories in real user contexts.

## Acceptance Criteria

- **Given/When/Then (Gherkin)**: Writing BDD-style criteria that QA can convert directly to automated tests.
- **Boundary Value Analysis**: Identifying edge cases at the limits of valid input ranges.
- **Equivalence Partitioning**: Grouping inputs into classes that should behave identically to avoid redundant test cases.
- **Definition of Done**: Collaborating with the team to define when a story is truly complete (code, tests, documentation, deployment).

## Domain Modelling

- **Glossary Management**: Maintaining a ubiquitous language glossary so developers and stakeholders use identical terminology.
- **Business Process Modelling**: Documenting AS-IS and TO-BE processes using BPMN or simple flowcharts.
- **Data Modelling Basics**: Identifying key entities, their attributes, and relationships at a business level (without prescribing database schema).
- **Bounded Context Mapping**: Working with the Architect to identify where domain boundaries lie.

## Product Strategy

- **Vision & Mission**: Articulating a compelling product vision that aligns the team and inspires stakeholders.
- **OKR Framework**: Defining Objectives (qualitative, inspirational) and Key Results (quantitative, measurable) at company, team, and individual levels.
- **Market Analysis**: Competitor benchmarking, SWOT analysis, and Jobs-to-be-Done (JTBD) framework for understanding user motivations.
- **Product-Market Fit**: Identifying signals of PMF (retention, NPS, organic growth) and pivoting strategy when signals are weak.

## Prioritisation Frameworks

- **MoSCoW**: Must Have, Should Have, Could Have, Won't Have — rapid stakeholder alignment on scope.
- **RICE Scoring**: Reach × Impact × Confidence ÷ Effort — data-driven ranking of backlog items.
- **Kano Model**: Distinguishing between basic expectations, performance features, and delighters.
- **Opportunity Scoring**: Rating features by importance and current satisfaction to find the highest-value gaps.
- **Cost of Delay**: Calculating the financial or strategic cost of deferring a feature to justify prioritisation decisions.

## Backlog Management

- **Epics → Stories → Tasks**: Maintaining a clean hierarchy so every backlog item maps to a business outcome.
- **Definition of Ready (DoR)**: Ensuring stories entering a sprint have clear acceptance criteria, design, and no unresolved dependencies.
- **Definition of Done (DoD)**: Agreeing team-wide standards (code merged, tests passing, documentation updated, deployed to staging).
- **Continuous Grooming**: Weekly backlog refinement sessions to keep the top 2–3 sprints always sprint-ready.
- **Dependency Management**: Surfacing inter-team and third-party dependencies before they become blockers.

## Agile Ceremonies

- **Sprint Planning**: Setting a sprint goal, selecting stories, and confirming team capacity before committing.
- **Daily Standups**: Unblocking the team; surfacing impediments before they compound.
- **Sprint Review**: Demonstrating completed work to stakeholders and gathering feedback.
- **Retrospectives**: Facilitating blameless retrospectives with actionable improvement items (e.g. "Start / Stop / Continue").
- **Roadmap Reviews**: Quarterly roadmap updates with stakeholders, balancing commitments with emerging opportunities.

## Metrics & Analytics

- **Product Metrics**: DAU/MAU, activation rate, retention (Day 1/7/30), churn rate, LTV, NPS.
- **Funnel Analysis**: Identifying drop-off points in the user activation and conversion funnel.
- **A/B Testing**: Designing experiments with clear hypotheses, control/variant split, and minimum detectable effect.
- **Feature Flagging**: Rolling out features incrementally with kill-switch capability.
- **Dashboards**: Building stakeholder-facing dashboards in Mixpanel, Amplitude, or Grafana to track product KPIs.

## Stakeholder Management

- **Executive Communication**: Presenting roadmaps and trade-offs in business terms, not technical detail.
- **Alignment Sessions**: Running structured decision meetings that produce a clear, documented outcome.
- **Negotiation**: Balancing competing stakeholder priorities without sacrificing product coherence.
- **Release Communication**: Writing clear, user-friendly release notes and internal announcements.
- **Feedback Loops**: Closing the loop with stakeholders after their requested feature ships by sharing outcome metrics.
- **Conflict Resolution**: When stakeholders disagree on requirements, surfacing the underlying goals and finding common ground.
- **Written Communication**: Producing clear, jargon-free requirement documents readable by both business and technical audiences.

## Technical Literacy

- **Reading Architecture Diagrams**: Understanding C4 diagrams, sequence diagrams, and ERDs well enough to ask the right questions.
- **API Basics**: Understanding REST, webhooks, and rate limiting to have informed conversations with engineers.
- **Technical Debt Management**: Quantifying the cost of tech debt in terms of developer velocity and advocating for dedicated paydown capacity each sprint.
- **Incident Awareness**: Understanding SLOs, error budgets, and the product impact of reliability incidents.
- **Specification by Example**: Using concrete examples to clarify ambiguous requirements before writing formal criteria.
- **Traceability Matrix**: Linking requirements to stories, stories to tests, and tests to defects for full audit trails.
