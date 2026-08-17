from pathlib import Path
import sys
import unittest

BENCHMARK_DIR = Path(__file__).resolve().parents[1] / "experiments" / "model_benchmark"
sys.path.insert(0, str(BENCHMARK_DIR))

from benchmark_models import validate_output
from retrieval import CatalogProcess, retrieve_candidates
from utils import extract_json_object


class ModelBenchmarkTests(unittest.TestCase):
    def test_extract_json_object_with_wrapper_text(self):
        parsed = extract_json_object(
            'prefix {"normalized_material":"cement","selected_candidate":0,"decision":"Direct"} suffix'
        )
        self.assertEqual(parsed["selected_candidate"], 0)

    def test_review_required_minus_one_is_preserved(self):
        candidates = [CatalogProcess(uuid="u1", name="Portland cement production")]
        result = validate_output(
            {
                "normalized_material": "bamboo",
                "selected_candidate": -1,
                "decision": "Review Required",
                "reason": "No defensible candidate",
            },
            candidates,
        )
        self.assertEqual(result["selected_candidate"], -1)
        self.assertEqual(result["selected_process_uuid"], "")

    def test_invalid_minus_one_direct_is_rejected(self):
        candidates = [CatalogProcess(uuid="u1", name="Portland cement production")]
        with self.assertRaises(ValueError):
            validate_output(
                {
                    "normalized_material": "cement",
                    "selected_candidate": -1,
                    "decision": "Direct",
                },
                candidates,
            )

    def test_retrieval_is_deterministic(self):
        catalog = [
            CatalogProcess(uuid="b", name="Steel reinforcing bar production"),
            CatalogProcess(uuid="a", name="Portland cement production"),
            CatalogProcess(uuid="c", name="Steel sheet production"),
        ]
        first = retrieve_candidates("10mm Rebar", catalog, limit=2)
        second = retrieve_candidates("10mm Rebar", catalog, limit=2)
        self.assertEqual([p.uuid for p in first], [p.uuid for p in second])
        self.assertEqual(first[0].uuid, "b")


if __name__ == "__main__":
    unittest.main()
