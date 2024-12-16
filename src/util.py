TAGCHARS = '0289PYLQGRJCUV'

def tag_to_hi_lo(tag: str):
    assert tag.startswith("#")
    assert len(tag) > 1
    assert all((c in TAGCHARS) for c in tag[1:])
    
    tag = tag[1:]
    
    id = 0
    for a in range(len(tag)):
        i = TAGCHARS.index(tag[a])
        id *= len(TAGCHARS)
        id += i
    
    high = id % 256
    low = (id - high) >> 8 & 0xFFFF_FFFF

    return high, low