# coding=utf-8
from __future__ import absolute_import

import os
import serial
import logging
from typing import List

import octoprint.plugin
from octoprint.settings import settings
from octoprint.util.platform import get_os, set_close_exec
from octoprint.util.comm import BufferedReadlineWrapper


class NetworkPrintingPlugin(
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
):
    def get_port_names(self, candidates) -> List[str]:
        additionalPorts = settings().get(["serial", "additionalPorts"])
        return [port for port in additionalPorts if "://" in port]

    def get_serial_factory(
        self, machinecom_self, port: str, baudrate: int, timeout_s: int
    ):
        self._logger.info(
            f"machinecom_self: {machinecom_self}, port: {port}, baudrate: {baudrate}, timeout_s: {timeout_s}"
        )

        # check for rfc2217 uri
        if not "://" in port:
            return None

        # connect to regular serial port
        machinecom_self._dual_log(
            "Connecting to port {}, baudrate {}".format(port, baudrate),
            level=logging.INFO,
        )

        serial_port_args = {
            "baudrate": baudrate,
            "timeout": timeout_s,
            "write_timeout": 0,
        }

        serial_obj = serial.serial_for_url(str(port), **serial_port_args)
        return BufferedReadlineWrapper(serial_obj)

    def get_update_information(self):
        # See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html for details.
        return dict(
            network_printing=dict(
                displayName="Network-printing Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="hellerbarde",
                repo="OctoPrint-Network-Printing",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/hellerbarde/OctoPrint-Network-Printing/archive/{target_version}.zip",
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py.
__plugin_name__ = "Network-Printing Plugin"
__plugin_pythoncompat__ = ">=3,<4"  # only python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = NetworkPrintingPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.transport.serial.factory": __plugin_implementation__.get_serial_factory,
        "octoprint.comm.transport.serial.additional_port_names": __plugin_implementation__.get_port_names,
    }
