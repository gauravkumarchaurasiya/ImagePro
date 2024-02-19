import cv2
from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from image_processor import ImageProcessor  
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'file2' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    file2 = request.files['file2']

    if file.filename == '' or file2.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename) and file2 and allowed_file(file2.filename):
        filename = secure_filename(file.filename)
        filename2 = secure_filename(file2.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        file.save(file_path)
        file2.save(file_path2)

        return redirect(url_for('process_image', filename=filename, filename2=filename2))

@app.route('/process/<filename>/<filename2>', methods=['GET', 'POST'])
def process_image(filename, filename2):
    if request.method == 'POST':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        processor = ImageProcessor(image_path,image_path2)
        
        print("Image paths:", image_path, image_path2)
        print("Processor created") 
        
        try:
            if 'rgb' in request.form:
                processor.convert_to_rgb()
            if 'grayscale' in request.form:
                processor.convert_to_grayscale()
            if 'binary' in request.form:
                threshold = request.form.get('threshold', '')
                try:
                    threshold_value = int(threshold)
                    processor.convert_to_binary(threshold_value)
                except ValueError:
                    pass
            if 'brightness_contrast' in request.form:
                alpha = request.form.get('alpha', '')
                beta = request.form.get('beta', '')
                try:
                    alpha_value = float(alpha)
                    beta_value = int(beta)
                    processor.adjust_brightness_contrast(alpha_value, beta_value)
                except ValueError:
                    pass
            if 'annotation' in request.form:
                if 'line' in request.form:
                    if 'line_start_x' in request.form and 'line_start_y' in request.form and request.form['line_start_x'] and request.form['line_start_y']:
                        start_point = (int(request.form['line_start_x']), int(request.form['line_start_y']))
                        end_point = (int(request.form['line_end_x']), int(request.form['line_end_y']))
                        processor.add_line(start_point, end_point)
                if 'rectangle' in request.form:
                    if 'rect_start_x' in request.form and 'rect_start_y' in request.form and request.form['rect_start_x'] and request.form['rect_start_y']:
                        start_point = (int(request.form['rect_start_x']), int(request.form['rect_start_y']))
                        end_point = (int(request.form['rect_end_x']), int(request.form['rect_end_y']))
                        processor.add_rectangle(start_point, end_point)
                if 'circle' in request.form:
                    if 'circle_center_x' in request.form and 'circle_center_y' in request.form and request.form['circle_center_x'] and request.form['circle_center_y']:
                        center = (int(request.form['circle_center_x']), int(request.form['circle_center_y']))
                        radius = int(request.form['circle_radius'])
                        processor.add_circle(center, radius)
                if 'text' in request.form:
                    if 'text_x' in request.form and 'text_y' in request.form and request.form['text_x'] and request.form['text_y'] and 'text' in request.form:
                        print("Text position and content provided")  # Debug statement
                        text = request.form['text']
                        org = (int(request.form['text_x']), int(request.form['text_y']))
                        print("Text:", text)  # Debug statement
                        print("Position (x, y):", org)  # Debug statement
                        processor.add_text(text, org)

            if 'crop' in request.form:
                if all(k in request.form for k in ('crop_x', 'crop_y', 'crop_width', 'crop_height')):
                    x = int(request.form['crop_x'])
                    y = int(request.form['crop_y'])
                    width = int(request.form['crop_width'])
                    height = int(request.form['crop_height'])
                    processor.crop(x, y, width, height)
            if 'resize' in request.form:
                if all(k in request.form for k in ('resize_width', 'resize_height')):
                    width = int(request.form['resize_width'])
                    height = int(request.form['resize_height'])
                    processor.resize(width, height)
            if 'scale' in request.form:
                factor = request.form.get('scale_factor', '')
                try:
                    factor_value = float(factor)
                    processor.scale(factor_value)
                except ValueError:
                    pass
            if 'flip' in request.form:
                direction = request.form.get('flip_direction', '')
                try:
                    direction_value = int(direction)
                    processor.flip(direction_value)
                except ValueError:
                    pass
            if 'add' in request.form:
                value = request.form.get('add_value', '')
                try:
                    value = int(value)
                    processor.add(value)
                except ValueError:
                    pass
            if 'subtract' in request.form:
                value = request.form.get('subtract_value', '')
                try:
                    value = int(value)
                    processor.subtract(value)
                except ValueError:
                    pass
            if 'multiply' in request.form:
                value = request.form.get('multiply_value', '')
                try:
                    value = float(value)
                    processor.multiply(value)
                except ValueError:
                    pass
            if 'contrast' in request.form:
                alpha = request.form.get('contrast_alpha', '')
                try:
                    alpha_value = float(alpha)
                    processor.adjust_contrast(alpha_value)
                except ValueError:
                    pass
            if 'threshold' in request.form:
                threshold = request.form.get('threshold_value', '')
                try:
                    threshold_value = int(threshold)
                    processor.threshold(threshold_value)
                except ValueError:
                    pass
            
            if 'operation' in request.form:
                if processor.image.shape != processor.other_image.shape:
                    processor.resize(width=processor.other_image.shape[1], height=processor.other_image.shape[0])

                    
                if 'bitwise_and' in request.form:
                
                    processor.bitwise_and(processor.other_image)
                
                if 'bitwise_or' in request.form:
                        processor.bitwise_or(processor.other_image)
                
                if 'bitwise_xor' in request.form:
                    processor.bitwise_xor(processor.other_image)
                
                if 'bitwise_not' in request.form:
                        processor.bitwise_not()

            
            processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
            
            print("Processed image path:", processed_image_path)
            print("About to save processed image")
            
            cv2.imwrite(processed_image_path, processor.image)
            
            print("Processed image saved")
            
            return redirect(url_for('show_processed_image', filename='processed_' + filename))
        except Exception as e:
            print("An error occurred during image processing:", e)
            return render_template('error.html', error=str(e))
    return render_template('process.html', filename=filename,filename2=filename2)

@app.route('/show_processed/<filename>')
def show_processed_image(filename):
    return render_template('show_processed.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
