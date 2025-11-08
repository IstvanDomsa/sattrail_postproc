from calendar import c
from tracemalloc import start
import postproc2

import time


subfile = '../data/1-557199_63-sub.fits'
detfile = '../data/1-557199_63-detection.json'
outputfile = '../data/1-557199_63-postproc.hdf5'
plot_directory = '../data'

start_time = time.time()

# df0, FINALLIST, mask_master, cpoints, rpoints = pp.postproc(    # type: ignore[reportAttributeAccessIssue]
#     subfile, detfile, outputfile,
#     None,   # parameter not used, should be removed?
#     SAVE=True, PLOT=False,
#     skeleton=False, progressive=True, gpu=False,
#     filter_radius=10,
#     nclose=10, nhalf=1, nsig=3, gap=2
# )

df0 = postproc2.process_mask(subfile, detfile, outputfile, skeleton=True, progressive=True, plot_directory=plot_directory)

end_time = time.time()
elapsed = end_time - start_time

print(f"Result: {df0}")
print(f"Execution time: {elapsed:.4f} seconds")
