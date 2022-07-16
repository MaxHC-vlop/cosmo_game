import asyncio
import time
import curses


TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(3):
            await asyncio.sleep(0)


def draw(canvas):
    row, column = (5, 20)
    coroutines = []
    for i in range(5):
        coroutine = blink(canvas, row, column)
        coroutines += [coroutine]
        column += 2
    while True:
        for var in coroutines.copy():
            try:
                var.send(None)
                
            except StopIteration:
                coroutines.remove(coroutines[var])
        if not len(coroutines):
            break
            
        curses.curs_set(False)
        canvas.border()
        canvas.refresh()
        time.sleep(0.1)



if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
