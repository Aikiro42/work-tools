# Sheets Query Language

Since you are already comfortable with MySQL, you’ll find Google Sheets Query Language (technically the Google Visualization API Query Language) very familiar, but with some "diet" restrictions and unique syntax quirks.

Here is the translation guide to help you map your MySQL knowledge to Sheets.

### 1. Core Syntax Comparison

| Feature | MySQL | Sheets Query |
| --- | --- | --- |
| **Column Identifiers** | `title`, ``date`` | `A, B, C` (for ranges) or `Col1, Col2` (for arrays) |
| **String Literals** | `'text'` or `"text"` | `'text'` (Single quotes only) |
| **Date Literals** | `'2025-01-01'` | `date '2025-01-01'` (Keyword required) |
| **Boolean** | `TRUE` / `1` | `true` / `false` |
| **Inequality** | `!=` or `<>` | `!=` or `<>` |
| **Concatenation** | `CONCAT(a, b)` | Not supported inside the string (use `&` in the range) |

---

### 2. The "Clause Hierarchy"

MySQL is somewhat flexible with where some clauses go, but Sheets Query is **extremely strict**. If you put these out of order, the formula will break.

**The Required Order:**

1. `SELECT`
2. `WHERE`
3. `GROUP BY`
4. `PIVOT` (Unique to Sheets)
5. `ORDER BY`
6. `LIMIT`
7. `OFFSET`
8. `LABEL` (The analogue to `AS` in SQL)
9. `FORMAT`

---

### 3. Function Mapping

Most standard aggregate functions work exactly the same way, but they are case-insensitive in Sheets.

| SQL Function | Sheets Query Equivalent | Notes |
| --- | --- | --- |
| `COUNT()` | `count()` | Works on any column type. |
| `SUM()` | `sum()` | Numbers only. |
| `AVG()` | `avg()` | Numbers only. |
| `NOW()` | `now()` | Returns a timestamp. |
| `YEAR(date)` | `year(B)` | Extracts year from column B. |
| `AS` | `LABEL` | Used at the end: `LABEL Col1 'Name'` |

---

### 4. Critical Differences (The "Gotchas")

#### No JOINs

This is the biggest hurdle for MySQL users. Sheets Query **cannot** join two tables.

* **Workaround:** You have to use `{Range1, Range2}` to create a virtual array or use `VLOOKUP`/`XLOOKUP` to bring data into one table before querying it.

#### The LABEL Clause

In MySQL, you alias a column immediately: `SELECT name AS 'User'`.
In Sheets, you do it at the very end of the string:
`"SELECT A, B LABEL A 'User', B 'Timestamp'"`

#### PIVOT (The Superpower)

Sheets has a `PIVOT` clause that MySQL doesn't have natively. It turns row values into columns automatically.

```sql
-- Creates a cross-tab table of sales by Year and Region
"SELECT SUM(A) GROUP BY B PIVOT C"

```

#### The Header Argument

The `QUERY` function has a 3rd argument that MySQL doesn't have:
`=QUERY(range, sql_string, [headers])`

* Set this to `1` if your range includes headers.
* Set it to `0` if it doesn't.
* If you leave it blank, Sheets will "guess," and it often guesses wrong.

---

### 5. Quick Translation Example

**MySQL Style:**

```sql
SELECT category, SUM(price) AS 'Total'
FROM products
WHERE price > 100
GROUP BY category
ORDER BY Total DESC;

```

**Sheets Query Style:**

```excel
=QUERY(A:C, "SELECT B, SUM(C) WHERE C > 100 GROUP BY B ORDER BY SUM(C) DESC LABEL SUM(C) 'Total'", 1)

```

# SheetsQL with Structured Tables
Please translate the following SQL into Sheets Query Language:

```
SELECT Title, Date, ModeOfConduct FROM Table1 WHERE Date <= "2025/06/30" ORDER BY Date GROUP BY ModeOfConduct;
```

Suppose I'm using a structured table named "Table1" with the columns (Title, Date, ModeOfConduct). Assume the top-left-most cell is in a random cell in a random sheet. Suppose I'm also a whimsical person that likes swapping columns.

Make me a solution that gives me the data I want -- give a way to do the original query I gave no matter the order of the columns.

**Answer:**
```
=QUERY(
  CHOOSECOLS(Table1, 
    MATCH("Title", INDEX(Table1, 1, 0), 0), 
    MATCH("Date", INDEX(Table1, 1, 0), 0), 
    MATCH("ModeOfConduct", INDEX(Table1, 1, 0), 0)
  ), 
  "SELECT Col1, Col2, Col3 WHERE Col2 <= date '2025-06-30' ORDER BY Col2", 1
)
```