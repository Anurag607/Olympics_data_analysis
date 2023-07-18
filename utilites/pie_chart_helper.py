import numpy as np

def pie_pct(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return f"{pct:.2f}%\n({absolute:d})"

def pie_concat_val(sex,value,total_athletes):
    if sex==0:
        return value.__str__()+'\n Male Athletes \n'+f"{(value / total_athletes) * 100:.2f}%"
    else:
        return value.__str__()+'\n Female Athletes \n'+f"{(value / total_athletes) * 100:.2f}%"