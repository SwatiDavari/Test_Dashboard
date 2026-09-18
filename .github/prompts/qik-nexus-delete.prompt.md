---
description: 'Permanently remove one or more explicitly named entries (dropped or idea only), optionally also deleting the linked tracker issue. Cannot be undone.'
---
<!-- @needs nexus delete --tracker skill surface, prd_unit_imp__nexus__skill_delete_tracker, prd_unit_imp, [prd_unit_des__nexus__skill_delete_tracker], released -->

# qik nexus delete — permanently remove named entries

Use `mcp_qik-mcp_nexus_delete` or CLI:

```bash
qik nexus delete <ID>...
```

**Permanently removes** the named entries. Cannot be undone.

**Allowed stages:** `dropped` and `idea` only. `pi`, `staged`, and `released` entries are protected.

## Also delete the linked tracker issue

```bash
qik nexus delete <ID>... --tracker <name>
```

For each linked ExternalRef matching `<name>`, calls `delete_issue` on the provider before deleting the nexus entry. Tracker errors are warnings and do not block the nexus deletion.

- **Jira**: attempts `DELETE /rest/api/3/issue/{key}` (requires project-admin). Falls back to `state_map["dropped"]` transition or first done-category transition.
- **GitHub**: no delete API — closes with `state_reason: not_planned` as best-effort.

**Typical workflow:**
```bash
qik nexus drop <ID> --reason "no longer needed"
qik nexus delete <ID> --tracker jira
```

All ids are validated before any deletion; partial success is not possible.
