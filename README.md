# Go

Go is a GitHub Pages data application backed by the MongoDB collection `go.link`. It publishes inventory identifiers and related records as static JSON, renders individual records from short URLs, produces QR labels, and preserves exported data changes in Git history.

The repository began as a URL-shortening service. The current implementation is primarily an inventory lookup and publishing system: the live database contains no active external redirect targets, and the browser client displays records rather than redirecting to their `target` values.

## Architecture

```text
MongoDB: go.link
  |  Python management and export tools
  v
data/<first>/<second>/<prefix>.json
  |  commit and push
  v
GitHub repository / GitHub Pages
  |
  +-- /<identifier>       record view through 404.html
  +-- /single/?id=...     one QR code
  +-- /sheet/?start=...   printable QR-code sheet
  +-- /shelves/?s=...     shelf and contents view
  +-- /map/               storage map
```

MongoDB is the mutable working database. The JSON files are published projections grouped by identifier prefix; Git provides version history for those exports. A repository record is therefore evidence of what was exported at a particular commit, not a guarantee that it remains the current database state.

## Identifier layout

Identifiers use four lowercase characters. The code's alphabet excludes ambiguous characters `0`, `i`, `l`, and `o`, leaving 32 symbols:

```text
123456789abcdefghjkmnpqrstuvwxyz
```

Static exports are partitioned by the first two characters. For identifier `x2pj`, the browser requests:

```text
data/x/2/x2.json
```

That file is a JSON array containing every exported record whose identifier begins with `x2`. The client then selects the object whose full `identifier` equals `x2pj`.

The 32-character alphabet produces 1,024 possible two-character partitions. Empty or unused partitions may contain an empty JSON array.

## Record model

Most records originate in MongoDB with fields drawn from this set:

| Field | Meaning |
| --- | --- |
| `_id` | MongoDB object identifier, serialized as text in primary exports |
| `identifier` | Stable four-character public identifier |
| `permalink` | GitHub Pages URL for the identifier |
| `target` | Historical redirect destination; currently `#` in the live collection |
| `class` | Broad record class, primarily `inventory` or `media` |
| `type` | More specific role such as `item`, `storage`, `consumable`, `consumable_instance`, or `work` |
| `allocated` | Whether an identifier has been assigned |
| `label` | Human-readable description |
| `last_updated` | Time of the last recorded update |
| `shelf`, `bay`, `slot`, `shcn` | Storage-location metadata |
| `quantity`, `expires`, `upc` | Consumable or item-specific metadata |
| `notion_id` | Legacy link to the former Notion inventory workflow |

Fields are optional and vary by class and type. Location and descriptive fields should be read as the last recorded assertion at `last_updated`, not as proof of the object's present physical state.

The live collection observed on 2026-11-19 contained 1,015,806 documents. Nearly all were preallocated inventory identifiers; comparatively few had been enriched as items, storage locations, consumables, instances, or media works.

## Static application

### Identifier view

GitHub Pages serves [`404.html`](404.html) for paths such as:

```text
https://joeeasterly.github.io/go/x2pj
```

The page extracts the identifier, loads its two-character partition, selects the matching object, and renders all non-null fields. It also constructs links to:

- a QR-code view for the identifier;
- a shelf map when a shelf is present; and
- a legacy Notion page when `notion_id` is present.

### QR-code views

[`single/index.html`](single/index.html) renders a QR code for one identifier.

[`sheet/index.html`](sheet/index.html) generates printable label sheets. Supported query parameters include:

| Parameter | Purpose |
| --- | --- |
| `single` | Render one identifier |
| `start` | Start at an identifier within a partition |
| `count` | Limit the number of codes; the default is 56 |
| `noborder` | Remove label borders |

When producing a multi-label sheet, the client starts at the requested record and then selects subsequent unallocated identifiers from the same two-character partition.

### Shelves and map

The `shelves/` application loads generated shelf projections from:

```text
shelves/data/<first character>/<shelf code>.json
```

Each projection contains a `shelving_record` and a `shelf_contents` array. The site renders the shelf metadata followed by its recorded contents.

The `map/` directory contains a storage map and supporting assets. Some map content is generated output rather than a general-purpose application source.

## Python management tools

The scripts under `bin/` form an interactive inventory-management toolkit. The main interface is:

```bash
/usr/local/gh/go/.venv/bin/python3 /usr/local/gh/go/bin/inventory.py
```

Its menu exposes record creation, search, update, deletion, storage management, reshelving, consumables, and export operations.

Important modules include:

| Module | Responsibility |
| --- | --- |
| `inventory.py` | Menu-driven entry point |
| `lib_mungo.py` | MongoDB connection, identifier allocation, and record lookup |
| `lib_git.py` | Prefix export and Git commit helpers |
| `create_record.py` | Allocate and enrich an inventory identifier |
| `update_record.py` | Modify a record and regenerate its partition |
| `delete_record.py` | Reset an allocated record rather than physically deleting its identifier |
| `update_github.py` | Export partitions changed since the latest data commit |
| `export_indices.py` | Rebuild all 1,024 primary partitions |
| `export_shelves.py` | Generate shelf projections |
| `print_inventory.py` | Format records for interactive display |
| `lib_notion.py` and related scripts | Legacy Notion synchronization |

The tools use absolute paths rooted at `/usr/local/gh/go` and connect directly to MongoDB at `192.168.86.70:27017`, database `go`, collection `link`. They are therefore tied to the Bellatrix network and repository layout.

No dependency manifest is present. The imports establish at least these non-standard Python requirements:

```text
pymongo
requests
```

Create the expected virtual environment and install dependencies before running the tools:

```bash
cd /usr/local/gh/go
python3 -m venv .venv
.venv/bin/pip install pymongo requests
```

## Export and publication workflows

### Export one changed prefix

Record-creation and update flows call `generate_recset_by_id()`, which:

1. derives the identifier's first two characters;
2. queries every MongoDB record sharing that prefix;
3. serializes the results to the corresponding JSON file; and
4. creates a Git commit for the changed file.

The helper commits but does not push.

### Export changes since the latest data commit

Run:

```bash
cd /usr/local/gh/go
.venv/bin/python3 bin/update_github.py
```

The script compares MongoDB `last_updated` values with the most recent Git commit affecting `data/`, rebuilds each affected prefix, and commits each partition. Review the result before publishing:

```bash
git status --short
git log --oneline --max-count=10
git diff HEAD~1 -- data/
git push
```

This comparison assumes that Git commit time is a reliable export watermark. Rewritten history, commits created on another clock, missing `last_updated` values, or uncommitted exports can make that assumption false.

### Full export

`bin/export_indices.py` rewrites all primary partitions. It is a bulk operation over approximately one million MongoDB records and does not itself commit or push the results. Review repository size and diff volume before using it.

## URL-shortening status

The repository description calls Go a URL redirect service, and records retain a `target` field. However, the current code does not implement an external redirect:

- `404.html` renders the selected record but does not navigate to `matchingObject.target`;
- the live `go.link` collection contained no `target` value other than `#` at inspection time; and
- management helpers initialize or reset `target` to `#`.

Accordingly, identifier lookup is verified in source, while active URL shortening is not. Restoring shortening would require an explicit rule for distinguishing redirect records from inventory records, validation of permitted target schemes, and corresponding client behavior.

## Legacy and generated content

Several areas should not be mistaken for current authoritative source:

- `bin/one_offs/` contains historical migrations and repair scripts.
- `script_out/` contains dated QR-code and shelf-list output.
- `source/new_identifiers.csv` and `source/new_identifiers.txt` are very large identifier-generation artifacts.
- Notion-related modules target fixed database IDs and a largely retired inventory workflow.
- `Untitled Diagram.drawio` is an unnamed design artifact.
- `labels_20240127.txt` and `shelf_labels.txt` are generated or operational output.

Do not rerun one-off scripts merely because they remain executable-looking. Archaeology is not an operations manual.

## Public-data considerations

This repository and its GitHub Pages site are public. Exported JSON can include labels, storage locations, quantities, timestamps, and historical metadata. Removing a value from MongoDB or a later commit does not remove it from Git history.

Before adding a new field to exported records, decide whether it is appropriate for permanent public disclosure. Secrets, precise sensitive locations, private notes, purchase information, and authentication data do not belong in this export.

## Backup and recovery

MongoDB is the working source for record mutation. GitHub is the versioned publication and a partial recovery source for exported fields.

A complete recovery plan should retain:

1. a verified backup of MongoDB `go.link`;
2. this Git repository and its full history;
3. the Python management code;
4. any externally maintained credentials required by retained integrations; and
5. documentation of the GitHub Pages configuration.

After restoration, verify a representative sample across different identifier prefixes, allocated and unallocated records, shelf projections, QR rendering, and update/export behavior.

## Verification record

This documentation was derived from the complete repository tree, the static application, management scripts, representative JSON partitions, and read-only queries against MongoDB `go.link` on 2026-11-19.

Observed repository state:

- 1,746 tracked files totaling approximately 327 MB;
- 1,671 JSON files;
- 1,024 primary `data/` partitions;
- 646 shelf projection files; and
- approximately 93 MB of identifier source artifacts.

Observed live database state:

- 1,015,806 total records;
- 1,015,722 records with class `inventory`;
- 21 records with class `media`;
- 646 records typed as storage locations;
- 475 typed as items;
- 356 typed as consumables;
- 26 typed as consumable instances; and
- no active external redirect targets.

No MongoDB write, export execution, GitHub Pages deployment, QR print, browser lookup, redirect, backup, or restoration test was performed.
