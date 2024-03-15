__author__ = """Alan Ramponi, Camilla Casula, Stefano Menini"""
__version__ = """0.1.0"""

from .inspector import Inspector, InspectorArgs
from .visualizer import Visualizer, VisualizerArgs

def get_version(
	) -> str:
	"""A method that simply returns the package version."""
	return __version__