# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the source directory to the Python path
sys.path.insert(0, os.path.abspath('../src'))

# Add custom extensions directory to Python path
sys.path.insert(0, os.path.abspath('_extensions'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Financial Debt Optimizer'
copyright = '2025, Bryan Kemp'
author = 'Bryan Kemp'
release = '1.3.0'
version = '1.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',  # Added for better API documentation
    'sphinx_autodoc_typehints',
    'myst_parser',
    'test_reports',  # Custom extension for test report integration
]

# Generate autosummary stubs automatically
autosummary_generate = True

# Source file parsers
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_css_files = [
    'custom_test_reports.css',  # Custom styling for test reports
]

# Fix for newer Sphinx versions
html_permalinks_icon = '🔗'
# Disable jQuery SRI for compatibility
jquery_use_sri = False

# -- Extension configuration -------------------------------------------------

# -- Options for autodoc extension ------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Configure autodoc to handle import errors gracefully
autodoc_mock_imports = ['pandas', 'numpy', 'matplotlib', 'xlsxwriter', 'openpyxl', 'click']
autodoc_typehints = 'description'
nitpicky = False

# Suppress autodoc warnings for missing modules and other common warnings
suppress_warnings = [
    'autodoc.import_object',
    'ref.python',  # Suppress Python reference warnings
    'myst.header',  # Suppress MyST header warnings
]

# -- Options for napoleon extension -----------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# -- Options for intersphinx extension --------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

# -- Options for MyST parser ------------------------------------------------
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
]

# -- Options for test reports extension -------------------------------------
test_reports_enabled = True
test_reports_fail_on_error = False  # Don't fail docs build if tests fail
test_reports_run_on_build = True

# -- HTML context variables -------------------------------------------------
html_context = {
    "display_github": True,
    "github_user": "bryankemp",
    "github_repo": "financial-debt-optimizer",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
