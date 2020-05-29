#!/usr/bin/env python
# coding: utf-8

import json
import logging
import random
import sys
from urlparse import urlparse, parse_qs
from config import CONFIG
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

# create logger
logger = logging.getLogger("Tasks")
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(
    fmt='[%(asctime)s]  %(name)-10s %(levelname)-8s %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class MyRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        length = int(self.headers['Content-Length'])
        if length:
            post_data = self.rfile.read(length).decode('utf-8')
            try:
                post_data = json.loads(post_data)
            except ValueError:
                logger.debug(post_data)
                post_data = {kv.split("=")[0]: kv.split("=")[1]
                             for kv in post_data.split("&")}
        else:
            post_data = {}
        params = parse_qs(urlparse(self.path).query)

        if "/surf_task/set/code_status" in self.path:
            responce = {"message": "not implemented"}
        elif "/surf_task/set/behavior" in self.path:
            responce = {"message": "not implemented"}
        elif "/page_object/resolve" in self.path:
            data = self.__page_object_resolve(post_data, params)
            responce = {"success": True if data else False,
                        "reason": "OK" if data else "No such PO:{0}".format(
                            post_data.get("page_object_key", "lol wut?")
                        ),
                        "po_filename": data}
        elif "/surf_task/set/biz_status" in self.path:
            responce = {"message": "not implemented"}
        elif "/surf_task/set/code_status" in self.path:
            responce = {"message": "not implemented"}
        else:
            responce = {"message": "not supported"}

        self.wfile.write(json.dumps(responce))

    def __page_object_resolve(self, request, params):
        inventory = {
            'giveaways-au.com': ('giveaways_au_w', 'giveaways_au_m'),
        }
        po_key = request.get("page_object_key")
        po_type = request.get("traffic_type")
        if not po_key:
            return None
        logger.debug(po_key)
        po_name = inventory.get(po_key)
        if isinstance(po_name, tuple):
            return po_name[0] if po_type == "web" else po_name[1]
        else:
            return po_name

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        params = parse_qs(urlparse(self.path).query)

        if "/surf_task/get" in self.path:
            responce = self.__get_surf_task(params)
        else:
            responce = {"message": "not supported"}

        self.wfile.write(json.dumps(responce))

    def __get_surf_task(self, request):
        # start
        country = 'AU'
        traffic_type = 'wap'
        task_type = "surf"      # "click", "surf"

        landing_url = "http://fly-np.giveaways-au.com/?aid=RFC&utm_source={utm_source}&utm_medium={utm_medium}&utm_campaign=923-1138&utm_content={utm_content}&first_name={firstname}&last_name={lastname}&email={email}&dob={dob}&gender={gender}&street={street}&street_nr={street_nr}&zipcode={zipcode}&mobile={mobile}&city={thecity}&affid=1138&aff_sub2=1020cf50c0079236a70a406f3a880d&aff_sub3=13376"
        tds_url = 'http://www.nat4trck8.com/aff_c?offer_id=18158&aff_id=13376'

        # http://oxew.adsb4trk.com/c/1cb868b25a1d1f49

        lumi_username = "lum-customer-trilink-zone-tmr-country-{0}-dns-remote-session-rand{1}"
        lumi_username = lumi_username.format(country.lower(),
                                             random.randint(0, 100))
        lumi_password = "a0f2m3dufrn5"
        lumi_proxy = "zproxy.luminati.io"
        if country == 'NL':
            # Use superproxy in Netherlands
            lumi_proxy = "servercountry-nl.zproxy.luminati.io"
        lumi_port = 22225

        j = {"a": "get_surf_task",
             "ipinfo_url": "http://ipinfo.io",
             "proxy": {"params": {"country": country.lower(),
                                  "good_ip_attempts": 25,
                                  "password": lumi_password,
                                  "port": lumi_port,
                                  "proxy": lumi_proxy,
                                  "username": lumi_username},
                       #=backward compatibility===========================
                       "country": country.lower(),
                       "good_ip_attempts": 25,
                       "password": lumi_password,
                       "port": lumi_port,
                       "proxy": lumi_proxy,
                       "username": lumi_username,
                       #============================
                       "type": "lumi"},
             "success": True,
             "surf_task": {"account_id": random.randint(1, 9),
                           "age_max": random.randint(26, 40),
                           "age_min": random.randint(19, 25),
                           "country": country,
                           "cpa_offer_id": random.randint(1000, 9999),
                           "group_key": "test",
                           "is_paid": True,
                           "landing_url": landing_url,
                           "params": {
                                "disable_images": False,
                                "payment_probability": 1,
                                "required_surf": True,
                                "ip_reuse_days": 120,
                            },
                           "male_percentage": 100,
                           "network_name": "test",
                           "page_object_id": random.randint(1, 99),
                           "parent_surf_task_id": 4268,
                           "po_filename": "po_filename",
                           "product_name": "product_name",
                           "project_id": random.randint(10, 99),
                           "referrer_key_url": tds_url,
                           "referrer_value_url": tds_url,
                           "surf_behaviour": {"act_5": {"steps": [
                                        {
                                            "action": "landing_register",
                                            # "params": {"email_type": "doi"},
                                            "params": {"email_type": "soi"}
                                        },
                                        # {
                                        #    "action": "confirm_registration",
                                        #    "params": None
                                        # },
                                        # {"action": "skip_funnel",
                                         # "params": None},
                                        {
                                            "action": "fill_funnel",
                                            "params": None
                                        },
                                        {
                                            "action": "upload_photo",
                                            "params": None
                                        },
                                        # {"action": "site_surf",
                                        # "params": {"10": 100}},
                                        {
                                            "action": "site_surf",
                                            "params": {"5": 100}
                                        }
                                    ]}},
                           "retention_behaviour": {
                               "act_5": {
                                   "steps": [
                                       {
                                           "action": "retention_login_index",
                                            "params": None
                                       },
                                       # {"action": "retention_login_email",
                                       # "params": None},
                                       # {"action": "fill_funnel",
                                       # "params": None},
                                        {
                                            "action": "skip_funnel",
                                            "params": None
                                        },
                                       # {"action": "upload_photo",
                                       # "params": None},
                                        {
                                            "action": "retention_surf",
                                            "params": None
                                        },
                                       # {"action": "site_surf",
                                       # "params": {"10": 100}},
                                    ]}},
                           "retention_day": [50, 15, 8, 5, 1, 3, 2, 1],
                           "retention_day_n": "2017-06-08",
                           "retention_stats": {"act_5": 100},
                           "run_at": "2017-06-08T09:20:06",
                           "surf_stats": {"act_5": 100},
                           "surf_task_id": random.randint(1000, 9999),
                           "task_type": task_type,
                           "tds_url": tds_url,
                           "traffic_type": traffic_type},
             "type": None,    # backward compatibility
             }
        return j


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    port = int(CONFIG['tasks_http_port'])

    logger.debug("Running on port: {0}".format(port))

    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, MyRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
