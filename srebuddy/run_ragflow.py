from modules import logging_checker
import importlib
from pathlib import Path

SRE_CHECKERS = [
    ("logging_checker", "check_logging_implementation"),
    ("monitoring_checker", "check_monitoring_implementation"),
    ("alerting_checker", "check_alerting_implementation"),
    ("dynatrace_checker", "check_dynatrace_implementation"),
]

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / "../data/sample_repo/sample_service.py"
    code_lines = []
    with open(file_path.resolve(), encoding="utf-8") as f:
        for line in f:
            code_lines.append(line)
    code = ''.join(code_lines)

    results = {}
    for module_name, func_name in SRE_CHECKERS:
        try:
            module = importlib.import_module(f"modules.{module_name}")
            check_func = getattr(module, func_name)
            result = check_func(code)
            results[module_name] = result
        except Exception as e:
            results[module_name] = f"Error: {e}"

    print("\nSRE Check Results:")
    for check, res in results.items():
        print(f"\n{check.replace('_checker', '').capitalize()} Check Result:\n", res)
