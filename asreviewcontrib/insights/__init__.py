from asreviewcontrib.insights.metrics import erf
from asreviewcontrib.insights.metrics import recall
from asreviewcontrib.insights.metrics import wss
from asreviewcontrib.insights.plot import plot_erf
from asreviewcontrib.insights.plot import plot_recall
from asreviewcontrib.insights.plot import plot_wss

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

__all__ = ['plot_recall', 'plot_wss', 'plot_erf', 'erf', 'recall', 'wss']
