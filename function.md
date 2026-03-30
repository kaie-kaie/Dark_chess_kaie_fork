# python 函式

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

init_game() 初始化棋盤，遊戲開始時呼叫一次即可洗牌並重製棋盤顯示的內容

get_current_turn() 取得當前回合玩家，為"A"或"B"，遊戲開始時會隨機為其中一個，進行client_action執行成功後會自動切換

client_action(name, x1, y1, x2=-1, y2=-1) 傳入玩家名("A"或"B")和1~2組座標 1組時為翻牌 2組時為移動/吃 將回傳此行動是否合法，會直接更改checkerboard_display，第一次翻牌時會自動決定玩家顏色

getColor(name) 得到某玩家顏色

get_checkboard() 得到目前棋盤顯示

check_game_over()檢查遊戲是否結束與結果
# 回傳值: "Playing" (遊戲繼續), "Draw" (平手), 或 "{玩家名} Win" (某玩家獲勝)

