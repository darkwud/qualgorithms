from psiqworkbench.resource_estimation.qre import resource_estimator
from src.counting import quantum_counting

def run_scaling_analysis():
    weights = [1, 2, 4, 5, 6]
    target = 7
    precision = 5

    print(f"--- Scaling Analysis: {len(weights)} items, {precision} bits precision ---")

    try:
        # Execute the circuit and get QPU
        qpu_hardware = quantum_counting(weights, target, precision_qubits=precision, return_qpu=True)

        # Pass it to the estimator
        estimator = resource_estimator(qpu_hardware)

        # Execute the resources
        report = estimator.resources() if callable(estimator.resources) else estimator.resources

        print("\n[HARDWARE RESOURCE REPORT]")
        print("-" * 40)

        if hasattr(report, 'items'):
            for key, val in report.items():
                display_val = val.value if hasattr(val, 'value') else val
                print(f"{key:25}: {display_val}")
        else:
            print(report)

        print("-" * 40)

    except Exception as e:
        print(f"\n[!] Critical Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    run_scaling_analysis()