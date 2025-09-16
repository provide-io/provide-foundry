"""
MkDocs hooks for Provide Foundry documentation aggregation.

These hooks run automatically during mkdocs build/serve to collect
documentation from all projects in the provide.io ecosystem.
"""

import logging
import os
import sys
from pathlib import Path

# Add the scripts directory to the path so we can import the aggregator
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

try:
    from docs_aggregator import DocsAggregator
except ImportError as e:
    logging.error(f"Failed to import docs_aggregator: {e}")
    sys.exit(1)

logger = logging.getLogger(__name__)


def on_pre_build(config, **kwargs):
    """
    Hook that runs before MkDocs starts building the site.

    This collects documentation from all projects and places it in the
    aggregated directory for MkDocs to process.
    """
    logger.info("🏗️ Running pre-build hook: collecting documentation")

    # Get the foundry root directory (parent of this script)
    foundry_root = Path(__file__).parent.parent

    try:
        # Initialize the aggregator
        aggregator = DocsAggregator(foundry_root)

        # Collect all documentation
        success = aggregator.collect_all()

        if not success:
            logger.warning("⚠️ Documentation collection completed with some failures")
        else:
            logger.info("✅ Documentation collection completed successfully")

    except Exception as e:
        logger.error(f"❌ Failed to collect documentation: {e}")
        # Don't fail the build - just warn
        logger.warning("⚠️ Continuing with existing documentation")


def on_post_build(config, **kwargs):
    """
    Hook that runs after MkDocs finishes building the site.

    This can be used for cleanup or post-processing.
    """
    logger.info("🎉 Documentation build completed")


def on_serve(config, server, **kwargs):
    """
    Hook that runs when starting the development server.

    This sets up file watching for all project documentation directories.
    """
    logger.info("🚀 Starting development server with federated documentation")

    # The aggregator's watch mode would conflict with mkdocs serve,
    # so we rely on the 'watch' paths in mkdocs.yml for now
    # In the future, we could implement more sophisticated watching


def on_config(config, **kwargs):
    """
    Hook that runs when the configuration is loaded.

    This can be used to modify the configuration based on available projects.
    """
    logger.info("⚙️ Configuring federated documentation")

    # Ensure the aggregated docs directory exists
    foundry_root = Path(__file__).parent.parent
    aggregated_dir = foundry_root / '.docs_aggregated'

    if not aggregated_dir.exists():
        logger.info("📁 Creating aggregated documentation directory")
        aggregated_dir.mkdir(exist_ok=True)

        # Create a minimal index.md if none exists
        index_file = aggregated_dir / 'index.md'
        if not index_file.exists():
            index_file.write_text("""# Provide Foundry Documentation

Welcome to the comprehensive documentation for the Provide Foundry collection of Python tools and frameworks.

Documentation is being aggregated from individual projects...
""")

    return config