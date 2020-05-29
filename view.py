from app import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json
from func import *
import os
# from forms import *
from urllib import unquote


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        landing_url = request.form.get('landing_url')
        tds_url = request.form.get('tds_url')
        tds_url = landing_url if tds_url == '' else tds_url
        traffic_type = request.form.get('traffic_type')
        email_type = request.form.get('email_type')
        country = request.form.get('country')

        task = SurfTask(
            landing_url=landing_url,
            tds_url=tds_url,
            traffic_type=traffic_type,
            email_type=email_type,
            country=country)
        db.session.add(task)
        db.session.commit()

        log_file = '/home/user/work/msa/hello.log'
        with open(log_file, 'w') as file:
            pass
        import subprocess
        import os
        subprocess.Popen(['/bin/sh', os.path.expanduser('~/work/msa/e.sh')])
        return json.dumps(request.form)
    countries = ['US', 'GB', 'ES', 'IT', 'AU', 'DE', 'FR', 'NL']
    surf_task = SurfTask.query.order_by('-id').first()
    inventorys = Inventory.query.all()
    forms = Form.query.all()
    data = {
        'landing_url': '',
        'tds_url': '',
        'traffic_type': '',
        'email_type': '',
        'countries': countries,
        'forms': forms,
        'country': ''}
    if surf_task:
        data.update({
            'landing_url': surf_task.landing_url,
            'tds_url': surf_task.tds_url,
            'traffic_type': surf_task.traffic_type,
            'email_type': surf_task.email_type,
            'country': surf_task.country})
    data['inventorys'] = inventorys
    return render_template('index.html', **data)


@app.route('/po', methods=['POST'])
def po():
    print request
    if request.method == "POST":
        data = [(i[0], {ii.split('=')[0]: unquote(ii.split('=')[1]) for ii in i[1].split('&')}) for i in request.json]
    else:
        return ''
    print data
    return render_template('po/landing_register.html', context=data)


@app.route('/xpath_for_type/<elem_type>')
def xpath_for_type(elem_type):
    form = Form.query.filter_by(slug=elem_type).first().id
    xpaths = Xpath.query.filter_by(form_id=form).all()
    return json.dumps([u.xpath for u in xpaths])


@app.route('/inv', methods=['GET', 'POST'])
def inventory():
    if request.method == "POST":
        for domen in request.json.keys():
            inventor = Inventory.query.filter_by(domen=domen).first()
            if inventor:
                if not (inventor.web == request.json[domen][0] and inventor.wap == request.json[domen][1]):
                    inventor.web = request.json[domen][0]
                    inventor.wap = request.json[domen][1]
                    db.session.add(inventor)
                continue
            else:
                inv = Inventory(domen=domen, web=request.json[domen][0], wap=request.json[domen][1])
            db.session.add(inv)
        db.session.commit()

    return ''


@app.route('/list')
def mylist():
    my_list = ['loaded', 'gender', 'email', 'ClickRandomVisible', 'password', 'username',
               'birthday_day', 'birthday_month', 'birthday_year',
               'zip', 'age', 'age_min', 'age_max', 'city', 'fname', 'lname', 'phone']
    return json.dumps(my_list)


@app.route('/log/<date>')
def lof(date):
    log_file = '/home/user/work/msa/hello.log'
    mtime = str(os.path.getmtime(log_file))
    if date != mtime:
        with open(log_file, 'r') as file:
            f = file.read()
        responce = {'date': mtime, 'log': f}
    else:
        responce = {'date': mtime, 'log': 0}
    return json.dumps(responce)


@app.route('/<path:path>', methods=['POST'])
def post(path):
    if "surf_task/set/code_status" in path:
        responce = {"message": "not implemented"}
    elif "surf_task/set/behavior" in path:
        responce = {"message": "not implemented"}
    elif "page_object/resolve" in path:
        print(request.form)
        data = page_object_resolve(request.form)
        responce = {"success": True if data else False,
                    "reason": "OK" if data else "No such PO:{0}".format(
                        request.form.get("page_object_key", "lol wut?")
                    ),
                    "po_filename": data}
    elif "surf_task/set/biz_status" in path:
        responce = {"message": "not implemented"}
    elif "surf_task/set/code_status" in path:
        responce = {"message": "not implemented"}
    # =========================================
    # elif "/profile/get" in path:
    #     responce = {"success": True,
    #                 "profile": self.__get_profile(post_data, params)}
    elif "/profile/unuse" in path:
        responce = {"message": "not implemented",
                    "success": False}
    # elif "/profile/block" in path:
    #     responce = {"success": True,
    #                 "message": self.__remove_profile(post_data, params)}
    elif "/retention_record/add" in path:
        responce = add_retention_data(request.form)
    elif "/profile/proxy_id/set" in path:
        responce = {"message": "not implemented",
                    "success": False}
    elif "/multi_data/get_random" in path:
        responce = get_multidata(request.form)
        responce["success"] = True if responce.get('data') else False
    elif "/multi_data/release" in path:
        responce = {"message": "multidata release",
                    "post_data": request.form}
    elif "/multi_data/block" in path:
        responce = {"message": "multidata block",
                    "post_data": request.form}
    else:
        responce = {"message": "not supported",
                    "success": False}

    return json.dumps(responce)


@app.route('/<path:path>', methods=['GET'])
def get(path):
    print(path)
    params = request.args
    if "page_object/get" in path:
        return get_page_object(params.get('page_object_name'))
    elif "surf_task/get" in path:
        responce = get_surf_task()
    elif "/browser/get" in path:
        responce = {"message": "not implemented",
                    "success": False}
    elif "/country_data/get" in path:
        data = get_country_data(params)
        responce = {"data": data, "success": True if data else False}
    elif "/proxy/get_random" in path:
        responce = get_proxy(params)
        responce["success"] = True if responce else False
    elif "/proxy/get" in path:
        responce = get_proxy(params)
        responce["success"] = True if responce else False
    elif "/retention_record/get_by_surf_task_id" in path:
        responce = get_retention_record(path, params)
    elif "/profile/photo" in path:
        responce = get_photo_url(path, params)
        responce["success"] = True if responce else False
    else:
        responce = {"message": "not supported"}

    return json.dumps(responce)
