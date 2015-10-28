#!/usr/bin/env python3
from . import backtrace_MED
from . import normal_MED
from . import weighted_MED

from ..preprocessing import utilities

utilities.print_banner('Normal MED')
print("MED by normal method:", normal_MED.calculate('xyffsd', 'aewrt'))

utilities.print_banner('MED with backtracing')
med = backtrace_MED.BackTraceMED()
med.set_str('intention', 'execution')
print("MED with backtracing ", med.calculate())
med.print_steps()
med.print_alignment()

utilities.print_banner('Weighted MED')
med = weighted_MED.WeightedMED()
med.set_str('intention', 'execution')
print('Weighted MED', med.calculate())
med.print_steps()
med.print_alignment()

