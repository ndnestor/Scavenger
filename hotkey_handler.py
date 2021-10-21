import os

from ahk import AHK, Hotkey


ahk = AHK()

toggle_visibility_key: str = '#n'
pid: int = os.getpid()

hide_window_snippet = f'WinHide, ahk_pid {pid}'

show_window_snippet = f'''
    MouseGetPos, mouseXPos, mouseYPos
    WinMove, ahk_pid {pid}, , %mouseXPos%, %mouseYPos%
    WinShow, ahk_pid {pid}
    WinActivate, ahk_pid {pid}
'''

get_visibility_snippet = f'''
    WinGet, Style, Style, ahk_pid {pid}
    visible := Style & 0x10000000
'''

toggle_visibility_hotkey = Hotkey(ahk, toggle_visibility_key, f'''

    CoordMode, Mouse, Screen
    DetectHiddenWindows, On

    {get_visibility_snippet}

    if(visible) {{
        {hide_window_snippet}
    }} else {{
        {show_window_snippet}
    }}

''')

left_button_hotkey = Hotkey(ahk, '~LButton', f'''

    Click, Down

    {get_visibility_snippet}

    if(visible) {{
        MouseGetPos, , , winUnderCursorId
        WinGet, winUnderCursorPid, PID, ahk_id %winUnderCursorId%
        if(winUnderCursorPid != {pid}) {{
            {hide_window_snippet}
        }}
    }}

''')

left_button_up_hotkey = Hotkey(ahk, 'LButton Up', 'Click, Up')

def start():
    toggle_visibility_hotkey.start()
    left_button_up_hotkey.start()
    left_button_hotkey.start()

def stop():
    left_button_hotkey.stop()
    left_button_up_hotkey.stop()
    toggle_visibility_hotkey.stop()
