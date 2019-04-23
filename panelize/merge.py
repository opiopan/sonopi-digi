#!/usr/bin/env python
import gerberex
from gerberex import DxfFile, GerberComposition, DrillComposition

exts = ['GTL', 'GTO', 'GTP', 'GTS', 'GBL', 'GBO', 'GBP', 'GBS', 'TXT']
boards=[
    ('../pcb/CAMOutputs/sonopi-digi.', 0, 0, 0),
    ('../pcb/CAMOutputs/sonopi-digi.', 0, 25, 0),
    ('../pcb/CAMOutputs/sonopi-digi.', 0, 50, 0),
    ('../pcb/CAMOutputs/sonopi-digi.', 0, 75, 0),
    ('../pcb/CAMOutputs/sonopi-digi.', 100, 15.15, 95),
]
outline = 'outline.dxf'
mousebites = 'mousebites.dxf'
fill = 'fill.dxf'
outputs = 'outputs/sonopi-digi-panelized'

for ext in exts:
    print('merging %s: ' % ext ,end='', flush=True)
    if ext == 'TXT':
        ctx = DrillComposition()
    else:
        ctx = GerberComposition()
    for board in boards:
        file = gerberex.read(board[0] + ext)
        file.to_metric()
        file.rotate(board[3])
        file.offset(board[1], board[2])
        ctx.merge(file)
        print('.', end='', flush=True)
    if ext == 'TXT':
        file = gerberex.read(mousebites)
        file.draw_mode = DxfFile.DM_MOUSE_BITES
        file.width = 0.5
        file.format = (3, 3)
        ctx.merge(file)
    else:
        file = gerberex.read(outline)
        ctx.merge(file)
    ctx.dump(outputs + '.' + ext)
    print(' end', flush=True)

print('generating GML: ', end='', flush=True)
file = gerberex.read(outline)
file.write(outputs + '.GML')
print('.', end='', flush=True)
ctx = GerberComposition()
file = gerberex.read(fill)
file.to_metric()
file.draw_mode = DxfFile.DM_FILL
ctx.merge(file)
ctx.dump(outputs + '-fill.GML')

print('. end', flush=True)
