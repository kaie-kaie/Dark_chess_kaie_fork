#象棋的代表字串:

#未翻開:Covered

#空地:Null

#將/帥:King

#士/仕:Guard

#相/象:Elephant

#俥/車:Car

#傌/馬:Horse

#炮/砲:Cannon

#兵/卒:Soldier

#陣營:Red_與Black_的前墜

#例如帥:Red_King

#Covered沒有陣營前墜

import random

# 全域變數
piece_pool = []  # 存放還沒被翻開的棋子
color_table = dict()  # 存放玩家對應的顏色 ("Red" 或 "Black")
move_count_since_action = 0  # 用於判斷 50 步和局
current_turn = None # 記錄當前回合玩家 ("A" 或 "B")

# 定義棋子階級 (數值越大越高)
RANK = {
    'King': 7, 'Guard': 6, 'Elephant': 5, 'Car': 4, 
    'Horse': 3, 'Cannon': 2, 'Soldier': 1
}

checkerboard_display = []

#初始化 遊戲開始時呼叫
def init_game():
    global piece_pool, checkerboard_display, move_count_since_action, color_table, current_turn
    
    # 1. 重置全域狀態
    color_table = dict()
    move_count_since_action = 0
    
    # 新增：隨機決定一開始是誰的回合
    current_turn = random.choice(["A", "B"])
    
    # 2. 初始化 4*8 全為 'Covered' 的棋盤
    checkerboard_display = [['Covered'] * 8 for _ in range(4)]
    
    # 3. 建立 32 顆棋子的牌池
    piece_pool = [
        'Red_King', 
        'Red_Guard', 'Red_Guard',
        'Red_Elephant', 'Red_Elephant',
        'Red_Car', 'Red_Car',
        'Red_Horse', 'Red_Horse',
        'Red_Cannon', 'Red_Cannon',
        'Red_Soldier', 'Red_Soldier', 'Red_Soldier', 'Red_Soldier', 'Red_Soldier',
        'Black_King', 
        'Black_Guard', 'Black_Guard',
        'Black_Elephant', 'Black_Elephant',
        'Black_Car', 'Black_Car',
        'Black_Horse', 'Black_Horse',
        'Black_Cannon', 'Black_Cannon',
        'Black_Soldier', 'Black_Soldier', 'Black_Soldier', 'Black_Soldier', 'Black_Soldier'
    ]
    
    # 4. 洗牌
    random.shuffle(piece_pool)

#取得當前回合玩家
def get_current_turn():
    return current_turn

def draw_piece_from_pool():
    global piece_pool
    if len(piece_pool) > 0:
        return piece_pool.pop()
    return None

#傳入玩家名(A或B)和1~2組座標 1組時為翻牌 2組時為移動/吃 將回傳此行動是否合法
def client_action(name, x1, y1, x2=-1, y2=-1):
    global move_count_since_action, current_turn
    
    valid, message = isValid(name, x1, y1, x2, y2)
    
    if valid:
        if x2 == -1:
            # 1. 抽牌
            piece = draw_piece_from_pool()
            
            # 2. 👉 統一在這裡明確地更新棋盤
            checkerboard_display[x1][y1] = piece
            
            if not color_table:
                p_color = piece.split('_')[0]
                other_name = "B" if name == "A" else "A"
                setColor(name, p_color)
                setColor(other_name, "Black" if p_color == "Red" else "Red")
            
            move_count_since_action = 0 
        else:
            target = checkerboard_display[x2][y2]
            if target != 'Null':
                move_count_since_action = 0
            else:
                move_count_since_action += 1
            
            checkerboard_display[x2][y2] = checkerboard_display[x1][y1]
            checkerboard_display[x1][y1] = 'Null'
        
        current_turn = "B" if current_turn == "A" else "A"
            
        return True
    return False

def isValid(name, x1, y1, x2, y2):
    # 0. 檢查回合：是不是輪到該玩家
    if name != current_turn:
        return False, "Not your turn"

    # 1. 基本邊界檢查
    if not (0 <= x1 < 4 and 0 <= y1 < 8): return False, "Out of bounds"
    if x2 != -1 and not (0 <= x2 < 4 and 0 <= y2 < 8): return False, "Out of bounds"
    
    piece = checkerboard_display[x1][y1]
    
    # --- 翻牌邏輯 ---
    if x2 == -1:
        return (piece == 'Covered'), "Can only flip covered pieces"

    # --- 移動/吃子邏輯 ---
    if piece == 'Covered' or piece == 'Null': return False, "Invalid source"
    
    # 檢查是否為該玩家的棋子 (包含防呆：顏色是否已決定)
    p_color = getColor(name)
    if not p_color or not piece.startswith(p_color): 
        return False, "Not your piece or color not set"
    
    target = checkerboard_display[x2][y2]
    if target.startswith(p_color): return False, "Cannot eat your own piece"
    
    dist = abs(x1 - x2) + abs(y1 - y2)
    
    # 2. 處理「砲」的特殊規則
    if "Cannon" in piece:
        if target == 'Null':
            return (dist == 1), "Cannon moves 1 step if not eating"
        else:
            # 吃子：必須同一直線且中間隔一個棋子
            if x1 == x2: # 水平
                count = sum(1 for y in range(min(y1, y2) + 1, max(y1, y2)) if checkerboard_display[x1][y] != 'Null')
                return (count == 1), "Cannon needs 1 piece to jump over"
            elif y1 == y2: # 垂直
                count = sum(1 for x in range(min(x1, x2) + 1, max(x1, x2)) if checkerboard_display[x][y1] != 'Null')
                return (count == 1), "Cannon needs 1 piece to jump over"
            return False, "Cannon must be in line"

    # 3. 一般棋子移動與吃子
    if dist != 1: return False, "Must move 1 step"
    if target == 'Null': return True, "Safe move"
    if target == 'Covered': return False, "Cannot eat covered piece"
    
    # 階級判斷
    p1_type = piece.split('_')[1]
    p2_type = target.split('_')[1]
    
    # 特殊規則：兵吃帥，帥不吃兵
    if p1_type == 'Soldier' and p2_type == 'King': return True, "Soldier eats King"
    if p1_type == 'King' and p2_type == 'Soldier': return False, "King cannot eat Soldier"
    
    # 一般階級比較
    return (RANK[p1_type] >= RANK[p2_type]), "Rank too low"

#得到某玩家顏色
def getColor(name):
    return color_table.get(name, None)

#設定某玩家顏色
def setColor(name, color):
    color_table[name] = color

#得到棋盤顯示
def get_checkboard():
    return checkerboard_display

def get_player_by_color(color):
    for name, c in color_table.items():
        if c == color:
            return name
    return None

# 檢查遊戲是否結束與結果
# 回傳值: "Playing" (遊戲繼續), "Draw" (平手), 或 "{玩家名} Win" (某玩家獲勝)
def check_game_over():
    # 1. 檢查是否達成 50 步和局條件
    if move_count_since_action >= 50:
        return "Draw"
        
    # 2. 如果雙方陣營連決定都還沒決定，遊戲一定還在進行
    if not color_table:
        return "Playing"

    # 3. 如果還有未翻開的棋子 (Covered)，那就不能判定某一方全滅
    # 因為未翻開的棋子可能就是場上處於劣勢那方的棋子
    if len(piece_pool) > 0:
        return "Playing"

    # 4. 若場上已經沒有未翻開的棋子，統計雙方剩下的棋子數量
    red_count = 0
    black_count = 0
    
    for row in checkerboard_display:
        for piece in row:
            if piece.startswith('Red_'):
                red_count += 1
            elif piece.startswith('Black_'):
                black_count += 1

    # 5. 判斷勝負
    if red_count == 0 and black_count > 0:
        winner = get_player_by_color("Black")
        return f"{winner} Win"
    elif black_count == 0 and red_count > 0:
        winner = get_player_by_color("Red")
        return f"{winner} Win"
    elif red_count == 0 and black_count == 0:
        # 極端罕見情況：同歸於盡 (實體暗棋通常不會發生，但寫程式防呆一下)
        return "Draw"
        
    return "Playing"

# 判斷和局
def is_draw():
    return move_count_since_action >= 50