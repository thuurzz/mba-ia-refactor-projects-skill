# Audit Report Template

This is the standardized format for the Phase 2 audit report. Follow this template EXACTLY.

---

## Report Structure

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <project-name>
Stack:   <language> + <framework>
Files:   <count> analyzed | ~<lines> lines of code

## Summary
CRITICAL: <count> | HIGH: <count> | MEDIUM: <count> | LOW: <count>

## Findings

### [CRITICAL] <Title>
File: <filepath>:<line-range>
Description: <what was found, 1-2 sentences>
Impact: <why it matters, 1 sentence>
Recommendation: <how to fix, 1 sentence>

### [CRITICAL] <Title>
File: <filepath>:<line-range>
Description: ...
Impact: ...
Recommendation: ...

[... all CRITICAL findings first, then HIGH, then MEDIUM, then LOW ...]

================================
Total: <total> findings
================================
```

---

## Formatting Rules

1. **Order:** CRITICAL → HIGH → MEDIUM → LOW (within each severity, order by file path)
2. **File references:** Use exact relative paths from project root (e.g., `src/app.js:48`, `models/user.py:30-33`)
3. **Line numbers:** Single line (`:42`) or range (`:1-350`). For patterns across multiple locations, list all: `:28,48,58,95`
4. **Description:** Be specific. Say WHAT was found, not just the category name.
   - ✅ "SQL Injection: query string built with `+` concatenation of user input"
   - ❌ "SQL Injection"
5. **Impact:** Explain the consequence in business/security terms.
   - ✅ "Attacker can execute arbitrary SQL to read/modify/delete all data"
   - ❌ "Bad practice"
6. **Recommendation:** Give actionable, concrete fix.
   - ✅ "Replace string concatenation with parameterized query: `cursor.execute('SELECT * FROM x WHERE id = ?', (id,))`"
   - ❌ "Fix it"

---

## Example Report

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 4 | MEDIUM: 3 | LOW: 3

## Findings

### [CRITICAL] SQL Injection in All Queries
File: models.py:28,48,58,95,108,130,175,195,280,295
Description: All database queries use string concatenation with user input instead of parameterized queries. Example: `cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))`
Impact: Attacker can execute arbitrary SQL commands — read, modify, or delete any data in the database.
Recommendation: Replace all string concatenation with parameterized queries using `?` placeholders: `cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))`

### [CRITICAL] Hardcoded Secret Key
File: app.py:8
Description: Flask SECRET_KEY is hardcoded as a plain string literal: `app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"`
Impact: If the source code is ever exposed (public repo, leak), attackers can forge session cookies and impersonate any user.
Recommendation: Load SECRET_KEY from environment variable: `app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")` with a fallback for development only.

[... more findings ...]

================================
Total: 14 findings
================================
```

---

## Summary Line Format

The summary line must use this exact format:
```
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>
```

If a severity has zero findings, still include it:
```
CRITICAL: 3 | HIGH: 0 | MEDIUM: 5 | LOW: 2
```

---

## Deprecated API Detection

When deprecated APIs are found, include them in the findings with the appropriate severity:

- **MEDIUM:** Using deprecated APIs that still work but have known issues
- **LOW:** Using older API patterns where newer, more readable alternatives exist

Format:
```
### [MEDIUM] Deprecated API: datetime.utcnow()
File: models/task.py:15,18, routes/task_routes.py:35
Description: `datetime.utcnow()` is deprecated since Python 3.12. Used in 3 locations.
Impact: Will break when upgrading Python. Returns naive datetime objects.
Recommendation: Replace with `datetime.now(datetime.UTC)` or `datetime.now(timezone.utc)`.
```