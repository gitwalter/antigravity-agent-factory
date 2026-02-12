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
        
        # Context for main.py
        main_context = {
            'AUTHOR': 'Test Author',
            'DATE': '2026-01-01',
            'ERROR_HANDLER_CLASS_NAME': 'GlobalErrorHandler',
            'MODULE_NAME': 'test_app',
            'APP_DESCRIPTION': 'A test application',
            'APP_NAME': 'Test App', # Settings context
        }
        
        # Context for settings.py
        settings_context = {
            'AUTHOR': 'Test Author',
            'DATE': '2026-01-01',
            'APP_NAME': 'Test App'
        }

        print("Rendering main.py.tmpl...")
        main_output = engine.render('python/fastapi/main.py.tmpl', main_context)
        print("Success! Output length:", len(main_output))
        
        print("\nRendering settings.py.tmpl...")
        settings_output = engine.render('python/fastapi/config/settings.py.tmpl', settings_context)
        print("Success! Output length:", len(settings_output))
        
        print("\nVERIFICATION SUCCESSFUL")
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    verify()
