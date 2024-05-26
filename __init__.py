# from .crewai import Crew
import os
from .modules.log import create_logger
logger = create_logger()

ROOT = os.path.abspath(os.path.dirname(__file__))
NAME = "Crewai Nodes"
PACKAGE = "ComfyUI-CrewAI"
MENU_NAME = "Crewai"
# SUB_MENU_NAME = "Language Toolkit"
NODES_DIR = os.path.join(ROOT, 'nodes')
EXTENSION_WEB_DIRS = {}
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Load modules
from .modules.node_importer import ModuleLoader

module_timings = {}
module_loader = ModuleLoader(PACKAGE)
module_loader.load_modules(NODES_DIR)

# Mappings
NODE_CLASS_MAPPINGS = module_loader.NODE_CLASS_MAPPINGS
NODE_DISPLAY_NAME_MAPPINGS = module_loader.NODE_DISPLAY_NAME_MAPPINGS

# # Timings and such
logger.info("")
module_loader.report(NAME)
logger.info("")

# Export nodes
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# NODE_CLASS_MAPPINGS = {"Crew": Crew}

# NODE_DISPLAY_NAME_MAPPINGS = { "CrewNode": "Node of crew" }

# __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']