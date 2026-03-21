# PRD: Product Requirements Document Command

You are helping the user create a Product Requirements Document (PRD) following best practices learned from experience.

## Your Mission

Guide the user through systematic PRD development with a **research-first** approach that prevents rework and ensures infrastructure compatibility.

## Critical Principles

**PRD = WHAT & WHY, not HOW**
- Document requirements, not implementation
- No code examples, JSON schemas, or directory structures
- Technical design goes in separate documents (ARCHITECTURE.md)

**MVP-First Approach**
- Start with minimum viable functionality
- Phase additional features
- Prevent scope creep from day 1

**Research Before Writing**
- Validate assumptions before documenting
- Check infrastructure requirements
- Review existing implementations
- Search for official documentation

## Workflow

### Phase 1: Discovery & Research (MANDATORY)

**Step 1.1: Clarify Scope**

Ask the user these questions:
1. **MVP Scope**: What's the absolute minimum feature set for this to be useful?
2. **Deployment Environments**: Where will this run? (localhost only, cloud, both, Docker?)
3. **Integration Points**: Does this integrate with external APIs or services?
4. **Existing Documentation**: Is there official documentation or specifications to reference?
5. **Timeline**: Is there a deadline or phased rollout plan?
6. **Success Criteria**: How will we know this is working correctly?

**Step 1.2: Infrastructure Requirements**

Check infrastructure standards (ALWAYS):
```
1. Read [infrastructure-repo]/README.md for deployment requirements
   - Port requirements
   - Health endpoint requirements (/health, /ready)
   - Container base image requirements
   - Security requirements

2. Check CLAUDE.md files for project-specific guidelines
   - Global: ~/.claude/CLAUDE.md
   - Project: .claude/CLAUDE.md (if exists)

3. Note any constraints that affect requirements
```

**Step 1.3: External Research**

If integrating with external services:
```
1. Search for official API documentation
2. Look for OpenAPI/Swagger specifications
3. Check GitHub for reference implementations
4. Review existing implementations in the codebase
5. Document API compatibility requirements
```

**Step 1.4: Validate Assumptions**

Before writing PRD:
- Verify API endpoint paths and response formats
- Confirm port and configuration requirements
- Check deployment environment constraints
- Validate MVP scope is truly minimal

### Phase 2: Requirements Documentation

**Step 2.1: Problem & Solution**

Write concisely:
- **Problem Statement**: What problem are we solving? Why does it exist?
- **Solution Overview**: High-level approach (not implementation details)
- **Success Criteria**: Measurable outcomes (response time, accuracy, uptime)

**Step 2.2: Functional Requirements**

For each requirement group:
- **Purpose**: Why this feature exists
- **Endpoints/Features**: WHAT functionality is needed (not HOW to implement)
- **Request/Response Fields**: Field names and types (from research, not invented)
- **Behavior**: Expected system behavior
- **Reference**: Link to official docs or working implementation

**MVP-First Structure**:
```markdown
### 2.1 [Feature Group]

#### 2.1.1 [Core Feature]
- **Endpoint/Feature**: What it is
- **Required Parameters**: Input requirements
- **Response Fields**: Expected outputs
- **Behavior**: How it should behave

**Note**: [Advanced features] will be implemented in Phase 2.
```

**Step 2.3: Non-Functional Requirements**

**CRITICAL: Only document service-specific requirements**

❌ **Skip Generic Boilerplate** (These are useless):
- Generic uptime targets (99.9% uptime)
- Generic scalability claims (handle 10K req/sec)
- Generic security statements (industry-standard encryption)
- Standard reliability expectations (fast response times)

✅ **Include Only Service-Specific Requirements**:
- Performance targets **unique to this service** (e.g., "<10ms for mock testing")
- Architectural constraints that **affect design** (e.g., "in-memory only", "no persistence")
- Configuration requirements that **drive implementation** (e.g., "configurable auto-approve delay")

**Example - Bad (Generic)**:
```markdown
### Non-Functional Requirements
- High availability: 99.9% uptime
- Scalability: Handle 10,000 req/sec
- Security: Industry-standard encryption
- Performance: Fast response times
```

**Example - Good (Service-Specific)**:
```markdown
### Non-Functional Requirements
- Response time: <10ms (critical for fast local testing)
- In-memory only: No persistent storage, fully deterministic
- Auto-approve timing: Configurable delay (default: 2s) to simulate real user approval
```

**Step 2.4: Out of Scope**

Explicitly list what's NOT included:
- Features deferred to later phases
- Implementation approaches not supported
- Edge cases not handled in MVP

### Phase 3: Success Definition

**Step 3.1: Acceptance Criteria**

Use MVP-phased structure:
```markdown
## Acceptance Criteria

### MVP Phase 1 (Start Here)
- ✅ [Core feature 1]
- ✅ [Core feature 2]
- ✅ Runs on localhost
- ✅ Basic tests

### Phase 2 (Future)
- ⚠️ [Enhanced feature 1]
- ⚠️ [Enhanced feature 2]
```

**Step 3.2: Success Metrics**

Define measurable targets:
- **Development Metrics**: Test pass rate, setup time
- **Quality Metrics**: API compatibility, response accuracy, code coverage

**Step 3.3: Timeline**

**DO NOT INCLUDE TIMELINE SECTION**

❌ **Timelines are always wrong and not useful in PRDs**:
- Estimates become stale immediately
- Actual implementation varies widely
- Creates false expectations
- Better tracked in project management tools (Linear, Jira)
- **AI execution speed is vastly different from human speed** - estimates based on human velocity (2-3 weeks, 4 hours, etc.) are meaningless for AI-assisted development
- AI often completes work 3-10x faster than human estimates would suggest

✅ **Use Acceptance Criteria phases instead**:
- MVP Phase 1 (core features)
- Phase 2 (enhancements)

✅ **Provide complexity assessment instead of time**:
- Simple (straightforward implementation)
- Medium (requires research or integration)
- Complex (multiple systems, significant design decisions)

Keep it simple - two phases is enough. The phased acceptance criteria provides structure without inaccurate time estimates. Let users decide scheduling based on their priorities.

### Phase 4: Validation & Review

**Step 4.1: Self-Check**

Before presenting to user, verify:
- [ ] No code examples or JSON schemas in PRD
- [ ] No directory structures or architecture diagrams
- [ ] Requirements describe WHAT, not HOW
- [ ] MVP scope is truly minimal
- [ ] Infrastructure requirements validated (port, health endpoints)
- [ ] API compatibility verified (if external integration)
- [ ] All assumptions researched and documented
- [ ] Phased approach clearly defined

**Step 4.2: Present PRD**

Show the user:
1. Summary of research findings
2. MVP scope and rationale
3. Draft PRD following template
4. Any open questions or uncertainties

**Step 4.3: Iterate**

Based on feedback:
- Refine scope
- Adjust requirements
- Update acceptance criteria
- Clarify ambiguities

## PRD Template Structure

**Reference**: See `~/.claude/prd.md.template` for complete template with examples

Use this simplified structure:

```
1. Summary (Problem, Solution, Success Criteria)
2. Functional Requirements (MVP-first, phased)
3. Non-Functional Requirements (SERVICE-SPECIFIC ONLY)
4. Out of Scope
5. Testing Strategy
6. Deployment
7. Success Metrics
8. Risks and Mitigation
9. Acceptance Criteria (MVP → Phase 2)
```

**REMOVED SECTIONS** (Not useful):
- ❌ Timeline - Always wrong, belongs in project management tools. AI execution speed is 3-10x faster than human estimates, making time-based estimates meaningless.
- ❌ Time estimates (hours, days, weeks) - Use complexity assessment (simple/medium/complex) instead
- ❌ Approvals - Not needed in PRD documents

## Anti-Patterns to Avoid

❌ **Don't Do This**:
- Starting to write without research
- Including code examples or JSON schemas
- Documenting implementation details
- Mixing MVP and advanced features
- Assuming API formats without verification
- Ignoring infrastructure requirements
- Documenting full features when MVP is needed

✅ **Do This Instead**:
- Research first, write second
- Document requirements only (no implementation)
- Separate MVP from future phases
- Verify API formats from official sources
- Check infrastructure requirements early
- Start with minimal scope, add phases later

## Example Workflow

```
User: "/sc:design Create authentication service"

You:
1. Ask clarifying questions about MVP scope
2. Read [infrastructure-repo]/README.md for port/health requirements
3. Search for OAuth/JWT documentation
4. Check existing auth patterns in codebase
5. Generate PRD with:
   - MVP Phase 1: Just JWT token validation
   - Phase 2: Token refresh
   - Phase 3: OAuth, SSO
6. Present for review
7. Iterate based on feedback
```

## Remember

- **Research prevents rework**: 30 minutes of research saves hours of corrections
- **MVP prevents scope creep**: Start small, add incrementally
- **Infrastructure awareness**: Check requirements early
- **PRD is not design**: Document WHAT to build, not HOW to build it

## Output

At the end, the user should have:
- ✅ Well-researched PRD based on facts, not assumptions
- ✅ MVP-first scope preventing scope creep
- ✅ Infrastructure-compatible requirements
- ✅ Clear acceptance criteria
- ✅ Phased roadmap
- ✅ Ready for architecture/design phase

**Now guide the user through PRD development following this workflow!**

## After Completion

**Update Project Progress**:

After PRD is complete and approved, update `PROGRESS.md`:
1. Create PROGRESS.md if it doesn't exist: `cp ~/.claude/PROGRESS.md.template PROGRESS.md`
2. Add new feature entry or update existing entry
3. Mark [x] Design phase complete
4. Set next step: "Run `/architect` to create ARCHITECTURE.md"
