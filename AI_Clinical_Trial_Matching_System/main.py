# Clinical Trial Patient Matching System
# Main entry point for the system

from src.utils.setup import setup_environment
from src.pipeline.run_pipeline import run_matching_pipeline

if __name__ == "__main__":
    setup_environment()
    run_matching_pipeline()
