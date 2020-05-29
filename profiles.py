#!/usr/bin/env python
# coding: utf-8

import base64
import csv
import gzip
import json
import logging
import mimetypes
import random
import sys
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from os import path, listdir
from urlparse import urlparse, parse_qs, unquote

from config import CONFIG


# create logger
logger = logging.getLogger("Profiles")
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
    task_surf_id = 0

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
                post_data = {kv.split("=")[0]: kv.split("=")[1]
                             for kv in post_data.split("&")}
        else:
            post_data = {}
        params = parse_qs(urlparse(self.path).query)

        if "/profile/get" in self.path:
            responce = {"success": True,
                        "profile": self.__get_profile(post_data, params)}
        elif "/profile/unuse" in self.path:
            responce = {"message": "not implemented",
                        "success": False}
        elif "/profile/block" in self.path:
            responce = {"success": True,
                        "message": self.__remove_profile(post_data, params)}
        elif "/retention_record/add" in self.path:
            responce = self.__add_retention_data(post_data, params)
        elif "/profile/proxy_id/set" in self.path:
            responce = {"message": "not implemented",
                        "success": False}
        elif "/multi_data/get_random" in self.path:
            responce = self.__get_multidata(post_data, params)
            responce["success"] = True if responce.get('data') else False
        elif "/multi_data/release" in self.path:
            responce = {"message": "multidata release",
                        "post_data": post_data,
                        "params": params}
        elif "/multi_data/block" in self.path:
            responce = {"message": "multidata block",
                        "post_data": post_data,
                        "params": params}
        elif "/api/po" in self.path:
            return self.__get_po()
        else:
            responce = {"message": "not supported",
                        "success": False}

        self.wfile.write(json.dumps(responce))

    def __add_retention_data(self, request, params):
        task_id = request["surf_task_id"]
        filename = "db/retension/ret_{0}.json.gz".format(task_id)
        try:
            with gzip.open(filename, "wb") as f:
                f.write(unquote(request["data"]))
        except IOError as err:
            return {"success": False, "reason": str(err)}
        return {"success": True, "message": "saved to {0}".format(filename)}

    def __get_profile(self, request, params):
        try:
            mail_profile = self.server._load_email_profile(
                doi=request.get('is_doi', False)
            )
        except AttributeError as ex:
            logger.warning(ex)
            mail_profile = None
        # fake_email = json.loads(request["surf_task"])
        # logger.info(fake_email)
        # if mail_profile is None or fake_email["fake_email"]:
        # if mail_profile is None:
            # mail_profile = {
                # "email": "whocares{0}@mailabyss.com".format(
                    # random.randint(10000, 99999)
                # ),
                # "password": "",
                # "gender": "male",
                # "fname": "Arthi",
                # "email_server_type": "IMAP",
                # "lname": "Antoniotti",
                # "domain": "mailabyss.com",
                # "proxy_id": 0,
                # "id": 0,
            # }
        return mail_profile

    def __remove_profile(self, request, params):
        try:
            profile_id = int(request["profile_id"])
        except StandardError:
            return "error: profile id is invalid"
        if self.server._last_mail["id"] != profile_id:
            return "error: no such profile id"
        if not self.server._remove_email_from_profile(
            self.server._last_mail["email"]
        ):
            return "error: can't write to file"
        return "removed successfully!"

    def __get_multidata(self, request, params):
        buckets = {'profile', 'leadleadersfb', 'datingsoi', 'contestchest_PV',
                   'fbverified', 'mixtape', 'OlyaAU', 'PublisherWall', 'leonFBcamp',
                   'amazando_uk', 'greenflag', 'tolead', 'frgillymob', 'aufbverified',
                   'fbNOTverified', 'xdata'}
        if 'eur' in request["bucket"]:
            data = {'number': '5562963149116111',
                    'cvv': '850',
                    'first_name': 'Ethan',
                    'last_name': 'Whittaker',
                    'year': '2020',
                    'month': '09',
                    'amount': '12',
                    'type': 'Mastercard'
                    }
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-09-15 13:04:32",
                    "data": json.dumps(data),
                    "id": 8,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        if 'usd' in request["bucket"]:
            data = {'number': '5562962135116390',
                    'cvv': '640',
                    'first_name': 'Leo',
                    'last_name': 'Swift',
                    'year': '2020',
                    'month': '09',
                    'amount': '4',
                    'type': 'Mastercard'
                    }
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-09-15 13:04:32",
                    "data": json.dumps(data),
                    "id": 8,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        if 'valid' in request["bucket"]:
            data = self.__get_valid_card(request)
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-09-15 13:04:32",
                    "data": json.dumps(data['card']),
                    "id": 8,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        if request["bucket"] == "card":
            data = self.__get_card(request)
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-03-31 13:04:32",
                    "data": json.dumps(data['card']),
                    "id": 8,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        if any(bucket in request["bucket"] for bucket in buckets):
            data = self.__get_country_data({"country": (request["country"],)})
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-03-31 13:04:32",
                    "data": json.dumps(data) if data else None,
                    "id": 9,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        if "win_message" in request["bucket"]:
            # data = 'Test case'
            data = 'I want a gift!!!'
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-03-31 13:04:32",
                    "data": data,
                    "id": 1,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        if "message" in request["bucket"]:
            # data = 'Test case'
            data = '{"intro": "I would say I am kind , understanding,' \
                   ' good listener, independent, hard worker.",' \
                   ' "title": "Well hello", "lookfor": ""}'
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-03-31 13:04:32",
                    "data": data,
                    "id": 1,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        if "photo" in request["bucket"]:
            data = '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'
            return {"a": "/multi_data/get_random",
                    "bucket": request["bucket"],
                    "country": request["country"],
                    "created_on": "2017-03-31 13:04:32",
                    "data": data,
                    "id": 1,
                    "is_blocked": False,
                    "updated_on": "2017-03-31 13:04:32"}
        return {"a": "/multi_data/get_random",
                "bucket": request["bucket"],
                "country": request["country"],
                "created_on": "2017-03-31 13:04:32",
                "data": None,
                "id": 0,
                "is_blocked": False,
                "updated_on": "2017-03-31 13:04:32"}

    def __get_po(self):
        po_name = self.path.rsplit('/', 1)[-1]
        if not po_name:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False,
                                         "error": "po name not specified"}))
            return
        full_path = path.join("/home/vlad/Work/PO/page-objects/offers", po_name)
        full_path = path.normpath(full_path + '.py')
        try:
            with open(full_path, "rb") as f:
                # self.send_response(200)
                # self.send_header("Content-type", "text/x-python")
                # self.end_headers()
                self.wfile.write(f.read())
        except IOError:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False,
                                         "error": "file not found",
                                         "name": po_name,
                                         "path": full_path}))

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)

        if "/browser/get" in self.path:
            responce = {"message": "not implemented",
                        "success": False}
        elif "/country_data/get" in self.path:
            data = self.__get_country_data(params)
            responce = {"data": data, "success": True if data else False}
        elif "/proxy/get_random" in self.path:
            responce = self.__get_proxy(params)
            responce["success"] = True if responce else False
        elif "/proxy/get" in self.path:
            responce = self.__get_proxy(params)
            responce["success"] = True if responce else False
        elif "/retention_record/get_by_surf_task_id" in self.path:
            responce = self.__get_retention_record(params)
        elif "/profile/photo" in self.path:
            responce = self.__get_photo_url(params)
            responce["success"] = True if responce else False
        elif "/image/" in self.path:
            return self.__get_static(params)
        elif "/card/" in self.path:
            responce = self.__get_card(params)
            responce["success"] = True if responce else False
        elif "/profile/get" in self.path:
            responce = {"success": True,
                        "profile": self.__get_profile({}, params)}
        else:
            responce = {"message": "not supported",
                        "success": False}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(responce))

    def __get_country_data(self, request):
        if request.get("country") is not None:
            source_db = "profiles_{0}".format(request["country"][0]).lower()
            try:
                if os.path.exists("db/{0}.json.gz".format(source_db)):
                    with gzip.open("db/{0}.json.gz".format(source_db),
                                   "rb") as user_data_db:
                        userdata = random.choice(json.load(user_data_db))
                else:
                    with open("db/{0}.json".format(source_db),
                                   "rb") as user_data_db:
                        line = random.choice(user_data_db.readlines())
                        self.log_message(line)
                        userdata = json.loads(line)
            except IOError:
                userdata = {}
            return userdata
        else:
            return {}

    def __get_retention_record(self, request):
        task_id = self.path.rsplit("/", 1)[-1].split("?", 1)[0]
        filename = "db/retension/ret_{0}.json.gz".format(task_id)
        try:
            with gzip.open(filename, "rb") as f:
                data = f.read()
        except IOError as err:
            return {"success": False, "reason": str(err)}
        return {"success": True, "data": data}

    def __get_photo_url(self, request):
        gender = request.get("gender")
        gender = gender[0] if gender else None
        url = 'http://localhost:4002/image/?name={0}'
        # TODO make file_path own class or server class field
        file_path = "/local_path/"
        if gender == "male":
            img_folder = 'upload_pics'
        elif gender == "female":
            img_folder = '5k Female Photos'
        else:
            return {}
        img_path = path.join(file_path, img_folder)
        img_name = random.choice(listdir(img_path))
        return {"photo_url": url.format(path.join(img_folder, img_name))}

    def __get_static(self, request):
        file_name = request.get("name")
        if not file_name:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'success': False,
                                         'error': 'file name not specified'}))
            return
        file_name = path.normpath(file_name[0])
        file_type = mimetypes.guess_type(file_name)[0]
        # TODO make file_path own class or server class field
        file_path = "/local_path/"
        full_path = path.join(file_path, file_name)
        try:
            with open(full_path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", file_type)
                self.end_headers()
                self.wfile.write(f.read())
        except IOError:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({'success': False,
                                         'error': 'file not found'}))

    def __get_card(self, request):
        return {'card':
                {'number': '5527278170807809',
                 'cvv': '744',
                 'first_name': 'JOHN',
                 'last_name': 'DOE',
                 'year': '2019',
                 'month': '01',
                 'amount': '24',
                 'type': 'Mastercard'
                 }}

    def __get_valid_card(self, request):
        return {'card':
                    {'number': '5562962113426076',
                     'cvv': '568',
                     'first_name': 'Spencer',
                     'last_name': 'Howells',
                     'year': '2020',
                     'month': '03',
                     'amount': '4',
                     'type': 'Mastercard',
                     'StreetAddress': '1031 Ocean dr',
                     'ZipCode': '33139',
                     'State': 'FL'
                    }
                }

    def __get_proxy(self, request):
        proxies = [
        ]
        proxy_ind = random.randint(0, len(proxies) - 1)
        return {"proxy_type": "SOCKS5",
                "ip": proxies[proxy_ind],
                "id": proxy_ind}


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def _load_email_profile(self, doi=True, profile_path="./db/emails.csv"):
        """
        Load profile from file
        """
        if hasattr(self, "_emails"):
            try:
                if doi:
                    mail_profile = next(
                        (i for i in self._emails if i["active"] == "t")
                    )
                else:
                    mail_profile = next(self._emails)
            except StopIteration:
                pass
            else:
                del mail_profile["active"]
                mail_profile["id"] = random.randint(1, 99)
                self._last_mail = mail_profile
                return mail_profile
        try:
            with open(profile_path, "rb") as profile_file:
                emails_csv = csv.DictReader(profile_file)
                emails = list(emails_csv)
                if (not emails or
                        doi and not [i for i in emails if i["active"] == "t"]):
                    return None
                self._emails = iter(emails)
                return self._load_email_profile(doi, profile_path)
        except IOError:
            return None

    def _remove_email_from_profile(self, mail,
                                   profile_path="./db/emails.csv"):
        keys = ['email', 'password', 'domain', 'email_server_type', 'gender',
                'fname', 'lname', 'proxy_id', 'active']
        try:
            with open(profile_path, "rb") as profile_file:
                emails_csv = csv.DictReader(profile_file)
                emails = list(emails_csv)
        except IOError:
            return False
        removed_mail = next((m for m in emails if m["email"] == mail), None)
        if not removed_mail:
            return False
        removed_mail["active"] = "f"
        try:
            with open(profile_path, "wb") as profile_file:
                emails_csv = csv.DictWriter(profile_file, fieldnames=keys)
                emails_csv.writeheader()
                emails_csv.writerows(emails)
        except IOError:
            return False
        return True


def main():
    port = int(CONFIG['profiles_http_port'])

    logger.debug("Running on port: {0}".format(port))

    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, MyRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()