import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
import cash_postgresql
import json
import zapros_OFD
import parser_check
import base64
import os

encoded_image = '''AAABAAEAMDAAAAEAIACoJQAAFgAAACgAAAAwAAAAYAAAAAEAIAAAAAAAACQAALcRAAC3EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACho4IAoaOCAKGjggCho4ICoaOCBKGjgwCdpoAAo6GDAKGjgiWho4JkoaOCnqGjgsmho4LmoaOC9qGjgv6ho4L+oaOC9qGjguaho4LKoaOCn6GjgmWho4ImoaaEAJ6dfwCho4EAoaOCBKGjggKho4IAoaOCAKGjggAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoqOCAKGjggCho4IAoaOCAaGjggOho4IBoaOCAKGjghiho4JwoaOCxqGjgveho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L4oaOCxqGjgnGho4IYoaOCAKGjggGho4IDoaOCAaGjggCho4IAoaOCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACho4IAoaOCAKGjggCho4ICoaOCA6GjggCho4IeoaOClaGjgvOho4L/oaOC/qGjgv+ho4L9oaOC/KGjgv2ho4L+oaOC/6Gjgv+ho4L/oaOC/6Gjgv6ho4L9oaOC/KGjgv2ho4L/oaOC/qGjgv+ho4L0oaOCl6Gjgh6ho4IAoaOCA6GjggKho4IAoaOCAKGjggAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKGjggCio4IApaaEAKGjggOhpIIAoaOCBqGjgnuho4L0oaOC/6Gjgv6ho4L7oaOC/KGjgv6ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L+oaOC/KGjgvuho4L+oaOC/6GjgvSho4J7oaSCBaGlgwCho4IDorCCAKGlggCho4IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoaOCAKGjggCho4IAoaOCBKGjggCho4IqoaOCzqGjgv+ho4L9oaOC+6Gjgv6ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L+oaOC+6Gjgv2ho4L/oaOCzqGjgiuho4IAoaOCBKGjggCho4IAoaOCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACho4IAoaOCAKGjggCho4IEoaOCAKGjglWho4L1oaOC/6Gjgvuho4L+oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv6ho4L7oaOC/6GjgvWho4JVoaOCAKGjggSho4IAoaOCAKGjggAAAAAAAAAAAAAAAAAAAAAAAAAAAKGjggCho4IAoaOCAKGjggSho4IAoaOCbaGjgv+ho4L9oaOC/KGjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/KGjgv2ho4L/oaOCbaGjggCho4IEoaODAKGjgQCho4IAAAAAAAAAAAAAAAAAoaKCAKGjggCho4IAoaOCBKGjggCho4JtoaOC/6Gjgvuho4L9oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv2ho4L7oaOC/6Gjgm6ho4IAoaOCBKGjggCho4IAoKOBAAAAAAAAAAAAoaOCAKGjggCho4IDoaOCAKGjglaho4L/oaOC/KGjgv6ho4L/oaOC/6Gjgf+ipIL/oaOD/6Gjgv+ho4L/oaOD/6Gjgf+ho4H/oaOD/6Gjgv+ho4L/oaOD/6Gjgf+ho4H/oaOD/6Gjgv+ho4L/oaOD/6Gjgf+ho4H/oaOD/6Gjgv+ho4L/oaOD/6Kkgv+ho4H/oaOC/6Gjgv+ho4L+oaOC/KGjgv+ho4JWoaOCAKGjggOho4IAoaOCAAAAAACho4IAoaOCAKGjggKho4IAoaOCLqGjgvOho4L/oaOC/aGjgv+ho4L/oaOC/5+ig/+Ymn3/oaOB/6Gjgv+ho4P/oaOA/5ibgP+Ym4D/oaOA/6Gjg/+ho4P/oaOA/5ibgP+Ym4D/oaOA/6Gjg/+ho4P/oaOA/5ibgP+Ym4D/oaOA/6Gjg/+ho4L/oaOB/5iaff+fooP/oaOC/6Gjgv+ho4L/oaOC/aGjgv+ho4LzoaOCLqGjggCho4ICoaOCAKGjggCho4IAoaOCAaCiggCho4IGoaOCyqGjgv+ho4L8oaOC/6Gjgv+ho4L/oKJ//6Kni/+xw77/lpd3/6OlhP+jpYT/k5Rz/7vQz/+70M//k5Rz/6OlhP+jpYT/k5Rz/7vQz/+70M//k5Rz/6OlhP+jpYT/k5Rz/7vQz/+70M//k5Rz/6OlhP+jpYT/lpd3/7HCvv+ip4v/oKJ//6Gjgv+ho4L/oaOC/6Gjgvyho4L/oaOCyaGjggWhpIEAoaOCAaGjggCgoYAAoaOCA6GjggCho4J8oaOC/6Gjgvuho4L/oaOC/6Gjgv+ho4L/oaOB/56hg//R7PL/rby0/5iYdv+YmXb/q7qy/9fz+//X8/v/q7qy/5iZdv+YmXb/q7qy/9fz+//X8/v/q7qy/5iZdv+YmXb/q7qy/9fz+//X8/v/q7qy/5iZdv+YmHb/rby0/9Hs8v+eoYP/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L7oaOC/6Gjgnuho4IAoaOCA5+ffgCho4ICoaOCAKGjgiKho4LwoaOC/6Gjgv6ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihP/L4+f/1/P8/5yllP+dppX/1vH6/9Hr8f/R6/H/1vH6/52mlf+dppX/1vH6/9Hr8f/R6/H/1vH6/52mlf+dppX/1vH6/9Hr8f/R6/H/1vH6/52mlf+cpZT/1/P8/8vj5/+eooT/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L+oaOC/6GjgvCho4IioaOCAKGjggKho4IDoaOCAKGjgpSho4L/oaOC+6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4+f/1vH3/8vk6f/L4+n/0+3z/9Dp7//Q6e//0+zz/8vk6f/L4+n/0+3z/9Dp7//Q6e//0+zz/8vk6f/L4+n/0+3z/9Dp7//Q6e//0+3z/8vj6f/L5On/1vH3/8vj5/+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC+6Gjgv+ho4KUoaOCAKGjggOho4IAoaOCHKGjgvCho4L/oaOC/qGjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/M5Oj/0+3z/9j0+P/a+f3/2Pb8/9n3/f/Z9/3/2Pb8/9r4/f/a+P3/2Pb8/9n3/f/Z9/3/2Pb8/9r4/f/a+P3/2Pb8/9n3/f/Z9/3/2Pb8/9r5/f/Y9Pj/0+3z/8zk6P+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/qGjgv+ho4LwoaOCHKGjggCho4IAoaOCcaGjgv+ho4L7oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4+f/2PT6/6azuP99eX7/goGG/4GAhP+BgIT/gYCF/4F/hP+Bf4T/gYCF/4GAhP+BgIT/gYCF/4F/hP+Bf4T/gYCF/4GAhP+BgIT/goGG/315fv+ms7j/2PT6/8vj5/+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgvuho4L/oaOCcKGjggCho4IAoaOCw6Gjgv+ho4L9oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/K4ub/2ff9/5yfpP9pU1j/cF5k/29cYv9vXGH/b1xh/29cYf9vXGH/b1xh/29cYf9vXGH/b1xh/29cYf9vXGH/b1xh/29cYf9vXGL/cF5k/2lTWP+cn6T/2ff9/8ri5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv2ho4L/oaOCw6GjggCho4IooaOC9aGjgv+ho4L+oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L5Oj/1e/2/8ni5/+3zdL/uM3T/7fN0v+3zdL/t83S/7fN0v+3zdL/t83S/7fN0v+3zdL/t83S/7fN0v+3zdL/t83S/7fN0v+3zdL/uM3T/7fN0v/J4uj/1e/2/8vk6P+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv6ho4L/oaOC9aGjgiiho4JkoaOC/6Gjgv2ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/K4ub/2/j//4qIjf9MLTH/VTo//1M4Pf9TOD3/Uzg9/1M4Pf9TOD3/Uzg9/1M4Pf9TOD3/Uzg9/1M4Pf9TOD3/Uzg9/1M4Pf9TOD3/VTo//0wtMf+KiI3/2/n//8ri5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L9oaOC/6GjgmSho4KdoaOC/6Gjgvyho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4+f/1fD3/8jf5f+1xcv/tsfN/7bHzP+2x8z/tsfM/7bHzP+2x8z/tsfM/7bHzP+2x8z/tsfM/7bHzP+2x8z/tsfM/7bHzP+2x8z/tsfN/7XFy//I3+X/1fD3/8vj5/+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L8oaOC/6Gjgpyho4LIoaOC/6Gjgv2ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/K4ub/2fX8/5uip/9qXWL/cGZr/29laf9vZWn/b2Vp/29laf9vZWn/b2Vp/29laf9vZWn/b2Vp/29laf9vZWn/b2Vp/29laf9vZWn/cGZr/2pdYv+boqf/2fX8/8ri5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L9oaOC/6Gjgsiho4LloaOC/6Gjgv6ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4ub/2PX7/6u0uv+DeX7/iIGH/4eAhf+HgIX/h4CF/4eAhf+HgIX/h4CF/4eAhf+HgIX/h4CF/4eAhf+HgIX/h4CF/4eAhf+HgIX/iIGH/4N5fv+rtbr/2PX7/8vi5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L+oaOC/6GjguWho4L1oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4+f/1vH3/73S1/+jsbb/prS5/6W0uf+ltLn/pbS5/6W0uf+ltLn/pbS5/6W0uf+ltLn/pbS5/6W0uf+ltLn/pbS5/6W0uf+ltLn/prS5/6Oxtv+90tf/1vH3/8vj5/+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6GjgvWho4L+oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/K4ub/2/j//42Mkf9QMTb/WT5D/1c8Qf9XPEH/VzxB/1c8Qf9XPEH/VzxB/1c8Qf9XPEH/VzxB/1c8Qf9XPEH/VzxB/1c8Qf9XPEH/WT5D/1AxNv+NjJH/2/j//8ri5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv6ho4L+oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L5Oj/1O/1/9Do7v/J3+X/yuDm/8rg5v/K4Ob/yuDm/8rg5v/K4Ob/yuDm/8rg5v/K4Ob/yuDm/8rg5v/K4Ob/yuDm/8rg5v/K4Ob/yuDm/8nf5f/Q6O7/1O/1/8vk6P+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv6ho4L2oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/M5Oj/0+30/9Xx9//W9Pr/1fP5/9X0+f/V9Pn/1fT5/9X0+f/V9Pn/1fT5/9X0+f/V9Pn/1fT5/9X0+f/V9Pn/1fT5/9X0+f/V9Pn/1fP5/9b0+v/V8ff/0+30/8zk6P+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6GjgvWho4LloaOC/6Gjgv6ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/K4ub/2fb9/5ieo/9jU1f/al1h/2hbYP9oW2D/aFtg/2hbYP9oW2D/aFtg/2hbYP9oW2D/aFtg/2hbYP9oW2D/aFtg/2hbYP9oW2D/al1h/2NTV/+YnqP/2fb9/8ri5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L+oaOC/6GjguWho4LIoaOC/6Gjgv2ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4ub/2PX7/6y1u/+Ee4D/ioOJ/4mCh/+Jgof/iYKH/4mCh/+Jgof/iYKH/4mCh/+Jgof/iYKH/4mCh/+Jgof/iYKH/4mCh/+Jgof/ioOJ/4R7gP+stbv/2PX7/8vi5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L9oaOC/6Gjgsiho4KdoaOC/6Gjgvyho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4+f/1vH3/7zS1/+jsbb/pbO4/6SzuP+ks7j/pLO4/6SzuP+ks7j/pLO4/6SzuP+ks7j/pLO4/6SzuP+ks7j/pLO4/6SzuP+ks7j/pbO4/6Oxtv+80tf/1vH3/8vj5/+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L8oaOC/6Gjgp2ho4JloaOC/6Gjgv2ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/K4ub/2vj//46Nkv9TNDn/XEJH/1o/RP9aP0T/Wj9E/1o/RP9aP0T/Wj9E/1o/RP9aP0T/Wj9E/1o/RP9aP0T/Wj9E/1o/RP9aP0T/XEJH/1M0Of+OjZL/2vj//8ri5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L9oaOC/6GjgmSho4IpoaOC9qGjgv+ho4L+oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L5Oj/1e/2/83n7f++1Nr/vtXb/77V2/++1dr/vtXa/77V2v++1dr/vtXa/77V2v++1dr/vtXa/77V2v++1dr/vtXa/77V2v++1dv/vtXb/77U2v/N5+3/1e/2/8vk6P+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv6ho4L/oaOC9aGjgiiho4IAoaOCw6Gjgv+ho4L9oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/K4ub/2vf+/4+Rlv9VPUH/XUlN/1xGS/9cRkv/XEdL/1xHTP9cRkv/XEdL/1xGS/9cRkv/XEdL/1xHTP9cRkv/XEdL/1xHS/9cRkv/XUlN/1U9Qf+PkZb/2vf+/8ri5v+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgv2ho4L/oaOCw6GjggCho4IAoaOCcaGjgv+ho4L7oaOC/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4+f/1/P5/7jGzP+bnaP/n6Ko/56hp/+eoaf/nqGn/5ydo/+foqj/nqGn/56iqP+eoaf/nqGn/52gpf+foqj/nqGn/56hp/+eoqj/n6Ko/5udo/+3xsz/1/P5/8vj5/+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/6Gjgvuho4L/oaOCcaGjggCho4IAoaOCHKGjgvGho4L/oaOC/qGjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/M5Oj/0+70/9Xw9v/H2tz/zePn/8nd4P/L3+P/zePm/938///H2dz/zeTn/8jc3//M4eT/zOHl/9Pt8v/I297/y+Dj/8zi5f/I3N//zePn/8jb3v/X8/n/0+30/8zk6P+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC/qGjgv+ho4LwoaOCHKGjggCho4IDoaOCAKGjgpWho4L/oaOC+6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L4+f/1vL5/8XY3P+0vb7/rLGx/7O8vv+tsrL/u8jK/8fb4P+1v8H/q7Cw/7S+v/+rr6//ucbI/7nFx/+wt7j/sbi5/66ztP+0vr//q7Cw/7W/wf/I3eL/1vH4/8vj5/+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L/oaOC+6Gjgv+ho4KUoaOCAKGjggOho4ICoaOCAKGjgiKho4LxoaOC/6Gjgv6ho4L/oaOC/6Gjgv+ho4L/oaOB/56ihf/L5Oj/1O/2/8/n7P+7x8n/wNDU/73Lzv++zM//wdLV/9Pu9P+7yMr/wNDT/73Kzf+/ztH/wNHU/8jc4P+8ycv/vs3Q/7/P0v+9ys3/wNDT/7vJy//R6vD/1O71/8vk6P+eooX/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L+oaOC/6GjgvGho4IioaOCAKGjggKdnokAoaOCA6GjggCho4J8oaOC/6Gjgvuho4L/oaOC/6Gjgv+ho4L/oaOB/56ihP/L4+b/0+3z/9Lr8f/T7vT/0+70/9Pu8//T7vT/0+3z/9Lr8f/T7vP/0+70/9Pu8//T7vT/0+3z/9Pt8//T7vT/0+70/9Pu9P/T7vP/0+70/9Pu8//R6/D/0+3z/8vj5v+eooT/oaOB/6Gjgv+ho4L/oaOC/6Gjgv+ho4L7oaOC/6Gjgn2ho4IAoaOCA6SjhQCho4IAoaOCAaCjgwCho4IGoaOCyqGjgv+ho4L8oaOC/6Gj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'''
decoded_image = base64.b64decode(encoded_image)
with open("icon.ico", "wb") as icon_file:
    icon_file.write(decoded_image)

def extract_last_value(string):
    parts = string.split('_')
    last_value = parts[-1]
    return last_value


def compare_receipts_in_shift(
        login,
        password,
        cash,
        catalog,
        result_num_fiscal,
        id):
    set_text_to_entry_logi("\nПолучены данные из ОФД")
    entry0_1_1.yview(tk.END)
    try:
        last_values = zapros_OFD.search_shift_all(
            login, password, result_num_fiscal[0], result_num_fiscal[1])
    except:
        messagebox.showerror("Error", "Произошла ошибка при подключении к ОФД")        
    list1 = []
    for i in range(last_values['pagination']['totalItems']):
        last_value = extract_last_value(last_values['transactions'][i]['id'])
        list1.append(last_value)

    set_text_to_entry_logi("\nПолучены данные из базы данных")
    entry0_1_1.yview(tk.END)
    check_bd = cash_postgresql.num_check_db(cash, id)
    list2 = [int(item[0]) for item in check_bd]
    list1 = [int(i) for i in list1]
    set1 = set(list1)
    set2 = set(list2)
    set_text_to_entry_logi("\nСверяются данные из ОФД и БД кассы")
    entry0_1_1.yview(tk.END)
    missing_elements = list(set1 - set2)
    if (missing_elements == []):
        messagebox.showinfo(
            "Результат",
            "Смены сверены с ОФД расхождений нету")
    else:
        answer = messagebox.askquestion(
            "Результат", f"Смены сверены расхождения с ОФД в {
                len(missing_elements)} чека \n Исправить смену ?")
        if answer == "yes":
            prefix_cass = last_values['transactions'][0]['id'].rsplit('_', 1)[
                0]
            for i in range(len(missing_elements)):
                num_check = f"{prefix_cass}_{str(missing_elements[i])}"
                set_text_to_entry_logi(f"\nФормируем чек {num_check}")
                entry0_1_1.yview(tk.END)
                check = zapros_OFD.select_ofd_check(num_check)
                receipt_details = parser_check.pars_check(check)
                receipt_pos_details = parser_check.pars_pos(check)

                cash_postgresql.new_cap_check(
                    cash,
                    catalog,
                    id,
                    receipt_details['data_time'],
                    receipt_details['fiscal'],
                    receipt_details['sum_check'],
                    receipt_details['qr'],
                    receipt_details['paymont'],
                    receipt_pos_details)
            messagebox.showinfo(
                "Результат", "Отсутствующие чеки сформированны")
        else:
            set_text_to_entry_logi("\nОставляем смену")
            entry0_1_1.yview(tk.END)


def check_and_create_OFD_file():
    try:
        with open('OFD', "r") as file:
            data = json.load(file)

        if 'fix' not in data or 'azbuka' not in data:
            messagebox.showerror(
                "Error OFD.json",
                "Неверная структура в файле OFD\nДля исправления просто удалите его и он сформируется по новой")

        if not data['fix']['login'] or not data['fix']['password']:
            messagebox.showerror(
                "Error OFD.json",
                "В файле OFD.json у fix не заполнены login и password")

        if not data['azbuka']['login'] or not data['azbuka']['password']:
            messagebox.showerror(
                "Error OFD.json",
                "В файле OFD.json у azbuka не заполнены login и password")
    except FileNotFoundError:
        data = {}
        data['fix'] = {'login': '', 'password': ''}
        data['azbuka'] = {'login': '', 'password': ''}
        with open('OFD', "w") as file:
            json.dump(data, file, indent=2)
        messagebox.showinfo(
            "Внимание",
            "Не закрывая форму заполните сейчас в создавшемся файле OFD.json поля у всех login и password и только после этого нажимай ОК!\nИначе дальнейшая работа приведёт к ошибкам!")

    return data


def send_data():
    connOFD = combo.get()
    id = entry1_1.get().strip()
    try:
        ofd_data = check_and_create_OFD_file()
        try:
            cash = cash_postgresql.con_cash(
                entry0.get().strip(),
                entry1.get().strip(),
                entry2.get().strip())
            catalog = cash_postgresql.con_catalog(
                entry0.get().strip(), entry1.get().strip(), entry2.get().strip())
            try:
                result_num_fiscal = cash_postgresql.num_smen_and_fiscalnum(cash, id)
                if not all(result_num_fiscal):
                    raise ValueError("Получены пустые значения из базы данных")
                if connOFD == "Fix Price":
                    login = ofd_data['fix']['login']
                    password = ofd_data['fix']['password']
                    try:
                        compare_receipts_in_shift(
                            login, password, cash, catalog, result_num_fiscal, id)
                    except FileNotFoundError as e:
                        messagebox.showerror("Error", f'Возникла ошибка при создание чека: {e}')
                elif connOFD == "Азбука Вкус":
                    login = ofd_data['azbuka']['login']
                    password = ofd_data['azbuka']['password']
                    compare_receipts_in_shift(
                        login, password, cash, catalog, result_num_fiscal, id)
            except ValueError:
                messagebox.showerror("Error", "Вероятно не заполнены все данные в ch_shift")    
        except BaseException:
            messagebox.showerror("Error", "Нет подключеня к базе кассы!")
    except FileNotFoundError as e:
        set_text_to_entry_logi(f"\n Не обрабатываются данные для ОФД{e}")


def set_text_to_entry_logi(text):
    entry0_1_1.insert(tk.END, text)


root = tk.Tk()
root.title("Восстановление чеков в смене")
root.geometry("400x210")
root.iconbitmap("icon.ico")

frame = tk.Frame(root)
frame.pack(expand=True)

label0 = tk.Label(frame, text="IP Кассы")
label0.grid(row=0, column=0)

entry0 = tk.Entry(frame)
entry0.insert(0, "localhost")
entry0.grid(row=0, column=1)

label0_1 = tk.Label(frame, text="id смены")
label0_1.grid(row=0, column=2)

entry1_1 = tk.Entry(frame)
entry1_1.insert(0, "12962541")
entry1_1.grid(row=0, column=3)

label1 = tk.Label(frame, text="Логин")
label1.grid(row=1, column=0)

entry1 = tk.Entry(frame)
entry1.insert(0, "postgres")
entry1.grid(row=1, column=1)

label2 = tk.Label(frame, text="Пароль")
label2.grid(row=2, column=0)

entry2 = tk.Entry(frame)
entry2.insert(0, "postgres")
entry2.grid(row=2, column=1)

button1 = tk.Button(frame, text="Проверить", command=send_data)
button1.grid(row=3, column=0, columnspan=4, sticky='ew')
button1.configure(width=10, height=1)

container = tk.Frame(root)
container.pack(side='bottom', fill='both', expand=True)

entry0_1_1 = tk.Text(frame, height=8, width=40)
entry0_1_1.insert(tk.END, "Вывод лог файлов:")

entry0_1_1.grid(row=4, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
entry0_1_1.configure(font=("Arial", 6))

combo = Combobox(container)
combo['values'] = ("Fix Price", "Азбука Вкус")
combo.current(0)
combo.pack(side='right', padx=5)

label_version = tk.Label(container, text="version 1 / 2024 г")
label_version.pack(side='left', padx=5)

root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

os.remove("icon.ico")
root.mainloop()
