from flask import Flask
from flask import request
import json
from func import *


app = Flask(__name__)


@app.route('/<path:path>', methods=['POST'])
def post(path):
    if "surf_task/set/code_status" in path:
        responce = {"message": "not implemented"}
    elif "surf_task/set/behavior" in path:
        responce = {"message": "not implemented"}
    elif "page_object/resolve" in path:
        data = page_object_resolve(request.form)
        responce = {"success": True if data else False,
                    "reason": "OK" if data else "No such PO:{0}".format(
                        request.form.get("page_object_key", "lol wut?")
                    ),
                    "po_filename": data}
        # responce = {"message": "not 1"}
    elif "surf_task/set/biz_status" in path:
        responce = {"message": "not implemented"}
    elif "surf_task/set/code_status" in path:
        responce = {"message": "not implemented"}
    else:
        responce = {"message": "not supported"}

    return json.dumps(responce)


@app.route('/<path:path>', methods=['GET'])
def get(path):
    print(path)
    if "surf_task/get" in path:
        responce = get_surf_task()
    else:
        responce = {"message": "not supported"}

    return json.dumps(responce)


if __name__ == "__main__":
    app.run(host='localhost', port=4001, debug=True)
