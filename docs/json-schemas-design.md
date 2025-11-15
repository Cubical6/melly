# Melly JSON Schema Architecture Design

**Version**: 1.0.0
**Date**: 2025-11-15
**Status**: Schema Design Complete - Ready for Implementation

---

## Executive Summary

This document defines the complete JSON schema architecture for the Melly C4 model workflow. The schema design supports:
- **Progressive abstraction** from repositories → systems → containers → components
- **Incremental updates** via timestamp-based change detection
- **Parallel processing** through independent entity tracking
- **Referential integrity** via parent timestamp references
- **Validation-ready** structures with clear constraints

---

## Table of Contents

1. [Common Patterns Across All Schemas](#1-common-patterns-across-all-schemas)
2. [init.json Schema](#2-initjson-schema)
3. [c1-systems.json Schema](#3-c1-systemsjson-schema)
4. [c2-containers.json Schema](#4-c2-containersjson-schema)
5. [c3-components.json Schema](#5-c3-componentsjson-schema)
6. [Key Design Decisions](#6-key-design-decisions)
7. [Schema Evolution Strategy](#7-schema-evolution-strategy)
8. [Validation Strategy](#8-validation-strategy)
9. [Implementation Recommendations](#9-implementation-recommendations)

---

## 1. Common Patterns Across All Schemas

### 1.1 Metadata Section (Required in all schemas)

```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "generator": "melly-workflow",
    "generated_by": "c4model-explorer",
    "timestamp": "2025-11-15T20:00:00.000Z",
    "melly_version": "1.0.0",
    "parent_timestamp": "2025-11-15T19:00:00.000Z"
  }
}
```

**Fields:**
- `schema_version` (string, required): Version of JSON schema (semver format)
- `generator` (string, required): Always "melly-workflow"
- `generated_by` (string, required): Agent/command that created this file
- `timestamp` (string, required): ISO 8601 format with milliseconds and UTC timezone
- `melly_version` (string, required): Version of Melly that created this file
- `parent_timestamp` (string, optional): Timestamp of parent JSON file (for dependency tracking)

**Design Rationale:**
- ISO 8601 with milliseconds provides precise ordering for incremental updates
- `parent_timestamp` enables timestamp ordering validation
- `generator` and `generated_by` provide traceability for debugging
- `schema_version` enables schema evolution and migration

### 1.2 Timestamp Format

**Standard:** ISO 8601 extended format with UTC timezone
**Pattern:** `YYYY-MM-DDTHH:mm:ss.sssZ`
**Example:** `2025-11-15T20:30:45.123Z`

**Validation Rules:**
- Must be valid ISO 8601 datetime
- Must include timezone (Z or +HH:mm)
- Must be in UTC (Z timezone)
- Should include milliseconds for precision
- Child timestamp must be > parent timestamp

### 1.3 ID/Naming Conventions

**Entity IDs:**
- Format: `kebab-case`
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Examples: `web-app`, `backend-api`, `auth-component`

**Rationale:**
- Kebab-case is URL-safe, filesystem-safe, and human-readable
- Lowercase prevents case-sensitivity issues across platforms
- No special characters simplifies reference resolution

### 1.4 Observations Format (Common to all levels)

See **[observations-relations-schema.md](./observations-relations-schema.md)** for complete specification.

**Summary Structure:**
```json
{
  "observations": [
    {
      "id": "obs-001",
      "category": "architecture|technology|security|performance|quality|pattern",
      "severity": "info|warning|critical",
      "description": "Human-readable observation",
      "evidence": {
        "type": "file|code|config|metric|pattern",
        "location": "path/to/file",
        "snippet": "code excerpt"
      },
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

### 1.5 Relations Format (Common to all levels)

See **[observations-relations-schema.md](./observations-relations-schema.md)** for complete specification.

**Summary Structure:**
```json
{
  "relations": [
    {
      "id": "rel-001",
      "source": "entity-id",
      "target": "entity-id",
      "type": "http-rest|grpc|database-query|dependency|...",
      "direction": "unidirectional|bidirectional",
      "description": "Relationship description",
      "protocol": {
        "method": "GET, POST",
        "endpoint": "/api/v1/*",
        "format": "JSON",
        "authentication": "JWT"
      },
      "strength": "weak|moderate|strong"
    }
  ]
}
```

---

## 2. init.json Schema

### 2.1 Purpose

Captures repository metadata, package manifests, and directory structure to enable subsequent abstraction phases.

### 2.2 Complete JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "repositories", "summary"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["schema_version", "generator", "generated_by", "timestamp", "melly_version"],
      "properties": {
        "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
        "generator": { "type": "string", "const": "melly-workflow" },
        "generated_by": { "type": "string", "const": "c4model-explorer" },
        "timestamp": { "type": "string", "format": "date-time" },
        "melly_version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" }
      }
    },
    "repositories": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "name", "path", "type", "manifests", "structure"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$"
          },
          "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "path": {
            "type": "string",
            "description": "Absolute path to repository"
          },
          "type": {
            "type": "string",
            "enum": ["monorepo", "single", "microservice", "library", "unknown"]
          },
          "git": {
            "type": "object",
            "properties": {
              "remote_url": { "type": "string" },
              "branch": { "type": "string" },
              "commit_hash": { "type": "string", "pattern": "^[a-f0-9]{7,40}$" },
              "is_dirty": { "type": "boolean" }
            }
          },
          "manifests": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["type", "path", "data"],
              "properties": {
                "type": {
                  "type": "string",
                  "enum": ["npm", "composer", "cargo", "go-mod", "gradle", "maven", "requirements-txt", "pyproject-toml", "gemfile", "unknown"]
                },
                "path": {
                  "type": "string",
                  "description": "Relative path from repository root"
                },
                "data": {
                  "type": "object",
                  "description": "Parsed manifest content",
                  "properties": {
                    "name": { "type": "string" },
                    "version": { "type": "string" },
                    "dependencies": { "type": "object" },
                    "dev_dependencies": { "type": "object" },
                    "scripts": { "type": "object" },
                    "metadata": { "type": "object" }
                  }
                }
              }
            }
          },
          "structure": {
            "type": "object",
            "description": "Directory structure organized by purpose",
            "properties": {
              "source_dirs": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Source code directories"
              },
              "test_dirs": {
                "type": "array",
                "items": { "type": "string" }
              },
              "config_files": {
                "type": "array",
                "items": { "type": "string" }
              },
              "build_dirs": {
                "type": "array",
                "items": { "type": "string" }
              },
              "docs_dirs": {
                "type": "array",
                "items": { "type": "string" }
              },
              "entry_points": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "file": { "type": "string" },
                    "type": { "type": "string", "enum": ["main", "cli", "server", "worker", "test"] }
                  }
                }
              }
            }
          },
          "technology": {
            "type": "object",
            "properties": {
              "primary_language": { "type": "string" },
              "languages": {
                "type": "array",
                "items": { "type": "string" }
              },
              "frameworks": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": { "type": "string" },
                    "version": { "type": "string" },
                    "category": { "type": "string", "enum": ["web", "testing", "build", "orm", "ui", "other"] }
                  }
                }
              },
              "runtime": {
                "type": "object",
                "properties": {
                  "environment": { "type": "string" },
                  "version": { "type": "string" }
                }
              }
            }
          },
          "metrics": {
            "type": "object",
            "properties": {
              "total_files": { "type": "integer", "minimum": 0 },
              "source_files": { "type": "integer", "minimum": 0 },
              "lines_of_code": { "type": "integer", "minimum": 0 },
              "test_coverage": { "type": "number", "minimum": 0, "maximum": 100 },
              "last_commit_date": { "type": "string", "format": "date-time" }
            }
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "required": ["total_repositories", "repository_types"],
      "properties": {
        "total_repositories": { "type": "integer", "minimum": 1 },
        "repository_types": {
          "type": "object",
          "properties": {
            "monorepo": { "type": "integer", "minimum": 0 },
            "single": { "type": "integer", "minimum": 0 },
            "microservice": { "type": "integer", "minimum": 0 },
            "library": { "type": "integer", "minimum": 0 },
            "unknown": { "type": "integer", "minimum": 0 }
          }
        },
        "languages": {
          "type": "array",
          "items": { "type": "string" }
        },
        "total_manifests": { "type": "integer", "minimum": 0 }
      }
    }
  }
}
```

### 2.3 Design Decisions

**Repository Type Classification:**
- `monorepo`: Multiple packages in one repo (e.g., Nx, Lerna)
- `single`: Standard single-purpose repository
- `microservice`: Small service in microservice architecture
- `library`: Reusable package/library
- `unknown`: Cannot determine type

**Manifest Parsing:**
- Standardized `data` structure across manifest types
- Preserves original manifest information
- Enables dependency analysis and technology detection

**Structure Organization:**
- Categorizes directories by purpose (not just listing all)
- Entry points help identify application boundaries
- Supports polyglot repositories

---

## 3. c1-systems.json Schema

### 3.1 Purpose

Identifies C1-level systems, their boundaries, actors, and high-level relationships.

### 3.2 Complete JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "systems", "actors", "summary"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["schema_version", "generator", "generated_by", "timestamp", "melly_version", "parent_timestamp"],
      "properties": {
        "schema_version": { "type": "string" },
        "generator": { "type": "string", "const": "melly-workflow" },
        "generated_by": { "type": "string", "const": "c1-abstractor" },
        "timestamp": { "type": "string", "format": "date-time" },
        "melly_version": { "type": "string" },
        "parent_timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp from init.json"
        }
      }
    },
    "systems": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "repositories", "description", "observations", "relations"],
        "properties": {
          "id": { "type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$" },
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["web-application", "mobile-application", "desktop-application", "api-service", "database", "message-broker", "cache", "cdn", "external-service", "user-facing", "internal-service", "data-store", "integration", "other"]
          },
          "description": { "type": "string", "maxLength": 1000 },
          "repositories": {
            "type": "array",
            "minItems": 1,
            "items": { "type": "string" }
          },
          "boundaries": {
            "type": "object",
            "properties": {
              "scope": { "type": "string", "enum": ["internal", "external", "hybrid"] },
              "deployment": { "type": "string", "enum": ["on-premise", "cloud", "hybrid", "saas", "unknown"] },
              "network": { "type": "string", "enum": ["public", "private", "dmz", "unknown"] }
            }
          },
          "responsibilities": {
            "type": "array",
            "items": { "type": "string" }
          },
          "observations": {
            "type": "array",
            "description": "See observations-relations-schema.md"
          },
          "relations": {
            "type": "array",
            "description": "See observations-relations-schema.md"
          }
        }
      }
    },
    "actors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type"],
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "type": { "type": "string", "enum": ["user", "admin", "system", "service", "external-actor"] },
          "description": { "type": "string" },
          "interacts_with": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "required": ["total_systems", "system_types"],
      "properties": {
        "total_systems": { "type": "integer", "minimum": 1 },
        "total_actors": { "type": "integer", "minimum": 0 },
        "system_types": { "type": "object" },
        "total_observations": { "type": "integer", "minimum": 0 },
        "total_relations": { "type": "integer", "minimum": 0 }
      }
    }
  }
}
```

### 3.3 Design Decisions

**System Types:**
- Comprehensive taxonomy for common system patterns
- External services explicitly identified
- User-facing vs internal distinction

**Boundaries Object:**
- `scope`: Ownership and control
- `deployment`: Hosting model
- `network`: Network accessibility

**Actors:**
- Separate from systems for clarity
- Links to systems via `interacts_with`

---

## 4. c2-containers.json Schema

### 4.1 Purpose

Identifies C2-level containers (deployable/runnable units) within each system.

### 4.2 Key Fields

```json
{
  "containers": [
    {
      "id": "string",
      "name": "string",
      "system_id": "string (references c1-systems.json)",
      "type": "web-server|application-server|spa-client|database|cache|...",
      "technology": {
        "stack": "React 18 + TypeScript",
        "language": "TypeScript",
        "framework": "React",
        "libraries": [...]
      },
      "runtime": {
        "environment": "Browser|Node.js|JVM|...",
        "platform": "linux|windows|browser|...",
        "container_technology": "docker|kubernetes|...",
        "deployment_model": "standalone|replicated|..."
      },
      "observations": [...],
      "relations": [...]
    }
  ]
}
```

### 4.3 Design Decisions

**Technology Object:**
- Comprehensive stack description
- Libraries array with purpose documentation

**Runtime Object:**
- Environment specifies where container executes
- Container technology for deployment understanding

---

## 5. c3-components.json Schema

### 5.1 Purpose

Identifies C3-level components (logical building blocks) within each container.

### 5.2 Key Fields

```json
{
  "components": [
    {
      "id": "string",
      "name": "string",
      "container_id": "string (references c2-containers.json)",
      "type": "controller|service|repository|model|...",
      "path": "src/components/auth",
      "structure": {
        "files": [...],
        "exports": [...]
      },
      "patterns": [
        {
          "name": "Repository Pattern",
          "category": "design-pattern",
          "description": "..."
        }
      ],
      "metrics": {
        "lines_of_code": 500,
        "cyclomatic_complexity": 8.5,
        "test_coverage": 85.3
      },
      "observations": [...],
      "relations": [...]
    }
  ]
}
```

### 5.3 Design Decisions

**Patterns Array:**
- Explicitly document detected design patterns
- Supports pattern analysis across codebase

**Metrics Object:**
- Code quality metrics
- Objective measurements for refactoring prioritization

---

## 6. Key Design Decisions

### 6.1 Timestamp-Based Incremental Updates

**Decision:** Use ISO 8601 timestamps with millisecond precision

**Rationale:**
- Enables precise ordering of workflow steps
- Supports incremental processing
- Parent timestamp references create dependency chain

**Implementation:**
```javascript
if (child.metadata.parent_timestamp >= child.metadata.timestamp) {
  throw new ValidationError("Child timestamp must be > parent");
}

if (c1_systems.metadata.timestamp > init.metadata.timestamp) {
  // C1 is up-to-date, skip processing
}
```

### 6.2 Progressive Entity References

**Decision:** Each level references parent entities by ID

**Benefits:**
- Can traverse from component → container → system → repository
- Enables validation of referential integrity
- Supports incremental updates per entity

### 6.3 Flexible vs Strict Fields

**Required Fields:**
- Core identification (id, name, type)
- Metadata (timestamp, schema_version)
- Observations and relations arrays (can be empty)

**Optional Fields:**
- Evidence (best-effort)
- Metrics (when available)
- Confidence (for inferred entities)

---

## 7. Schema Evolution Strategy

### 7.1 Version Field

All schemas include `schema_version` following semantic versioning:
- **Major**: Breaking changes
- **Minor**: Additive changes (new optional fields)
- **Patch**: Clarifications, documentation

### 7.2 Migration Path

When schema evolves:
1. Old files validated against old schema
2. Migration script transforms to new schema
3. Both versions supported during transition

---

## 8. Validation Strategy

### 8.1 Validation Layers

**1. JSON Schema Validation** - Structural validation
**2. Business Logic Validation** - Timestamp ordering, referential integrity
**3. Quality Validation** - Observation/relation completeness

See **[validation-requirements.md](./validation-requirements.md)** for complete validation specification.

---

## 9. Implementation Recommendations

### 9.1 Validation First

1. Create schema definitions
2. Build validation scripts
3. Create test fixtures
4. Validate test data
5. Then build agents that generate valid data

### 9.2 Template Usage

Templates should:
- Define structure, not content
- Be used by agents as reference
- Include inline documentation

### 9.3 Error Handling

When validation fails:
- Clear error messages with line numbers
- Suggest corrections
- Link to schema documentation

---

## Conclusion

This JSON schema architecture provides:

✅ **Progressive Abstraction** - Clear hierarchy from repositories → systems → containers → components
✅ **Incremental Updates** - Timestamp-based change detection
✅ **Parallel Processing** - Independent entities processed concurrently
✅ **Referential Integrity** - Parent references and ID linkage
✅ **Evidence-Based Analysis** - Structured observations with supporting evidence
✅ **Validation-Ready** - Clear constraints and validation rules
✅ **Schema Evolution** - Version field and migration strategy

---

**Document Version**: 1.0.0
**Date**: 2025-11-15
**Author**: Melly Architecture Team
