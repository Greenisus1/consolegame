#!/usr/bin/env python3
import curses, time, random, math, pprint, sys, os

# ─── Rename Terminal Tab ─────────────────────────────
# This ANSI escape sequence will (in many terminals) rename the tab.
print("\033]0;PLAYING - STARBUCKS-=-PLATFORMER\a")

# ─── HELPER FUNCTION ─────────────────────────────────────
def collides(a, b, a_w_key='width', b_w_key='w'):
    """Basic AABB collision between objects 'a' and 'b' using provided width keys."""
    return (a['x'] < b['x'] + b[b_w_key] and
            a['x'] + a['width'] > b['x'] and
            a['y'] < b['y'] + b['h'] and
            a['y'] + a['height'] > b['y'])

# ─── HANDCRAFTED LEVELS (Levels 1–10) ─────────────────────
def load_handcrafted_level(level_num, sh, sw):
    if level_num == 1:
        platforms = [
            {'x': 0, 'y': sh - 2, 'w': sw, 'h': 1},
            {'x': 10, 'y': sh - 6, 'w': 15, 'h': 1}
        ]
        enemies = [
            {'x': 12.0, 'y': sh - 7, 'vx': 0.5, 'width': 3, 'height': 1,
             'min_x': 10, 'max_x': 25, 'type': 'basic'}
        ]
        goal = {'x': sw - 10, 'y': sh - 4, 'width': 5, 'height': 2}
        planes = []
        lava = []
    elif level_num == 2:
        platforms = [
            {'x': 0, 'y': sh - 2, 'w': sw, 'h': 1},
            {'x': 20, 'y': sh - 5, 'w': 20, 'h': 1},
            {'x': 45, 'y': sh - 8, 'w': 15, 'h': 1},
        ]
        enemies = [
            {'x': 22.0, 'y': sh - 6, 'vx': 0.7, 'width': 3, 'height': 1,
             'min_x': 20, 'max_x': 40, 'type': 'basic'}
        ]
        goal = {'x': sw - 15, 'y': sh - 4, 'width': 5, 'height': 2}
        planes = []
        lava = []
    elif level_num == 3:
        platforms = [
            {'x': 0, 'y': sh - 2, 'w': sw, 'h': 1},
            {'x': 15, 'y': sh - 6, 'w': 20, 'h': 1},
            {'x': 40, 'y': sh - 9, 'w': 15, 'h': 1},
        ]
        enemies = [
            {'x': 18.0, 'y': sh - 7, 'vx': 0.5, 'width': 3, 'height': 1,
             'min_x': 15, 'max_x': 35, 'type': 'slime'}
        ]
        goal = {'x': sw - 10, 'y': sh - 4, 'width': 5, 'height': 2}
        planes = []
        lava = [{'x': sw//2 - 10, 'y': sh - 2, 'w': 20, 'h': 1}]
    elif level_num == 4:
        platforms = [
            {'x': 0, 'y': sh - 2, 'w': sw, 'h': 1},
            {'x': 10, 'y': sh - 7, 'w': 15, 'h': 1},
            {'x': 35, 'y': sh - 10, 'w': 20, 'h': 1},
            {'x': 60, 'y': sh - 8, 'w': 15, 'h': 1},
        ]
        enemies = [
            {'x': 12.0, 'y': sh - 7, 'vx': 0.5, 'width': 3, 'height': 1,
             'min_x': 10, 'max_x': 25, 'type': 'basic'},
            {'x': 38.0, 'y': sh - 11, 'vx': 0.6, 'width': 3, 'height': 1,
             'min_x': 35, 'max_x': 55, 'type': 'flying'}
        ]
        goal = {'x': sw - 12, 'y': sh - 4, 'width': 6, 'height': 2}
        planes = [{'x': sw//3, 'y': sh - 12, 'w': 10, 'h': 1}]
        lava = [{'x': sw//2 - 5, 'y': sh - 2, 'w': 10, 'h': 1}]
    else:
        platforms = [
            {'x': 0, 'y': sh - 2, 'w': sw, 'h': 1},
            {'x': 10 + level_num * 2, 'y': sh - (6 + level_num), 'w': 15, 'h': 1},
            {'x': 30 + level_num * 3, 'y': sh - (8 + level_num * 2), 'w': 20, 'h': 1},
            {'x': sw//2, 'y': sh - (10 + level_num), 'w': 10, 'h': 1}
        ]
        enemy_type = random.choice(['basic', 'slime', 'flying'])
        enemies = [
            {'x': 12.0 + level_num, 'y': sh - (7 + level_num), 'vx': 0.5,
             'width': 3, 'height': 1,
             'min_x': 10 + level_num, 'max_x': 25 + level_num,
             'type': enemy_type}
        ]
        goal = {'x': sw - (10 + level_num), 'y': sh - 4, 'width': 5, 'height': 2}
        planes = [{'x': sw//3, 'y': sh - (12 + level_num), 'w': 10, 'h': 1}]
        lava = []
    player = {'x': 5.0, 'y': sh - 5, 'vx': 0.0, 'vy': 0.0,
              'width': 3, 'height': 2, 'jumping': False}
    bonus_hearts = []  # list for bonus heart pickups
    level_dict = {
        "platforms": platforms,
        "enemies": enemies,
        "goal": goal,
        "player": player,
        "planes": planes,
        "lava": lava,
        "bonus_hearts": bonus_hearts
    }
    return level_dict

# ─── PROCEDURALLY GENERATED LEVELS (Level 11+) ───────────
def generate_level(level_num, sh, sw):
    rng = random.Random(int(level_num * math.pi * 1000))
    platforms = []
    platforms.append({'x': 0, 'y': sh - 2, 'w': sw, 'h': 1})
    num_platforms = rng.randint(2, 5)
    for i in range(num_platforms):
        x = rng.randint(5, sw - 20)
        y = rng.randint(5, sh - 5)
        w_plat = rng.randint(10, 20)
        platforms.append({'x': x, 'y': y, 'w': w_plat, 'h': 1})
    enemies = []
    num_enemies = rng.randint(1, 3)
    for i in range(num_enemies):
        x = rng.randint(10, sw - 10)
        enemy_type = rng.choice(['basic', 'slime', 'flying'])
        enemy = {'x': float(x), 'y': float(sh - 3),
                 'vx': rng.choice([0.5, -0.5]),
                 'width': 3, 'height': 1,
                 'min_x': max(0, x - 5), 'max_x': min(sw - 3, x + 5),
                 'type': enemy_type}
        enemies.append(enemy)
    goal = {'x': sw - 10, 'y': sh - 4, 'width': 5, 'height': 2}
    player = {'x': 5.0, 'y': sh - 5, 'vx': 0.0, 'vy': 0.0,
              'width': 3, 'height': 2, 'jumping': False}
    if rng.random() < 0.5:
        x_lava = rng.randint(10, sw - 20)
        y_lava = rng.randint(sh - 10, sh - 2)
        w_lava = rng.randint(5, 15)
        lava = [{'x': x_lava, 'y': y_lava, 'w': w_lava, 'h': 1}]
    else:
        lava = []
    if rng.random() < 0.4:
        x_plane = rng.randint(5, sw - 15)
        y_plane = rng.randint(3, sh - 15)
        planes = [{'x': x_plane, 'y': y_plane, 'w': rng.randint(8, 15), 'h': 1}]
    else:
        planes = []
    bonus_hearts = []
    level_dict = {
        "platforms": platforms,
        "enemies": enemies,
        "goal": goal,
        "player": player,
        "planes": planes,
        "lava": lava,
        "bonus_hearts": bonus_hearts
    }
    return level_dict

# ─── BOSS FIGHT MINI‑GAME (Tic Tac Toe style) ─────────────
def boss_fight(stdscr):
    board = [[' ' for _ in range(3)] for _ in range(3)]
    def generate_board():
        new_board = []
        for i in range(3):
            row = []
            for j in range(3):
                r = random.random()
                if r < 0.4:
                    row.append('X')
                elif r < 0.7:
                    row.append('O')
                else:
                    row.append(' ')
            new_board.append(row)
        return new_board

    board = generate_board()
    start_time = time.time()
    last_update = start_time
    player_count = 0
    boss_count = 0
    cursor_r, cursor_c = 0, 0
    stdscr.nodelay(True)
    while time.time() - start_time < 20:
        now = time.time()
        if now - last_update >= 5:
            board = generate_board()
            last_update = now
        stdscr.clear()
        stdscr.addstr(0, 0, "Boss Fight! Collect X's before boss collects O's!")
        stdscr.addstr(1, 0, f"Your X's: {player_count}   Boss O's: {boss_count}")
        for i in range(3):
            line = ""
            for j in range(3):
                cell = board[i][j]
                if i == cursor_r and j == cursor_c:
                    line += "[" + cell + "]"
                else:
                    line += " " + cell + " "
            stdscr.addstr(3+i, 0, line)
        stdscr.addstr(7, 0, "Use arrow keys to move, Enter to collect. (Press q to quit)")
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP and cursor_r > 0:
            cursor_r -= 1
        elif key == curses.KEY_DOWN and cursor_r < 2:
            cursor_r += 1
        elif key == curses.KEY_LEFT and cursor_c > 0:
            cursor_c -= 1
        elif key == curses.KEY_RIGHT and cursor_c < 2:
            cursor_c += 1
        elif key in [10, 13]:
            if board[cursor_r][cursor_c] == 'X':
                player_count += 1
                board[cursor_r][cursor_c] = ' '
        elif key == ord('q'):
            break
        # Boss automatically collects O's.
        o_count = sum(row.count('O') for row in board)
        if o_count > 0:
            boss_count += o_count
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 'O':
                        board[i][j] = ' '
        if player_count >= 3:
            stdscr.addstr(9, 0, "You win the boss fight! Bonus speed awarded!")
            stdscr.refresh()
            time.sleep(2)
            return 1
        if boss_count >= 3:
            stdscr.addstr(9, 0, "Boss wins the mini-game! No bonus speed.")
            stdscr.refresh()
            time.sleep(2)
            return 0
        time.sleep(0.1)
    if player_count > boss_count:
        stdscr.addstr(9, 0, "Time's up! You win! Bonus speed awarded!")
        stdscr.refresh()
        time.sleep(2)
        return 1
    else:
        stdscr.addstr(9, 0, "Time's up! Boss wins! No bonus speed.")
        stdscr.refresh()
        time.sleep(2)
        return 0

# ─── HUD DRAWING ─────────────────────────────────────────────
def draw_hud(stdscr, game_state, sh, sw):
    lives = game_state["lives"]
    hearts = ""
    for i in range(3):
        if i < lives:
            hearts += "♡ "
        else:
            hearts += "♥ "
    try:
        stdscr.addstr(0, 0, "Lives: " + hearts)
        box_text = " [♥ ♥ ♥] "
        stdscr.addstr(0, sw - len(box_text) - 1, box_text)
        stdscr.addstr(1, 0, "Ctrl+S = Pause   Ctrl+Z = Continue")
    except curses.error:
        pass

# ─── GAMEPLAY LOOP FOR A LEVEL ─────────────────────────────
def play_level(stdscr, level, level_num, game_state):
    sh, sw = stdscr.getmaxyx()
    stdscr.nodelay(True)
    def effective_speed(): 
        return 1.5 + game_state.get("speed_bonus", 0)
    player = level["player"]
    bonus_hearts = level["bonus_hearts"]
    paused = False  # pause state flag
    while True:
        prev_y = player['y']
        # Process keys
        key = stdscr.getch()
        while key != -1:
            if key == 1:  # Ctrl+A: left
                player['vx'] = -effective_speed()
            elif key == 4:  # Ctrl+D: right
                player['vx'] = effective_speed()
            elif key == 23:  # Ctrl+W: jump
                if not player['jumping']:
                    player['vy'] = -5.0
                    player['jumping'] = True
            elif key == 16:  # Ctrl+P: reload current level
                return "reload"
            elif key == 2:   # Ctrl+B: reset game
                return "reset"
            elif key == 19:  # Ctrl+S: pause
                paused = True
            elif key == 26:  # Ctrl+Z: resume (continue)
                paused = False
            key = stdscr.getch()

        # If paused, display pause message and skip physics update.
        if paused:
            stdscr.addstr(sh//2, sw//2 - len("[PAUSED]   Ctrl+Z to continue")//2, "[PAUSED]   Ctrl+Z to continue")
            stdscr.refresh()
            time.sleep(0.1)
            continue

        # Apply gravity and update player.
        player['vy'] += 0.5
        player['x'] += player['vx']
        player['y'] += player['vy']

        # Platform collision.
        for plat in level["platforms"]:
            if (player['x'] + player['width'] > plat['x'] and
                player['x'] < plat['x'] + plat['w']):
                if (player['vy'] >= 0 and 
                    player['y'] + player['height'] >= plat['y'] and
                    player['y'] + player['height'] - player['vy'] <= plat['y']):
                    player['y'] = plat['y'] - player['height']
                    player['vy'] = 0
                    player['jumping'] = False

        # Out-of-screen fall.
        if player['y'] > sh:
            game_state["lives"] -= 1
            if game_state["lives"] <= 0:
                return "game_over"
            player['x'] = 5.0
            player['y'] = sh - 5
            player['vx'] = 0
            player['vy'] = 0
            player['jumping'] = False

        # Enemy collisions and stomping.
        for enemy in level["enemies"][:]:
            enemy['x'] += enemy['vx']
            if enemy['x'] < enemy['min_x'] or enemy['x'] + enemy['width'] > enemy['max_x']:
                enemy['vx'] *= -1
            collision = (player['x'] < enemy['x'] + enemy['width'] and
                         player['x'] + player['width'] > enemy['x'] and
                         player['y'] < enemy['y'] + enemy['height'] and
                         player['y'] + player['height'] > enemy['y'])
            if collision:
                if (player['vy'] > 0) and (prev_y + player['height'] <= enemy['y'] + 1):
                    try:
                        level["enemies"].remove(enemy)
                    except ValueError:
                        pass
                    player['vy'] = -3
                    if random.random() < 0.1:
                        bonus_hearts.append({
                            "x": enemy['x'],
                            "y": enemy['y'],
                            "vx": -0.2,
                            "symbol": "♡"
                        })
                else:
                    game_state["lives"] -= 1
                    if game_state["lives"] <= 0:
                        return "game_over"
                    player['x'] = 5.0
                    player['y'] = sh - 5
                    player['vx'] = 0
                    player['vy'] = 0
                    player['jumping'] = False

        # Hazard collisions: planes.
        for plane in level.get("planes", []):
            if collides(player, plane, a_w_key='width', b_w_key='w'):
                game_state["lives"] -= 1
                if game_state["lives"] <= 0:
                    return "game_over"
                player['x'] = 5.0
                player['y'] = sh - 5
                player['vx'] = 0
                player['vy'] = 0
                player['jumping'] = False

        # Hazard collisions: lava (any overlap is lethal).
        for lava in level.get("lava", []):
            if (player['x'] < lava['x'] + lava['w'] and
                player['x'] + player['width'] > lava['x'] and
                player['y'] < lava['y'] + lava['h'] and
                player['y'] + player['height'] > lava['y']):
                game_state["lives"] -= 1
                if game_state["lives"] <= 0:
                    return "game_over"
                player['x'] = 5.0
                player['y'] = sh - 5
                player['vx'] = 0
                player['vy'] = 0
                player['jumping'] = False

        # Bonus hearts movement.
        for heart in level["bonus_hearts"][:]:
            heart['x'] += heart['vx']
            if heart['x'] < 0 or heart['x'] > sw:
                level["bonus_hearts"].remove(heart)
            heart_box = {"x": heart['x'], "y": heart['y'], "width": 1, "height": 1}
            if collides(player, heart_box, a_w_key='width', b_w_key='width'):
                if game_state["lives"] < 3:
                    game_state["lives"] += 1
                level["bonus_hearts"].remove(heart)

        # Goal collision.
        goal = level["goal"]
        if (player['x'] < goal['x'] + goal['width'] and
            player['x'] + player['width'] > goal['x'] and
            player['y'] < goal['y'] + goal['height'] and
            player['y'] + player['height'] > goal['y']):
            stdscr.nodelay(False)
            stdscr.clear()
            try:
                stdscr.addstr(sh // 2, sw // 2 - 20, "You delivered the drinks! Press any key...")
            except curses.error:
                pass
            stdscr.refresh()
            stdscr.getch()
            stdscr.nodelay(True)
            return "complete"

        # ─── DRAWING ─────────────────────────────
        stdscr.clear()
        draw_hud(stdscr, game_state, sh, sw)
        for plat in level["platforms"]:
            for i in range(plat['w']):
                try:
                    stdscr.addch(plat['y'], plat['x'] + i, "█")
                except curses.error:
                    pass
        for enemy in level["enemies"]:
            symbol = "E"
            if enemy.get("type") == "slime":
                symbol = "S"
            elif enemy.get("type") == "flying":
                symbol = "F"
            try:
                stdscr.addstr(int(enemy['y']), int(enemy['x']), symbol)
            except curses.error:
                pass
        for plane in level.get("planes", []):
            for i in range(plane['w']):
                try:
                    stdscr.addch(plane['y'], plane['x'] + i, "X")
                except curses.error:
                    pass
        for lava in level.get("lava", []):
            for i in range(lava['w']):
                try:
                    stdscr.addch(lava['y'], lava['x'] + i, "~", curses.color_pair(1))
                except curses.error:
                    pass
        for heart in level["bonus_hearts"]:
            try:
                stdscr.addch(int(heart['y']), int(heart['x']), heart['symbol'])
            except curses.error:
                pass
        for i in range(goal['height']):
            try:
                stdscr.addstr(goal['y'] + i, goal['x'], "H" * goal['width'])
            except curses.error:
                pass
        for i in range(player['height']):
            try:
                stdscr.addstr(int(player['y']) + i, int(player['x']), "P" * player['width'])
            except curses.error:
                pass
        stdscr.refresh()
        player['vx'] = 0
        time.sleep(0.05)

# ─── SHOW LEVEL CODE (PRE-LEVEL PREVIEW) ─────────────
def show_level_code(stdscr, level):
    stdscr.clear()
    code_str = pprint.pformat(level)
    lines = code_str.splitlines()
    sh, sw = stdscr.getmaxyx()
    for i, line in enumerate(lines):
        if i >= sh - 2:
            break
        try:
            stdscr.addstr(i, 0, line[:sw])
        except curses.error:
            pass
    msg = "Ctrl+R: Run Level   |   Ctrl+B: Reset Game"
    try:
        stdscr.addstr(sh - 1, 0, msg[:sw])
    except curses.error:
        pass
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == 18:      # Ctrl+R
            return "run"
        elif key == 2:     # Ctrl+B
            return "reset"
        time.sleep(0.05)

# ─── MAIN GAME LOOP ─────────────────────────────────────────────
def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    try:
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    except:
        pass
    sh, sw = stdscr.getmaxyx()
    current_level = 1
    game_state = {"lives": 3, "speed_bonus": 0}
    while True:
        if current_level <= 10:
            level = load_handcrafted_level(current_level, sh, sw)
        else:
            level = generate_level(current_level, sh, sw)
        # Boss fight on every 10th level.
        if current_level % 10 == 0:
            bonus = boss_fight(stdscr)
            game_state["speed_bonus"] = bonus
        else:
            game_state["speed_bonus"] = 0
        action = show_level_code(stdscr, level)
        if action == "reset":
            current_level = 1
            game_state["lives"] = 3
            continue
        result = play_level(stdscr, level, current_level, game_state)
        if result == "reload":
            continue
        elif result == "reset":
            current_level = 1
            game_state["lives"] = 3
        elif result == "game_over":
            stdscr.nodelay(False)
            stdscr.clear()
            stdscr.addstr(sh // 2, sw // 2 - 10, "Game Over! Press any key...")
            stdscr.refresh()
            stdscr.getch()
            current_level = 1
            game_state["lives"] = 3
        elif result == "complete":
            current_level += 1

if __name__ == "__main__":
    curses.wrapper(main)
