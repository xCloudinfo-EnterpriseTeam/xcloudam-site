# -*- coding: utf-8 -*-
"""官網用圖的真本。產出 assets/arch.svg（微軟風架構圖）與 assets/flow-*.svg（技術論文式流程圖）。
用法：python3 tools/build_diagrams.py   （在專案根目錄執行）"""
import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
sys.path.insert(0, os.path.expanduser("~/.claude/skills/ms-arch-diagram"))
from msarch import *  # noqa: F401,F403


# ── 架構圖：管理介面 → 搭配系統 → MIC-743-AT 地端主機 → 現場資料；右側企業防火牆
def arch():
    d = Canvas(1600, 690)
    X, R, L = 40, 1440, 178
    y = 20
    d.band(X, y, R - X, 56, BLUE, TINT_BLUE)
    for i, (ic, c) in enumerate([("Management console", BLUE), ("Settings", TEAL), ("Health monitoring", GOLD)]):
        d.icon(ic, X + 16 + i * 46, y + 10, 36, c)
    d.t((X + R) / 2 + 60, y + 35, "網頁管理後台：帳號與權限、系統設定、稽核紀錄", 18, INK, 700, "middle")
    d.num(R - 36, y + 28, 5)

    y = 92
    d.band(X, y, R - X, 150)
    d.side_label(X + 82, y + 16, "搭配系統", "云碩科技自研", icon="Application server", icon_color=PURPLE, icon_size=56)
    tw = 199
    for k, (lab, ic, col) in enumerate([("x360 數位孿生", "Server farm", PURPLE), ("xESG 碳盤查", "Graph", GREEN),
                                         ("xMeetAI 會議記錄", "Audio", TEAL), ("工程師小助手", "Generic code", RED),
                                         ("知識庫問答", "Document", BLUE), ("儀表板與報表", "Performance monitor", ORANGE)]):
        d.tile(L + k * (tw + 10), y + 23, tw, 104, lab, ic, col)
    d.num(R - 2, y + 2, 4)

    y = 258
    d.band(X, y, R - X, 214, BLUE, "#FFFFFF")
    d.side_label(X + 68, y + 26, "MIC-743-AT", "Jetson T5000", icon="Server rack", icon_size=56)
    d.card(L, y + 16, 400, 96, "Strata 大模型推論", "OpenAI 相容 API、2070 TFLOPS", "Virtual machine", PURPLE)
    d.card(L + 410, y + 16, 400, 96, "RAG 檢索引擎", "向量檢索、重排序、附出處", "Connectors", ORANGE)
    d.card(L + 820, y + 16, 426, 96, "向量資料庫", "企業知識語意索引", "Database server", BLUE)
    d.box(L, y + 124, 1246, 76, TEAL, TINT_TEAL2)
    for k, (a, ic) in enumerate([("JetPack 7.0", "Settings"), ("Docker 容器", "Server (generic)"),
                                 ("HTTPS 加密連線", "Certificate"), ("資料不出內網", "Lock, protected")]):
        bx = L + 14 + k * 306
        d.box(bx, y + 136, 298, 52, TEAL, "#FFFFFF", 1.2)
        d.icon(ic, bx + 12, y + 144, 36, TEAL)
        d.t(bx + 58, y + 169, a, 17, INK, 700)
    d.num(X + 68, y + 186, 3)

    fx, yb = 1458, 300
    d.t(fx + 62, 44, "企業使用者", 16, GREEN, 700, "middle")
    d.line(f"M{fx+62} 56 V {yb-4}")
    d.boundary(fx, yb, 124, 150, "企業防火牆", "內網邊界")
    d.num(fx, yb, 2)
    d.line(f"M{fx} {yb+75} H {R+6}")

    y = 512
    d.band(X, y, R - X, 104, DATA_LINE, "#FFFFFF")
    d.side_label(X + 82, y + 44, "現場資料", None, color=PURPLE)
    d.t(X + 82, y + 72, "唯讀匯入", 16, PURPLE, 600, "middle")
    sw = 250
    for k, (a, ic, col) in enumerate([("設備與感測器", "Performance monitor", ORANGE), ("會議錄音", "Audio", GREEN),
                                      ("ERP 與單據", "Table", BLUE), ("企業文件 SOP", "Document", PURPLE)]):
        bx = L + k * (sw + 70)
        d.card(bx, y + 15, sw, 74, a, None, ic, col, DATA_LINE2, TINT_PURPLE)
        d.line(f"M{bx + sw / 2} {y-2} V {258+214+6}", DATA_LINE, "ap", 2.2)
    d.t(L + sw / 2 + 46, y - 14, "唯讀匯入，不回寫現場", 16, PURPLE, 700)
    d.num(L + sw / 2 + 24, y - 20, 1)

    d.legend(["1 現場資料唯讀匯入", "2 使用者經企業防火牆進入", "3 推論與檢索都在 MIC-743-AT 上",
              "4 各系統共用同一台設備", "5 管理者網頁操作並留痕"], y=660)
    d.save(os.path.join(OUT, "arch"))


# ── 流程圖：技術論文式，四段由左到右，每段一個色相
HUES = [("#2563eb", "#eff6ff"), ("#059669", "#ecfdf5"), ("#7c3aed", "#f5f3ff"), ("#ea580c", "#fff7ed")]
SHOW_LEGEND = False   # 段名已編號上色，圖例與段名重複
FONT2 = "Microsoft JhengHei, PingFang TC, Noto Sans TC, sans-serif"


def flow(name, label, steps, pills, legend):
    W, H, SW, GAP = 1400, 284, 293, 60
    p, defs = [], []
    for i, (hue, tint) in enumerate(HUES):
        defs.append(f'<marker id="m{i}" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">'
                    f'<path d="M0 0 L10 5 L0 10 Z" fill="{hue}"/></marker>')
    for i, (title, sub, lines, chips) in enumerate(steps):
        hue, tint = HUES[i]
        x = 24 + i * (SW + GAP)
        p.append(f'<rect x="{x}" y="14" width="{SW}" height="254" rx="18" fill="{tint}"/>')
        p.append(f'<circle cx="{x+32}" cy="52" r="18" fill="{hue}"/>')
        p.append(f'<text x="{x+32}" y="59" font-size="19" font-weight="700" fill="#fff" text-anchor="middle">{i+1}</text>')
        p.append(f'<text x="{x+62}" y="62" font-size="27" font-weight="700" fill="#16202a">{title}</text>')
        p.append(f'<text x="{x+20}" y="98" font-size="17" font-style="italic" fill="#3d4b56">{sub}</text>')
        cx, cy, cw, ch = x + 16, 114, SW - 32, 96
        defs.append(f'<clipPath id="c{i}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12"/></clipPath>')
        p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="#fff"/>')
        p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="8" fill="{hue}" clip-path="url(#c{i})"/>')
        p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="none" stroke="{hue}" stroke-width="2.4"/>')
        for k, ln in enumerate(lines):
            p.append(f'<text x="{cx+16}" y="{cy+46+k*28}" font-size="16" fill="#3d4b56">{ln}</text>')
        chx = x + 16
        for c in chips:
            cwid = 26 + sum(15 if ord(ch_) > 255 else 9 for ch_ in c)
            p.append(f'<rect x="{chx}" y="226" width="{cwid}" height="30" rx="15" fill="{hue}"/>')
            p.append(f'<text x="{chx+cwid/2}" y="246" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">{c}</text>')
            chx += cwid + 8
        if i < 3:
            ax = x + SW
            p.append(f'<path d="M{ax+4} 162 H{ax+GAP-6}" stroke="{hue}" stroke-width="2.6" fill="none" marker-end="url(#m{i})"/>')
            pw = 26 + 15 * len(pills[i])
            p.append(f'<rect x="{ax+GAP/2-pw/2}" y="122" width="{pw}" height="26" rx="13" fill="{hue}"/>')
            p.append(f'<text x="{ax+GAP/2}" y="140" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">{pills[i]}</text>')
    lx = 24
    for i, s in enumerate(legend if SHOW_LEGEND else []):
        p.append(f'<rect x="{lx}" y="292" width="16" height="16" rx="4" fill="{HUES[i][0]}"/>')
        p.append(f'<text x="{lx+24}" y="306" font-size="15" fill="#3d4b56">{s}</text>')
        lx += 24 + 15 * len(s) + 32
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT2}" role="img" aria-label="{label}"><defs>{"".join(defs)}</defs>'
           f'<rect width="{W}" height="{H}" fill="#fff"/>{"".join(p)}</svg>')
    path = os.path.join(OUT, f"flow-{name}")
    open(path + ".svg", "w", encoding="utf-8").write(svg)
    subprocess.run(["rsvg-convert", "-z", "1", path + ".svg", "-o", path + ".png"], check=True)


flow("x360", "x360 現場到工單流程圖", [
    ("資料接入", "工控與物聯網來源", ["Modbus TCP・OPC UA", "MQTT・HTTP 輪詢"], ["5 種來源"]),
    ("數位孿生", "把現場搬進畫面", ["全景巡檢點・3D 機房", "感測值疊在設備旁"], ["全景", "3D"]),
    ("告警判斷", "超過門檻即通知", ["每顆感測器可設上下限", "觸發即通知負責人"], ["即時"]),
    ("工單留痕", "從告警到結案", ["告警直接開工單", "回報到結案全程可查"], ["稽核留痕"])],
    ["匯入", "監看", "派工"], ["資料接入", "現場呈現", "告警判斷", "處理留痕"])
flow("esg", "xESG 碳盤查到報告流程圖", [
    ("資料蒐集", "盤查來源一次到位", ["ERP・電錶・燃料單據", "API 自動匯入"], ["自動匯入"]),
    ("碳排計算", "內建排放係數庫", ["範疇 1／2／3 自動計算", "係數自動帶入"], ["範疇 1/2/3"]),
    ("合規試算", "對齊國際規範", ["ISO 14064-1 盤查", "CBAM 碳關稅試算"], ["ISO 14064-1", "CBAM"]),
    ("報告產出", "一鍵產出", ["GRI・TCFD・ISSB", "供應鏈碳管理報表"], ["GRI", "TCFD"])],
    ["計算", "試算", "產出"], ["資料蒐集", "自動運算", "合規試算", "報告產出"])
flow("meet", "xMeetAI 會議到行動清單流程圖", [
    ("會議進行", "線上實體都能收", ["Teams 線上會議", "實體會議室錄音"], ["Teams", "Outlook"]),
    ("語音辨識", "聽得懂在地語言", ["自動轉錄・說話者分離", "台語／客語支援"], ["98.2% 準確率"]),
    ("AI 摘要", "雙輪摘要", ["重點與決議自動整理", "7 種會議模式"], ["7 種模式"]),
    ("產出分發", "會後直接行動", ["逐字稿・摘要・行動清單", "回寫 Teams／Outlook"], ["行動清單"])],
    ["轉錄", "摘要", "分發"], ["會議來源", "語音處理", "AI 摘要", "產出分發"])
arch()
