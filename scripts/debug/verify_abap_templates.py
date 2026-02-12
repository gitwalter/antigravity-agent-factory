import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from scripts.core.template_engine import create_engine

def verify():
    # Detect factory root
    factory_root = Path(__file__).parent.parent.parent
    print(f"Factory root: {factory_root}")
    
    try:
        engine = create_engine(factory_root)
        
        # Context for interface.abap
        abap_context = {
            'INTERFACE_NAME': 'ZIF_TEST_INTERFACE',
            'INTERFACE_DESCRIPTION': 'Test Interface',
            'AUTHOR': 'Developer',
            'DATE': '2026-02-12',
            'PURPOSE': 'Demonstrate ABAP macros',
            'methods': [
                {
                    'name': 'CALCULATE_TOTAL',
                    'description': 'Calculates the sum of two numbers',
                    'importing': [
                        {'name': 'IV_A', 'type': 'I', 'description': 'First number'},
                        {'name': 'IV_B', 'type': 'I', 'description': 'Second number'}
                    ],
                    'returning': {'type': 'I', 'description': 'Sum'},
                    'raising': [{'name': 'CX_SY_ARITHMETIC_OVERFLOW', 'description': 'Overflow occurred'}]
                },
                {
                    'name': 'UPDATE_STATUS',
                    'description': 'Updates object status',
                    'importing': [{'name': 'IV_STATUS', 'type': 'STRING', 'description': 'New status'}],
                    'exporting': [{'name': 'EV_SUCCESS', 'type': 'ABAP_BOOL', 'description': 'Success flag'}]
                }
            ],
            'constants': [
                {'name': 'GC_STATUS_ACTIVE', 'type': 'STRING', 'value': "'ACTIVE'"},
                {'name': 'GC_MAX_RETRIES', 'type': 'I', 'value': '3'}
            ],
            'types': [
                {'name': 'TY_STATUS', 'definition': 'CHAR10'}
            ]
        }

        print("Rendering abap/clean-abap/interface.abap.tmpl...")
        output = engine.render('abap/clean-abap/interface.abap.tmpl', abap_context)
        print("Success! Output length:", len(output))
        print("--- RENDERED ABAP START ---")
        print(output)
        print("--- RENDERED ABAP END ---")
        
        # Basic validation
        assert "INTERFACE ZIF_TEST_INTERFACE PUBLIC." in output
        assert "METHODS CALCULATE_TOTAL" in output
        assert "IMPORTING" in output
        assert "IV_A TYPE I" in output
        assert "RETURNING" in output
        assert "VALUE(result) TYPE I" in output
        assert "CONSTANTS:" in output
        assert "GC_MAX_RETRIES TYPE I VALUE 3." in output
        
        print("\nVERIFICATION SUCCESSFUL")
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    verify()
