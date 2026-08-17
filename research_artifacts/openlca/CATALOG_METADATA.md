# openLCA process catalog metadata

- **Research label:** ELCD process catalog
- **Process count:** 608
- **Export mechanism:** openLCA IPC server + `olca-ipc` / `olca-schema`
- **IPC port used during the revision workflow:** 8080
- **Export period:** August 2026
- **Exact database release/version:** ELCD 3.2
- **Included fields:** process UUID, process name, category, location, library,
  process type
- **Not included:** complete LCI exchanges, product systems, LCIA results, or the
  underlying database package

## Re-exporting the catalog

Use:

```bash
python scripts/export_openlca_process_catalog.py --database-label "ELCD 3.2"
```

Before running the script, open the intended database in openLCA and start the
IPC server on port 8080. The script exports descriptors from whichever database
is active in openLCA at that moment.
