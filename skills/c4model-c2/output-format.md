# C2 Output Format

JSON structure for `c2-containers.json` output file.

## Complete Example

```json
{
  "metadata": {
    "version": "1.0.0",
    "timestamp": "2025-11-17T20:20:00.000Z",
    "generated_by": "c2-abstractor",
    "parent": {
      "file": "c1-systems.json",
      "timestamp": "2025-11-17T10:00:00.000Z"
    }
  },
  "containers": [
    {
      "id": "ecommerce-spa",
      "name": "E-Commerce Customer Portal",
      "type": "spa",
      "system_id": "ecommerce-system",
      "technology": {
        "primary_language": "TypeScript",
        "framework": "React 18.2.0",
        "libraries": [
          {"name": "React Router", "version": "6.14.0", "purpose": "Client-side routing"},
          {"name": "Redux Toolkit", "version": "1.9.5", "purpose": "State management"}
        ]
      },
      "runtime": {
        "environment": "browser",
        "platform": "Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)",
        "containerized": false
      },
      "relations": [
        {
          "target": "ecommerce-api",
          "type": "http-rest",
          "direction": "outbound",
          "description": "Fetches product data and submits orders"
        }
      ],
      "observations": [],
      "metadata": {
        "repository": "frontend/",
        "discovered_at": "2025-11-17T20:15:00.000Z"
      }
    }
  ]
}
```

## Validation

After generating `c2-containers.json`:

```bash
# Validate JSON structure
python ${CLAUDE_PLUGIN_ROOT}/validation/scripts/validate-c2-containers.py c2-containers.json

# Verify timestamps
python ${CLAUDE_PLUGIN_ROOT}/validation/scripts/check-timestamp.sh c2-containers.json c1-systems.json
```

## Required Fields

See main [SKILL.md](./SKILL.md#required-fields-checklist) for complete required fields matrix.
