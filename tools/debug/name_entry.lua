-- Cold Name Entry QA. warp.lua supplies the real loader; all character selection,
-- editing, confirmation and return use the controller. No display/RAM substitutions.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local function tap(key) L.press(key, 6); L.press('-', 24) end
local phase, target, ready, step, captured = 'glyphs', 0, nil, 0, false
local started
local return_at
if NAME_QUICK then phase, step = 'enter', 1 end
local ids = {0, 51, 61, 66} -- Az9! in the English font; same IDs on original.
if NAME_SHORT then phase, step, ids = 'enter', 1, {25} end -- Z, then Start.
local name_record
local function slots()
  local a = {}
  for i = 0, 3 do a[#a + 1] = r16(0xE2E3E + i * 28) end
  return table.concat(a, ',')
end
local function select(id)
  local active = r32(0xE30D8)
  assert(active < 4, 'invalid active name slot')
  local a = 0xE2E38 + active * 28
  local col, row = r16(a + 16), r16(a + 18)
  local wantcol, wantrow
  for y = 0, 18 do
    for x = 0, 9 do
      if r32(0xE0D6C + (y * 10 + x) * 4) == id then wantcol, wantrow = x, y end
    end
  end
  assert(wantcol, 'ID absent from native selection table')
  if col ~= wantcol then
    if row > 0 then tap('up') else tap(col < wantcol and 'right' or 'left') end
  elseif row ~= wantrow then tap(row < wantrow and 'down' or 'up')
  else
    assert(r16(a + 6) == id, 'selection does not match rendered sprite ID')
    return true
  end
end
L.on_frame(function(n)
  if n > 60000 then L.fail('Name Entry tour timed out in ' .. phase); return end
  local mode = mem[0x8C490]
  if NAME_TRACE and n % 120 == 0 and mode == 0x51 then
    L.log(string.format('NAME_TRACE f%d phase=%s state=%d slot=%d op=%d result=%d',
      n, phase, r16(0xE2D78), r32(0xE30D8), r16(0xBF7FC), r32(0xBF818)))
  end
  if NAME_TRACE and NAME_QUICK and n == 10000 then
    L.shot('trace_final.png'); L.finish(1); return
  end
  if phase == 'return' then
    return_at = return_at or n
    if n - return_at == 1200 and mode == 0x51 then
      L.shot('return_stuck.png')
      L.log('NAME_STUCK state=' .. r16(0xE2D78) .. ' result=' .. r32(0xBF818))
      L.finish(1); return
    end
  end
  if mode == 0x51 and r16(0xE2D78) == 1 then
    ready = ready or n
    if n - ready < 600 or not L.route_done() then return end
    if not started then tap('right'); started = true; return end
    if phase == 'glyphs' then
      if select(target) then
        local blink = r32(0xE2E50)
        if blink < 3 or blink > 30 then return end
        L.shot(string.format('glyph_%02d.png', target))
        L.log(string.format('NAME_GLYPH %d f%d', target, n))
        target = target + 1
        if target == 80 then phase, step = 'enter', 1 end
      end
    elseif phase == 'enter' then
      step = r32(0xE30D8) + 1
      if step > #ids then tap('start'); return end
      if select(ids[step]) then
        L.log(string.format('NAME_SLOT %d id=%d', step, ids[step]))
        L.shot(string.format('slot_%d.png', step))
        tap('circle')
      end
    elseif phase == 'declined' then
      L.log('NAME_DECLINED slots=' .. slots())
      L.shot('declined.png')
      -- Cross moves back from the fourth slot; return to it with Circle.
      tap('cross'); phase = 'back'
    elseif phase == 'back' then
      assert(r32(0xE30D8) == 2, 'Cross did not return to the third slot')
      L.log('NAME_BACK slots=' .. slots()); L.shot('back.png')
      tap('circle'); phase = 'restore'
    elseif phase == 'restore' then
      assert(r32(0xE30D8) == 3)
      if select(ids[4]) then tap('circle') end
    end
  elseif mode == 0x51 and r16(0xE2D78) == 2 and L.route_done() then
    if phase == 'enter' then phase = NAME_SHORT and 'accept' or 'confirm' end
    if phase == 'restore' then phase = 'accept' end
    if phase == 'confirm' or phase == 'accept' then
      if not captured then L.press('-', 360); captured = true; return end
      L.shot(phase .. '.png'); L.log('NAME_PROMPT ' .. phase .. ' slots=' .. slots())
      -- The native yes/no prompt defaults to Yes. First reject, then accept.
      if phase == 'confirm' then L.press('down', 6); L.press('-', 90) end
      L.press('circle', 6); L.press('-', 90)
      phase = phase == 'confirm' and 'declined' or 'return'
      captured = false
      name_record = r32(0x8C564)
    elseif (phase == 'declined' or phase == 'return') and r16(0xBF7FC) == 4 then
      -- A short edge can be lost at the script/choice boundary. Keep the
      -- selected option and retry Circle until the game's state changes.
      L.log('NAME_RETRY ' .. phase)
      L.press('circle', 6); L.press('-', 90)
    end
  elseif mode == 0x50 and phase == 'return' then
    if not captured then ready, captured = n, true end
    if n - ready >= 900 then
      local address = 0xBDBFC + name_record * 28
      for i = 0, #ids - 1 do assert(mem[address + i] == ids[i + 1], 'saved name differs') end
      for i = #ids, 7 do assert(mem[address + i] == 255, 'name padding differs') end
      L.shot('record_name.png')
      L.log('NAME_RETURN record=' .. name_record .. ' ids=' .. table.concat(ids, ',') .. ' mode=' .. mode)
      if NAME_CONTINUE then
        NAME_COMPLETE = true
        phase = 'done'
      else
        L.finish(0)
      end
    end
  end
end)
