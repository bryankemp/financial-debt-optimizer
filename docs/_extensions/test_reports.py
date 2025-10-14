"""
Sphinx extension for automatic test report integration.

This extension automatically runs test report generation during documentation builds
and integrates the results into the documentation.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.util import logging

logger = logging.getLogger(__name__)


def generate_test_reports(app: Sphinx) -> None:
    """Generate test reports before documentation build."""
    if app.config.test_reports_enabled:
        logger.info("Generating test reports...")
        
        # Get project root (assuming docs is in project root)
        project_root = Path(app.srcdir).parent
        script_path = project_root / "scripts" / "generate_test_reports.py"
        
        if script_path.exists():
            try:
                # Run the test report generator
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode == 0:
                    logger.info("Test reports generated successfully")
                else:
                    logger.warning(f"Test report generation failed: {result.stderr}")
                    if app.config.test_reports_fail_on_error:
                        raise RuntimeError(f"Test report generation failed: {result.stderr}")
                
            except Exception as e:
                logger.error(f"Error running test report generator: {e}")
                if app.config.test_reports_fail_on_error:
                    raise
        else:
            logger.warning(f"Test report generator script not found: {script_path}")


def add_test_report_css(app: Sphinx, exception: Exception = None) -> None:
    """Add custom CSS for test reports."""
    if exception is None and app.builder.name == 'html':
        # Add custom CSS for test report styling
        css_content = """
/* Test Report Styling */
.test-report-summary {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 0.375rem;
    padding: 1rem;
    margin: 1rem 0;
}

.test-success {
    color: #198754;
    font-weight: bold;
}

.test-failure {
    color: #dc3545;
    font-weight: bold;
}

.test-warning {
    color: #fd7e14;
    font-weight: bold;
}

.coverage-excellent {
    background-color: #d1e7dd;
    color: #0f5132;
}

.coverage-good {
    background-color: #fff3cd;
    color: #664d03;
}

.coverage-needs-improvement {
    background-color: #f8d7da;
    color: #721c24;
}

/* Coverage progress bars */
.coverage-bar {
    width: 100%;
    height: 20px;
    background-color: #e9ecef;
    border-radius: 0.25rem;
    overflow: hidden;
}

.coverage-fill {
    height: 100%;
    background-color: #198754;
    transition: width 0.3s ease;
}

.coverage-fill.excellent {
    background-color: #198754;
}

.coverage-fill.good {
    background-color: #ffc107;
}

.coverage-fill.needs-improvement {
    background-color: #dc3545;
}

/* Test report tables */
.test-report table {
    margin: 1rem 0;
}

.test-report .headerless th {
    background-color: #f8f9fa;
    border-color: #dee2e6;
}

.test-report .coverage-cell {
    text-align: center;
    font-weight: bold;
}
"""
        
        # Write CSS to static directory
        static_dir = Path(app.outdir) / "_static"
        static_dir.mkdir(exist_ok=True)
        
        css_file = static_dir / "test_reports.css"
        with open(css_file, 'w') as f:
            f.write(css_content)
        
        # Add CSS to HTML
        if hasattr(app.builder, 'add_css_file'):
            app.builder.add_css_file('test_reports.css')


def setup(app: Sphinx) -> Dict[str, Any]:
    """Set up the test reports extension."""
    
    # Add configuration options
    app.add_config_value('test_reports_enabled', True, 'html')
    app.add_config_value('test_reports_fail_on_error', False, 'html')
    app.add_config_value('test_reports_run_on_build', True, 'html')
    
    # Connect to Sphinx events
    app.connect('builder-inited', generate_test_reports)
    app.connect('build-finished', add_test_report_css)
    
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }