#!env/bin/python

# Logitech G203 Prodigy / G203 LightSync Mouse LED control
# https://github.com/smasty/g203-led
# Authors: Smasty, TheAquaSheep (LightSync support)
# Licensed under the MIT license.

import sys
import usb.core
import usb.util
import re
import binascii

class G203LEDController:
    def __init__(self):
        self.g203_vendor_id = 0x046d
        self.g203_prodigy_product_id = 0xc092
        self.g203_lightsync_product_id = 0xc092
        self.g203_product_id = self.g203_lightsync_product_id

        self.default_rate = 10000
        self.default_brightness = 100
        self.default_direction = 'right'

        self.dev = None
        self.wIndex = None

    def print_error(self, msg):
        print('Error: ' + msg)
        sys.exit(1)

    def process_color(self, color):
        if not color:
            self.print_error('No color specified.')
        if color[0] == '#':
            color = color[1:]
        if not re.match('^[0-9a-fA-F]{6}$', color):
            self.print_error('Invalid color specified.')
        return color.lower()

    def process_rate(self, rate):
        if not rate:
            rate = self.default_rate
        try:
            return '{:04x}'.format(max(1000, min(65535, int(rate))))
        except ValueError:
            self.print_error('Invalid rate specified.')

    def process_brightness(self, brightness):
        if not brightness:
            brightness = self.default_brightness
        try:
            return '{:02x}'.format(max(1, min(100, int(brightness))))
        except ValueError:
            self.print_error('Invalid brightness specified.')

    def process_direction(self, direction):
        if not direction:
            direction = self.default_direction
        else:
            if not (direction == 'left' or direction == 'right'):
                self.print_error('Invalid direction specified.')
        return direction

    def process_dpi(self, dpi):
        if not dpi:
            self.print_error('No DPI specified.')
        lower_lim = 200
        if self.g203_product_id == self.g203_lightsync_product_id:
            lower_lim = 50
        try:
            return '{:04x}'.format(max(lower_lim, min(8000, int(dpi))))
        except ValueError:
            self.print_error('Invalid DPI specified.')
        return dpi

    def set_led_solid(self, color):
        return self.set_led('01', color + '0000000000')

    def set_led_breathe(self, color, rate, brightness):
        return self.set_led('03', color + rate + '00' + brightness + '00')

    def set_led_cycle(self, rate, brightness):
        return self.set_led('02', '0000000000' + rate + brightness)

    def set_led(self, mode, data):
        prefix = '11ff0e3b00'
        suffix = '000000000000'
        self.send_command(prefix + mode + data + suffix)

    def set_intro_effect(self, arg):
        if arg == 'on' or arg == '1':
            toggle = '01'
        elif arg == 'off' or arg == '0':
            toggle = '02'
        else:
            self.print_error('Invalid value.')

        self.send_command('11ff0e5b0001'+toggle+'00000000000000000000000000')

    def set_dpi(self, dpi):
        cmd = '10ff0a3b00{}'.format(dpi)
        self.send_command(cmd, disable_ls_onboard_memory=False)

    def set_ls_solid(self, color):
        cmd = '11ff0e1b0001{}0000000000000001000000'.format(color)
        self.send_command(cmd, disable_ls_onboard_memory=True)

    def set_ls_cycle(self, rate, brightness):
        cmd = '11ff0e1b00020000000000{}{}000001000000'.format(rate, brightness)
        self.send_command(cmd, disable_ls_onboard_memory=True)

    def set_ls_breathe(self, color, rate, brightness):
        cmd = '11ff0e1b0004{}{}00{}00000001000000'.format(color, rate, brightness)
        self.send_command(cmd, disable_ls_onboard_memory=True)

    def set_ls_intro(self, arg):
        if arg == 'on' or arg == '1':
            toggle = '01'
        elif arg == 'off' or arg == '0':
            toggle = '02'
        else:
            self.print_error('Invalid value.')
        cmd = '11ff0e3b010001{}000000000000000000000000'.format(toggle)
        self.send_command(cmd, disable_ls_onboard_memory=False)

    def set_ls_triple(self, color_left, color_middle, color_right):
        cmd = '11ff121b01{}02{}03{}00000000'.format(color_left, color_middle, color_right)
        self.send_command(cmd, disable_ls_onboard_memory=False)

    def set_ls_wave(self, rate, brightness, direction):
        rate_U8 = rate[0:2]
        rate_L8 = rate[2:4]
        state = '01'
        if direction == 'left':
            state = '06'
        cmd = '11ff0e1b0003000000000000{}{}{}{}01000000'.format(rate_L8, state, brightness, rate_U8)
        self.send_command(cmd, disable_ls_onboard_memory=True)

    def set_ls_blend(self, rate, brightness):
        rate_U8 = rate[0:2]
        rate_L8 = rate[2:4]
        cmd = '11ff0e1b0006000000000000{}{}{}0001000000'.format(rate_L8, rate_U8, brightness)
        self.send_command(cmd, disable_ls_onboard_memory=True)

    def clear_ls_buffer(self): #tested on lightsync but may also affect prodigy
        try:
            while True:
                self.dev.read(0x82, 20)
        except usb.core.USBError:
            return

    def send_command(self, data, disable_ls_onboard_memory=False, clear_ls_buf=False):
        self.attach_mouse()

        if clear_ls_buf: # if this is ever needed in practise the default can be changed above.
            self.clear_ls_buffer()

        if disable_ls_onboard_memory:
            self.dev.ctrl_transfer(0x21, 0x09, 0x210, self.wIndex, binascii.unhexlify('10ff0e5b010305'))
            self.dev.read(0x82, 20)

        wValue=0x211
        if len(data) == 14:
            wValue = 0x210

        self.dev.ctrl_transfer(0x21, 0x09, wValue, self.wIndex, binascii.unhexlify(data))
        self.dev.read(0x82, 20)

        if data[0:8] == '11ff121b':
            apply_triple_cmd = '11ff127b00000000000000000000000000000000'
            self.dev.ctrl_transfer(0x21, 0x09, 0x211, self.wIndex, binascii.unhexlify(apply_triple_cmd))
            self.dev.read(0x82, 20)

        if clear_ls_buf: # done again to ensure the buffer did not fill between the last clear and cmd
            self.clear_ls_buffer()

        self.detach_mouse()

    def attach_mouse(self):
        self.dev = usb.core.find(idVendor=self.g203_vendor_id, idProduct=self.g203_product_id)
        if self.dev is None:
            self.print_error('Device {:04x}:{:04x} not found.'.format(self.g203_vendor_id, self.g203_product_id))
        self.wIndex = 0x01
        if self.dev.is_kernel_driver_active(self.wIndex) is True:
            self.dev.detach_kernel_driver(self.wIndex)
            usb.util.claim_interface(self.dev, self.wIndex)

    def detach_mouse(self):
        if self.wIndex is not None:
            usb.util.release_interface(self.dev, self.wIndex)
            self.dev.attach_kernel_driver(self.wIndex)
            self.dev = None
            self.wIndex = None

if __name__ == '__main__':
    controller = G203LEDController()
    controller.main()