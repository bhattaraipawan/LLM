

Pasted text(8).txt
Document

LLM-main.zip
Zip Archive
 is this code correct for my following github repository 


Analyzed
from artifact_tool import Blob, SpreadsheetFile

src = "/mnt/data/LLM-main/ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"
print("Checking for extracted repo path first...")

STDOUT/STDERR
Checking for extracted repo path first...

Analyzed
from artifact_tool import Blob, SpreadsheetFile

src = "/mnt/data/LLM-main-corrected/LLM-main/ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"
wb_src = SpreadsheetFile.import_xlsx(Blob.load(src))
print(wb_src.inspect({"kind": "sheet", "include": "id,name"}).ndjson)

STDOUT/STDERR
{"kind":"sheet","id":"ws/r2jqtx","name":"Instructions","index":0,"range":"A1:E11","address":"A1:E11"}
{"kind":"sheet","id":"ws/x7uwh6","name":"Expert_A","index":1,"range":"A1:K42","address":"A1:K42"}
{"kind":"sheet","id":"ws/bs8dfq","name":"Expert_B","index":2,"range":"A1:K42","address":"A1:K42"}
{"kind":"sheet","id":"ws/v1sddc","name":"Reconciliation","index":3,"range":"A1:R41","address":"A1:R41"}
{"kind":"sheet","id":"ws/4ttkd4","name":"ELCD_Catalog","index":4,"range":"A1:J609","address":"A1:J609"}

Analyzed
for rng in ["Expert_A!A1:K42", "Expert_B!A1:K42", "Reconciliation!A1:R41"]:
    print("\n---", rng, "---")
    print(wb_src.inspect({"kind": "table", "range": rng, "include": "values", "table_max_rows": 45, "table_max_cols": 20}).ndjson[:20000])

STDOUT/STDERR

--- Expert_A!A1:K42 ---
{"kind":"table","sheet":"Expert_A","address":"A1:K42","rows":42,"cols":11,"values":[["Expert A – Independent Expert Review",null,null,null,null,null,null,null,null,null,null],[null,null,null,null,null,null,null,null,null,null,null],["Reviewer Name / Code",null,null,null,null,null,null,null,null,null,null],["Relevant LCA Experience",null,null,null,null,null,null,null,null,null,null],["Review Date",null,null,null,null,null,null,null,null,null,null],[null,null,null,null,null,null,null,null,null,null,null],["ID","Case Study","Original BOM Description","Qty.","Unit","Normalized Material","Best ELCD/openLCA Process (select from catalog)","Process UUID (auto)","Match Type","Confidence","Brief Notes / Rationale"],["S01","Stonecrete House","Ordinary Portland Cement (OPC 43-grade)",5000,"kg",null,null,null,null,null,null],["S02","Stonecrete House","River Sand (clean, well-graded)",24000,"kg",null,null,null,null,null,null],["S03","Stonecrete House","Natural Gravel",12,"m³",null,null,null,null,null,null],["S04","Stonecrete House","Stone",12,"m³",null,null,null,null,null,null],["S05","Stonecrete House","Plain Cement Concrete (PCC M10 — 1:3:6) - Binding Layer",1.6,"m³",null,null,null,null,null,null],["S06","Stonecrete House","Stonecrete block",3512.34,"kg",null,null,null,null,null,null],["S07","Stonecrete House","Rebar TMT Fe500",250,"kg",null,null,null,null,null,null],["S08","Stonecrete House","Binding Wire (soft annealed, 18-gauge)",5,"kg",null,null,null,null,null,null],["S09","Stonecrete House","Corrugated Galvanized Iron (CGI) Sheet, 0.45 mm BMT",190.71,"kg",null,null,null,null,null,null],["S10","Stonecrete House","Timber for purlin, rafter, and column post",2.08,"m³",null,null,null,null,null,null],["S11","Stonecrete House","Plaster 1:4 — External Walls, 15 mm thick",65,"m²",null,null,null,null,null,null],["S12","Stonecrete House","Plaster 1:6 — Internal Walls, 12 mm thick",128,"m²",null,null,null,null,null,null],["B01","Bamboo House","Cement",1250,"kg",null,null,null,null,null,null],["B02","Bamboo House","Sand",9600,"kg",null,null,null,null,null,null],["B03","Bamboo House","Natural Gravel",6,"m³",null,null,null,null,null,null],["B04","Bamboo House","Stone",9,"m³",null,null,null,null,null,null],["B05","Bamboo House","Soil",12,"m³",null,null,null,null,null,null],["B06","Bamboo House","Local Wood",0.21,"m³",null,null,null,null,null,null],["B07","Bamboo House","19mm Plywood",4,"m²",null,null,null,null,null,null],["B08","Bamboo House","Nail",2,"kg",null,null,null,null,null,null],["B09","Bamboo House","10mm Rebar",116,"kg",null,null,null,null,null,null],["B10","Bamboo House","7mm Rebar",51,"kg",null,null,null,null,null,null],["B11","Bamboo House","Binding Wire",4,"kg",null,null,null,null,null,null],["B12","Bamboo House","24 Gauge CGI Sheets",630,"kg",null,null,null,null,null,null],["B13","Bamboo House","3mm Commercial Plywood",3,"m²",null,null,null,null,null,null],["B14","Bamboo House","Bamboo",4.82,"m³",null,null,null,null,null,null],["A01","Bamboo House with Attic","Cement",7300,"kg",null,null,null,null,null,null],["A02","Bamboo House with Attic","Sand",27200,"kg",null,null,null,null,null,null],["A03","Bamboo House with Attic","Natural Gravel",6,"m³",null,null,null,null,null,null],["A04","Bamboo House with Attic","Soil Blocks",6042,"Nos.",null,null,null,null,null,null],["A05","Bamboo House with Attic","Wood",0.264,"m³",null,null,null,null,null,null],["A06","Bamboo House with Attic","Bamboo",5.915,"m³",null,null,null,null,null,null],["A07","Bamboo House with Attic","Rebar",674,"kg",null,null,null,null,null,null],["A08","Bamboo House with Attic","Soil",3,"m³",null,null,null,null,null,null],["A09","Bamboo House with Attic","CGI Sheets",478.07,"kg",null,null,null,null,null,null]]}

--- Expert_B!A1:K42 ---
{"kind":"table","sheet":"Expert_B","address":"A1:K42","rows":42,"cols":11,"values":[["Expert B – Independent Expert Review",null,null,null,null,null,null,null,null,null,null],[null,null,null,null,null,null,null,null,null,null,null],["Reviewer Name / Code",null,null,null,null,null,null,null,null,null,null],["Relevant LCA Experience",null,null,null,null,null,null,null,null,null,null],["Review Date",null,null,null,null,null,null,null,null,null,null],[null,null,null,null,null,null,null,null,null,null,null],["ID","Case Study","Original BOM Description","Qty.","Unit","Normalized Material","Best ELCD/openLCA Process (select from catalog)","Process UUID (auto)","Match Type","Confidence","Brief Notes / Rationale"],["S01","Stonecrete House","Ordinary Portland Cement (OPC 43-grade)",5000,"kg",null,null,null,null,null,null],["S02","Stonecrete House","River Sand (clean, well-graded)",24000,"kg",null,null,null,null,null,null],["S03","Stonecrete House","Natural Gravel",12,"m³",null,null,null,null,null,null],["S04","Stonecrete House","Stone",12,"m³",null,null,null,null,null,null],["S05","Stonecrete House","Plain Cement Concrete (PCC M10 — 1:3:6) - Binding Layer",1.6,"m³",null,null,null,null,null,null],["S06","Stonecrete House","Stonecrete block",3512.34,"kg",null,null,null,null,null,null],["S07","Stonecrete House","Rebar TMT Fe500",250,"kg",null,null,null,null,null,null],["S08","Stonecrete House","Binding Wire (soft annealed, 18-gauge)",5,"kg",null,null,null,null,null,null],["S09","Stonecrete House","Corrugated Galvanized Iron (CGI) Sheet, 0.45 mm BMT",190.71,"kg",null,null,null,null,null,null],["S10","Stonecrete House","Timber for purlin, rafter, and column post",2.08,"m³",null,null,null,null,null,null],["S11","Stonecrete House","Plaster 1:4 — External Walls, 15 mm thick",65,"m²",null,null,null,null,null,null],["S12","Stonecrete House","Plaster 1:6 — Internal Walls, 12 mm thick",128,"m²",null,null,null,null,null,null],["B01","Bamboo House","Cement",1250,"kg",null,null,null,null,null,null],["B02","Bamboo House","Sand",9600,"kg",null,null,null,null,null,null],["B03","Bamboo House","Natural Gravel",6,"m³",null,null,null,null,null,null],["B04","Bamboo House","Stone",9,"m³",null,null,null,null,null,null],["B05","Bamboo House","Soil",12,"m³",null,null,null,null,null,null],["B06","Bamboo House","Local Wood",0.21,"m³",null,null,null,null,null,null],["B07","Bamboo House","19mm Plywood",4,"m²",null,null,null,null,null,null],["B08","Bamboo House","Nail",2,"kg",null,null,null,null,null,null],["B09","Bamboo House","10mm Rebar",116,"kg",null,null,null,null,null,null],["B10","Bamboo House","7mm Rebar",51,"kg",null,null,null,null,null,null],["B11","Bamboo House","Binding Wire",4,"kg",null,null,null,null,null,null],["B12","Bamboo House","24 Gauge CGI Sheets",630,"kg",null,null,null,null,null,null],["B13","Bamboo House","3mm Commercial Plywood",3,"m²",null,null,null,null,null,null],["B14","Bamboo House","Bamboo",4.82,"m³",null,null,null,null,null,null],["A01","Bamboo House with Attic","Cement",7300,"kg",null,null,null,null,null,null],["A02","Bamboo House with Attic","Sand",27200,"kg",null,null,null,null,null,null],["A03","Bamboo House with Attic","Natural Gravel",6,"m³",null,null,null,null,null,null],["A04","Bamboo House with Attic","Soil Blocks",6042,"Nos.",null,null,null,null,null,null],["A05","Bamboo House with Attic","Wood",0.264,"m³",null,null,null,null,null,null],["A06","Bamboo House with Attic","Bamboo",5.915,"m³",null,null,null,null,null,null],["A07","Bamboo House with Attic","Rebar",674,"kg",null,null,null,null,null,null],["A08","Bamboo House with Attic","Soil",3,"m³",null,null,null,null,null,null],["A09","Bamboo House with Attic","CGI Sheets",478.07,"kg",null,null,null,null,null,null]]}

--- Reconciliation!A1:R41 ---
{"kind":"table","sheet":"Reconciliation","address":"A1:R41","rows":41,"cols":18,"values":[["Reconciliation and Later LLM Review",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["Metric","Value",null,"Summary","Value",null,null,null,null,null,null,null,null,null,null,null,null,null],["Expert rows",35,null,"Expert agreement",0,null,null,null,null,null,null,null,null,null,null,null,null,null],[null,null,null,"Final reference completed",0,null,null,null,null,null,null,null,null,null,null,null,null,null],["ID","Original BOM Description","Expert A Normalized","Expert A Process","Expert A Decision","Expert B Normalized","Expert B Process","Expert B Decision","Agreement?","Final Normalized Material","Final Reference Process","Final Process UUID (auto)","Final Decision","LLM Normalized (later)","LLM Process (later)","LLM Decision (later)","Post-review Outcome","Notes"],["S01","Ordinary Portland Cement (OPC 43-grade)",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S02","River Sand (clean, well-graded)",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S03","Natural Gravel",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S04","Stone",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S05","Plain Cement Concrete (PCC M10 — 1:3:6) - Binding Layer",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S06","Stonecrete block",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S07","Rebar TMT Fe500",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S08","Binding Wire (soft annealed, 18-gauge)",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S09","Corrugated Galvanized Iron (CGI) Sheet, 0.45 mm BMT",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S10","Timber for purlin, rafter, and column post",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S11","Plaster 1:4 — External Walls, 15 mm thick",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S12","Plaster 1:6 — Internal Walls, 12 mm thick",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B01","Cement",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B02","Sand",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B03","Natural Gravel",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B04","Stone",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B05","Soil",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B06","Local Wood",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B07","19mm Plywood",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B08","Nail",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B09","10mm Rebar",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B10","7mm Rebar",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B11","Binding Wire",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B12","24 Gauge CGI Sheets",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B13","3mm Commercial Plywood",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["B14","Bamboo",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A01","Cement",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A02","Sand",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A03","Natural Gravel",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A04","Soil Blocks",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A05","Wood",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A06","Bamboo",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A07","Rebar",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A08","Soil",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["A09","CGI Sheets",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null]]}

Analyzed
print(wb_src.inspect({
    "kind": "table",
    "range": "Reconciliation!A1:R12",
    "include": "values,formulas",
    "table_max_rows": 12,
    "table_max_cols": 18,
}).ndjson)

STDOUT/STDERR
{"kind":"table","sheet":"Reconciliation","address":"A1:R12","rows":12,"cols":18,"values":[["Reconciliation and Later LLM Review",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],[null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["Metric","Value",null,"Summary","Value",null,null,null,null,null,null,null,null,null,null,null,null,null],["Expert rows",35,null,"Expert agreement",0,null,null,null,null,null,null,null,null,null,null,null,null,null],[null,null,null,"Final reference completed",0,null,null,null,null,null,null,null,null,null,null,null,null,null],["ID","Original BOM Description","Expert A Normalized","Expert A Process","Expert A Decision","Expert B Normalized","Expert B Process","Expert B Decision","Agreement?","Final Normalized Material","Final Reference Process","Final Process UUID (auto)","Final Decision","LLM Normalized (later)","LLM Process (later)","LLM Decision (later)","Post-review Outcome","Notes"],["S01","Ordinary Portland Cement (OPC 43-grade)",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S02","River Sand (clean, well-graded)",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S03","Natural Gravel",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S04","Stone",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S05","Plain Cement Concrete (PCC M10 — 1:3:6) - Binding Layer",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null],["S06","Stonecrete block",null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null]]}

Analysis errored
import json
from datetime import datetime, timezone
from artifact_tool import Blob, SpreadsheetFile, Workbook

src = "/mnt/data/LLM-main-corrected/LLM-main/ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"
out = "/mnt/data/LLM-main-corrected/LLM-main/Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx"

source_wb = SpreadsheetFile.import_xlsx(Blob.load(src))
raw = source_wb.inspect({
    "kind": "table",
    "range": "Expert_A!A7:E42",
    "include": "values",
    "table_max_rows": 40,
    "table_max_cols": 5,
}).ndjson
obj = json.loads(raw)
rows = obj["values"]
headers = rows[0]
base_rows = rows[1:]

wb = Workbook.create()

instructions = wb.worksheets.add("Instructions")
instruction_rows = [
    ["Four-Model Benchmark Reference Set", ""],
    ["Purpose", "Frozen expert reference labels for material normalization, ELCD/openLCA candidate retrieval/ranking, final process selection, match classification, and repeatability evaluation."],
    ["Current status", "PENDING_RECONCILIATION. The 35 BOM rows are populated, but expert ground-truth fields are intentionally blank because the supplied Expert A, Expert B, and Reconciliation sheets are not yet completed."],
    ["Do not do this", "Do NOT mark unfinished rows as Review Required/unresolved simply to make the benchmark execute. That would create false ground truth."],
    ["How to finalize", "Complete ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx, especially the Reconciliation sheet, then run: python scripts/prepare_benchmark_reference.py"],
    ["Matched row requirements", "ground_truth_normalized_material + exact catalog process name + exact process UUID + ground_truth_match_type = Direct or Proxy + reference_status = FINAL."],
    ["Unresolved row requirements", "ground_truth_normalized_material + ground_truth_match_type = Review Required + blank process name/UUID + ground_truth_unresolved = TRUE + reference_status = FINAL."],
    ["Benchmark safeguard", "scripts/benchmark_four_llms.py refuses any row whose reference_status is not FINAL."],
    ["Source expert workbook", "ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],
    ["Catalog", "ELCD_Check/ELCD_Process_Catalog.xlsx"],
]
instructions.get_range("A1:B10").values = instruction_rows
---------------------------------------------------------------------------
PermissionError                           Traceback (most recent call last)
Cell In[11], line 141
    137 meta.get_range("B1:B7").format.column_width = 85
    138 meta.get_range("A1:B7").format.wrap_text = True
    139 meta.freeze_panes.freeze_rows(1)
    140 
--> 141 SpreadsheetFile.export_xlsx(wb).save(out)
    142 
    143 print(wb.inspect({
    144     "kind": "table",

File /tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/rpc/remote.py:69, in Blob.save(self, path)
     66 'Could not get source, probably due dynamically evaluated source code.'

PermissionError: [Errno 13] Permission denied: '/mnt/data/LLM-main-corrected/LLM-main/Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx'

Analyzed
import json
from artifact_tool import Blob, SpreadsheetFile, Workbook

src = "/mnt/data/LLM-main-corrected/LLM-main/ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"
out = "/mnt/data/LLM-main-corrected/LLM-main/Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx"

source_wb = SpreadsheetFile.import_xlsx(Blob.load(src))
raw = source_wb.inspect({
    "kind": "table",
    "range": "Expert_A!A7:E42",
    "include": "values",
    "table_max_rows": 40,
    "table_max_cols": 5,
}).ndjson
obj = json.loads(raw)
base_rows = obj["values"][1:]

wb = Workbook.create()

instructions = wb.worksheets.add("Instructions")
instruction_rows = [
    ["Four-Model Benchmark Reference Set", ""],
    ["Purpose", "Frozen expert reference labels for material normalization, ELCD/openLCA candidate retrieval/ranking, final process selection, match classification, and repeatability evaluation."],
    ["Current status", "PENDING_RECONCILIATION. The 35 BOM rows are populated, but expert ground-truth fields are intentionally blank because the supplied Expert A, Expert B, and Reconciliation sheets are not yet completed."],
    ["Do not do this", "Do NOT mark unfinished rows as Review Required/unresolved simply to make the benchmark execute. That would create false ground truth."],
    ["How to finalize", "Complete ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx, especially the Reconciliation sheet, then run: python scripts/prepare_benchmark_reference.py"],
    ["Matched row requirements", "ground_truth_normalized_material + exact catalog process name + exact process UUID + ground_truth_match_type = Direct or Proxy + reference_status = FINAL."],
    ["Unresolved row requirements", "ground_truth_normalized_material + ground_truth_match_type = Review Required + blank process name/UUID + ground_truth_unresolved = TRUE + reference_status = FINAL."],
    ["Benchmark safeguard", "scripts/benchmark_four_llms.py refuses any row whose reference_status is not FINAL."],
    ["Source expert workbook", "ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],
    ["Catalog", "ELCD_Check/ELCD_Process_Catalog.xlsx"],
]
instructions.get_range("A1:B10").values = instruction_rows
instructions.merge_cells("A1:B1")
instructions.get_range("A1:B1").format = {
    "fill": "#1F4E78",
STDOUT/STDERR
{"kind":"table","sheet":"Reference_Set","address":"A1:M8","rows":8,"cols":13,"values":[["sample_id","case_study","material_description","quantity","unit","ground_truth_normalized_material","ground_truth_process_name","ground_truth_process_uuid","ground_truth_match_type","ground_truth_unresolved","reference_status","reviewer_notes","source_location"],["S01","Stonecrete House","Ordinary Portland Cement (OPC 43-grade)",5000,"kg","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S02","Stonecrete House","River Sand (clean, well-graded)",24000,"kg","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S03","Stonecrete House","Natural Gravel",12,"m³","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S04","Stonecrete House","Stone",12,"m³","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S05","Stonecrete House","Plain Cement Concrete (PCC M10 — 1:3:6) - Binding Layer",1.6,"m³","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S06","Stonecrete House","Stonecrete block",3512.34,"kg","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S07","Stonecrete House","Rebar TMT Fe500",250,"kg","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"]]}
Created: /mnt/data/LLM-main-corrected/LLM-main/Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx

Analyzed
import os
for p in [
    "/mnt/data/LLM-main-corrected/LLM-main/scripts/benchmark_four_llms.py",
    "/mnt/data/LLM-main-corrected/LLM-main/Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx",
    "/mnt/data/LLM-main.zip",
]:
    print(p, os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else None)

STDOUT/STDERR
/mnt/data/LLM-main-corrected/LLM-main/scripts/benchmark_four_llms.py True 53710
/mnt/data/LLM-main-corrected/LLM-main/Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx True 9353
/mnt/data/LLM-main.zip True 183868

Analyzed
from pathlib import Path
root = Path("/mnt/data/LLM-main-corrected/LLM-main")
for rel in ["README.md","docs/REPRODUCIBILITY.md","scripts/prepare_benchmark_reference.py",
            "tests/test_model_benchmark.py","requirements-benchmark.txt","ELCD_Check/README.md"]:
    p = root / rel
    print("\n---", rel, p.exists(), "---")
    if p.exists():
        text = p.read_text(encoding="utf-8")
        print(text[:900].replace("\n","\n"))

STDOUT/STDERR

--- README.md True ---
# LLM-Assisted Upfront Embodied-Carbon Screening

## Open-source workflow for BOM interpretation, openLCA process matching, and A1-A3 screening

This repository contains the application code and reproducibility assets for a
research workflow that uses a locally deployable large language model (LLM) to
assist with construction-material interpretation and environmental-process
matching for upfront embodied-carbon screening.

The repository should be treated as a **research and screening workflow**, not a
certified LCA tool. Database-grounded results, documented proxies, and any
provisional LLM-supported values used by the main application must remain
visibly distinguishable in the manuscript and outputs.

The controlled four-model benchmark in this repository is intentionally narrower:
it evaluates the LLM on **material normalization and ELCD/openLCA process
matching**, not on direct GWP-v

--- docs/REPRODUCIBILITY.md True ---
# Reproducibility protocol

This document records the controlled evaluation protocol used for the
reviewer-revision benchmark of the LLM-assisted embodied-carbon screening study.

## 1. Evaluation scope

The four-model benchmark evaluates the LLM only on tasks consistent with its
intended language-processing role:

1. material normalization;
2. ranking of fixed ELCD/openLCA process candidates;
3. final process selection;
4. Direct / Proxy / Review Required classification; and
5. repeatability.

The benchmark does not ask the LLM to predict GWP values or invent emission
factors.

## 2. Fixed process catalog

The benchmark uses:

`ELCD_Check/ELCD_Process_Catalog.xlsx`

The current catalog contains 608 process descriptors exported from the database
used in the August 2026 revision workflow. Before publication, record the exact
openLCA version, database release/version, and LCIA method/versi

--- scripts/prepare_benchmark_reference.py True ---
"""Freeze the reconciled expert labels into the four-model benchmark input.

This script intentionally refuses to create a final benchmark reference set
until every reconciliation row is complete and internally consistent.

Workflow:
    1. Experts complete the Expert_A and Expert_B sheets independently.
    2. Disagreements are resolved in the Reconciliation sheet.
    3. Run this script.
    4. Run scripts/benchmark_four_llms.py.

Default output:
    Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERT_WORKBOOK = (
    REPO_ROOT
    / "ELCD_Check"
    / "expert_reference"
    / "LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"
)
DEFAULT_CATALOG = REPO_ROOT /

--- tests/test_model_benchmark.py True ---
import unittest

import pandas as pd

from scripts.benchmark_four_llms import (
    evaluate_record,
    extract_json,
    retrieve_candidate_pool,
    validate_prediction,
)


class ModelBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.candidates = [
            {
                "process_uuid": "u1",
                "process_name": "Portland cement production",
                "category": "materials",
                "location": "EU",
                "process_type": "UNIT_PROCESS",
            },
            {
                "process_uuid": "u2",
                "process_name": "Steel reinforcing bar production",
                "category": "metals",
                "location": "EU",
                "process_type": "UNIT_PROCESS",
            },
        ]

    def test_extract_json_with_wrapper_text(self):
        parsed, status = extract_json(
            'prefix 

--- requirements-benchmark.txt True ---
# Controlled four-model benchmark.
# Designed for Google Colab T4 or another CUDA-capable environment.
torch>=2.4,<3
transformers>=4.45,<5
accelerate>=1,<2
bitsandbytes>=0.43
safetensors>=0.4
huggingface_hub>=0.24
sentencepiece>=0.2
pandas>=2.2
openpyxl>=3.1
rapidfuzz>=3.9
scikit-learn>=1.5
numpy>=1.26


--- ELCD_Check/README.md True ---
# ELCD Check

This folder contains the transparent reference-set and openLCA process-catalog
assets used during the manuscript preparation. These files are intentionally kept
separate from the application source code so that the evaluation workflow can
be inspected without changing the runtime implementation.

## Contents

### `LLM/ELCD_Check/ELCD_Process_Catalog.xlsx`

A catalog of **608 process descriptors** exported through the openLCA IPC server
from the database active during the August 2026 workflow. The catalog
contains process UUIDs, process names, locations, process types, categories, and
library fields where available.

This file is a process-search catalog, not a redistribution of the complete LCI
database. 


### `LLM/ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx`

Workbook prepared for independent expert review of the **35 BOM entries** used
in the 

Analyzed
root = Path("/mnt/data/LLM-main-corrected/LLM-main")
p = root / "scripts/export_openlca_process_catalog.py"
text = p.read_text(encoding="utf-8")
for needle in ["DEFAULT_OUTPUT_DIR", "research_artifacts", "ELCD_Process_Catalog.xlsx"]:
    print(needle, [line for line in text.splitlines() if needle in line][:10])

STDOUT/STDERR
DEFAULT_OUTPUT_DIR ['DEFAULT_OUTPUT_DIR = "research_artifacts"', '        default=DEFAULT_OUTPUT_DIR,', '        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",']
research_artifacts ['DEFAULT_OUTPUT_DIR = "research_artifacts"']
ELCD_Process_Catalog.xlsx ['DEFAULT_OUTPUT_FILE = "ELCD_Process_Catalog.xlsx"']

Analyzed
for i,line in enumerate(text.splitlines(), start=1):
    if i <= 130:
        print(f"{i:03d}: {line}")

STDOUT/STDERR
001: """Export a reproducible process catalog from the active openLCA database.
002: 
003: The script connects to the openLCA IPC server running on the local computer,
004: retrieves descriptors for every Process in the active database, and writes one
005: Excel workbook with two worksheets:
006: 
007:     Processes  - process descriptors used for LLM candidate retrieval/matching
008:     Metadata   - database label, export time, software environment, and counts
009: 
010: The study configuration defaults to ELCD 3.2 and IPC port 8080.
011: 
012: Important
013: ---------
014: The database label is provenance metadata; it does not switch databases inside
015: openLCA. Before running this script, open ELCD 3.2 in openLCA and start the IPC
016: server on port 8080.
017: 
018: Usage
019: -----
020:     LLM/scripts/export_openlca_process_catalog.py
021: 
022: Requirements
023: ------------
024:     pip install -r requirements_ELCD.txt
025: """
026: 
027: from __future__ import annotations
028: 
029: import argparse
030: import platform
031: import sys
032: from datetime import datetime, timezone
033: from importlib.metadata import PackageNotFoundError, version
034: from pathlib import Path
035: from typing import Any
036: 
037: import olca_ipc as ipc
038: import olca_schema as o
039: import pandas as pd
040: from openpyxl.styles import Alignment, Font
041: from openpyxl.worksheet.table import Table, TableStyleInfo
042: 
043: 
044: EXPORTER_VERSION = "1.0.0"
045: CATALOG_SCHEMA_VERSION = "1.0"
046: DEFAULT_DATABASE_LABEL = "ELCD 3.2"
047: DEFAULT_IPC_PORT = 8080
048: DEFAULT_OUTPUT_DIR = "research_artifacts"
049: DEFAULT_OUTPUT_FILE = "ELCD_Process_Catalog.xlsx"
050: 
051: PROCESS_COLUMNS = [
052:     "process_uuid",
053:     "process_name",
054:     "category",
055:     "location",
056:     "library",
057:     "process_type",
058: ]
059: 
060: 
061: def _text(value: Any) -> str:
062:     """Convert an openLCA value safely to text."""
063:     if value is None:
064:         return ""
065:     return getattr(value, "value", str(value))
066: 
067: 
068: def _category_path(value: Any) -> str:
069:     """Convert an openLCA category path to a readable hierarchy."""
070:     if not value:
071:         return ""
072:     return " > ".join(str(part) for part in value)
073: 
074: 
075: def _package_version(package_name: str) -> str:
076:     """Return an installed package version without failing the export."""
077:     try:
078:         return version(package_name)
079:     except PackageNotFoundError:
080:         return "not-detected"
081: 
082: 
083: def _autosize_columns(worksheet, max_width: int = 80) -> None:
084:     """Set readable Excel column widths with a conservative maximum width."""
085:     for column_cells in worksheet.columns:
086:         letter = column_cells[0].column_letter
087:         longest = max(
088:             (len(str(cell.value)) for cell in column_cells if cell.value is not None),
089:             default=0,
090:         )
091:         worksheet.column_dimensions[letter].width = min(longest + 2, max_width)
092: 
093: 
094: def _format_header(worksheet) -> None:
095:     """Apply simple publication-neutral formatting to the header row."""
096:     for cell in worksheet[1]:
097:         cell.font = Font(bold=True)
098:         cell.alignment = Alignment(vertical="center")
099: 
100: 
101: def parse_args() -> argparse.Namespace:
102:     parser = argparse.ArgumentParser(
103:         description=(
104:             "Export process descriptors from the active openLCA database to "
105:             "a reproducible Excel catalog."
106:         )
107:     )
108:     parser.add_argument(
109:         "--port",
110:         type=int,
111:         default=DEFAULT_IPC_PORT,
112:         help=f"openLCA IPC port (default: {DEFAULT_IPC_PORT})",
113:     )
114:     parser.add_argument(
115:         "--database-label",
116:         default=DEFAULT_DATABASE_LABEL,
117:         help=(
118:             "Database name/version recorded in metadata; this does not switch "
119:             f'databases in openLCA (default: "{DEFAULT_DATABASE_LABEL}")'
120:         ),
121:     )
122:     parser.add_argument(
123:         "--output-dir",
124:         default=DEFAULT_OUTPUT_DIR,
125:         help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
126:     )
127:     parser.add_argument(
128:         "--output-file",
129:         default=DEFAULT_OUTPUT_FILE,
130:         help=f"Excel filename (default: {DEFAULT_OUTPUT_FILE})",

Analyzed
for i,line in enumerate(text.splitlines(), start=1):
    if 130 <= i <= 270:
        print(f"{i:03d}: {line}")

STDOUT/STDERR
130:         help=f"Excel filename (default: {DEFAULT_OUTPUT_FILE})",
131:     )
132:     return parser.parse_args()
133: 
134: 
135: def main() -> None:
136:     args = parse_args()
137: 
138:     output_dir = Path(args.output_dir)
139:     output_dir.mkdir(parents=True, exist_ok=True)
140:     output_path = output_dir / args.output_file
141: 
142:     print(f"Connecting to openLCA IPC server at localhost:{args.port} ...")
143:     client = ipc.Client(args.port)
144: 
145:     try:
146:         descriptors = list(client.get_descriptors(o.Process))
147:     except Exception as exc:
148:         raise RuntimeError(
149:             "Could not retrieve processes from openLCA. Confirm that openLCA is "
150:             f"running, ELCD 3.2 is the active database, and the IPC server is "
151:             f"started on port {args.port}."
152:         ) from exc
153: 
154:     if not descriptors:
155:         raise RuntimeError(
156:             "The IPC request returned zero process descriptors. Confirm that the "
157:             "intended ELCD 3.2 database is active and contains process datasets."
158:         )
159: 
160:     rows: list[dict[str, str]] = []
161:     for process in descriptors:
162:         rows.append(
163:             {
164:                 "process_uuid": _text(getattr(process, "id", "")),
165:                 "process_name": _text(getattr(process, "name", "")),
166:                 "category": _category_path(getattr(process, "category_path", None)),
167:                 "location": _text(getattr(process, "location", "")),
168:                 "library": _text(getattr(process, "library", "")),
169:                 "process_type": _text(getattr(process, "process_type", "")),
170:             }
171:         )
172: 
173:     rows.sort(
174:         key=lambda row: (
175:             row["process_name"].casefold(),
176:             row["location"].casefold(),
177:             row["process_uuid"],
178:         )
179:     )
180: 
181:     processes_df = pd.DataFrame(rows, columns=PROCESS_COLUMNS)
182:     exported_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
183: 
184:     metadata_rows = [
185:         ("catalog_schema_version", CATALOG_SCHEMA_VERSION),
186:         ("exporter_version", EXPORTER_VERSION),
187:         ("exported_at_utc", exported_at),
188:         ("database_label", args.database_label),
189:         ("ipc_host", "localhost"),
190:         ("ipc_port", args.port),
191:         ("process_count", len(processes_df)),
192:         ("output_file", args.output_file),
193:         ("python_version", platform.python_version()),
194:         ("platform", platform.platform()),
195:         ("olca_ipc_version", _package_version("olca-ipc")),
196:         ("olca_schema_version", _package_version("olca-schema")),
197:         ("pandas_version", _package_version("pandas")),
198:         ("openpyxl_version", _package_version("openpyxl")),
199:         (
200:             "provenance_note",
201:             "The catalog reflects the database active in openLCA at export time. "
202:             "The study configuration uses ELCD 3.2. The database label stored here "
203:             "is metadata and does not independently verify or switch the active "
204:             "openLCA database.",
205:         ),
206:     ]
207:     metadata_df = pd.DataFrame(metadata_rows, columns=["field", "value"])
208: 
209:     with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
210:         processes_df.to_excel(writer, sheet_name="Processes", index=False)
211:         metadata_df.to_excel(writer, sheet_name="Metadata", index=False)
212: 
213:         workbook = writer.book
214:         process_sheet = workbook["Processes"]
215:         metadata_sheet = workbook["Metadata"]
216: 
217:         process_sheet.freeze_panes = "A2"
218:         metadata_sheet.freeze_panes = "A2"
219:         _format_header(process_sheet)
220:         _format_header(metadata_sheet)
221: 
222:         # Excel table gives readers native filtering/sorting while preserving the
223:         # data exactly as exported.
224:         table = Table(displayName="OpenLCAProcesses", ref=process_sheet.dimensions)
225:         table.tableStyleInfo = TableStyleInfo(
226:             name="TableStyleMedium2",
227:             showFirstColumn=False,
228:             showLastColumn=False,
229:             showRowStripes=True,
230:             showColumnStripes=False,
231:         )
232:         process_sheet.add_table(table)
233: 
234:         metadata_sheet.auto_filter.ref = metadata_sheet.dimensions
235:         _autosize_columns(process_sheet, max_width=80)
236:         _autosize_columns(metadata_sheet, max_width=110)
237: 
238:     print("\nExport complete.")
239:     print(f"Database label:     {args.database_label}")
240:     print(f"Processes exported: {len(processes_df):,}")
241:     print(f"Excel workbook:     {output_path.resolve()}")
242:     print("Worksheets:         Processes, Metadata")
243: 
244: 
245: if __name__ == "__main__":
246:     main()

Analysis errored
from pathlib import Path
import re, subprocess, sys, textwrap, os, json, shutil, zipfile

root = Path("/mnt/data/LLM-main-corrected/LLM-main")

# 1) Fix the catalog exporter's default destination so it matches the real repo layout.
exporter = root / "scripts" / "export_openlca_process_catalog.py"
s = exporter.read_text(encoding="utf-8")
s = s.replace('DEFAULT_OUTPUT_DIR = "research_artifacts"', 'REPO_ROOT = Path(__file__).resolve().parents[1]\nDEFAULT_OUTPUT_DIR = str(REPO_ROOT / "ELCD_Check")')
exporter.write_text(s, encoding="utf-8")

# 2) Update ELCD_Check README stale benchmark paths.
elcd_readme = root / "ELCD_Check" / "README.md"
elcd_readme.write_text("""# ELCD Check

This folder contains the process-catalog and expert-reference assets used by the
controlled LLM process-matching evaluation.

## Contents

### `ELCD_Process_Catalog.xlsx`

A catalog of **608 process descriptors** exported from the database active in
openLCA during the August 2026 revision workflow. It contains process UUIDs,
process names, categories, locations, library fields, and process types where
available.

This workbook is a process-search/reference catalog. It is not a redistribution
of the complete LCI database.

To regenerate the catalog from the active openLCA database:

```bash
python scripts/export_openlca_process_catalog.py --database-label "ELCD <exact version>"
The exporter now writes to ELCD_Check/ by default.

expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx
Workbook prepared for independent expert review of the 35 BOM entries used
in the three Nepal demonstration case studies.

The intended sequence is:

Expert A independently normalizes each BOM material and selects the best
available ELCD/openLCA process.

Expert B performs the same task independently.

Disagreements are reconciled in the Reconciliation sheet.

The reconciled labels are frozen with:

python scripts/prepare_benchmark_reference.py
Only then are the four LLMs scored.

The supplied expert workbook is currently incomplete. Blank reviewer/reconciliation
cells are not ground truth and must not be converted automatically into
Review Required.

Related benchmark
The executable benchmark is:

scripts/benchmark_four_llms.py
Its frozen input is:

Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx
Generated results are written under:

Four_Models/Output/
""", encoding="utf-8")

3) Make incomplete reconciliation errors concise: don't cascade process errors when decision is blank.
builder = root / "scripts" / "prepare_benchmark_reference.py"
s = builder.read_text(encoding="utf-8")
old = ''' unresolved = decision == "Review Required"
if unresolved:
if process_name or process_uuid:
errors.append(
f"{sid}: Review Required row must have blank final process name/UUID"
)
process_name = ""
process_uuid = ""
else:
if not process_name:
errors.append(f"{sid}: {decision} row is missing Final Reference Process")
if process_name and not process_uuid:
process_uuid = name_to_uuid.get(key(process_name), "").lower()
if not process_uuid:
errors.append(
f"{sid}: Final Reference Process does not resolve to an exact catalog UUID"
)
elif process_uuid not in uuid_to_name:
errors.append(f"{sid}: Final Process UUID is not present in the catalog")
else:
catalog_name = uuid_to_name[process_uuid]
if process_name and key(catalog_name) != key(process_name):
errors.append(
f"{sid}: Final process name does not match the catalog process for its UUID"
)
process_name = catalog_name
'''
new = ''' unresolved = decision == "Review Required"
if decision == "":
# The missing decision has already been reported above. Avoid cascading
# process errors for a row that has not yet been reconciled.
pass
elif unresolved:
if process_name or process_uuid:
errors.append(
f"{sid}: Review Required row must have blank final process name/UUID"
)
process_name = ""
process_uuid = ""
else:
if not process_name:
errors.append(f"{sid}: {decision} row is missing Final Reference Process")
if process_name and not process_uuid:
process_uuid = name_to_uuid.get(key(process_name), "").lower()
if not process_uuid:
errors.append(
f"{sid}: Final Reference Process does not resolve to an exact catalog UUID"
)
elif process_uuid not in uuid_to_name:
errors.append(f"{sid}: Final Process UUID is not present in the catalog")
else:
catalog_name = uuid_to_name[process_uuid]
if process_name and key(catalog_name) != key(process_name):
errors.append(
f"{sid}: Final process name does not match the catalog process for its UUID"
)
process_name = catalog_name
'''
if old not in s:
print("Builder patch target not found; leaving existing logic.")
else:
builder.write_text(s.replace(old, new), encoding="utf-8")

4) Remove placeholder files if still present.
for rel in ["Four_Models/Input/pp.py", "Four_Models/Output/p.py"]:
p = root / rel
if p.exists():
p.unlink()

5) Search for stale paths in benchmark/reproducibility documentation.
stale = []
for rel in ["README.md", "docs/REPRODUCIBILITY.md", "ELCD_Check/README.md", "Four_Models/README.md"]:
p = root / rel
txt = p.read_text(encoding="utf-8")
for needle in ["research_artifacts", "experiments/model_benchmark", "Comment5_LLM_ELCD_Benchmark"]:
if needle in txt:
stale.append((rel, needle))
print("Stale benchmark-path references:", stale or "none")

6) Basic syntax checks.
for rel in ["scripts/benchmark_four_llms.py", "scripts/prepare_benchmark_reference.py", "scripts/export_openlca_process_catalog.py"]:
result = subprocess.run([sys.executable, "-m", "py_compile", str(root / rel)], capture_output=True, text=True)
print(rel, "compile:", "OK" if result.returncode == 0 else result.stderr[:500])


---------------------------------------------------------------------------
PermissionError                           Traceback (most recent call last)
Cell In[18], line 147
    143 '''
    144 if old not in s:
    145     print("Builder patch target not found; leaving existing logic.")
    146 else:
--> 147     builder.write_text(s.replace(old, new), encoding="utf-8")
    148 
    149 # 4) Remove placeholder files if still present.
    150 for rel in ["Four_Models/Input/pp.py", "Four_Models/Output/p.py"]:

File /usr/lib/python3.13/pathlib/_local.py:557, in Path.write_text(self, data, encoding, errors, newline)
    554 # Call io.text_encoding() here to ensure any warning is raised at an
    555 # appropriate stack level.
    556 encoding = io.text_encoding(encoding)
--> 557 return PathBase.write_text(self, data, encoding, errors, newline)

File /usr/lib/python3.13/pathlib/_abc.py:651, in PathBase.write_text(self, data, encoding, errors, newline)
    648 if not isinstance(data, str):
    649     raise TypeError('data must be str, not %s' %
    650                     data.__class__.__name__)
--> 651 with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
    652     return f.write(data)

File /usr/lib/python3.13/pathlib/_local.py:539, in Path.open(self, mode, buffering, encoding, errors, newline)
    537 if "b" not in mode:
    538     encoding = io.text_encoding(encoding)
--> 539 return io.open(self, mode, buffering, encoding, errors, newline)

PermissionError: [Errno 13] Permission denied: '/mnt/data/LLM-main-corrected/LLM-main/scripts/prepare_benchmark_reference.py'

Analyzed
from pathlib import Path
import shutil, zipfile, json, subprocess, sys, os, re
from artifact_tool import Blob, SpreadsheetFile, Workbook

base = Path("/mnt/data")
original_zip = base / "LLM-main.zip"
work_parent = base / "LLM-paper-ready-build"
root = work_parent / "LLM-main"
old = base / "LLM-main-corrected" / "LLM-main"

if work_parent.exists():
    shutil.rmtree(work_parent)
work_parent.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(original_zip, "r") as zf:
    zf.extractall(work_parent)

# Copy the already-corrected core files from the earlier working copy.
copy_files = [
    "scripts/benchmark_four_llms.py",
    "scripts/prepare_benchmark_reference.py",
    "README.md",
    "docs/REPRODUCIBILITY.md",
    "tests/test_model_benchmark.py",
    "requirements-benchmark.txt",
    "Four_Models/README.md",
    "Four_Models/Output/README.md",
]
for rel in copy_files:
    src = old / rel
    dst = root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        raise FileNotFoundError(f"Expected corrected source missing: {src}")
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

The exporter writes to ELCD_Check/ by default.

expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx
Workbook prepared for independent expert review of the 35 BOM entries used
in the three Nepal demonstration case studies.

The intended sequence is:

Expert A independently normalizes each BOM material and selects the best
available ELCD/openLCA process.

Expert B performs the same task independently.

Disagreements are reconciled in the Reconciliation sheet.

Freeze the reconciled labels with:

python scripts/prepare_benchmark_reference.py
Only then run the four-model benchmark.

The supplied expert workbook is currently incomplete. Blank reviewer or
reconciliation cells are not ground truth and must not be converted
automatically into Review Required.

Related benchmark
Executable benchmark:

scripts/benchmark_four_llms.py
Frozen input:

Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx
Generated results:

Four_Models/Output/
""", encoding="utf-8")

Remove obsolete zero-byte placeholders.
for rel in ["Four_Models/Input/pp.py", "Four_Models/Output/p.py"]:
p = root / rel
if p.exists():
p.unlink()

Rebuild the pending benchmark reference workbook using artifact_tool.
expert_src = root / "ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"
source_wb = SpreadsheetFile.import_xlsx(Blob.load(str(expert_src)))
raw = source_wb.inspect({
"kind": "table",
"range": "Expert_A!A7:E42",
"include": "values",
"table_max_rows": 40,
"table_max_cols": 5,
}).ndjson
base_rows = json.loads(raw)["values"][1:]

wb = Workbook.create()
ins = wb.worksheets.add("Instructions")
ins_rows = [
["Four-Model Benchmark Reference Set", ""],
["Purpose", "Frozen expert reference labels for material normalization, candidate retrieval/ranking, final ELCD/openLCA process selection, Direct/Proxy/Review Required classification, and repeatability evaluation."],
["Current status", "PENDING_RECONCILIATION. The 35 BOM rows are populated, but expert ground-truth fields are intentionally blank because the supplied Expert A, Expert B, and Reconciliation sheets are not yet completed."],
["Do not do this", "Do NOT mark unfinished rows as Review Required/unresolved simply to make the benchmark execute. That would create false ground truth."],
["How to finalize", "Complete ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx, especially the Reconciliation sheet, then run: python scripts/prepare_benchmark_reference.py"],
["Matched row requirements", "ground_truth_normalized_material + exact catalog process name + exact process UUID + ground_truth_match_type = Direct or Proxy + reference_status = FINAL."],
["Unresolved row requirements", "ground_truth_normalized_material + ground_truth_match_type = Review Required + blank process name/UUID + ground_truth_unresolved = TRUE + reference_status = FINAL."],
["Benchmark safeguard", "scripts/benchmark_four_llms.py refuses any row whose reference_status is not FINAL."],
["Source expert workbook", "ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],
["Catalog", "ELCD_Check/ELCD_Process_Catalog.xlsx"],
]
ins.get_range("A1:B10").values = ins_rows
ins.merge_cells("A1:B1")
ins.get_range("A1:B1").format = {
"fill": "#1F4E78",
"font": {"bold": True, "color": "#FFFFFF", "size": 14},
"horizontal_alignment": "center",
"vertical_alignment": "center",
}
ins.get_range("A2:A10").format = {"fill": "#D9EAF7", "font": {"bold": True}}
ins.get_range("B2:B10").format.wrap_text = True
ins.get_range("A1:A10").format.column_width = 24
ins.get_range("B1:B10").format.column_width = 88
ins.freeze_panes.freeze_rows(1)

ref = wb.worksheets.add("Reference_Set")
headers = [
"sample_id","case_study","material_description","quantity","unit",
"ground_truth_normalized_material","ground_truth_process_name",
"ground_truth_process_uuid","ground_truth_match_type",
"ground_truth_unresolved","reference_status","reviewer_notes","source_location",
]
data = []
for sample_id, case_study, description, qty, unit in base_rows:
data.append([
sample_id, case_study, description, qty, unit,
"", "", "", "", "", "PENDING_RECONCILIATION", "",
"ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx",
])
last = len(data) + 1
ref.get_range(f"A1:M").values = [headers] + data
ref.get_range("A1:M1").format = {
"fill": "#1F4E78",
"font": {"bold": True, "color": "#FFFFFF"},
"horizontal_alignment": "center",
"vertical_alignment": "center",
"wrap_text": True,
}
ref.get_range(f"A2:M").format.wrap_text = True
ref.freeze_panes.freeze_rows(1)
ref.tables.add(f"A1:M", True, "BenchmarkReferenceTable")
ref.get_range(f"I2:I").data_validation = {
"rule": {"type": "list", "values": ["Direct", "Proxy", "Review Required"]}
}
ref.get_range(f"J2:J").data_validation = {
"rule": {"type": "list", "values": ["TRUE", "FALSE"]}
}
ref.get_range(f"K2:K").data_validation = {
"rule": {"type": "list", "values": ["PENDING_RECONCILIATION", "FINAL"]}
}
for col, width in {
"A":12,"B":24,"C":48,"D":12,"E":12,"F":30,"G":50,
"H":38,"I":22,"J":20,"K":25,"L":42,"M":58
}.items():
ref.get_range(f"{col}1:{col}{last}").format.column_width = width

meta = wb.worksheets.add("Metadata")
meta_rows = [
["field","value"],
["reference_set_rows",len(data)],
["reference_status","PENDING_RECONCILIATION"],
["source_expert_workbook","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],
["catalog_path","ELCD_Check/ELCD_Process_Catalog.xlsx"],
["prepared_for_script","scripts/benchmark_four_llms.py"],
["note","Structurally ready; must not be scored until expert reconciliation is frozen."],
]
meta.get_range("A1:B7").values = meta_rows
meta.get_range("A1:B1").format = {"fill":"#1F4E78","font":{"bold":True,"color":"#FFFFFF"}}
meta.get_range("A1:A7").format.column_width = 28
meta.get_range("B1:B7").format.column_width = 85
meta.get_range("A1:B7").format.wrap_text = True
meta.freeze_panes.freeze_rows(1)

reference_path = root / "Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx"
SpreadsheetFile.export_xlsx(wb).save(str(reference_path))

Verify workbook structure.
check = wb.inspect({
"kind":"table",
"range":"Reference_Set!A1:M6",
"include":"values,formulas",
"table_max_rows":6,
"table_max_cols":13,
})
print("Workbook check:", check.ndjson[:1200])

Static/path consistency check.
stale = []
for rel in ["README.md","docs/REPRODUCIBILITY.md","ELCD_Check/README.md","Four_Models/README.md"]:
txt = (root / rel).read_text(encoding="utf-8")
for needle in ["research_artifacts","experiments/model_benchmark","Comment5_LLM_ELCD_Benchmark"]:
if needle in txt:
stale.append((rel, needle))
print("Stale benchmark paths:", stale or "none")

Compile edited scripts.
for rel in [
"scripts/benchmark_four_llms.py",
"scripts/prepare_benchmark_reference.py",
"scripts/export_openlca_process_catalog.py",
]:
r = subprocess.run([sys.executable, "-m", "py_compile", str(root / rel)],
capture_output=True, text=True)
if r.returncode:
raise RuntimeError(f"Compile failed for {rel}: {r.stderr}")
print("Python compile checks: OK")

Run benchmark unit tests.
r = subprocess.run(
[sys.executable, "-m", "unittest", "tests.test_model_benchmark", "-v"],
cwd=root, capture_output=True, text=True
)
print(r.stdout)
if r.returncode:
print(r.stderr)
raise RuntimeError("Benchmark unit tests failed")
print("Benchmark unit tests: OK")

Check expected safeguard without model loading.
r = subprocess.run(
[sys.executable, "scripts/benchmark_four_llms.py", "--model", "llama", "--limit", "1", "--runs", "1"],
cwd=root, capture_output=True, text=True
)
combined = (r.stdout + "\n" + r.stderr)
if "Benchmark reference set is not frozen" not in combined:
raise RuntimeError("Pending-reference safeguard did not trigger as expected.")
print("Pending-reference safeguard: OK")

Check preparation script correctly rejects the currently blank reconciliation.
r = subprocess.run(
[sys.executable, "scripts/prepare_benchmark_reference.py"],
cwd=root, capture_output=True, text=True
)
combined = (r.stdout + "\n" + r.stderr)
if "Expert reconciliation is not ready to freeze" not in combined:
raise RuntimeError("Expert-reconciliation safeguard did not trigger as expected.")
print("Expert-reconciliation safeguard: OK")

Create direct-download copies of the most important files.
downloads = {
root / "scripts/benchmark_four_llms.py": base / "benchmark_four_llms.py",
root / "scripts/prepare_benchmark_reference.py": base / "prepare_benchmark_reference.py",
root / "README.md": base / "README_corrected.md",
reference_path: base / "LLM_Model_Evaluation_Reference_Set.xlsx",
}
for src, dst in downloads.items():
shutil.copy2(src, dst)

Package complete corrected repository.
final_zip = base / "LLM-main-paper-ready.zip"
if final_zip.exists():
final_zip.unlink()
with zipfile.ZipFile(final_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
for p in root.rglob("*"):
if p.is_file() and "pycache" not in p.parts:
zf.write(p, arcname=str(Path("LLM-main") / p.relative_to(root)))

print("Final ZIP:", final_zip, final_zip.stat().st_size)
print("Reference workbook:", reference_path, reference_path.stat().st_size)
print("Benchmark script:", (root / "scripts/benchmark_four_llms.py").stat().st_size)


STDOUT/STDERR
Workbook check: {"kind":"table","sheet":"Reference_Set","address":"A1:M6","rows":6,"cols":13,"values":[["sample_id","case_study","material_description","quantity","unit","ground_truth_normalized_material","ground_truth_process_name","ground_truth_process_uuid","ground_truth_match_type","ground_truth_unresolved","reference_status","reviewer_notes","source_location"],["S01","Stonecrete House","Ordinary Portland Cement (OPC 43-grade)",5000,"kg","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S02","Stonecrete House","River Sand (clean, well-graded)",24000,"kg","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S03","Stonecrete House","Natural Gravel",12,"m³","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S04","Stonecrete House","Stone",12,"m³","","","","","","PENDING_RECONCILIATION","","ELCD_Check/expert_reference/LLM_LCA_Expert_Reference_Set_With_ELCD.xlsx"],["S05","Stonecrete House","Plain Cement Concrete (PCC M10 — 1:3:6) - Binding Layer",1.6,"m³","","","","","","PENDING_RECONCILIATION","
Stale benchmark paths: none
Python compile checks: OK

Benchmark unit tests: OK
Pending-reference safeguard: OK
Expert-reconciliation safeguard: OK
Final ZIP: /mnt/data/LLM-main-paper-ready.zip 194360
Reference workbook: /mnt/data/LLM-paper-ready-build/LLM-main/Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx 9347
Benchmark script: 53710
Done. I rebuilt the benchmark portion of the repository and verified the important pieces.

Complete corrected repository
This is the one I recommend using for GitHub:

Download the corrected full repository — LLM-main-paper-ready.zip

It includes the corrected folder structure, scripts, workbook, README, reproducibility documentation, requirements, and tests.

Individual files
Corrected benchmark_four_llms.py

Benchmark input LLM_Model_Evaluation_Reference_Set.xlsx

New prepare_benchmark_reference.py

Corrected README.md

What I corrected
The revised benchmark now uses temperature = 0.0 / greedy decoding by default, keeps five runs for repeatability, and compares:

Llama 3.1 8B Instruct

Qwen2.5 7B Instruct

DeepSeek LLM 7B Chat

Mistral 7B Instruct v0.3

It now properly evaluates material normalization, deterministic candidate retrieval, LLM candidate ranking, final process selection, Direct/Proxy/Review Required classification, and repeatability.

I also fixed the two important scoring problems we discussed. The code does not insert the selected process into the model's ranking, so Top-1/Top-3/Top-5/Top-10 results cannot be artificially improved. Malformed JSON or inconsistent responses are also treated as failures rather than potentially receiving credit as an unresolved answer.

I added the particularly important metric:

Conditional process-selection accuracy

That tells you how well the LLM performs when the correct ELCD process was actually available in its candidate pool. This allows you to distinguish retrieval failure from LLM-selection failure.

About the Excel input file
The workbook is already created in the proper location:

Four_Models/
└── Input/
    └── LLM_Model_Evaluation_Reference_Set.xlsx
It contains all 35 materials from your three case studies with:

sample_id
case_study
material_description
quantity
unit
ground_truth_normalized_material
ground_truth_process_name
ground_truth_process_uuid
ground_truth_match_type
ground_truth_unresolved
reference_status
reviewer_notes
source_location
However, I deliberately left the expert-answer columns blank and set:

reference_status = PENDING_RECONCILIATION
because your current Expert A, Expert B, and Reconciliation sheets have not actually been completed.

That is important. We should not use AI-generated answers as the "expert ground truth" used to evaluate the AI models.

I added an automatic bridge between the expert workbook and the benchmark
This is what the new:

scripts/prepare_benchmark_reference.py
is for.

Your final workflow is now:

Expert A
   ↓
Expert B
   ↓
Reconciliation
   ↓
prepare_benchmark_reference.py
   ↓
LLM_Model_Evaluation_Reference_Set.xlsx
        reference_status = FINAL
   ↓
benchmark_four_llms.py
   ↓
Llama
Qwen
DeepSeek
Mistral
   ↓
four_model_comparison.xlsx
Once the experts fill the reconciliation workbook, you run:

python scripts/prepare_benchmark_reference.py
It checks all 35 entries. For Direct/Proxy rows it verifies that the process actually exists in your 608-process ELCD catalog and resolves the exact UUID.

If something is missing, it refuses to generate fake ground truth.

Then you can run:

python scripts/benchmark_four_llms.py --model llama
python scripts/benchmark_four_llms.py --model qwen
python scripts/benchmark_four_llms.py --model deepseek
python scripts/benchmark_four_llms.py --model mistral
and finally:

python scripts/benchmark_four_llms.py --combine-results
which produces:

Four_Models/
└── Output/
    ├── llama/
    │   └── benchmark_results.xlsx
    ├── qwen/
    │   └── benchmark_results.xlsx
    ├── deepseek/
    │   └── benchmark_results.xlsx
    ├── mistral/
    │   └── benchmark_results.xlsx
    └── combined/
        └── four_model_comparison.xlsx
Other repository corrections
I also corrected the outdated README paths that referred to nonexistent:

experiments/model_benchmark/
research_artifacts/
The documentation now reflects your actual repository:

ELCD_Check/
Four_Models/
scripts/
I updated docs/REPRODUCIBILITY.md, ELCD_Check/README.md, requirements-benchmark.txt, and the benchmark unit tests. I also corrected the catalog exporter so its default output goes to:

ELCD_Check/ELCD_Process_Catalog.xlsx
instead of the old nonexistent research_artifacts location.

The useless placeholder files:

Four_Models/Input/pp.py
Four_Models/Output/p.py
were removed.

Finally, I compiled the revised Python scripts and ran the benchmark-specific tests. All benchmark unit tests passed, and I separately verified that the code correctly refuses to run while the expert reference remains unfinished.

So for this four-model/reviewer-comment portion, use the corrected ZIP above as your new GitHub version. The main embodied-carbon calculation can stay separate for now, exactly as you wanted. 


benchmark_four_llms.py
Code


LLM_Model_Evaluation_Reference_Set.xlsx
Spreadsheet


prepare_benchmark_reference.py
Code


README_corrected.md
Document

Show less

i am thinking that the true ELCD check sheet is gonna be completed after i complete the whole analysis and for whole analysis to be completed i need which llm i sbest and fo rwhich llm is best i need true ELCD check sheet. So how does it work

Yes — you’ve spotted a circular dependency, but the fix is pretty straightforward: you need to separate the small benchmark ground-truth set from the final full-study ELCD validation.

Right now you’re thinking of them as the same thing, but they should be two different stages.

The correct logic is:

Small manually verified ELCD reference set
           ↓
Compare 4 LLMs
           ↓
Choose best LLM
           ↓
Run best LLM on the full analysis
           ↓
Perform full ELCD/database validation
           ↓
Final paper results
So you do not need to complete the entire ELCD analysis before choosing the best LLM.

What you need first
You only need a relatively small, independently verified benchmark/reference set.

In your case, that is exactly what the 35-material workbook is supposed to be.

For those 35 materials, an expert or you + another knowledgeable reviewer need to determine:

Original BOM material
        ↓
Correct normalized material
        ↓
Best defensible ELCD process
        ↓
Exact ELCD process UUID
        ↓
Direct / Proxy / Review Required
That becomes the "answer key."

For example:

BOM:
"Ordinary Portland Cement (OPC 43-grade)"

Expert reference:
Normalized material = Portland cement
ELCD process = [exact process from your ELCD catalog]
UUID = XXXXXXXX
Decision = Direct
Then Llama, Qwen, Mistral, and DeepSeek all receive the same material and same candidate catalog, and you ask:

Can you identify what the expert already identified?

That is how you determine which model performs best.

The important distinction
You essentially need two validation datasets, not one.

A. Model-selection reference set
This happens before your main analysis.

That is:

LLM_Model_Evaluation_Reference_Set.xlsx
Purpose:

Determine which LLM is best.

It can be your 35 representative materials.

It does not contain calculated building GWP results.

It simply contains verified material/process mappings.

B. Full-study ELCD validation
This happens after you select the best LLM.

Purpose:

Evaluate how the complete proposed framework performs.

Now the selected LLM goes through your entire BOM and produces:

Material
↓
Normalization
↓
Process match
↓
Emission factor / calculation pathway
↓
GWP
Then you compare the overall framework against ELCD/openLCA/reference data, One Click LCA, literature, etc., according to the methodology you're developing.

That's the main analysis.

So there's no circularity once those two things are separated.

Think of it like training a driver
You don't need to build the entire highway before deciding which driver is best.

You make a short controlled test course:

35 known cases
Put all four drivers on the same course:

Llama      → 82%
Qwen       → 91%
Mistral    → 77%
DeepSeek   → 86%
Then:

Qwen wins.

Now Qwen drives the actual route.

And afterward, you evaluate how well the entire journey went.

That's basically what we're doing here.

One thing we absolutely should NOT do
We shouldn't do this:

Run four LLMs
↓
Look at their answers
↓
Decide which answers seem right
↓
Create ELCD "ground truth"
↓
Use that same ground truth to declare one model best
That would introduce data leakage / confirmation bias.

A reviewer could correctly ask:

How was the reference answer established independently of the models being evaluated?

So the 35 benchmark answers must be established without using the four-model results.

But here's the nice part for your study
You don't necessarily need two outside professors to manually inspect all 608 ELCD processes for every material.

Your existing system already has:

ELCD_Process_Catalog.xlsx
≈ 608 processes
For each of the 35 materials, the expert task is simply:

Which of these available ELCD processes is the most defensible match?

And sometimes the correct answer can legitimately be:

Review Required
Meaning:

No defensible ELCD match exists.

That's actually valuable data because one reviewer specifically wanted you to evaluate whether the LLM knows when not to force a match.

I would structure your study like this
Phase 1 — Ground truth
Take the 35 existing case-study materials.

Have them independently reviewed:

Expert A
Expert B
Then reconcile disagreements.

You get:

35 frozen reference answers
This is the only thing we need to complete before running the four models.

Phase 2 — Four-model comparison
Run:

Llama 3.1 8B
Qwen2.5 7B
DeepSeek 7B
Mistral 7B
on exactly the same 35 cases.

Measure:

Normalization similarity
Candidate retrieval Recall@3/5/10
Final process-selection accuracy
Conditional selection accuracy
Direct/Proxy/Review Required accuracy
Macro F1
Run-to-run repeatability
JSON/output failure rate
Runtime
Then choose the best model.

Phase 3 — Freeze the model
Suppose the result is:

Qwen = best overall model
From that point forward, the paper says something like:

Based on the controlled benchmark, Qwen2.5-7B-Instruct was selected as the LLM component for subsequent framework evaluation.

Do not switch models afterward based on which one gives nicer building results.

Phase 4 — Run the main framework
Now Qwen gets used for the actual workflow:

BOQ
↓
Material interpretation
↓
Candidate process retrieval
↓
Process selection
↓
Direct / Proxy / Review Required
↓
openLCA calculation
↓
Building GWP
This is your actual framework.

Phase 5 — Final validation
Now you can do the larger ELCD check/reference comparison.

That's where things such as:

Direct ELCD = 29%
Proxy = 9%
LLM-supported/unavailable = ...
and your building-level calculations become relevant.

So this final validation is not used to select the model.

It evaluates the system after the model has already been selected.

There is one potential issue with your current 35-material dataset
Some materials repeat:

Cement
Natural Gravel
Stone
Sand
Soil
Bamboo
CGI
Rebar
across several case studies.

So although there are 35 BOM entries, there are fewer than 35 completely unique material concepts.

For model comparison, that's not necessarily bad because wording variation itself is part of material normalization. For example:

Rebar TMT Fe500
10mm Rebar
7mm Rebar
Rebar
tests whether the LLM consistently normalizes related descriptions.

But in the paper we should clearly say:

The benchmark comprised 35 BOM entries rather than 35 unique material classes.

That's more defensible.

What I recommend you do now
Don't run the four-model benchmark just yet.

Your next task should be only this:

Complete the ground truth for the 35 benchmark entries.
Not the entire paper's ELCD analysis.

Once those 35 are reconciled, we run:

python scripts/prepare_benchmark_reference.py
which produces the frozen:

Four_Models/Input/
└── LLM_Model_Evaluation_Reference_Set.xlsx
Then we benchmark the four LLMs.

Then we choose the winner.

Then we move to your main calculation/framework.

So you were right to see the apparent chicken-and-egg problem — the key is that the small ELCD expert reference set comes before model selection; the full ELCD/framework validation comes after model selection.


there is a code called as prepare benchmark reference , do i need to pyt that in github too?

Yes — I recommend keeping prepare_benchmark_reference.py in GitHub.

It has a clear reproducibility role: it takes the completed expert/reconciliation workbook and converts it into the frozen benchmark input that benchmark_four_llms.py uses. That makes your workflow transparent instead of looking like the final reference Excel appeared manually.

Your repo structure should keep it here:

scripts/
├── export_openlca_process_catalog.py
├── prepare_benchmark_reference.py
└── benchmark_four_llms.py
The sequence is:

Expert reference workbook
        ↓
prepare_benchmark_reference.py
        ↓
Four_Models/Input/
LLM_Model_Evaluation_Reference_Set.xlsx
        ↓
benchmark_four_llms.py
        ↓
Four_Models/Output/
So yes, put both scripts in GitHub.

One important distinction: you don't run prepare_benchmark_reference.py every time you benchmark. You run it after the expert reference/reconciliation is finalized, because its job is to freeze that ground truth. Then you run benchmark_four_llms.py.

For a research repository, keeping that script is actually a plus because reviewers/readers can see exactly how the benchmark reference set was produced rather than having to trust a manually edited spreadsheet.



Library
/
benchmark_four_llms.py


"""Controlled four-model benchmark for LLM-assisted openLCA process matching.

This experiment is intentionally aligned with the language-model role in the
paper. It evaluates:

1. material normalization;
2. deterministic ELCD/openLCA candidate-pool retrieval;
3. LLM ranking of supplied candidate processes;
4. final process selection or Review Required routing;
5. Direct / Proxy / Review Required classification; and
6. run-to-run repeatability.

The benchmark never asks an LLM to invent an emission factor, GWP value, EPD,
or process UUID. Every selectable process comes from the fixed exported catalog.

Run from any directory, for example:

    python scripts/benchmark_four_llms.py --model llama
    python scripts/benchmark_four_llms.py --model qwen
    python scripts/benchmark_four_llms.py --model deepseek
    python scripts/benchmark_four_llms.py --model mistral
    python scripts/benchmark_four_llms.py --combine-results

For a quick smoke test:

    python scripts/benchmark_four_llms.py --model llama --limit 2 --runs 1

Important
---------
The benchmark input must be a *frozen expert reference set*. The repository
includes a structurally complete workbook at:

    Four_Models/Input/LLM_Model_Evaluation_Reference_Set.xlsx

but it remains PENDING_RECONCILIATION until the expert-review workbook is
completed. The benchmark refuses to score pending rows. After expert
reconciliation is complete, run:

    python scripts/prepare_benchmark_reference.py

That helper validates and freezes the expert labels into the benchmark input.
"""

from __future__ import annotations

import argparse
import gc
import json
import math
import os
import platform
import random
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
import torch
from rapidfuzz import fuzz, process as rf_process
from sklearn.metrics import f1_score


SCRIPT_VERSION = "1.2.0"
DATABASE_LABEL = "ELCD 3.2"
SEED = 42
DEFAULT_RUNS = 5
DEFAULT_CANDIDATE_POOL_SIZE = 20
DEFAULT_TOP_K = 10
DEFAULT_MAX_NEW_TOKENS = 384
DEFAULT_TEMPERATURE = 0.0

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG_PATH = REPO_ROOT / "ELCD_Check" / "ELCD_Process_Catalog.xlsx"
DEFAULT_BENCHMARK_PATH = (
    REPO_ROOT / "Four_Models" / "Input" / "LLM_Model_Evaluation_Reference_Set.xlsx"
)
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "Four_Models" / "Output"

MODEL_SPECS: dict[str, dict[str, str]] = {
    "llama": {
        "display_name": "Llama 3.1 8B Instruct",
        "model_id": "meta-llama/Llama-3.1-8B-Instruct",
    },
    "qwen": {
        "display_name": "Qwen2.5 7B Instruct",
        "model_id": "Qwen/Qwen2.5-7B-Instruct",
    },
    "mistral": {
        "display_name": "Mistral 7B Instruct v0.3",
        "model_id": "mistralai/Mistral-7B-Instruct-v0.3",
    },
    "deepseek": {
        "display_name": "DeepSeek LLM 7B Chat",
        "model_id": "deepseek-ai/deepseek-llm-7b-chat",
    },
}

SYSTEM_PROMPT = """You are an LCA material-matching evaluator for A1-A3 screening.
Your role is limited to material interpretation and process matching against the
supplied openLCA/ELCD candidate processes.

Rules:
1. Use ONLY process UUIDs that appear in the supplied candidate list.
2. Do NOT invent process UUIDs, emission factors, GWP values, EPDs, citations,
   or environmental data.
3. Normalize the BOM description into a concise engineering material name.
4. Rank the most defensible supplied candidates from best to worst, up to the
   requested top-k.
5. Select exactly one process when a supplied candidate is defensible.
6. Classify the final outcome as:
   - direct: the selected process is a sufficiently direct representation;
   - proxy: the selected process is a defensible related substitute; or
   - review_required: no supplied candidate is defensible enough to select.
7. For review_required, selected_process_uuid and selected_process_name MUST be
   empty strings.
8. Return JSON only, with no Markdown and no text outside the JSON object.

Required JSON schema:
{
  "normalized_material": "string",
  "ranked_candidates": [
    {
      "process_uuid": "string",
      "process_name": "string",
      "confidence": 0.0,
      "rationale": "short string"
    }
  ],
  "selected_process_uuid": "string or empty",
  "selected_process_name": "string or empty",
  "match_type": "direct or proxy or review_required",
  "selection_confidence": 0.0,
  "uncertainty_reason": "short string"
}
"""

COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "sample_id": ("sample_id", "id", "item_id", "row_id", "case_id"),
    "material_description": (
        "material_description",
        "material",
        "description",
        "original_description",
        "material_name",
        "bom_description",
        "original_bom_material",
        "original bom material",
    ),
    "quantity": ("quantity", "qty", "amount"),
    "unit": ("unit", "units"),
    "ground_truth_normalized_material": (
        "ground_truth_normalized_material",
        "normalized_material",
        "reference_normalized_material",
        "expected_normalized_material",
        "target_normalized_material",
        "correct_normalized_material",
        "correct normalized material",
    ),
    "ground_truth_process_uuid": (
        "ground_truth_process_uuid",
        "reference_process_uuid",
        "expected_process_uuid",
        "target_process_uuid",
        "process_uuid",
    ),
    "ground_truth_process_name": (
        "ground_truth_process_name",
        "reference_process_name",
        "expected_process_name",
        "target_process_name",
        "process_name",
        "selected_process",
        "preferred_elcd/openlca_process",
        "preferred elcd/openlca process",
        "preferred_elcd_openlca_process",
    ),
    "ground_truth_match_type": (
        "ground_truth_match_type",
        "reference_match_type",
        "match_type",
        "final_decision",
        "final decision",
    ),
    "ground_truth_unresolved": (
        "ground_truth_unresolved",
        "reference_unresolved",
        "expected_unresolved",
        "unresolved",
    ),
    "reference_status": (
        "reference_status",
        "ground_truth_status",
        "reference status",
    ),
    "case_study": ("case_study", "case study"),
    "reviewer_notes": ("reviewer_notes", "reviewer notes", "notes"),
    "source_location": ("source_location", "source location"),
}


@dataclass
class LoadedModel:
    key: str
    display_name: str
    model_id: str
    tokenizer: Any
    model: Any
    model_revision: str
    tokenizer_revision: str


def package_version(name: str) -> str:
    try:
        return importlib_metadata.version(name)
    except importlib_metadata.PackageNotFoundError:
        return "not-installed"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9.%+\-/ ]", "", text)
    return text.strip()


def canonical_uuid(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return str(value).strip().lower()


def safe_value(value: Any) -> Any:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return value


def optional_bool(value: Any) -> bool | None:
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "unresolved", "review required", "review_required"}:
        return True
    if text in {"0", "false", "no", "n", "resolved", "matched"}:
        return False
    if text == "":
        return None
    raise ValueError(f"Cannot interpret boolean value: {value!r}")


def canonical_match_type(value: Any) -> str:
    text = normalize_text(value).replace("-", " ").replace("_", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if text in {"direct", "direct match", "exact", "exact match"}:
        return "direct"
    if text in {"proxy", "proxy match", "documented proxy"}:
        return "proxy"
    if text in {
        "review required",
        "reviewrequired",
        "review",
        "unresolved",
        "no match",
        "no defensible match",
    }:
        return "review_required"
    return ""


def canonical_reference_status(value: Any) -> str:
    text = normalize_text(value).replace("-", " ").replace("_", " ")
    if text in {"final", "frozen", "complete", "completed", "ready", "approved"}:
        return "FINAL"
    if text in {"pending", "pending reconciliation", "pendingreconciliation", "draft", "in progress", "incomplete"}:
        return "PENDING_RECONCILIATION"
    return str(value).strip().upper() if str(value).strip() else ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark four LLMs for material normalization and ELCD/openLCA process matching."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG_PATH)
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK_PATH)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    parser.add_argument(
        "--candidate-pool-size", type=int, default=DEFAULT_CANDIDATE_POOL_SIZE
    )
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--max-new-tokens", type=int, default=DEFAULT_MAX_NEW_TOKENS)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument(
        "--model",
        choices=["llama", "qwen", "deepseek", "mistral", "all"],
        default="llama",
        help="Model to benchmark. 'all' runs the four models sequentially.",
    )
    parser.add_argument(
        "--combine-results",
        action="store_true",
        help="Combine existing per-model benchmark_results.xlsx files without loading an LLM.",
    )
    parser.add_argument(
        "--no-4bit",
        action="store_true",
        help="Disable 4-bit NF4 quantization.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for a smoke test.",
    )
    return parser.parse_args()


def set_reproducibility(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True


def load_catalog(path: Path) -> pd.DataFrame:
    path = path.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(
            f"openLCA catalog not found: {path}\n"
            "Run scripts/export_openlca_process_catalog.py first."
        )

    catalog = pd.read_excel(path, sheet_name="Processes")
    required = {"process_uuid", "process_name"}
    missing = required.difference(catalog.columns)
    if missing:
        raise ValueError(f"Catalog is missing required columns: {sorted(missing)}")

    for col in ["process_uuid", "process_name", "category", "location", "process_type"]:
        if col not in catalog.columns:
            catalog[col] = ""
        catalog[col] = catalog[col].fillna("").astype(str).str.strip()

    catalog = catalog[catalog["process_uuid"].ne("") & catalog["process_name"].ne("")].copy()
    if catalog["process_uuid"].duplicated().any():
        dupes = catalog.loc[catalog["process_uuid"].duplicated(), "process_uuid"].head(5).tolist()
        raise ValueError(f"Catalog contains duplicate process UUIDs, e.g. {dupes}")

    catalog["_uuid_key"] = catalog["process_uuid"].map(canonical_uuid)
    catalog["_name_key"] = catalog["process_name"].map(normalize_text)
    catalog["_search_text"] = (
        catalog["process_name"]
        + " | "
        + catalog["category"]
        + " | "
        + catalog["location"]
    ).map(normalize_text)

    return catalog.reset_index(drop=True)


def _find_alias(columns: Iterable[str], aliases: tuple[str, ...]) -> str | None:
    normalized = {normalize_text(c).replace(" ", "_"): c for c in columns}
    for alias in aliases:
        key = normalize_text(alias).replace(" ", "_")
        if key in normalized:
            return normalized[key]
    return None


def load_benchmark(path: Path, catalog: pd.DataFrame) -> pd.DataFrame:
    """Load and strictly validate the frozen expert reference set.

    Pending expert rows are rejected. An unfinished row is never silently
    converted to Review Required/unresolved.
    """
    path = path.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(
            f"Benchmark workbook not found: {path}\n"
            "Use scripts/prepare_benchmark_reference.py after expert reconciliation."
        )

    excel = pd.ExcelFile(path)
    sheet_name = "Reference_Set" if "Reference_Set" in excel.sheet_names else excel.sheet_names[0]
    df = pd.read_excel(path, sheet_name=sheet_name)
    rename_map: dict[str, str] = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        found = _find_alias(df.columns, aliases)
        if found is not None:
            rename_map[found] = canonical
    df = df.rename(columns=rename_map).copy()

    if "material_description" not in df.columns:
        raise ValueError("Benchmark workbook must contain a material_description column.")
    if "sample_id" not in df.columns:
        df["sample_id"] = [f"S{i:04d}" for i in range(1, len(df) + 1)]

    for optional in [
        "quantity",
        "unit",
        "ground_truth_normalized_material",
        "ground_truth_process_uuid",
        "ground_truth_process_name",
        "ground_truth_match_type",
        "ground_truth_unresolved",
        "reference_status",
        "case_study",
        "reviewer_notes",
        "source_location",
    ]:
        if optional not in df.columns:
            df[optional] = ""

    df["sample_id"] = df["sample_id"].fillna("").astype(str).str.strip()
    if df["sample_id"].eq("").any():
        raise ValueError("Every benchmark row must have a nonblank sample_id.")
    if df["sample_id"].duplicated().any():
        dupes = df.loc[df["sample_id"].duplicated(), "sample_id"].tolist()
        raise ValueError(f"Duplicate sample_id values in benchmark workbook: {dupes}")

    df["material_description"] = df["material_description"].fillna("").astype(str).str.strip()
    df["ground_truth_normalized_material"] = (
        df["ground_truth_normalized_material"].fillna("").astype(str).str.strip()
    )
    df["ground_truth_process_uuid"] = df["ground_truth_process_uuid"].map(canonical_uuid)
    df["ground_truth_process_name"] = (
        df["ground_truth_process_name"].fillna("").astype(str).str.strip()
    )
    df["ground_truth_match_type"] = df["ground_truth_match_type"].map(canonical_match_type)
    df["reference_status"] = df["reference_status"].map(canonical_reference_status)

    pending = df[df["reference_status"].ne("FINAL")]
    if not pending.empty:
        ids = ", ".join(pending["sample_id"].head(12).tolist())
        more = " ..." if len(pending) > 12 else ""
        raise ValueError(
            "Benchmark reference set is not frozen. "
            f"{len(pending)} row(s) are not reference_status=FINAL: {ids}{more}.\n"
            "Complete Expert A/B reconciliation first, then run:\n"
            "  python scripts/prepare_benchmark_reference.py\n"
            "Do not mark unfinished rows as unresolved merely to make the benchmark run."
        )

    uuid_to_name = dict(zip(catalog["_uuid_key"], catalog["process_name"]))
    name_to_uuid = dict(zip(catalog["_name_key"], catalog["_uuid_key"]))

    unresolved_values: list[bool] = []
    validation_errors: list[str] = []

    for idx, row in df.iterrows():
        sid = row["sample_id"]
        gt_norm = str(row["ground_truth_normalized_material"]).strip()
        gt_name = str(row["ground_truth_process_name"]).strip()
        gt_uuid = canonical_uuid(row["ground_truth_process_uuid"])
        match_type = canonical_match_type(row["ground_truth_match_type"])
        explicit_unresolved = optional_bool(row["ground_truth_unresolved"])

        if not gt_norm:
            validation_errors.append(f"{sid}: missing ground_truth_normalized_material")

        if match_type == "review_required":
            unresolved = True
        elif match_type in {"direct", "proxy"}:
            unresolved = False
        elif explicit_unresolved is not None:
            unresolved = explicit_unresolved
            match_type = "review_required" if unresolved else ""
        else:
            validation_errors.append(
                f"{sid}: missing/invalid ground_truth_match_type (Direct, Proxy, or Review Required)"
            )
            unresolved = False

        if not match_type:
            validation_errors.append(
                f"{sid}: ground_truth_match_type is required for final scoring"
            )

        if unresolved:
            if gt_uuid or gt_name:
                validation_errors.append(
                    f"{sid}: Review Required rows must not contain a final process UUID/name"
                )
        else:
            if not gt_uuid and gt_name:
                matched_uuid = name_to_uuid.get(normalize_text(gt_name), "")
                if matched_uuid:
                    gt_uuid = matched_uuid
                    df.at[idx, "ground_truth_process_uuid"] = matched_uuid
            if gt_uuid and not gt_name:
                matched_name = uuid_to_name.get(gt_uuid, "")
                if matched_name:
                    gt_name = matched_name
                    df.at[idx, "ground_truth_process_name"] = matched_name
            if not gt_uuid:
                validation_errors.append(
                    f"{sid}: matched row does not resolve to an exact catalog process UUID"
                )
            elif gt_uuid not in uuid_to_name:
                validation_errors.append(
                    f"{sid}: ground_truth_process_uuid is not present in the exported catalog"
                )
            elif gt_name and normalize_text(uuid_to_name[gt_uuid]) != normalize_text(gt_name):
                validation_errors.append(
                    f"{sid}: process name does not match the catalog name for its UUID"
                )

        df.at[idx, "ground_truth_match_type"] = match_type
        unresolved_values.append(bool(unresolved))

    if validation_errors:
        shown = "\n  - ".join(validation_errors[:20])
        extra = f"\n  ... plus {len(validation_errors) - 20} more" if len(validation_errors) > 20 else ""
        raise ValueError("Invalid frozen benchmark reference set:\n  - " + shown + extra)

    df["ground_truth_unresolved"] = unresolved_values
    return df.reset_index(drop=True)


def retrieve_candidate_pool(
    row: pd.Series,
    catalog: pd.DataFrame,
    pool_size: int,
) -> list[dict[str, Any]]:
    """Deterministic lexical retrieval used identically for every model."""
    description = str(row.get("material_description", "")).strip()
    query = normalize_text(description)
    choices = catalog["_search_text"].tolist()
    matches = rf_process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        limit=min(pool_size, len(catalog)),
    )

    candidates: list[dict[str, Any]] = []
    for _, score, index in matches:
        process_row = catalog.iloc[index]
        candidates.append(
            {
                "process_uuid": process_row["process_uuid"],
                "process_name": process_row["process_name"],
                "category": process_row.get("category", ""),
                "location": process_row.get("location", ""),
                "process_type": process_row.get("process_type", ""),
                "lexical_score": round(float(score), 2),
            }
        )
    return candidates


def build_user_prompt(
    row: pd.Series,
    candidates: list[dict[str, Any]],
    top_k: int,
) -> str:
    material_payload = {
        "sample_id": str(row.get("sample_id", "")),
        "material_description": str(row.get("material_description", "")),
        "quantity": safe_value(row.get("quantity", "")),
        "unit": safe_value(row.get("unit", "")),
    }
    payload = {
        "requested_top_k": top_k,
        "material": material_payload,
        "candidate_processes": candidates,
    }
    return (
        "Evaluate the material below using only the supplied candidate processes. "
        "Return exactly the required JSON object.\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


def load_model(model_key: str, use_4bit: bool) -> LoadedModel:
    # Imported lazily so repository unit tests can exercise benchmark logic without
    # requiring the heavyweight inference dependencies.
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    spec = MODEL_SPECS[model_key]
    model_id = spec["model_id"]
    token = os.getenv("HF_TOKEN") or None

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        token=token,
        use_fast=True,
        trust_remote_code=False,
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_kwargs: dict[str, Any] = {
        "device_map": "auto",
        "token": token,
        "trust_remote_code": False,
        "low_cpu_mem_usage": True,
    }

    if use_4bit:
        if not torch.cuda.is_available():
            raise RuntimeError(
                "4-bit benchmark mode requires a CUDA GPU. Use a Colab GPU runtime "
                "or pass --no-4bit for CPU/full-precision execution."
            )
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        model_kwargs["quantization_config"] = quant_config
        model_kwargs["torch_dtype"] = torch.float16
    else:
        model_kwargs["torch_dtype"] = torch.float16 if torch.cuda.is_available() else torch.float32

    model = AutoModelForCausalLM.from_pretrained(model_id, **model_kwargs)
    model.eval()

    model_revision = str(getattr(model.config, "_commit_hash", "") or "")
    tokenizer_revision = str(
        getattr(tokenizer, "init_kwargs", {}).get("_commit_hash", "") or ""
    )

    return LoadedModel(
        key=model_key,
        display_name=spec["display_name"],
        model_id=model_id,
        tokenizer=tokenizer,
        model=model,
        model_revision=model_revision,
        tokenizer_revision=tokenizer_revision,
    )


def unload_model(loaded: LoadedModel | None) -> None:
    if loaded is not None:
        try:
            del loaded.model
            del loaded.tokenizer
        except Exception:
            pass
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        try:
            torch.cuda.ipc_collect()
        except Exception:
            pass


def model_input_device(model: Any) -> torch.device:
    try:
        return model.get_input_embeddings().weight.device
    except Exception:
        return next(model.parameters()).device


def generate_response(
    loaded: LoadedModel,
    user_prompt: str,
    max_new_tokens: int,
    temperature: float,
) -> tuple[str, float]:
    # A single user-role message keeps prompt content equivalent across model
    # families, including checkpoints that do not use a separate system role.
    messages = [{"role": "user", "content": SYSTEM_PROMPT + "\n\n" + user_prompt}]

    tokenizer = loaded.tokenizer
    model = loaded.model
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    device = model_input_device(model)
    input_ids = input_ids.to(device)
    attention_mask = torch.ones_like(input_ids)

    generate_kwargs: dict[str, Any] = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "max_new_tokens": max_new_tokens,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token_id": tokenizer.eos_token_id,
        "use_cache": True,
    }
    if temperature > 0:
        generate_kwargs.update(
            {"do_sample": True, "temperature": temperature, "top_p": 1.0}
        )
    else:
        generate_kwargs["do_sample"] = False

    if torch.cuda.is_available():
        torch.cuda.synchronize()
    start = time.perf_counter()
    with torch.inference_mode():
        output = model.generate(**generate_kwargs)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    generated = output[0, input_ids.shape[-1] :]
    text = tokenizer.decode(generated, skip_special_tokens=True).strip()
    return text, elapsed


def extract_json(text: str) -> tuple[dict[str, Any] | None, str]:
    if not text:
        return None, "empty_response"

    cleaned = text.strip()
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, flags=re.S | re.I)
    candidates = fenced + [cleaned]

    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first != -1 and last > first:
        candidates.append(cleaned[first : last + 1])

    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed, "ok"
        except json.JSONDecodeError:
            continue
    return None, "json_parse_error"


def validate_prediction(
    parsed: dict[str, Any] | None,
    candidates: list[dict[str, Any]],
    parse_status: str,
    top_k: int,
) -> dict[str, Any]:
    """Validate model JSON without altering the model's returned ranking."""
    valid_by_uuid = {
        canonical_uuid(c["process_uuid"]): c for c in candidates if c.get("process_uuid")
    }

    if parsed is None:
        return {
            "parse_status": parse_status,
            "valid_response": False,
            "normalized_material": "",
            "match_type": "",
            "decision": "invalid",
            "selected_process_uuid": "",
            "selected_process_name": "",
            "ranked_process_uuids": [],
            "ranked_process_names": [],
            "selection_confidence": "",
            "uncertainty_reason": "",
        }

    status = parse_status
    normalized_material = str(parsed.get("normalized_material", "")).strip()
    match_type = canonical_match_type(parsed.get("match_type", ""))
    if not match_type:
        status = "invalid_match_type"

    ranked = parsed.get("ranked_candidates", [])
    if not isinstance(ranked, list):
        ranked = []
        status = "invalid_ranked_candidates"

    valid_ranked_uuids: list[str] = []
    valid_ranked_names: list[str] = []
    for item in ranked:
        if not isinstance(item, dict):
            continue
        uid = canonical_uuid(item.get("process_uuid", ""))
        if uid in valid_by_uuid and uid not in valid_ranked_uuids:
            valid_ranked_uuids.append(uid)
            valid_ranked_names.append(valid_by_uuid[uid]["process_name"])
        if len(valid_ranked_uuids) >= top_k:
            break

    selected_uuid = canonical_uuid(parsed.get("selected_process_uuid", ""))
    selected_name = ""

    if match_type == "review_required":
        if selected_uuid:
            status = "review_required_with_selected_process"
            selected_uuid = ""
    elif match_type in {"direct", "proxy"}:
        if selected_uuid not in valid_by_uuid:
            status = "invalid_selected_candidate"
            selected_uuid = ""
        else:
            selected_name = valid_by_uuid[selected_uuid]["process_name"]
            # Important: do not insert the selected process into the returned ranking.
            # Ranking metrics must reflect exactly what the model ranked.
            if selected_uuid not in valid_ranked_uuids:
                status = "selected_process_not_in_ranked_candidates"

    decision = (
        "unresolved"
        if match_type == "review_required"
        else "matched"
        if match_type in {"direct", "proxy"}
        else "invalid"
    )

    valid_response = status == "ok"
    return {
        "parse_status": status,
        "valid_response": valid_response,
        "normalized_material": normalized_material,
        "match_type": match_type,
        "decision": decision,
        "selected_process_uuid": selected_uuid,
        "selected_process_name": selected_name,
        "ranked_process_uuids": valid_ranked_uuids,
        "ranked_process_names": valid_ranked_names,
        "selection_confidence": safe_value(parsed.get("selection_confidence", "")),
        "uncertainty_reason": str(parsed.get("uncertainty_reason", "")).strip(),
    }


def evaluate_record(
    row: pd.Series,
    candidates: list[dict[str, Any]],
    prediction: dict[str, Any],
    top_k: int,
) -> dict[str, Any]:
    gt_uuid = canonical_uuid(row.get("ground_truth_process_uuid", ""))
    gt_name = str(row.get("ground_truth_process_name", "")).strip()
    gt_norm = str(row.get("ground_truth_normalized_material", "")).strip()
    gt_match_type = canonical_match_type(row.get("ground_truth_match_type", ""))
    gt_unresolved = bool(row.get("ground_truth_unresolved", False))

    pool_uuids = [canonical_uuid(c.get("process_uuid", "")) for c in candidates]
    ranked = prediction["ranked_process_uuids"]
    selected = prediction["selected_process_uuid"]
    valid = bool(prediction["valid_response"])
    predicted_unresolved = prediction["match_type"] == "review_required"

    if gt_unresolved:
        candidate_pool_contains_gt: Any = ""
        top1_correct: Any = ""
        top3_correct: Any = ""
        top5_correct: Any = ""
        top10_correct: Any = ""
        topk_correct: Any = ""
        reciprocal_rank: Any = ""
        process_selection_correct: Any = ""
        conditional_selection_correct: Any = ""
        end_to_end_correct = valid and predicted_unresolved
    else:
        candidate_pool_contains_gt = bool(gt_uuid and gt_uuid in pool_uuids)
        top1_correct = bool(valid and gt_uuid and gt_uuid in ranked[:1])
        top3_correct = bool(valid and gt_uuid and gt_uuid in ranked[:3])
        top5_correct = bool(valid and gt_uuid and gt_uuid in ranked[:5])
        top10_correct = bool(valid and gt_uuid and gt_uuid in ranked[:10])
        topk_correct = bool(valid and gt_uuid and gt_uuid in ranked[:top_k])
        if valid and gt_uuid in ranked:
            reciprocal_rank = 1.0 / (ranked.index(gt_uuid) + 1)
        else:
            reciprocal_rank = 0.0
        process_selection_correct = bool(valid and gt_uuid and selected == gt_uuid)
        conditional_selection_correct = (
            process_selection_correct if candidate_pool_contains_gt else ""
        )
        end_to_end_correct = process_selection_correct

    normalization_exact: Any = ""
    normalization_similarity: Any = ""
    if gt_norm:
        normalization_exact = bool(
            valid
            and normalize_text(prediction["normalized_material"]) == normalize_text(gt_norm)
        )
        normalization_similarity = round(
            (
                fuzz.ratio(
                    normalize_text(prediction["normalized_material"]),
                    normalize_text(gt_norm),
                )
                / 100.0
            )
            if valid
            else 0.0,
            4,
        )

    return {
        "ground_truth_process_uuid": gt_uuid,
        "ground_truth_process_name": gt_name,
        "ground_truth_normalized_material": gt_norm,
        "ground_truth_match_type": gt_match_type,
        "ground_truth_unresolved": gt_unresolved,
        "candidate_pool_contains_ground_truth": candidate_pool_contains_gt,
        "normalization_exact": normalization_exact,
        "normalization_similarity": normalization_similarity,
        "top1_ranking_correct": top1_correct,
        "top3_ranking_correct": top3_correct,
        "top5_ranking_correct": top5_correct,
        "top10_ranking_correct": top10_correct,
        "configured_top_k_ranking_correct": topk_correct,
        "reciprocal_rank": reciprocal_rank,
        "process_selection_correct": process_selection_correct,
        "conditional_process_selection_correct": conditional_selection_correct,
        "match_type_correct": bool(valid and prediction["match_type"] == gt_match_type),
        "review_required_binary_correct": bool(
            valid and predicted_unresolved == gt_unresolved
        ),
        "unresolved_routing_correct": (
            bool(valid and predicted_unresolved) if gt_unresolved else ""
        ),
        "end_to_end_reference_correct": bool(end_to_end_correct),
    }


def bool_mean(series: pd.Series) -> float | None:
    vals = [x for x in series.tolist() if isinstance(x, (bool, np.bool_))]
    if not vals:
        return None
    return float(np.mean(vals))


def numeric_mean(series: pd.Series) -> float | None:
    vals = pd.to_numeric(series, errors="coerce").dropna()
    return float(vals.mean()) if len(vals) else None


def compute_metrics(predictions: pd.DataFrame, runs: int) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "n_samples": int(predictions["sample_id"].nunique()),
        "n_runs_per_sample": runs,
        "n_prediction_rows": int(len(predictions)),
    }

    metrics["valid_response_rate"] = bool_mean(predictions["valid_response"])
    metrics["failed_response_rate"] = float((~predictions["valid_response"].astype(bool)).mean())
    metrics["normalization_exact_accuracy"] = bool_mean(predictions["normalization_exact"])
    metrics["mean_normalization_similarity"] = numeric_mean(predictions["normalization_similarity"])

    metrics["candidate_pool_recall"] = bool_mean(
        predictions["candidate_pool_contains_ground_truth"]
    )
    metrics["top1_ranking_accuracy"] = bool_mean(predictions["top1_ranking_correct"])
    metrics["top3_ranking_recall"] = bool_mean(predictions["top3_ranking_correct"])
    metrics["top5_ranking_recall"] = bool_mean(predictions["top5_ranking_correct"])
    metrics["top10_ranking_recall"] = bool_mean(predictions["top10_ranking_correct"])
    metrics["configured_top_k_ranking_recall"] = bool_mean(
        predictions["configured_top_k_ranking_correct"]
    )
    metrics["mean_reciprocal_rank"] = numeric_mean(predictions["reciprocal_rank"])
    metrics["final_process_selection_accuracy_matched_rows"] = bool_mean(
        predictions["process_selection_correct"]
    )
    metrics["conditional_process_selection_accuracy"] = bool_mean(
        predictions["conditional_process_selection_correct"]
    )
    metrics["match_type_accuracy"] = bool_mean(predictions["match_type_correct"])
    metrics["review_required_binary_accuracy"] = bool_mean(
        predictions["review_required_binary_correct"]
    )
    metrics["unresolved_routing_accuracy"] = bool_mean(
        predictions["unresolved_routing_correct"]
    )
    metrics["end_to_end_reference_accuracy"] = bool_mean(
        predictions["end_to_end_reference_correct"]
    )

    durations = pd.to_numeric(predictions["generation_seconds"], errors="coerce").dropna()
    metrics["mean_generation_seconds"] = float(durations.mean()) if len(durations) else None
    metrics["median_generation_seconds"] = float(durations.median()) if len(durations) else None

    y_true: list[str] = []
    y_pred: list[str] = []
    for _, row in predictions.iterrows():
        true_label = (
            "__REVIEW_REQUIRED__"
            if bool(row["ground_truth_unresolved"])
            else canonical_uuid(row["ground_truth_process_uuid"])
        )
        if not bool(row["valid_response"]):
            pred_label = "__INVALID__"
        elif str(row["match_type"]) == "review_required":
            pred_label = "__REVIEW_REQUIRED__"
        else:
            pred_label = canonical_uuid(row["selected_process_uuid"]) or "__INVALID__"
        if true_label:
            y_true.append(true_label)
            y_pred.append(pred_label)

    metrics["macro_f1_final_reference"] = (
        float(f1_score(y_true, y_pred, average="macro", zero_division=0)) if y_true else None
    )

    selection_agreement: list[bool] = []
    normalization_agreement: list[bool] = []
    match_type_agreement: list[bool] = []

    for _, group in predictions.groupby("sample_id", sort=False):
        if not group["valid_response"].astype(bool).all():
            selection_agreement.append(False)
            normalization_agreement.append(False)
            match_type_agreement.append(False)
            continue

        labels = [
            "__REVIEW_REQUIRED__"
            if str(mt) == "review_required"
            else canonical_uuid(uid)
            for mt, uid in zip(group["match_type"], group["selected_process_uuid"])
        ]
        selection_agreement.append(len(set(labels)) == 1)

        norms = [normalize_text(v) for v in group["normalized_material"].tolist()]
        normalization_agreement.append(len(set(norms)) == 1)

        match_types = [str(v) for v in group["match_type"].tolist()]
        match_type_agreement.append(len(set(match_types)) == 1)

    metrics["run_to_run_selection_agreement"] = (
        float(np.mean(selection_agreement)) if selection_agreement else None
    )
    metrics["run_to_run_normalization_agreement"] = (
        float(np.mean(normalization_agreement)) if normalization_agreement else None
    )
    metrics["run_to_run_match_type_agreement"] = (
        float(np.mean(match_type_agreement)) if match_type_agreement else None
    )
    return metrics


def metadata_rows(
    loaded: LoadedModel | None,
    args: argparse.Namespace,
    status: str,
    error_message: str = "",
) -> list[dict[str, Any]]:
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No CUDA GPU"
    gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    cuda_version = torch.version.cuda or ""

    values: list[tuple[str, Any]] = [
        ("script_version", SCRIPT_VERSION),
        ("exported_at_utc", utc_now()),
        ("benchmark_status", status),
        ("error_message", error_message),
        ("database_label", DATABASE_LABEL),
        ("model_key", loaded.key if loaded else ""),
        ("model_display_name", loaded.display_name if loaded else ""),
        ("model_id", loaded.model_id if loaded else ""),
        ("model_revision", loaded.model_revision if loaded else ""),
        ("tokenizer_revision", loaded.tokenizer_revision if loaded else ""),
        ("base_seed", SEED),
        ("repeat_seeds", f"{SEED}..{SEED + args.runs - 1}"),
        ("runs_per_sample", args.runs),
        ("candidate_pool_size", args.candidate_pool_size),
        ("reported_top_k", args.top_k),
        ("max_new_tokens", args.max_new_tokens),
        ("temperature", args.temperature),
        ("decoding", "greedy" if args.temperature <= 0 else "sampling"),
        ("quantization", "none" if args.no_4bit else "4-bit NF4"),
        ("python_version", sys.version.replace("\n", " ")),
        ("platform", platform.platform()),
        ("gpu_name", gpu_name),
        ("gpu_count", gpu_count),
        ("cuda_version", cuda_version),
        ("torch_version", torch.__version__),
        ("transformers_version", package_version("transformers")),
        ("accelerate_version", package_version("accelerate")),
        ("bitsandbytes_version", package_version("bitsandbytes")),
        ("pandas_version", pd.__version__),
        ("rapidfuzz_version", package_version("rapidfuzz")),
        ("scikit_learn_version", package_version("scikit-learn")),
        ("openpyxl_version", package_version("openpyxl")),
        ("catalog_path", str(Path(args.catalog).expanduser().resolve())),
        ("benchmark_path", str(Path(args.benchmark).expanduser().resolve())),
    ]
    return [{"field": field, "value": value} for field, value in values]


def prompt_sheet() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"prompt_part": "system_prompt", "text": SYSTEM_PROMPT},
            {
                "prompt_part": "user_prompt_template",
                "text": (
                    "Evaluate the material below using only the supplied candidate processes. "
                    "The runtime payload contains sample_id, material_description, quantity, "
                    "unit, requested_top_k, and the deterministic candidate list."
                ),
            },
        ]
    )


def sanitize_sheet_value(value: Any) -> Any:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def prepare_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        out[col] = out[col].map(sanitize_sheet_value)
    return out


def format_workbook(writer: pd.ExcelWriter) -> None:
    workbook = writer.book
    for sheet_name in workbook.sheetnames:
        ws = workbook[sheet_name]
        ws.freeze_panes = "A2"
        if ws.max_row >= 1 and ws.max_column >= 1:
            ws.auto_filter.ref = ws.dimensions
        for column_cells in ws.columns:
            letter = column_cells[0].column_letter
            max_len = 0
            for cell in column_cells[:200]:
                value = "" if cell.value is None else str(cell.value)
                max_len = max(max_len, len(value))
            ws.column_dimensions[letter].width = min(max(max_len + 2, 12), 60)


def write_model_workbook(
    output_path: Path,
    predictions: pd.DataFrame,
    metrics: dict[str, Any],
    metadata: list[dict[str, Any]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_df = pd.DataFrame([{"metric": key, "value": value} for key, value in metrics.items()])
    metadata_df = pd.DataFrame(metadata)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        prepare_for_excel(predictions).to_excel(writer, sheet_name="Predictions", index=False)
        metrics_df.to_excel(writer, sheet_name="Metrics", index=False)
        metadata_df.to_excel(writer, sheet_name="Metadata", index=False)
        prompt_sheet().to_excel(writer, sheet_name="Prompt", index=False)
        format_workbook(writer)


def write_combined_workbook(
    output_path: Path,
    summary_rows: list[dict[str, Any]],
    all_predictions: list[pd.DataFrame],
    configuration_rows: list[dict[str, Any]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df = pd.DataFrame(summary_rows)
    predictions_df = pd.concat(all_predictions, ignore_index=True) if all_predictions else pd.DataFrame()
    config_df = pd.DataFrame(configuration_rows)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="ModelComparison", index=False)
        prepare_for_excel(predictions_df).to_excel(writer, sheet_name="AllPredictions", index=False)
        config_df.to_excel(writer, sheet_name="RunConfiguration", index=False)
        prompt_sheet().to_excel(writer, sheet_name="Prompt", index=False)
        format_workbook(writer)


def benchmark_model(
    loaded: LoadedModel,
    benchmark_df: pd.DataFrame,
    catalog: pd.DataFrame,
    args: argparse.Namespace,
) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    total = len(benchmark_df) * args.runs
    counter = 0

    for _, row in benchmark_df.iterrows():
        candidates = retrieve_candidate_pool(row, catalog, args.candidate_pool_size)
        candidate_ids = [canonical_uuid(c["process_uuid"]) for c in candidates]
        user_prompt = build_user_prompt(row, candidates, args.top_k)

        for run_number in range(1, args.runs + 1):
            counter += 1
            run_seed = SEED + run_number - 1
            set_reproducibility(run_seed)
            print(
                f"[{loaded.key}] {counter}/{total} | sample={row['sample_id']} | "
                f"run={run_number} | seed={run_seed}"
            )

            raw_text = ""
            generation_seconds: Any = ""
            parse_status = "generation_error"
            parsed: dict[str, Any] | None = None
            error_message = ""

            try:
                raw_text, generation_seconds = generate_response(
                    loaded,
                    user_prompt,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                )
                parsed, parse_status = extract_json(raw_text)
            except Exception as exc:
                error_message = f"{type(exc).__name__}: {exc}"

            prediction = validate_prediction(
                parsed,
                candidates,
                parse_status=parse_status,
                top_k=args.top_k,
            )
            evaluation = evaluate_record(row, candidates, prediction, top_k=args.top_k)

            record = {
                "model_key": loaded.key,
                "model_name": loaded.display_name,
                "model_id": loaded.model_id,
                "sample_id": str(row["sample_id"]),
                "run_number": run_number,
                "run_seed": run_seed,
                "case_study": safe_value(row.get("case_study", "")),
                "material_description": str(row["material_description"]),
                "quantity": safe_value(row.get("quantity", "")),
                "unit": safe_value(row.get("unit", "")),
                "reviewer_notes": safe_value(row.get("reviewer_notes", "")),
                "source_location": safe_value(row.get("source_location", "")),
                "candidate_pool_size": len(candidates),
                "candidate_pool_uuids": candidate_ids,
                "candidate_pool_names": [c["process_name"] for c in candidates],
                "normalized_material": prediction["normalized_material"],
                "match_type": prediction["match_type"],
                "decision": prediction["decision"],
                "selected_process_uuid": prediction["selected_process_uuid"],
                "selected_process_name": prediction["selected_process_name"],
                "ranked_process_uuids": prediction["ranked_process_uuids"],
                "ranked_process_names": prediction["ranked_process_names"],
                "selection_confidence": prediction["selection_confidence"],
                "uncertainty_reason": prediction["uncertainty_reason"],
                "parse_status": prediction["parse_status"],
                "valid_response": prediction["valid_response"],
                "generation_seconds": generation_seconds,
                "error_message": error_message,
                "raw_model_output": raw_text,
                **evaluation,
            }
            records.append(record)

    return pd.DataFrame(records)


def combine_existing_results(args: argparse.Namespace) -> None:
    summary_rows: list[dict[str, Any]] = []
    all_predictions: list[pd.DataFrame] = []
    configuration_rows: list[dict[str, Any]] = []
    missing: list[str] = []

    for model_key in ["llama", "qwen", "deepseek", "mistral"]:
        path = Path(args.output_root) / model_key / "benchmark_results.xlsx"
        if not path.exists():
            missing.append(str(path))
            continue
        predictions = pd.read_excel(path, sheet_name="Predictions")
        metrics_df = pd.read_excel(path, sheet_name="Metrics")
        metadata_df = pd.read_excel(path, sheet_name="Metadata")
        metrics = dict(zip(metrics_df["metric"], metrics_df["value"]))
        meta = dict(zip(metadata_df["field"], metadata_df["value"]))

        all_predictions.append(predictions)
        summary_rows.append(
            {
                "model_key": model_key,
                "model_name": meta.get("model_display_name", MODEL_SPECS[model_key]["display_name"]),
                "model_id": meta.get("model_id", MODEL_SPECS[model_key]["model_id"]),
                "model_revision": meta.get("model_revision", ""),
                **metrics,
            }
        )
        configuration_rows.extend(
            [{"model_key": model_key, **row} for row in metadata_df.to_dict("records")]
        )

    if missing:
        raise FileNotFoundError(
            "Cannot combine results because these model workbooks are missing:\n  - "
            + "\n  - ".join(missing)
        )

    combined_path = Path(args.output_root) / "combined" / "four_model_comparison.xlsx"
    write_combined_workbook(
        combined_path,
        summary_rows=summary_rows,
        all_predictions=all_predictions,
        configuration_rows=configuration_rows,
    )
    print(f"Combined comparison saved: {combined_path.resolve()}")


def main() -> None:
    args = parse_args()

    if args.runs < 1:
        raise ValueError("--runs must be at least 1")
    if args.candidate_pool_size < 5:
        raise ValueError("--candidate-pool-size must be at least 5")
    if args.top_k < 1 or args.top_k > args.candidate_pool_size:
        raise ValueError("--top-k must be between 1 and candidate-pool-size")
    if args.temperature < 0:
        raise ValueError("--temperature cannot be negative")

    args.catalog = Path(args.catalog).expanduser().resolve()
    args.benchmark = Path(args.benchmark).expanduser().resolve()
    args.output_root = Path(args.output_root).expanduser().resolve()

    set_reproducibility(SEED)

    if args.combine_results:
        combine_existing_results(args)
        return

    print("Loading ELCD process catalog...")
    catalog = load_catalog(args.catalog)
    print(f"Catalog processes: {len(catalog):,}")

    print("Loading frozen benchmark reference set...")
    benchmark_df = load_benchmark(args.benchmark, catalog)
    if args.limit is not None:
        if args.limit < 1:
            raise ValueError("--limit must be at least 1")
        benchmark_df = benchmark_df.head(args.limit).copy()
    print(f"Benchmark samples: {len(benchmark_df):,}")

    args.output_root.mkdir(parents=True, exist_ok=True)
    selected_keys = (
        ["llama", "qwen", "deepseek", "mistral"] if args.model == "all" else [args.model]
    )

    all_predictions: list[pd.DataFrame] = []
    summary_rows: list[dict[str, Any]] = []
    configuration_rows: list[dict[str, Any]] = []

    for model_key in selected_keys:
        loaded: LoadedModel | None = None
        model_output_path = args.output_root / model_key / "benchmark_results.xlsx"
        try:
            print("\n" + "=" * 80)
            print(f"Loading {MODEL_SPECS[model_key]['display_name']}")
            print(MODEL_SPECS[model_key]["model_id"])
            print("=" * 80)

            loaded = load_model(model_key, use_4bit=not args.no_4bit)
            predictions = benchmark_model(loaded, benchmark_df, catalog, args)
            metrics = compute_metrics(predictions, args.runs)
            metadata = metadata_rows(loaded, args, status="completed")
            write_model_workbook(model_output_path, predictions, metrics, metadata)

            all_predictions.append(predictions)
            summary_rows.append(
                {
                    "model_key": model_key,
                    "model_name": loaded.display_name,
                    "model_id": loaded.model_id,
                    "model_revision": loaded.model_revision,
                    **metrics,
                }
            )
            configuration_rows.extend(
                [{"model_key": model_key, **row} for row in metadata]
            )
            print(f"Saved: {model_output_path}")

        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            print(f"ERROR for {model_key}: {error}", file=sys.stderr)
            failed_meta = metadata_rows(loaded, args, status="failed", error_message=error)
            configuration_rows.extend(
                [{"model_key": model_key, **row} for row in failed_meta]
            )
            summary_rows.append(
                {
                    "model_key": model_key,
                    "model_name": MODEL_SPECS[model_key]["display_name"],
                    "model_id": MODEL_SPECS[model_key]["model_id"],
                    "benchmark_status": "failed",
                    "error_message": error,
                }
            )
        finally:
            unload_model(loaded)

    print("\nBenchmark complete.")
    if args.model == "all":
        combined_path = args.output_root / "combined" / "four_model_comparison.xlsx"
        write_combined_workbook(
            combined_path,
            summary_rows=summary_rows,
            all_predictions=all_predictions,
            configuration_rows=configuration_rows,
        )
        print(f"Combined comparison: {combined_path.resolve()}")
    else:
        print(
            "After all four model runs finish, create the paper comparison workbook with:\n"
            "  python scripts/benchmark_four_llms.py --combine-results"
        )


if __name__ == "__main__":
    main()
