# Architecture Design: [Service Name]

**Document Version**: 1.0
**Date**: [YYYY-MM-DD]
**Status**: Design Draft
**Related**: `PRD.md`

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Principles](#2-architecture-principles)
3. [API Design](#3-api-design) (if applicable)
4. [Component Architecture](#4-component-architecture)
5. [Data Flow](#5-data-flow)
6. [Data Architecture](#6-data-architecture) (if applicable)
7. [External Integrations](#7-external-integrations) (if applicable)
8. [Security Architecture](#8-security-architecture) (if applicable)
9. [Configuration](#9-configuration)
10. [Testing Strategy](#10-testing-strategy)
11. [Deployment](#11-deployment)
12. [Success Metrics](#12-success-metrics)
13. [References](#13-references)

**Note**: Technology stack is documented in `[project]/README.md` - no need to duplicate here

---

## 1. System Overview

### 1.1 Purpose

[What does this system do? What business problem does it solve?]

### 1.2 Key Responsibilities

- **[Responsibility 1]**: [Description]
- **[Responsibility 2]**: [Description]
- **[Responsibility 3]**: [Description]
- **[Responsibility 4]**: [Description]

### 1.3 Context Diagram

```
┌─────────────────────────┐
│   [Client System]       │
│                         │
│  - [Capability 1]       │
│  - [Capability 2]       │
└────────────┬────────────┘
             │
             │ [Protocol: HTTPS/JWT]
             │
             v
   ┌──────────────────────────┐
   │   [Your System]          │
   │                          │
   │  - [Capability 1]        │
   │  - [Capability 2]        │
   │  - [Capability 3]        │
   └───────────┬──────────────┘
               │
               │ [Protocol: mTLS/HTTP]
               │
 ┌─────────────┼─────────────┐
 │             │             │
 v             v             v
┌─────────┐ ┌─────────┐ ┌─────────┐
│External │ │External │ │Database │
│Service 1│ │Service 2│ │         │
└─────────┘ └─────────┘ └─────────┘
```

**Client**: [Who calls this system]

**External Dependencies**: [What this system calls]

---

## 2. Architecture Principles

### 2.1 Design Principles

1. **[Principle 1]**: [Description and why important]
2. **[Principle 2]**: [Description and why important]
3. **[Principle 3]**: [Description and why important]
4. **[Principle 4]**: [Description and why important]
5. **[Principle 5]**: [Description and why important]
6. **[Principle 6]**: [Description and why important]

### 2.2 Standards Compliance (if applicable)

[Document relevant ISO, RFC, industry standards]

**Geographic & Language** (if applicable):
- **ISO 3166-1 alpha-2**: Country codes
- **ISO 639-1**: Language codes

**Financial** (if applicable):
- **ISO 4217**: Currency codes
- **ISO 13616**: IBAN validation

**Date/Time**:
- **ISO 8601**: Dates and timestamps

**Data Format**:
- **JSON**: Request/response bodies
- **UTF-8**: Character encoding
- **[naming_convention]**: Field naming

### 2.3 SOLID Principles

Map design to SOLID:
- **Single Responsibility**: [How applied]
- **Open/Closed**: [How applied]
- **Liskov Substitution**: [How applied]
- **Interface Segregation**: [How applied]
- **Dependency Inversion**: [How applied]

---

## 3. API Design (if applicable)

### 3.1 Design Philosophy

- **[Principle 1]**: [e.g., RESTful, resource-based]
- **[Principle 2]**: [e.g., OpenAPI-first, spec-driven]
- **[Principle 3]**: [e.g., Standards-based]
- **[Principle 4]**: [e.g., Type-safe]

### 3.2 Key Endpoints

**[Endpoint Group 1]**:
- `[METHOD] /path` - [Description]
- `[METHOD] /path/{id}` - [Description]

**[Endpoint Group 2]**:
- `[METHOD] /path` - [Description]

### 3.3 Request/Response Standards

**Dates**: ISO 8601 format
```json
{
  "date_from": "2025-01-01",
  "created_at": "2025-12-08T10:00:00Z"
}
```

**[Other Standards]**: [Description]
```json
{
  "example": "value"
}
```

**Error Response**:
```json
{
  "message": "Error message",
  "code": "ERROR_CODE",
  "status": 400
}
```

### 3.4 OpenAPI Specification (if applicable)

Generated code provides:
- [What code is generated]
- [What it provides]

---

## 4. Component Architecture

### 4.1 Layered Architecture

```
┌───────────────────────────────────────┐
│         [Layer Name]                  │
│  - [Component 1]                      │
│  - [Component 2]                      │
└───────────────┬───────────────────────┘
                │
┌───────────────┴───────────────────────┐
│         [Layer Name]                  │
│  - [Component 1]                      │
│  - [Component 2]                      │
└───────────────┬───────────────────────┘
                │
┌───────────────┴───────────────────────┐
│         [Layer Name]                  │
│  - [Component 1]                      │
└───────────────────────────────────────┘
```

### 4.2 Directory Structure

```
apps/[service-name]/
├── cmd/api/main.go              # Entry point
├── app.go                       # Uber Fx wiring
├── PRD.md                       # Product requirements
├── ARCHITECTURE.md              # This document
│
├── internal/
│   ├── config.go                # Environment configuration
│   │
│   ├── domain/                  # [Purpose]
│   │   └── [files]
│   │
│   ├── api/                     # [Purpose]
│   │   ├── handlers/
│   │   └── router.go
│   │
│   ├── services/                # [Purpose]
│   │   └── [files]
│   │
│   └── [other layers]/
│
├── test/                        # Tests
├── go.mod
└── README.md
```

### 4.3 Component Responsibilities

**[Layer 1]**: [Purpose]
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

**[Layer 2]**: [Purpose]
- [Responsibility 1]
- [Responsibility 2]

**[Layer 3]**: [Purpose]
- [Responsibility 1]
- [Responsibility 2]

### 4.4 Implementation Patterns (if needed)

**IMPORTANT**: Keep code examples minimal. Reference `[reference-app]/` instead of full implementations.

**Pattern Name**: [Description]
- [Key responsibility 1]
- [Key responsibility 2]
- **Implementation reference**: See `[reference-app]/[path/to/file]`

---

## 5. Data Flow

### 5.1 [Main Flow Name]

**Description**: [What this flow accomplishes]

```
Step 1: [Description]
  ↓
Step 2: [Description]
  ↓
Step 3: [Description]
  ↓
Result
```

### 5.2 [Complex Flow] (Swimlane)

**Characteristics**: [Flow characteristics]

```
┌─────────────────────────────────────────────────┐
│         [Flow Name] (Swimlane)                  │
└─────────────────────────────────────────────────┘

Client        System        External
──────        ──────        ────────
  │             │              │
  │ 1. Request  │              │
  ├────────────>│              │
  │             │              │
  │             │ 2. Process   │
  │             │              │
  │             │ 3. Call API  │
  │             ├─────────────>│
  │             │              │
  │             │ 4. Response  │
  │             │<─────────────┤
  │             │              │
  │ 5. Result   │              │
  │<────────────┤              │
  │             │              │
```

---

## 6. Data Architecture (if applicable)

### 6.1 Domain Models

**[Entity Name]**:
- **Purpose**: [What business concept it represents]
- **Key Fields**: [Important attributes]
- **Relationships**: [How it relates to other entities]
- **Lifecycle**: [Creation, updates, deletion]

### 6.2 Data Storage

**Storage Type**: [PostgreSQL, S3, in-memory, none]

**Schema** (if database):
- **Tables**: [List of tables]
- **Key Constraints**: [Foreign keys, unique constraints]
- **Indexes**: [Performance-critical indexes]

### 6.3 Repository Pattern (if applicable)

**Purpose**: [Why repositories are used]

**Interface signature** (signatures only, <10 lines):
```go
type [Entity]Repository interface {
    Create(ctx context.Context, entity *domain.[Entity]) error
    GetByID(ctx context.Context, id string) (*domain.[Entity], error)
}
```

**Implementation reference**: See `[reference-app]/internal/store/` for full examples

---

## 7. External Integrations (if applicable)

### 7.1 [External Service Name]

**Purpose**: [Why we integrate]

**Authentication**: [How we authenticate]

**Client Design**:
- **Timeouts**: [Configuration]
- **Retries**: [Strategy]
- **Error Handling**: [Approach]

**Interface signature** (signature only, <10 lines):
```go
type [Service]Client interface {
    [Method](ctx context.Context, params Type) (*Result, error)
}
```

**Implementation reference**: See `[reference-app]/` for full client examples

---

## 8. Security Architecture (if applicable)

### 8.1 Authentication & Authorization

**Authentication Method**: [JWT, API keys, mTLS, none]

**Authorization**: [Role-based, scope-based, none]

### 8.2 Data Security

**Encryption at Rest**: [What data, how encrypted]

**Encryption in Transit**: [TLS configuration]

**Secrets Management**: [How secrets stored/accessed]

### 8.3 Security Best Practices

- **[Practice 1]**: [Description]
- **[Practice 2]**: [Description]

---

## 9. Configuration

### 9.1 Environment Variables

**Required Variables**:
```bash
PORT=3000                    # REQUIRED: Service port (AWS requirement)
LOG_LEVEL=info              # Logging verbosity
[VAR_NAME]=[default]        # [Description]
```

**AWS Auto-Provided** (when deployed to AWS):
```bash
SERVICE_NAME=[service]
STAGE=[dev/test/prod]
ALLIANCE=[your-project]
AWS_REGION=[eu-north-1]
SERVICE_URL=https://[service].[domain]
```

### 9.2 Secrets (if applicable)

**Location**: AWS Parameter Store or Secrets Manager

```
/svc/[service]/
├── [secret_name]           # [Description]
└── [secret_name]           # [Description]
```

---

## 10. Testing Strategy

### 10.1 Unit Tests

**Pattern**: [e.g., Table-driven tests]

**Coverage**: [e.g., >80% for business logic]

**Example**:
```go
func Test[Function](t *testing.T) {
    tests := []struct {
        name     string
        input    Type
        expected Type
    }{
        {"case 1", input1, expected1},
        {"case 2", input2, expected2},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Function(tt.input)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

### 10.2 Component Tests

**Purpose**: [What component tests verify]

**Pattern**: [Testing approach]

**Execution**: [Expected runtime]

### 10.3 Integration Tests (if applicable)

**Scope**: [What integration tests cover]

**Dependencies**: [What needs to run: Docker, mock services, etc.]

---

## 11. Deployment

**Infrastructure**: See `[infrastructure-repo]/README.md` for deployment standards

### 11.1 Local Development

**Running Locally**:
```bash
go run cmd/api/main.go
```

**Dependencies**: [What needs to be running]

### 11.2 Docker

**Build**:
```bash
docker build -t [service] .
```

**Run**:
```bash
docker run -p 3000:3000 [service]
```

### 11.3 AWS Deployment

**Key Requirements**:
- **Platform**: ECS Fargate ([region])
- **Health Endpoints**: `/health`, `/ready`
- **Port**: 3000 (REQUIRED)
- **Auto-scaling**: [Configuration]
- **Monitoring**: AppSignal + CloudWatch

**CI/CD**: GitHub Actions ([deployment strategy])

---

## 12. Success Metrics

| Metric | Target |
|--------|--------|
| [Metric 1] | [Target value] |
| [Metric 2] | [Target value] |
| [Metric 3] | [Target value] |

---

## 13. References

- **PRD.md**: Product requirements
- **[project]/README.md**: Monorepo tech stack and standards
- **[shared-lib]**: Shared framework
- **[reference-app]/**: Reference implementation patterns
- **[External Spec]**: [URL to specification]
- **[Standard]**: [URL to standard documentation]

---

**Document Status**: [Design Draft / Design Approved]

**Next Steps**: [What happens after architecture approval]
