from composer import composer

c = composer()
c.importaudio()
c.crossfade("0","1","10","18")
c.exportaudio()