-- Cold-boot Mask Maker controls. Pair with warp.lua, SCENE='mask_editor', HOLD=-1.
-- Controller input only. The default observes selected parts and the command
-- cursor before advancing; fixed taps can be lost while the palette scrolls.
-- MASK_ACTIONS supplies a fixed sequence for incomplete-mask/cancel branches.
local mem = PCSX.getMemPtr()
local entered
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local selected, next_input, confirming, move_row, accepted = 0, 0, nil, false, nil
L.on_frame(function(n)
  if not entered then
    if mem[0x8C490] ~= 0x3A then return end
    entered = n
  end
  local age = n - entered - 900
  if age < 0 then return end
  if n - entered > 12000 then L.fail('mask controls did not reach confirmation'); return end
  if not MASK_ACTIONS then
    if accepted then
      if n - accepted == 600 then
        assert(mem[0x8C490] == 1, 'completed mask did not return to Story')
        L.shot('mask_return.png')
        L.log('MASK accepted; returned to Story')
        L.finish(0)
      end
      return
    end
    assert(mem[0x8C490] == 0x3A, 'left Mask Maker before confirmation')
    if confirming then
      if n - confirming == 240 then
        assert(r16(0xCE858) == 2, 'mask confirmation script is not active')
        L.shot('mask_confirm.png')
        L.log('MASK six parts selected; confirmation reached')
        if MASK_ACCEPT then L.press('circle', 6); accepted = n
        else L.finish(0) end
      end
      return
    end
    if n < next_input or r16(0xCE858) ~= 1 then return end
    next_input = n + 120
    local commands = r32(0xCE7C8) == 1
    local count = 0
    for i = 0, 5 do if r16(0xCE7D0 + i * 2) < 0x8000 then count = count + 1 end end
    if count > selected then
      selected = count
      L.shot(string.format('mask_parts_%d.png', count))
      L.log(string.format('MASK %d of 6 parts selected', count))
    end
    if count < 6 then
      if commands then L.press('l1', 6)
      elseif move_row then L.press('down', 6); move_row = false
      else L.press('circle', 6); move_row = true end
    elseif not commands then
      L.shot('mask_parts_complete.png')
      L.press('r1', 6)
    else
      local cursor = r32(0xCE180)
      assert(cursor >= 0x80000000 and cursor < 0x80200000, 'missing mask cursor object')
      if r32(cursor + 0x1C) ~= 0x82000 then L.press('down', 6)
      else
        L.shot('mask_done_selected.png')
        L.press('circle', 6)
        confirming = n
      end
    end
    return
  end
  local step = math.floor(age / 240)
  if age % 240 == 0 then
    L.shot(string.format('mask_%02d.png', step))
    L.log(string.format('MASK step %d mode %02X', step, mem[0x8C490]))
    if step >= #MASK_ACTIONS then L.finish(0); return end
    L.press(MASK_ACTIONS[step + 1], 6)
  end
end)
