#!/usr/bin/env python3
"""
Keesje ASCII Art Collection for Melly Terminal Application
Based on professional ASCII art techniques and Unicode characters
"""

# ============================================================================
# CLASSIC ASCII STYLE (Using traditional ASCII characters)
# ============================================================================

KEESJE_CLASSIC_SMALL = r"""
   /\_/\
  ( o.o )
   > ^ <
  /|   |\
 (_|   |_)
"""

KEESJE_CLASSIC_MEDIUM = r"""
      /\_/\
     ( o o )
    (  =^=  )
     )   (
    (     )
   /       \
  /  /\ /\  \
 (__||_||__)
"""

KEESJE_CLASSIC_LARGE = r"""
           /\_/\
          ( o.o )
           > ^ <
          /|   |\
         / |   | \
        /  |   |  \
       /   |   |   \
      /    |   |    \
     (_____|   |_____)
          |   |
          |   |
         _|   |_
        (       )
"""

# ============================================================================
# DETAILED ASCII WITH PATTERNS (More realistic, based on Keesje's markings)
# ============================================================================

KEESJE_DETAILED = r"""
            /\_/\
           /     \
          | #   # |
          |  o.o  |
          |   ^   |
           \  =  /
            |||||
           /     \
          /       \
         /  /\ /\  \
        (__)(  )(___)
"""

# Sitting pose - matches Keesje's photo
KEESJE_SITTING = r"""
        |\__/,|   (\
        |_ _  |.--.)
        ( T   )     /
       (((^___((((_/
"""

# With grey markings on head (like the photo)
KEESJE_MARKED = r"""
       /\_/\
      /## ##\
     (  o o  )
      \  ^  /
       |||||
      /     \
     /  / \  \
    /__/   \__\
"""

# ============================================================================
# UNICODE BLOCK STYLE (Using block elements)
# ============================================================================

KEESJE_BLOCK_SMALL = """
    ▗▄▄▄▖
   ▟▀ ▀▀▙
  ▐● ▼ ●▌
   ▀▄▄▄▀
"""

KEESJE_BLOCK_MEDIUM = """
     ▗▄▄▄▄▄▖
    ▟▀▀▀▀▀▀▙
   ▟  ● ●  ▙
  ▐▌   ▼   ▐▌
   ▜▄  ═  ▄▛
    ▐█████▌
   ▐██▀▀██▌
   ███  ███
  ▀▀▀  ▀▀▀
"""

KEESJE_BLOCK_LARGE = """
        ▗▄▄▄▄▄▄▄▄▖
       ▟▀▀▀▀▀▀▀▀▀▀▙
      ▟▀▄▄▄▄▄▄▄▄▄▀▀▙
     ▐▌  ●     ●  ▐▌
     ▐▌     ▼     ▐▌
      ▙     ═     ▟
       ▜▄▄▄▄▄▄▄▄▛
        ▐███████▌
        ████▀████
       ▐███  ███▌
       ████  ████
      ▐▀▀▀  ▀▀▀▀▌
"""

# ============================================================================
# SHADED STYLE (Using different density characters)
# ============================================================================

KEESJE_SHADED = """
        ░▒▓▓▓▓▒░
       ▓▒░░░░░░▒▓
      ▓░  ● ●  ░▓
     ▓░    ▼    ░▓
      ▒▄   ═   ▄▒
       ▓█████████▓
      ▓████▀▀████▓
      ████░  ░████
     ▀▀▀▀    ▀▀▀▀
"""

# ============================================================================
# BOX DRAWING STYLE (Using box drawing characters)
# ============================================================================

KEESJE_BOX_BORDER = """
╔═══════════╗
║  /\\_/\\   ║
║ ( o.o )  ║
║  > ^ <   ║
║ /|   |\\  ║
║(_|   |_) ║
╚═══════════╝
"""

# ============================================================================
# MINIMALIST ONE-LINERS
# ============================================================================

KEESJE_MINIMAL = {
    'default': '(=^･ω･^=)',
    'happy': '(=^‥^=)',
    'sad': '(=T_T=)',
    'excited': '(=^･ｪ･^=)',
    'love': '(=♡ω♡=)',
    'sleeping': '(=˘ω˘=)',
    'surprised': '(=O_O=)',
    'wink': '(=^‥~=)',
}

# ============================================================================
# COWSAY STYLE WITH SPEECH BUBBLE
# ============================================================================

def keesje_say(message: str, width: int = 40) -> str:
    """
    Create cowsay-style output with Keesje
    """
    import textwrap

    lines = textwrap.wrap(message, width=width-4)
    if not lines:
        lines = ['']

    max_len = max(len(line) for line in lines)

    bubble = []
    bubble.append(' ' + '_' * (max_len + 2))

    if len(lines) == 1:
        bubble.append(f'< {lines[0]:<{max_len}} >')
    else:
        for i, line in enumerate(lines):
            if i == 0:
                bubble.append(f'/ {line:<{max_len}} \\')
            elif i == len(lines) - 1:
                bubble.append(f'\\ {line:<{max_len}} /')
            else:
                bubble.append(f'| {line:<{max_len}} |')

    bubble.append(' ' + '-' * (max_len + 2))

    cat = r"""        \
         \
      /\_/\
     ( o.o )
      > ^ <
     /|   |\
    (_|   |_)"""

    return '\n'.join(bubble) + '\n' + cat

# ============================================================================
# ANSI COLORED VERSIONS
# ============================================================================

# Colors: Grey patches on head, white face/body, pink nose
KEESJE_COLORED = """
\033[90m        ▗▄▄\033[37m▄▄▄\033[90m▄▄▖\033[0m
\033[90m       ▟\033[90m▀▀\033[37m▀▀▀\033[90m▀▀▙\033[0m
\033[90m      ▟\033[90m▀▄\033[37m▄▄▄\033[90m▄▀▙\033[0m
\033[37m     ▐▌  ● ●  ▐▌\033[0m
\033[37m     ▐▌    \033[38;5;217m▼\033[37m   ▐▌\033[0m
\033[37m      ▙    ═   ▟\033[0m
\033[37m       ▜▄▄▄▄▄▄▛\033[0m
\033[37m        ▐█████▌\033[0m
\033[37m       ▐███████▌\033[0m
\033[37m      ▐▀▀▀  ▀▀▀▌\033[0m
"""

KEESJE_COLORED_CLASSIC = """
\033[90m       /\033[37m\\_\033[90m/\\\033[0m
\033[90m      /\033[90m##\033[37m \033[90m##\033[37m\\\033[0m
\033[37m     (  \033[38;5;220mo\033[37m \033[38;5;220mo\033[37m  )\033[0m
\033[37m      \\  \033[38;5;217m^\033[37m  /\033[0m
\033[37m       |||||\033[0m
\033[37m      /     \\\033[0m
\033[37m     /  / \\  \\\033[0m
\033[37m    /__/   \\__\\\033[0m
"""

# ============================================================================
# EMOTICON STYLES FOR INLINE USE
# ============================================================================

KEESJE_INLINE = {
    'SUCCESS': '\033[0;32m(=^‥^=) ✓\033[0m',
    'ERROR': '\033[0;31m(=x_x=) ✗\033[0m',
    'WARNING': '\033[1;33m(=o_o=) ⚠\033[0m',
    'INFO': '\033[0;36m(=^･ω･^=) ℹ\033[0m',
    'WORKING': '\033[0;35m(=◉ω◉=) ⟳\033[0m',
}

# ============================================================================
# BANNER STYLE
# ============================================================================

KEESJE_BANNER = """
╔════════════════════════════════════════════════════════╗
║                                                        ║
║                    /\\_/\\          MELLY                ║
║                   ( o.o )         C4 Model Analyzer    ║
║                    > ^ <                               ║
║                   /|   |\\         by Keesje           ║
║                  (_|   |_)                             ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
"""

KEESJE_BANNER_COMPACT = """
┌─────────────────────────────────────┐
│    /\\_/\\      MELLY v1.0           │
│   ( o.o )     C4 Architecture       │
│    > ^ <      Analysis Tool         │
└─────────────────────────────────────┘
"""

# ============================================================================
# ANIMATION FRAMES FOR LOADING
# ============================================================================

KEESJE_FRAMES = [
    r"""
   /\_/\
  (● o  )
   > ^ <
  /|   |\
 (_|   |_)
""",
    r"""
   /\_/\
  ( o ●)
   > ^ <
  /|   |\
 (_|   |_)
""",
    r"""
   /\_/\
  (  o●)
   > ^ <
  /|   |\
 (_|   |_)
""",
    r"""
   /\_/\
  (● o )
   > ^ <
  /|   |\
 (_|   |_)
""",
]

# ============================================================================
# BRAILLE STYLE (High resolution)
# ============================================================================

KEESJE_BRAILLE = """
⠀⠀⠀⢀⣀⣀⡀⠀⠀
⠀⢀⣾⣿⣿⣿⣷⡀
⠀⣾⣿⡿⢿⣿⣿⣧
⢸⣿⣿⠀⠀⣿⣿⣿
⠸⣿⣿⣄⣠⣿⣿⠇
⠀⠙⠿⠿⠿⠿⠋⠀
"""

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_keesje(style: str = 'classic_medium', colored: bool = True):
    """Print Keesje ASCII art"""
    styles = {
        'classic_small': KEESJE_CLASSIC_SMALL,
        'classic_medium': KEESJE_CLASSIC_MEDIUM,
        'classic_large': KEESJE_CLASSIC_LARGE,
        'detailed': KEESJE_DETAILED,
        'sitting': KEESJE_SITTING,
        'marked': KEESJE_MARKED,
        'block_small': KEESJE_BLOCK_SMALL,
        'block_medium': KEESJE_BLOCK_MEDIUM,
        'block_large': KEESJE_BLOCK_LARGE,
        'shaded': KEESJE_SHADED,
        'boxed': KEESJE_BOX_BORDER,
        'banner': KEESJE_BANNER,
        'banner_compact': KEESJE_BANNER_COMPACT,
        'braille': KEESJE_BRAILLE,
    }

    if colored and style in ['block_medium', 'block_large', 'shaded']:
        print(KEESJE_COLORED)
    elif colored and 'classic' in style:
        print(KEESJE_COLORED_CLASSIC)
    else:
        print(styles.get(style, KEESJE_CLASSIC_MEDIUM))

def melly_log(level: str, message: str) -> str:
    """Format Melly log message with Keesje emoticon"""
    return f"{KEESJE_INLINE.get(level, KEESJE_INLINE['INFO'])} {message}"

def animate_loading(message: str = "Processing...", cycles: int = 3):
    """Animate loading with Keesje"""
    import sys
    import time

    for _ in range(cycles):
        for frame in KEESJE_FRAMES:
            sys.stdout.write("\033[2J\033[H")  # Clear screen
            print(frame)
            print(f"\n  {message}")
            sys.stdout.flush()
            time.sleep(0.2)

# ============================================================================
# MAIN - DEMO ALL STYLES
# ============================================================================

if __name__ == '__main__':
    print("=== KEESJE ASCII ART COLLECTION ===\n")

    print("Classic Small:")
    print(KEESJE_CLASSIC_SMALL)

    print("\nClassic Medium:")
    print(KEESJE_CLASSIC_MEDIUM)

    print("\nDetailed with Markings:")
    print(KEESJE_MARKED)

    print("\nSitting Pose:")
    print(KEESJE_SITTING)

    print("\nBlock Style:")
    print(KEESJE_BLOCK_MEDIUM)

    print("\nShaded Style:")
    print(KEESJE_SHADED)

    print("\nBoxed Style:")
    print(KEESJE_BOX_BORDER)

    print("\nColored Version:")
    print(KEESJE_COLORED)

    print("\nCowsay Style:")
    print(keesje_say("Analyzing C4 models... 📊"))

    print("\nInline Emoticons:")
    for level, emoticon in KEESJE_INLINE.items():
        print(f"{emoticon} - {level}")

    print("\nBanner:")
    print(KEESJE_BANNER_COMPACT)

    print("\nOne-liners:")
    for mood, face in KEESJE_MINIMAL.items():
        print(f"{mood}: {face}")
