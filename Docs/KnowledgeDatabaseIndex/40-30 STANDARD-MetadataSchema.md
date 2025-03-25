# STANDARD-MetadataSchema
**Created: March 22, 2025 3:45 PM**
**Last Modified: March 22, 2025  3:45PM**

[Context: Knowledge_Organization]
[Status: Active]
[Version: 1.0]

## 1. Overview

This document defines the standard metadata schema for all Project Himalaya documentation. Consistent metadata ensures documents can be properly categorized, searched, and linked within the knowledge management system.

## 2. Document Metadata Format

### 2.1 Required Header Structure

Every document must begin with the following metadata header:

```markdown
# [Document Title]
**Created: [Month Day, Year] [Time AM/PM]**
**Last Modified: [Month Day, Year] [Time AM/PM]**

[Context: Category_Name]
[Status: Status_Value]
[Version: X.Y]
```

### 2.2 Document Title Format

- Use title case for all document titles
- Start with the document type prefix (e.g., "SPEC-", "GUIDE-")
- Keep titles concise but descriptive (under 60 characters)
- Do not include version numbers in titles

Examples:
- "SPEC-DocumentManager"
- "GUIDE-AICollaboration"
- "STANDARD-DatabaseSchema"

### 2.3 Timestamp Format

Timestamps must adhere to the following format:
- **Created/Modified Date**: Month Day, Year (e.g., "March 22, 2025")
- **Time**: 12-hour format with AM/PM (e.g., "3:45 PM")
- **Spacing**: Two spaces between date and time
- **No leading zeros**: Use "3:45 PM" not "03:45 PM"

Examples:
- "March 22, 2025  3:45 PM"
- "January 5, 2025  11:30 AM"

## 3. Metadata Fields

### 3.1 Core Metadata Fields

| Field | Required | Format | Description | Example |
|-------|----------|--------|-------------|---------|
| Title | Yes | Text | Document title | "STANDARD-MetadataSchema" |
| Created | Yes | Timestamp | Creation date and time | "March 22, 2025  3:45 PM" |
| Last Modified | Yes | Timestamp | Last modification date and time | "March 22, 2025  3:45 PM" |
| Context | Yes | Category_Name | Primary categorization | "Knowledge_Organization" |
| Status | Yes | Status_Value | Current document status | "Active" |
| Version | Yes | X.Y | Document version number | "1.0" |

### 3.2 Optional Metadata Fields

| Field | Format | Description | Example |
|-------|--------|-------------|---------|
| Component | Layer#_ComponentName | Related component | "Layer1_DocumentManager" |
| Author | Name | Document author | "Herbert J. Bowers" |
| Priority | Priority_Value | Implementation priority | "High" |
| Related | [DocID, DocID, ...] | Related documents | "[20-10, 20-30]" |
| Supersedes | DocID | Document this replaces | "20-20-v0.9" |
| Review_Date | Date | Next review date | "June 22, 2025" |

## 4. Metadata Field Values

### 4.1 Context Values

Valid context values categorize the document's primary purpose:

| Context Value | Description | Document Types |
|---------------|-------------|----------------|
| Project_Overview | Project-wide documents | README, VISION, SCOPE |
| Knowledge_Organization | Knowledge management documents | STRUCTURE, GUIDE |
| Technical_Standards | Technical requirements | STANDARD, RULE |
| Component_Specification | Component designs | SPEC, ARCH |
| Implementation_Plan | Implementation details | PLAN, IMPL |
| Testing_Documentation | Testing information | TEST, QA |
| Process_Documentation | Process descriptions | PROCESS, WORKFLOW |
| Project_Tracking | Project status tracking | STATUS, PROGRESS |
| Project_Governance | Decision making | DECISION, POLICY |
| Reference_Material | Reference information | REF, EXAMPLE |

### 4.2 Status Values

Document status indicates its current state in the lifecycle:

| Status Value | Description |
|--------------|-------------|
| Draft | Initial creation, not ready for review |
| In_Review | Currently being reviewed |
| Approved | Reviewed and approved |
| Active | Current and in use |
| Superseded | Replaced by newer version |
| Deprecated | No longer relevant but kept for reference |
| Archived | No longer active but preserved for history |
| Template | Base document for creating other documents |

### 4.3 Priority Values

Priority indicates implementation importance:

| Priority Value | Description |
|----------------|-------------|
| Critical | Blocking other work, immediate attention required |
| High | Important for current development phase |
| Medium | Needed but not immediately blocking |
| Low | Nice to have, can be deferred |

### 4.4 Version Numbering

Version numbers use the X.Y format:

- **X**: Major version, incremented for significant changes
- **Y**: Minor version, incremented for small updates
- Start with 0.1 for initial drafts
- Move to 1.0 for first approved/active version
- Use 2.0, 3.0, etc. for major revisions

## 5. In-Document Metadata

### 5.1 Section Tagging

Sections within documents can be tagged with metadata:

```markdown
## 3. Component Design
[Priority: High]
[Status: In_Progress]
```

### 5.2 Code Block Metadata

Code blocks can include metadata for language and context:

````markdown
```python
# File: example.py
# Context: Implementation_Example
def example_function():
    pass
```
````

### 5.3 Decision Point Tagging

Important decisions in documents should be tagged:

```markdown
[Decision: DECISION-20250322-1]
We will use SQLite for the initial database implementation based on simplicity and portability.
```

## 6. Cross-Document References

### 6.1 Document Reference Format

References to other documents should use:

1. **Document Number**: For numbered documents, e.g., `[10-20]`
2. **Document ID**: For specific document ID, e.g., `[SPEC-DocumentManager]`
3. **Document with Section**: For specific section, e.g., `[10-20 §3.2]`
4. **Decision Reference**: For decisions, e.g., `[DECISION-20250322-1]`

### 6.2 External Reference Format

External references should use:

```markdown
[Name of Resource](URL)
```

### 6.3 Component Reference Format

References to components should use:

```markdown
[Layer#_ComponentName]
```

## 7. Metadata Extraction and Processing

### 7.1 Extraction Algorithm

Metadata is extracted from documents using the following algorithm:

```python
def ExtractMetadata(content: str) -> Dict[str, Any]:
    """Extract metadata from document content."""
    metadata = {}
    
    # Look for metadata in standard format
    lines = content.split('\n')
    in_header = False
    
    for line in lines:
        # Check for metadata header section
        if line.startswith('**Created:'):
            in_header = True
            # Extract creation timestamp
            timestamp_str = line.replace('**Created:', '').strip()
            metadata['created_at'] = ParseTimestamp(timestamp_str)
            continue
            
        # Look for context markers [Key: Value]
        if in_header and line.startswith('[') and ']' in line:
            # Extract key-value pair
            kv_content = line[1:line.find(']')].strip()
            if ':' in kv_content:
                key, value = kv_content.split(':', 1)
                metadata[key.lower()] = value.strip()
            continue
            
        # End of metadata section
        if in_header and line.startswith('##'):
            in_header = False
    
    # Extract title from first heading
    for line in lines:
        if line.startswith('# '):
            metadata['title'] = line[2:].strip()
            break
    
    return metadata
```

### 7.2 Validation Rules

Metadata validation rules include:

1. All required fields must be present
2. Timestamps must follow the correct format
3. Context values must be from the approved list
4. Status values must be from the approved list
5. Version numbers must follow X.Y format
6. If Component is specified, it must follow correct format

### 7.3 Indexing Approach

Metadata is indexed for searching with:

1. Full-text indexing of document title and content
2. Specific indexes for each metadata field
3. Cross-reference indexing for document relationships
4. Timestamp indexes for chronological queries

## 8. Integration with Knowledge Database

### 8.1 Storage Format

Metadata is stored in the database as:

```sql
CREATE TABLE document_metadata (
    document_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    modified_at TEXT NOT NULL,
    context TEXT NOT NULL,
    status TEXT NOT NULL,
    version TEXT NOT NULL,
    component TEXT,
    author TEXT,
    priority TEXT,
    metadata_json TEXT,
    
    -- Constraints
    CHECK (json_valid(metadata_json) OR metadata_json IS NULL)
);
```

### 8.2 Searching By Metadata

Standard queries for metadata include:

```sql
-- Find all active component specifications
SELECT document_id, title 
FROM document_metadata 
WHERE context = 'Component_Specification' 
AND status = 'Active';

-- Find recently modified documents
SELECT document_id, title, modified_at 
FROM document_metadata 
ORDER BY modified_at DESC 
LIMIT 10;

-- Find documents by component
SELECT document_id, title 
FROM document_metadata 
WHERE component = 'Layer1_DocumentManager';
```

### 8.3 Metadata Synchronization

Metadata synchronization ensures database consistency:

1. On document save, extract and update metadata
2. On document move/rename, update references
3. On document delete, mark as deleted but maintain metadata
4. Periodic validation to ensure metadata integrity

## 9. Metadata Templates

### 9.1 Standard Document Header

```markdown
# [Document Title]
**Created: [Month Day, Year] [Time AM/PM]**
**Last Modified: [Month Day, Year] [Time AM/PM]**

[Context: Category_Name]
[Component: Layer#_ComponentName]
[Status: Status_Value]
[Version: X.Y]
[Priority: Priority_Value]
```

### 9.2 Meeting Notes Metadata

```markdown
# NOTES-Meeting-[Topic]
**Created: [Month Day, Year] [Time AM/PM]**
**Last Modified: [Month Day, Year] [Time AM/PM]**

[Context: Project_Tracking]
[Status: Active]
[Meeting_Date: Month Day, Year]
[Participants: Name1, Name2, ...]
[Agenda: Brief agenda description]
```

### 9.3 Decision Document Metadata

```markdown
# DECISION-[Topic]
**Created: [Month Day, Year] [Time AM/PM]**
**Last Modified: [Month Day, Year] [Time AM/PM]**

[Context: Project_Governance]
[Status: Active]
[Decision_ID: DECISION-YYYYMMDD-N]
[Decision_Maker: Name]
[Decision_Type: Architectural|Technical|Process|Priority]
```

## 10. References

- [00-10] GUIDE-DocumentMap
- [40-20] STRUCTURE-KnowledgeDatabase
- [20-50] STANDARD-DatabaseSchema
- [30-series] Document Templates

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
