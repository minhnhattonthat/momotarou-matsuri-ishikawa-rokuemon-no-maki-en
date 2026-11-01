-- Warp from a cold boot to a scene of tools/debug/scenes.txt (kinds: tools/debug/gen_scenes.py, RE: docs/re/debug.md).
--   emu.py CUE --out DIR --script tools/debug/warp.lua --var "SCENE='event20'" --frames 900
-- On arrival it logs "ARRIVED <scene> f<frame>", shoots <scene>.png, saves STATE_DIR/<scene>.sstate if STATE_DIR is
-- set, and quits HOLD frames later (default 60; set HOLD=-1 to keep running, e.g. with --mash to click through the
-- scene's text). --frames is ignored (emu.py wants one). No --debugger needed (no exec hooks).
local mem = PCSX.getMemPtr()
local function r8(a) return mem[a & 0x1FFFFF] end
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local function w16(a, v) a = a & 0x1FFFFF; mem[a] = v & 0xFF; mem[a + 1] = (v >> 8) & 0xFF end

local MODE, MAP, EVENT = 0x8008C490, 0x8008C570, 0x8008C4F9  -- docs/re/debug.md
local VM = 0x800BF7B8  -- script interpreter: +0 running script (0 = idle), +4 next op address, +0x44 current op

-- scene list ---------------------------------------------------------------------------------------------------
local path = SCENES or "../debug/scenes.txt"  -- emu.py runs PCSX-Redux in tools/pcsx
local f = assert(io.open(path, "r"), "scene list not found: " .. path .. " (pass --var \"SCENES=[[abs path]]\")")
local list = {}
for line in f:lines() do
  local w = {}
  for t in line:gsub("#.*", ""):gmatch("%S+") do w[#w + 1] = t end
  if #w >= 2 then list[w[1]] = w end
end
f:close()
local s = assert(list[assert(SCENE, "set --var \"SCENE='name'\"")], "unknown scene: " .. tostring(SCENE))
local kind, num = s[2], tonumber
FRAMES = 1e9  -- the run ends HOLD frames after arrival, not at --frames

local presses = {}  -- main-menu presses for this kind
if kind == "menu" then
  for p in s[4]:gmatch("[^,]+") do if p ~= "-" then presses[#presses + 1] = p end end
elseif kind == "game" then presses = { "c", "c" }  -- 初めて, then おためし対戦
else presses = { "c", "r", "c" } end            -- event, map: 初めて, いざ！物語へ
local KEY = { c = "circle", r = "right" }

local st = { mode = -1, since = 0, pressed = 0 }
local function arrive(n)
  L.log(string.format("ARRIVED %s f%d", s[1], n))
  L.shot(s[1] .. ".png")
  if STATE_DIR then L.save_state(STATE_DIR .. "/" .. s[1] .. ".sstate") end
  st.arrived = n
end

L.on_frame(function(n)
  local m = r8(MODE)
  if m ~= st.mode then st.mode, st.since = m, n; L.log(string.format("f%d mode %02X", n, m)) end
  local age = n - st.since

  if st.arrived then
    local hold = HOLD or 60
    if hold >= 0 and n - st.arrived >= hold then L.shot("final.png"); L.finish(0) end
    -- Save confirmation defaults to No. Opt in only with a disposable --sav card copy.
    if kind == "save" and SAVE_CONFIRM then
      local t = n - st.arrived
      if t == 1500 or t == 1920 then L.press("circle", 6) end
      if t == 1800 then L.press("up", 6) end
    end
    -- CLICK=N: press circle every N frames after arrival, to click through the scene's text (emu.py's --mash
    -- starts at frame 0 and breaks the menu presses above; MASH is the driver's own global)
    if CLICK and (n - st.arrived) % CLICK == CLICK - 1 then L.press("circle", 6) end
    return
  end

  -- title: Start until the main menu (it takes Start only from ~frame 2400)
  if m == 0x46 and age > 1000 and age % 60 == 0 then L.press("start", 6) end
  -- main menu: the scene's presses, the first once the menu takes input (~500 frames), the submenu ~400 later
  -- (60 was too soon), then one every 60; the last one again every 200 while the menu stays up
  if m == 0x49 then
    local due = 520 + (st.pressed >= 1 and 400 or 0) + 60 * math.max(0, st.pressed - 1)
    if st.pressed < #presses and age >= due then
      st.pressed = st.pressed + 1
      L.press(KEY[presses[st.pressed]], 6)
      st.last_press = n
    elseif st.pressed == #presses and #presses > 0 and (kind ~= "menu" or num(s[3]) ~= 0x49)
        and age >= due + 200 and (age - due) % 200 == 0 then
      L.press(KEY[presses[#presses]], 6)
    end
  end

  if kind == "menu" then
    if m == num(s[3]) and st.pressed == #presses and age >= 300 and n - (st.last_press or 0) >= 200 then
      arrive(n)
    end
  elseif kind == "cards" then
    -- Card Album is mode 0x4C. Set only the 100 collectible flags (not the
    -- adjacent story bits); the game's normal loader and renderer do the rest.
    if m == 0x4D and age == 0 then
      for i = 0, 11 do mem[0xBD9F8 + i] = 255 end
      mem[0xBDA04] = mem[0xBDA04] | 15
      mem[MODE & 0x1FFFFF] = 0x4C
    end
    if m == 0x4C and age >= 600 then arrive(n) end
  elseif kind == "game" then
    if m == 0x50 and age >= 200 and age % 120 == 0 then L.press("circle", 6) end
    if st.prev == 0x50 and m ~= 0x50 then mem[MODE & 0x1FFFFF] = num(s[3]); L.log("mode -> " .. s[3]) end
    if m == num(s[3]) and age >= 600 then arrive(n) end
  elseif kind == "event" then
    if m == 0x4D and age == 0 then mem[EVENT & 0x1FFFFF] = num(s[3]) end
    if m == 0x4D and age >= 300 then arrive(n) end  -- event 13 ends before 600
  elseif kind == "map" or kind == "save" then
    if m == 0x4D and age == 0 then mem[MODE & 0x1FFFFF] = 1 end  -- skip the intro; GMAIN starts the opening script
    -- the opening script's next op is its first message (while a message is up, +4 walks the text instead): write
    -- "0x1D map x y dir 0xFFFE; 0x1E 0x63" (change map, then the op every exit script ends with) over the next ops,
    -- close the message, put the words back once they ran. (Hijacking a later map's entry script the same way, for
    -- a two-hop warp, never loaded the second map.)
    if m == 1 and not st.hijack and r32(VM) ~= 0 and r16(VM + 0x44) ~= 2 and r16(r32(VM + 4)) == 2 then
      local p = r32(VM + 4)
      -- OPS = {u16, ...}: script ops to run first (e.g. an op 26 caption: tools/debug/caption_ops.py)
      local words = {}
      for _, v in ipairs(OPS or {}) do words[#words + 1] = v end
      local tail = kind == "save" and { 0x2D, 0x6A, 3, 0, 0, 0x2E, 3, 0, 0 }
          or { 0x1D, num(s[3]), num(s[4]), num(s[5]), num(s[6]), 0xFFFE, 0x1E, 0x63 }
      for _, v in ipairs(tail) do
        words[#words + 1] = v
      end
      st.orig = {}
      for i, v in ipairs(words) do st.orig[i] = r16(p + (i - 1) * 2); w16(p + (i - 1) * 2, v) end
      st.hijack, st.at, st.words = n, p, words
      L.log(string.format("hijack at %08X -> map %s", p, s[3]))
    end
    if st.hijack and st.orig then
      local pc = r32(VM + 4)
      if r32(VM) == 0 or pc < st.at or pc > st.at + #st.words * 2 - 4 then  -- all ops ran
        -- only if our words are still there: the new map's scripts may already sit in the same buffer
        local ours = true
        for i, v in ipairs(st.words) do if r16(st.at + (i - 1) * 2) ~= v then ours = false end end
        if ours then for i, v in ipairs(st.orig) do w16(st.at + (i - 1) * 2, v) end end
        L.log(string.format("f%d restore %s", n, ours and "done" or "skipped (buffer reloaded)"))
        st.orig = nil
      end
      if st.orig and m == 1 and (n - st.hijack) % 30 == 0 then L.press("circle", 6) end  -- close the message
    end
    if kind == "save" and m == 0x4B and age >= 600 then arrive(n) end
    if kind == "map" and st.hijack and not st.orig and r16(MAP) == num(s[3]) and m == 1
        and n - st.hijack >= 300 then arrive(n) end
    if m == 1 and not st.hijack and age > 3000 then L.fail("no message op to hijack") end
    if st.hijack and n - st.hijack > 3000 then L.fail("map " .. s[3] .. " never loaded") end
  end
  st.prev = m
end)
