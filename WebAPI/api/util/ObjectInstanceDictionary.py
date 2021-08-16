from .Minmaxers.HelpInvoker import HelpInvoker
from .Minmaxers.Highriser import Highriser
from .Minmaxers.Highriser2 import Highriser2
from .Minmaxers.LowIsGood import LowIsGood
from .Minmaxers.RooflessCuddler import RooflessCuddler
from .Minmaxers.SimpleInvoker import SimpleInvoker
from .Minmaxers.SansInvoker1 import SansInvoker1
from .Minmaxers.SansInvoker2 import SansInvoker2
from .Minmaxers.SansInvoker3 import SansInvoker3
from .Minmaxers.SansInvoker4 import SansInvoker4
from .Santorini import Santorini

INSTANCES = {'RandomMinmaxer' : Santorini(False),
             'LowIsGood' : LowIsGood(False),
             'Highriser2' : Highriser2(False),
             'Highriser' : Highriser(False),
             'HelpInvoker' : HelpInvoker(False),
             'RooflessCuddler' : RooflessCuddler(False),
             'SansInvoker1' : SansInvoker1(False),
             'SansInvoker2' : SansInvoker2(False),
             'SansInvoker3' : SansInvoker3(False),
             'SansInvoker4' : SansInvoker4(False),
             'SimpleInvoker' : SimpleInvoker(False)}