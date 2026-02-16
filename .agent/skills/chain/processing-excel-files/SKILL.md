---
description: Excel file processing and manipulation using the Excel MCP Server
name: processing-excel-files
type: skill
---
# Excel Processing

Use the Excel MCP Server to read, edit, and analyze Excel workbooks directly.

## When to Use
Use this skill when you need to automate tasks involving Excel workbooks, such as reading large datasets, updating specific cells with calculated values, or generating summary reports.

## Prerequisites
- Excel MCP server installed and configured.
- Access to local or network-mapped Excel files (.xlsx).

## Capabilities

- **Read Worksheets**: Extract data from specific sheets or ranges.
- **Edit Cells**: Modify cell values, formulas, and formatting.
- **Create Workbooks**: Generate new Excel files from data.
- **Analyze Data**: Perform calculations and aggregations using Excel's engine.

## Process

1. **Load Workbook**: Use `read_workbook` to inspect structure.
2. **Read Data**: Use `read_range` to get target data.
3. **Modify**: Use `write_cell` or `write_range` to update content.
4. **Save**: Changes are often auto-saved or require explicit save depending on the MCP implementation.

## Example Usage

### Reading Data
```python
response = await client.chat.completions.create(
    messages=[{"role": "user", "content": "Read the sales data from C:\\data\\sales.xlsx"}],
    tools=[{
        "type": "mcp",
        "name": "excel",
        "command": "uvx",
        "args": ["excel-mcp-server"]
    }]
)
```

### Writing Data
```python
# Write a summary
await excel.write_cell(
    file="C:\\data\\report.xlsx",
    sheet="Summary",
    cell="B2",
    value="=SUM(Sheet1!A1:A10)"
)
```

## Best Practices

- Always specify full paths for files.
- Validate cell ranges before reading large datasets.
- Use named ranges where possible for robustness.

## Related
- MCP Server: `excel-mcp-server`
