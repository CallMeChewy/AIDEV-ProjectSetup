# GUIDE-DocumentMap
**Created: March 22, 2025 2:30 PM**
**Last Modified: March 22, 2025  2:30PM**

[Context: Knowledge_Organization]
[Status: Active]
[Version: 1.0]

## 1. Document Numbering System

The Project Himalaya Knowledge Database uses a hierarchical numbering system to organize all documents. This system ensures intuitive navigation and clear relationships between documents.

### 1.1 Numbering Format

Documents follow this naming pattern:
```
[Series]-[Subseries] [Type]-[Topic].md
```

Example: `10-20 SCOPE-ProjectHimalaya.md`

- **Series (first two digits)**: Major category
- **Subseries (second two digits)**: Specific area within category
- **Type**: Document purpose (e.g., SPEC, PLAN, GUIDE)
- **Topic**: Subject matter

### 1.2 Series Categories

| Series | Purpose | Key Documents |
|--------|---------|---------------|
| 00     | Status & Navigation | Current project status, document maps, active sessions |
| 10     | Vision & Scope | Project vision, scope definition, roadmap |
| 20     | Standards | Coding standards, design principles, documentation standards |
| 30     | Templates | Reusable document templates for various purposes |
| 40     | Knowledge Organization | Database structure, metadata standards, taxonomy |
| 50     | Implementation | Implementation plans and details for active components |
| 60     | Testing | Test plans, test cases, testing frameworks |
| 70     | Documentation | User guides, API documentation, tutorials |
| 80     | Session Archives | Historical development session records |
| 90     | Reference Materials | External references, research notes, examples |

## 2. Core Documents

### 2.1 Project Foundation

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| [00-20 STATUS-ProjectHimalaya.md](00-20%20STATUS-ProjectHimalaya.md) | Current project status | Every session |
| [00-30 GUIDE-ActiveSessions.md](00-30%20GUIDE-ActiveSessions.md) | Tracks ongoing and recent sessions | Every session |
| [00-40 LOG-Decisions.md](00-40%20LOG-Decisions.md) | Record of key project decisions | As decisions occur |
| [10-10 VISION-ProjectHimalaya.md](10-10%20VISION-ProjectHimalaya.md) | Project vision and philosophy | Quarterly review |
| [10-20 SCOPE-ProjectHimalaya.md](10-20%20SCOPE-ProjectHimalaya.md) | Comprehensive scope definition | Monthly review |
| [20-10 STANDARD-AIDEV-PascalCase.md](20-10%20STANDARD-AIDEV-PascalCase.md) | Coding standards | As needed |
| [20-30 STANDARD-FoundationDesignPrinciples.md](20-30%20STANDARD-FoundationDesignPrinciples.md) | Core design principles | Quarterly review |

### 2.2 Implementation Documents

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| [50-10 IMPL-DocumentManager.md](50-10%20IMPL-DocumentManager.md) | DocumentManager implementation | As developed |
| [50-20 IMPL-StateManager.md](50-20%20IMPL-StateManager.md) | StateManager implementation | As developed |
| [50-30 IMPL-StandardsValidator.md](50-30%20IMPL-StandardsValidator.md) | StandardsValidator implementation | As developed |

### 2.3 Templates

| Document | Purpose | Usage |
|----------|---------|-------|
| [30-10 TEMPLATE-ComponentPlan.md](30-10%20TEMPLATE-ComponentPlan.md) | Planning component implementation | New components |
| [30-20 TEMPLATE-ComponentSpec.md](30-20%20TEMPLATE-ComponentSpec.md) | Component specification | New components |
| [30-30 TEMPLATE-ReferenceSubproject.md](30-30%20TEMPLATE-ReferenceSubproject.md) | Subproject reference | New subprojects |
| [30-40 TEMPLATE-SessionContinuity.md](30-40%20TEMPLATE-SessionContinuity.md) | Session handover | End of sessions |
| [30-50 TEMPLATE-TestCase.md](30-50%20TEMPLATE-TestCase.md) | Test case definition | Component testing |

## 3. Navigation Guidance

### 3.1 For First-Time AI Assistants

If you're an AI assistant joining this project for the first time, follow this sequence:

1. Review [00-20 STATUS-ProjectHimalaya.md](00-20%20STATUS-ProjectHimalaya.md) for current status
2. Examine [10-20 SCOPE-ProjectHimalaya.md](10-20%20SCOPE-ProjectHimalaya.md) for project scope
3. Study [20-30 STANDARD-FoundationDesignPrinciples.md](20-30%20STANDARD-FoundationDesignPrinciples.md) for design principles
4. Check [30-40 TEMPLATE-SessionContinuity.md](30-40%20TEMPLATE-SessionContinuity.md) for previous session context
5. Refer to [50-series documents](50-10%20IMPL-DocumentManager.md) for current implementation details

### 3.2 For Recurring AI Assistants

If you're returning to the project:

1. Note any updates in [00-20 STATUS-ProjectHimalaya.md](00-20%20STATUS-ProjectHimalaya.md)
2. Review recent sessions in [00-30 GUIDE-ActiveSessions.md](00-30%20GUIDE-ActiveSessions.md)
3. Check for new decisions in [00-40 LOG-Decisions.md](00-40%20LOG-Decisions.md)
4. Focus on the current implementation documents in the 50-series

### 3.3 For Human Developers

Human developers should:

1. Update [00-20 STATUS-ProjectHimalaya.md](00-20%20STATUS-ProjectHimalaya.md) at the beginning and end of each session
2. Record key decisions in [00-40 LOG-Decisions.md](00-40%20LOG-Decisions.md)
3. Ensure the latest implementation details are reflected in 50-series documents
4. Create session continuity documents using [30-40 TEMPLATE-SessionContinuity.md](30-40%20TEMPLATE-SessionContinuity.md)

## A4. Cross-Referencing System

All documents should use the following cross-referencing approaches:

1. **Document References**: Use bracketed document numbers, e.g., [10-20]
2. **Section References**: Use document number plus section, e.g., [10-20 §3.2]
3. **Decision References**: Use decision log ID, e.g., [DECISION-2025-03-22-1]
4. **Component References**: Use component name with layer, e.g., [Layer1_DocumentManager]

## 5. Document Lifecycle

### 5.1 Creation Guidelines

1. Use the appropriate template from the 30-series
2. Assign the next available number in the appropriate series
3. Include all required metadata headers
4. Add cross-references to related documents
5. Add to this document map

### 5.2 Update Process

1. Update the "Last Modified" timestamp
2. Add entry to version history section
3. Update cross-references if needed
4. Note significant changes in STATUS document

### 5.3 Archiving Process

1. Move deprecated documents to the 80-series
2. Update references in this map
3. Maintain a reference in the original location

## 6. Document Map Maintenance

This document map itself should be updated:

1. Whenever a new document is added to the knowledge base
2. When document relationships change significantly
3. When the document organization system is modified
4. After any major project milestone

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
