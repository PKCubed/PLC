#!/usr/bin/env python3

"""Write 4 coils to True, wait 2s, write False and redo it."""

import time

from pyModbusTCP.client import ModbusClient

# init
c = ModbusClient(host='192.168.0.82', port=502, auto_open=True)
bit = True

# main loop
while True:
    # write 4 bits in modbus address 0 to 3
    print('write bits')
    print('----------\n')
    is_ok = c.write_single_coil(100, bit)
    if is_ok:
        print('coil #%s: write to %s' % (100, bit))
    else:
        print('coil #%s: unable to write %s' % (100, bit))

    print('')

    # toggle
    bit = not bit
    # sleep 2s before next polling
    print('')
    time.sleep(1)