from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
import skimage.io
import triangler  # 导入convert函数
from triangler.config import TrianglerConfig
from triangler.edge_detectors import EdgeDetector
from triangler.renderers import Renderer
from triangler.samplers import Sampler

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')  # 渲染HTML页面

@app.route('/convert', methods=['POST'])
def convert_image():
    file = request.files['image']
    edge_detector = request.form['edge_detector']
    sampler = request.form['sampler']
    renderer = request.form['renderer']
    n_samples = int(request.form['n_samples'])

    # 创建TrianglerConfig对象并应用用户选择的配置
    config = TrianglerConfig(n_samples=n_samples, 
                             edge_detector=EdgeDetector[edge_detector.upper()],
                             sampler=Sampler[sampler.upper()],
                             renderer=Renderer[renderer.upper()])

    # 保存上传的图像
    filename = secure_filename(file.filename)
    filepath = os.path.join('/tmp', filename)
    file.save(filepath)

    # 调用convert函数生成低多边形图像
    #result = convert(filepath, config=config)

    # 保存结果图像并返回
    result_path = os.path.join('/tmp', 'result.png')
    result = triangler.convert(img=filepath, save_path=result_path, config=config)
    skimage.io.imsave(result_path, result)

    return send_file(result_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
