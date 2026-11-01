-- Cold-boot sprite assembly fixture, used with warp.lua and HOLD=-1.
-- SPRITE_FIXTURE={mode=52,file=345,target=2,source=4,items={0,1,2}}
-- Redirect an existing actor's ANM item pointers to real result records in the
-- same loaded archive. No record geometry, texture, palette or game code changes.
-- This proves assembly through the game renderer, NOT natural outcome logic or
-- placement. Require announcements_qa.py pixel coverage and a visual review.
local cfg = assert(SPRITE_FIXTURE, 'set SPRITE_FIXTURE')
assert(cfg.target ~= cfg.source, 'target must differ from source')
local mem = PCSX.getMemPtr()
local function r16(a) a = a & 0x1FFFFF; return mem[a] + mem[a + 1] * 256 end
local function r32(a) return r16(a) + r16(a + 2) * 65536 end
local function w32(a, v)
  a = a & 0x1FFFFF
  for i = 0, 3 do mem[a + i] = (v >> (i * 8)) & 255 end
end
local entered, target, tab, before, source, offsets
L.on_frame(function(n)
  if mem[0x8C490] ~= cfg.mode then return end
  entered = entered or n
  if not tab then
    for slot = 0, 31 do
      local a = 0xA3DE0 + slot * 8
      local base = r32(a)
      if r16(a + 4) == cfg.file and base >= 0x80000000 and base < 0x80200000 then
        target = base + r32(base + cfg.target * 4)
        source = base + r32(base + cfg.source * 4)
        if r32(target) == 0x004D4E41 and r32(source) == 0x004D4E41 then
          tab, before, offsets = target + r32(target + 8), {}, {}
          for i = 0, r32(target + 4) - 1 do before[i] = r32(tab + i * 4) end
          for _, item in ipairs(cfg.items) do
            assert(item >= 0 and item < r32(source + 4), 'source item out of range')
            offsets[item] = (source + r32(source + r32(source + 8) + item * 4) - target) % 0x100000000
          end
          L.log(string.format('SPRITE fixture %d target %08X source %08X', cfg.file, target, source))
          break
        end
      end
    end
  end
  local age = n - entered
  if age > 2400 and not tab then L.fail('sprite archive never loaded'); return end
  local elapsed = age - (cfg.start or 1200)
  if not tab or elapsed < 0 then return end
  local step = math.floor(elapsed / 120) + 1
  if step > #cfg.items then
    for i, old in pairs(before) do w32(tab + i * 4, old) end
    L.log('SPRITE fixture complete; target pointers restored')
    L.finish(0)
    return
  end
  local item = cfg.items[step]
  for i in pairs(before) do w32(tab + i * 4, offsets[item]) end
  if elapsed % 120 == 60 then L.shot(string.format('announcement_%02d.png', item)) end
end)
