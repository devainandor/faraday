---
categories: hello world, first!
tags: one, two
published_on: 2018-07-01T19:13+02:00
---

# Oh hai

<p>hello world</p>

```ruby
live_loop :drum_rack do
  iac_port = "iac_driver_bus_1"
  use_random_seed 808
  16.times do
    midi snare, port: iac_port if one_in(4)
    midi hh_closed, port: iac_port if one_in(2)
    midi hh_open, port: iac_port if one_in(3)
    midi kick, port: iac_port if one_in(4)
    sleep 0.25
  end
end
```
