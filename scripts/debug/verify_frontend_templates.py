import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from scripts.core.template_engine import create_engine


def verify():
    # Detect factory root
    factory_root = Path(__file__).parent.parent.parent
    print(f"Factory root: {factory_root}")

    try:
        engine = create_engine(factory_root)

        # Context for app.py
        streamlit_context = {
            "APP_NAME": "My Streamlit App",
            "APP_ICON": "🚀",
            "LAYOUT": "wide",
            "SIDEBAR_STATE": "expanded",
            "APP_PURPOSE": "Demonstrate template macros",
            "AUTHOR": "Test Author",
            "DATE": "2026-02-12",
            "PAGE_NAME": "about",
        }

        # Context for page.tsx
        nextjs_context = {
            "PAGE_PURPOSE": "Landing Page",
            "AUTHOR": "Frontend Dev",
            "DATE": "2026-02-12",
            "FEATURE_NAME": "Hero",
            "FEATURE_COMPONENT": "HeroSection",
            "LOADING_NAME": "Spinner",
            "LOADING_COMPONENT": "LoadingSpinner",
            "ERROR_NAME": "ErrorBoundary",
            "ERROR_COMPONENT": "ErrorDisplay",
            "DATA_SOURCE": "users",
            "DATA_NAME": "Users",
            "PAGE_TITLE": "Welcome",
            "PAGE_DESCRIPTION": "The best app ever",
            "PAGE_HEADING": "Welcome to Next.js",
        }

        print("Rendering streamlit/app.py.tmpl...")
        st_output = engine.render("python/streamlit/app.py.tmpl", streamlit_context)
        print("Success! Streamlit Output length:", len(st_output))
        # print(st_output) # Uncomment to see output

        print("\nRendering typescript/nextjs/app/page.tsx.tmpl...")
        ts_output = engine.render("typescript/nextjs/app/page.tsx.tmpl", nextjs_context)
        print("Success! Next.js Output length:", len(ts_output))
        print("--- RENDERED TS START ---")
        print(ts_output)
        print("--- RENDERED TS END ---")

        # Basic validation
        assert "import streamlit as st" in st_output
        assert "def main(" in st_output

        assert "import type { Metadata } from 'next';" in ts_output
        assert "export default async function HomePage" in ts_output

        print("\nVERIFICATION SUCCESSFUL")

    except Exception as e:
        print(f"FAILED: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    verify()
