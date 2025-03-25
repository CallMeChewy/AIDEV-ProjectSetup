# STANDARD-DatabaseSchema
**Created: March 22, 2025 3:15 PM**
**Last Modified: March 22, 2025  3:15PM**

[Context: Technical_Standards]
[Status: Active]
[Version: 1.0]

## 1. Overview

This document defines the standards for database schema design across Project Himalaya components. It covers naming conventions, structure principles, and implementation guidelines for the three-tier database architecture.

## 2. Three-Tier Database Architecture

### 2.1 Himalaya Core Database

**Purpose**: Store shared data and cross-project information
**File Name**: `himalaya-core.db`
**Scope**: Available to all Project Himalaya components

**Core ### 7.2 Schema Documentation Format

Each schema definition must be accompanied by documentation:

```
Table: document
Purpose: Stores document content and metadata
Core Entity: Yes

Columns:
- document_id (TEXT): Unique identifier for the document
- title (TEXT): Document title
- content_type (TEXT): MIME type or format of the document
- content (TEXT): Actual document content
- created_at (TEXT): ISO 8601 timestamp of creation
- created_by (TEXT): User or system that created the document
- updated_at (TEXT): ISO 8601 timestamp of last update
- updated_by (TEXT): User or system that last updated the document
- version (INTEGER): Document version number
- is_active (INTEGER): Soft deletion flag (1=active, 0=deleted)
- metadata_json (TEXT): JSON object containing document metadata

Indexes:
- idx_document_created_at: For sorting by creation date
- idx_document_updated_at: For sorting by update date
- idx_document_title: For searching by title

Notes:
- metadata_json must be valid JSON or NULL
- content_type should follow standard MIME type format
```

## 8. Himalaya Core Database Schema

The following tables represent the minimum required schema for the Himalaya Core Database:

### 8.1 Projects Table

```sql
CREATE TABLE IF NOT EXISTS project (
    project_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    
    -- Constraints
    UNIQUE(name)
);
```

### 8.2 Components Table

```sql
CREATE TABLE IF NOT EXISTS component (
    component_id TEXT PRIMARY KEY,
    project_id_fk TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    layer INTEGER NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    
    -- Constraints
    FOREIGN KEY (project_id_fk) REFERENCES project(project_id),
    UNIQUE(project_id_fk, name)
);
```

### 8.3 Standards Table

```sql
CREATE TABLE IF NOT EXISTS standard (
    standard_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    description TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    
    -- Constraints
    UNIQUE(name, version)
);
```

### 8.4 Validation Rules Table

```sql
CREATE TABLE IF NOT EXISTS validation_rule (
    rule_id TEXT PRIMARY KEY,
    standard_id_fk TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    rule_pattern TEXT NOT NULL,
    severity TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    
    -- Constraints
    FOREIGN KEY (standard_id_fk) REFERENCES standard(standard_id),
    UNIQUE(standard_id_fk, name)
);
```

## 9. Project-Specific Database Example

The following represents a starter schema for a project-specific database:

### 9.1 Project Configuration Table

```sql
CREATE TABLE IF NOT EXISTS project_config (
    config_id TEXT PRIMARY KEY,
    config_key TEXT NOT NULL,
    config_value TEXT NOT NULL,
    config_type TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    -- Constraints
    UNIQUE(config_key)
);
```

### 9.2 Project Components Table

```sql
CREATE TABLE IF NOT EXISTS project_component (
    component_id TEXT PRIMARY KEY,
    component_name TEXT NOT NULL,
    component_type TEXT NOT NULL,
    status TEXT NOT NULL,
    version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    -- Constraints
    UNIQUE(component_name)
);
```

### 9.3 Operational Data Example

```sql
CREATE TABLE IF NOT EXISTS document_metadata (
    metadata_id TEXT PRIMARY KEY,
    document_id_fk TEXT NOT NULL,
    context TEXT NOT NULL,
    component TEXT,
    status TEXT NOT NULL,
    version TEXT NOT NULL,
    tags TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    -- Constraints
    UNIQUE(document_id_fk)
);
```

## 10. Migration and Versioning

### 10.1 Schema Migration Format

Schema migrations should be defined as numbered SQL scripts:

```
001_initial_schema.sql
002_add_tags_table.sql
003_modify_document_table.sql
```

Each migration script should:

1. Begin with a version update:
   ```sql
   INSERT INTO schema_version (version, applied_at, description)
   VALUES (1, datetime('now'), 'Initial schema creation');
   ```

2. Include all schema changes:
   ```sql
   CREATE TABLE ...
   ALTER TABLE ...
   ```

3. Be idempotent when possible:
   ```sql
   CREATE TABLE IF NOT EXISTS ...
   ```

### 10.2 Migration Application Process

1. Check current schema version:
   ```sql
   SELECT max(version) FROM schema_version;
   ```

2. Apply each missing migration in sequence
3. Verify schema integrity after migration
4. Document any manual data transformations needed

## 11. References

- [20-30] STANDARD-FoundationDesignPrinciples
- [50-10] IMPL-DocumentManager
- SQLite Documentation: https://www.sqlite.org/docs.html
- PEP 249 – Python Database API Specification v2.0

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowerss**:
- `projects`: Register of all projects
- `components`: Component catalog
- `standards`: Standards definitions
- `validation_rules`: Shared validation rules
- `global_config`: System-wide configuration
- `users`: User profiles (if applicable)

### 2.2 Project-Specific Databases

**Purpose**: Store data specific to a single project
**File Name**: `[ProjectName].db` (e.g., `aidev-validate.db`)
**Scope**: Limited to the specific project

**Core Tables**:
- `project_config`: Project-specific configuration
- `project_components`: Project component instances
- `operational_data`: Project-specific data tables
- `project_logs`: Operation and activity logs

### 2.3 User Help System Database

**Purpose**: Store user-facing help content and usage data
**File Name**: `[ProjectName]-help.db` (e.g., `aidev-validate-help.db`)
**Scope**: User interface layer

**Core Tables**:
- `help_topics`: Help documentation entries
- `usage_logs`: User interaction logs
- `diagnostics`: System diagnostics data
- `feedback`: User feedback information

## 3. Naming Conventions

### 3.1 Database Files

- Use lowercase hyphenated names for database files
- Include project name for project-specific databases
- Use `.db` extension for SQLite databases

Examples:
- `himalaya-core.db`
- `aidev-validate.db`
- `ollama-model-editor.db`

### 3.2 Table Names

- Use lowercase snake_case for table names
- Use singular nouns for entity tables
- Use plural nouns for collection tables
- Use descriptive prefixes to group related tables

Examples:
- `document` (entity table)
- `validation_rules` (collection table)
- `doc_versions` (prefixed related table)
- `user_preferences` (prefixed related table)

### 3.3 Column Names

- Use lowercase snake_case for column names
- Include table name as prefix for ID columns
- Use standard suffixes for common column types
- Include data type hints for non-obvious types

Examples:
- `document_id` (primary key)
- `created_at` (timestamp)
- `is_active` (boolean)
- `user_id_fk` (foreign key)
- `config_json` (JSON data)

### 3.4 Index Names

- Use `idx_` prefix for regular indexes
- Use `unq_` prefix for unique indexes
- Use `fk_` prefix for foreign key constraints
- Include table name and indexed columns

Examples:
- `idx_document_created_at` (index on created_at)
- `unq_user_email` (unique constraint on email)
- `fk_document_user_id` (foreign key to user table)

## 4. Data Types and Constraints

### 4.1 Primary Data Types

| Logical Type | SQLite Type | Description | Example |
|--------------|-------------|-------------|---------|
| Integer | INTEGER | Whole numbers | `user_id INTEGER PRIMARY KEY` |
| String | TEXT | Text of any length | `name TEXT NOT NULL` |
| Boolean | INTEGER | 0 (false) or 1 (true) | `is_active INTEGER NOT NULL` |
| Float | REAL | Floating point numbers | `price REAL DEFAULT 0.0` |
| DateTime | TEXT | ISO 8601 format | `created_at TEXT` |
| Enumeration | TEXT | Constrained text values | `status TEXT CHECK(status IN ('draft','active','archived'))` |
| JSON | TEXT | JSON formatted data | `metadata TEXT` |
| UUID | TEXT | Universal unique identifier | `session_id TEXT` |

### 4.2 Constraints

All tables must include appropriate constraints:

- **Primary Keys**: Every table must have a primary key
- **Foreign Keys**: Use foreign key constraints for relationships
- **Not Null**: Apply to required fields
- **Default Values**: Provide sensible defaults when appropriate
- **Check Constraints**: Enforce value ranges and enumerations
- **Unique Constraints**: Apply to fields that must be unique

### 4.3 NULL Handling

- Avoid NULL values when possible
- Provide default values for nullable fields
- Document fields where NULL has specific meaning
- Use empty strings instead of NULL for text fields
- Use 0 instead of NULL for numeric fields when appropriate

## 5. Schema Structure

### 5.1 Table Organization

Organize tables by entity type and relationship:

1. **Core Entities**: Primary business objects
2. **Supporting Entities**: Objects that relate to core entities
3. **Junction Tables**: For many-to-many relationships
4. **Configuration Tables**: For system or component configuration
5. **Log Tables**: For activity tracking and history

### 5.2 Required Metadata Columns

All entity tables should include these standard columns:

- `[table_name]_id`: Primary key (INTEGER or TEXT for UUID)
- `created_at`: Creation timestamp (TEXT in ISO 8601)
- `created_by`: User or system that created the record (TEXT)
- `updated_at`: Last update timestamp (TEXT in ISO 8601)
- `updated_by`: User or system that last updated the record (TEXT)
- `version`: Record version number (INTEGER, starting at 1)
- `is_active`: Soft deletion flag (INTEGER, 0 or 1)

### 5.3 Relationship Pattern

For one-to-many relationships:
- Add foreign key in the "many" table referencing the "one" table
- Name the column `[referenced_table]_id_fk`
- Add appropriate indexes on foreign key columns

For many-to-many relationships:
- Create a junction table named `[table1]_[table2]`
- Include foreign keys to both tables
- Add a composite primary key across both foreign keys
- Consider adding metadata about the relationship

## 6. Implementation Guidelines

### 6.1 SQLite Best Practices

- Enable foreign key constraints:
  ```sql
  PRAGMA foreign_keys = ON;
  ```
- Use transactions for multi-statement operations:
  ```sql
  BEGIN TRANSACTION;
  -- Operations here
  COMMIT;
  ```
- Create proper indexes for query optimization
- Use prepared statements for all queries
- Implement proper error handling and retry logic

### 6.2 Schema Versioning

- Include a `schema_version` table in each database:
  ```sql
  CREATE TABLE schema_version (
      version INTEGER PRIMARY KEY,
      applied_at TEXT NOT NULL,
      description TEXT NOT NULL
  );
  ```
- Create migration scripts for schema updates
- Version your schema changes incrementally
- Document all schema changes

### 6.3 Data Access Layer

- Implement a data access layer (DAL) for each database
- Use the repository pattern to abstract database operations
- Centralize SQL queries in the DAL
- Implement proper connection management
- Use parameterized queries to prevent SQL injection

## 7. Database Schema Definition

### 7.1 Schema Definition Format

Define all database schemas using SQL DDL statements:

```sql
-- Table: document
CREATE TABLE IF NOT EXISTS document (
    document_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    is_active INTEGER NOT NULL DEFAULT 1,
    
    -- Metadata
    metadata_json TEXT,
    
    -- Validation
    CHECK (json_valid(metadata_json) OR metadata_json IS NULL)
);

-- Indexes
CREATE INDEX idx_document_created_at ON document(created_at);
CREATE INDEX idx_document_updated_at ON document(updated_at);
CREATE INDEX idx_document_title ON document(title);
```

### 7.2 Schema Documentation Format

Each schema definition must be accompanied by documentation:

```
Table