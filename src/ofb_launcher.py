import argparse
import logging
import os
import socket
import time
import urllib.error
import urllib.request

import openfreebuds_applet
import openfreebuds_backend
from openfreebuds import event_bus, manager, cli_io
from openfreebuds.constants.events import EVENT_MANAGER_STATE_CHANGED, EVENT_DEVICE_PROP_CHANGED
from openfreebuds_applet import utils
from openfreebuds_applet.l18n import t
from openfreebuds_applet.modules import http_server, self_check
from openfreebuds_applet.settings import SettingsStorage
from openfreebuds_applet.ui import tk_tools, settings_ui
from openfreebuds_backend.errors import BluetoothNotAvailableError

log = logging.getLogger("OfbLauncher")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Unofficial application to manage HUAWEI FreeBuds device")

    parser.add_argument("--verbose",
                        default=False, action="store_true",
                        help="Print debug log to console")
    parser.add_argument("--shell",
                        default=False, action="store_true",
                        help="Start CLI shell instead of applet")
    parser.add_argument("command",
                        default="", type=str, nargs='?',
                        help="If provided, will send command to httpserver and exit")
    return parser.parse_args()


def main():
    args = parse_args()

    # Setup logging
    logging.getLogger("asyncio").disabled = True
    logging.getLogger("CLI-IO").disabled = True
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=openfreebuds_applet.log_format, force=True)

    if args.command != "":
        do_command(args.command)
        return
    elif args.shell:
        run_shell()
        return

    applet = openfreebuds_applet.create()
    if is_start_possible(applet):
        # Start is allowed, running
        applet.start()
    else:
        # Run main thread to make windows interactive
        applet.tray_application.run()


def is_start_possible(applet):
    # Is already running?
    if utils.is_running():
        tk_tools.message(t("application_running_message"), "Error", _leave)
        return False

    # Is python built with AF_BLUETOOTH support?
    if not getattr(socket, "AF_BLUETOOTH", False):
        tk_tools.message(t("no_af_bluetooth"), "Error", _leave)
        return False

    # Is bluetooth adapter accessible
    # try:
    #     openfreebuds_backend.bt_list_devices()
    # except BluetoothNotAvailableError:
    #     tk_tools.message(t("no_bluetooth_error"), "Error", _leave)
    #     return False

    return True


def do_command(command):
    if utils.is_running():
        log.debug("App is launched, using HTTP server to process command...")
        _do_command_webserver(command)
    else:
        log.debug("App isn't launched, trying to run command without them")
        _do_command_offline(command)


def _do_command_webserver(command):
    port = http_server.get_port()

    try:
        url = "http://localhost:{}/{}".format(port, command)

        with urllib.request.urlopen(url) as f:
            print(f.read().decode("utf8"))

    except urllib.error.URLError:
        log.exception("Can't do command via HTTP-server")
        tk_tools.message(t("do_command_server_error").format(command), "Openfreebuds", _leave)


def _do_command_offline(command):
    man = manager.create()
    settings = SettingsStorage()
    if settings.address == "":
        log.error("No saved device, bye")
        return

    start = time.time()
    man.set_device(settings.device_name, settings.address)
    while man.state != man.STATE_CONNECTED and man.state != man.STATE_OFFLINE:
        if time.time() - start > 5:
            log.debug("connection timed out, bye")
            _leave()
        time.sleep(0.25)

    log.debug("ready to run")
    actions = openfreebuds_applet.modules.actions.get_actions(man)
    if command not in actions:
        log.error("Undefined command")
        _leave()

    actions[command]()
    event_bus.wait_for(EVENT_DEVICE_PROP_CHANGED, timeout=2)
    print("true")
    _leave()


def _leave():
    # noinspection PyProtectedMember,PyUnresolvedReferences
    os._exit(1)


def run_shell():
    man = manager.create()

    # Device picker
    devices = openfreebuds_backend.bt_list_devices()
    for i, a in enumerate(devices):
        print(i, a["name"], "(" + a["address"] + ")", a["connected"])
    print()

    num = int(input("Enter device num to use: "))
    name = devices[num]["name"]
    address = devices[num]["address"]

    # Start shell
    print("-- Using device", address)
    man.set_device(name, address)

    while True:
        print("-- Waiting for spp connect...")
        while man.state != man.STATE_CONNECTED:
            event_bus.wait_for(EVENT_MANAGER_STATE_CHANGED)

        while not man.device.closed:
            command = input("OpenFreebuds> ").split(" ")

            if command[0] == "":
                continue

            if command[0] == "q":
                man.close()
                print('bye')
                raise SystemExit

            print(cli_io.dev_command(man.device, command))
        print("-- Device disconnected")


if __name__ == "__main__":
    main()
