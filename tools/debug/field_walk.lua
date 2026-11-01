-- Controller-only map route after a cold warp; no story-state or camera writes.
-- WALK_MAP=59 WALK={{'up',240},{'right',120}} with warp.lua HOLD=-1.
local mem = PCSX.getMemPtr()
local function r16(a) return mem[a] + 256 * mem[a + 1] end
local start, last_step
L.on_frame(function(n)
  if mem[0x8C490] ~= 1 or r16(0x8C570) ~= WALK_MAP then return end
  start = start or n
  local age = n - start - 600
  if age < 0 then return end
  local elapsed = 0
  for i, step in ipairs(WALK) do
    local key, frames = step[1], step[2]
    if age < elapsed + frames then
      if last_step ~= i then
        last_step = i
        L.log(string.format('WALK step %d %s %d f%d', i, key, frames, n))
        if key ~= '-' then L.press(key, frames) end
      end
      if age % (WALK_EVERY or 30) == 0 then
        local prefix = string.format('walk_%04d', age)
        L.shot(prefix .. '.png')
        if WALK_VRAM then L.dump_ppu(prefix) end
      end
      return
    end
    elapsed = elapsed + frames
  end
  L.shot('walk_final.png')
  L.finish(0)
end)
