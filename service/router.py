#!/usr/bin/python
#-*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from bus import Bus
from bus_routers import Routers
from tts import create_voice
from InvalidParameterException import InvalidParameterException

app = Flask(__name__)


@app.route('/api/')
def hello_world():
    return '<h1>Hello World</h1>'

@app.route('/api/bus/<router_name_str>/search')
def query_router_str(router_name_str):
    res = filter(lambda x: router_name_str in x, Routers)
    return jsonify(res)

@app.route('/api/bus/<router_name>/stop/<stop_id>')
def query_stop(router_name, stop_id):
    direction = request.args.get('direction', '0')

    bus = Bus()
    res = bus.query_stop(router_name, direction, stop_id)

    return jsonify(res)


@app.route('/api/bus/<router_name>')
def query_router(router_name):
    direction = request.args.get('direction', '0')

    bus = Bus()
    routers = bus.query_router(router_name, direction)

    return jsonify(routers)


@app.route('/api/bus/<router_name>/details')
def query_router_details(router_name):
    direction = request.args.get('direction', '0')

    bus = Bus()
    router_details = bus.query_router_details(router_name, direction)

    return jsonify(router_details)

@app.route('/api/voice/bus/<router_name>/minutes/<minutes>')
def query_and_create_voice(router_name, minutes):
    create_voice(router_name, minutes)
    def generate():
        path = 'audio/' + router_name + '-' + minutes + '.mp3'
        with open(path, 'rb') as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)

    return Response(generate(), mimetype="audio/mpeg3")

    # return None
@app.route('/api/bus/check_update')
def check_update():
    platform = request.args.get('platform')
    version = request.args.get('version')
    if version == None:
        return jsonify({
            'text': '本次升级修复部分bug',
            'link': 'http://pz-common.oss-cn-qingdao.aliyuncs.com/H5387A906_0507223016.apk',
            'version': '1.0'
        })
    else:
        return jsonify({
            'text': '本次升级修复部分bug',
            'link': 'http://pz-common.oss-cn-qingdao.aliyuncs.com/H560DA3F8_1028170524.apk',
            'version': None
        })
@app.route('/api/bus/get_notice', methods=['GET', 'POST'])
def get_notice():
    return jsonify({
        'text': '因用户量过少，后续服务将不定期下线，请使用其他app！',
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'not_found',
        'error_msg': '链接不存在'
    }), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'error': 'internal_server_error',
        'error_msg': '服务器内部错误'
    }), 500


@app.errorhandler(InvalidParameterException)
def handle_invalid_parameter(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response
# 1
if __name__ == '__main__':
    app.run(debug=True)
