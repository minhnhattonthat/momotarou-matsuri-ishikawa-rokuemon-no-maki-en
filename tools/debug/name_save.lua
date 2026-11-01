-- Continue name_entry.lua through Quick Match's save/overwrite flow, or
-- cold-load its game-written card with status_saved.txt and check the name.
-- All interaction after Name Entry's loader warp is ordinary controller input.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local function tap(key, delay) L.press(key, 6); L.press('-', delay or 180) end
local phase, last, since = 'wait', '', 0
local seen_save, loaded, returned
local expected = NAME_SHORT and {25, 255, 255, 255, 255, 255, 255, 255}
  or {0, 51, 61, 66, 255, 255, 255, 255}
local function verify()
  for i, value in ipairs(expected) do
    assert(mem[0xBDBFC + i - 1] == value, 'cold-loaded record name differs at byte ' .. i)
  end
end
FRAMES = 80000
L.on_frame(function(n)
  if n > 60000 then L.fail('name save/reload timed out in ' .. phase); return end
  local mode = mem[0x8C490]
  if NAME_RELOAD then
    if mode == 0x4A then loaded = true end
    if loaded and mode == 0x49 and phase == 'wait' then
      verify(); L.log('NAME_RELOADED bytes=' .. table.concat(expected, ',')); phase = 'loaded'
    end
    if phase == 'loaded' and mode == 0x49 and L.route_done() then
      -- A Quick Match-only file has no Story/Status progress. The shared
      -- route leaves the cursor on disabled Status after loading; use the
      -- enabled Quick Match item directly instead of requiring Status.
      verify(); L.shot('loaded_menu.png')
      tap('left', 90); tap('up', 90); tap('circle', 900)
      phase = 'record'
    elseif phase == 'record' and mode == 0x50 and r16(0xE2ABC) == 1 and L.route_done() then
      verify(); assert(r32(0x8C5B8) == 0, 'wrong Quick Match page')
      L.shot('reloaded_name.png'); L.log('NAME_PERSISTENCE_OK'); L.finish(0)
    end
    return
  end
  if not NAME_COMPLETE then return end
  if phase == 'wait' then
    verify(); tap('cross', 600); phase = 'exit'; return
  end
  if not L.route_done() then return end
  if phase == 'exit' and mode == 0x50 and r16(0xBF7FC) == 4 then
    L.shot('save_prompt.png'); L.log('NAME_SAVE_PROMPT')
    tap('up', 90); tap('circle', 900); phase = 'saving'
  end
  if phase == 'saving' and mode == 0x50 and r16(0xBF7FC) == 2 then
    L.shot('save_advice.png'); tap('circle', 300)
  end
  if mode == 0x4B then
    seen_save = true
    local state = r32(0xE1F30)
    local key = mode .. ':' .. state
    if key ~= last then last, since = key, n; L.log('NAME_SAVE_STATE ' .. state .. ' f' .. n) end
    if n - since < 240 then return end
    if state == 2 then
      L.shot('save_slot.png'); tap('circle', 300)
    elseif state == 3 then
      L.shot('use_file.png')
      if r32(0xE1F28) == 1 then tap('up', 90) end
      tap('circle', 300)
    elseif state == 4 and phase ~= 'overwrite' then
      L.shot('overwrite.png'); L.log('NAME_OVERWRITE')
      tap('up', 90); tap('circle', 900); phase = 'overwrite'
    elseif state == 6 then
      L.shot('save_complete.png'); L.log('NAME_SAVE_COMPLETE')
      tap('circle', 900)
    end
  elseif seen_save and mode == 0x49 then
    returned = returned or n
    if n - returned >= 600 then
      L.shot('saved_return.png'); L.log('NAME_SAVED_RETURN'); L.finish(0)
    end
  end
end)
