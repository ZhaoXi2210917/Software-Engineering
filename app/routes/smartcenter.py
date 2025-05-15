from flask import Blueprint, jsonify, render_template,request
from app.Kimi.train import predict_species_length
from app.Kimi.chat import chat as bchat
from app.Kimi.image import process_image_with_question
import os

bp = Blueprint('smartcenter',__name__)

# 定义上传文件夹路径
UPLOAD_FOLDER = 'app/upload'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 如果文件夹不存在，则创建

# 智能中心
@bp.route('/smartcenter')
def smartcenter():
    return render_template('smartcenter.html')

# 养殖趋势预测
@bp.route('/trend_analysis')
def trend_analysis():
    return render_template('trend_analysis.html')

# 风险评估
@bp.route('/risk_assessment')
def risk_assessment():
    return render_template('risk_assessment.html')

# 决策支持
@bp.route('/decision_support')
def decision_support():
    return render_template('decision_support.html')

# 处理用户的预测请求，能用
@bp.route('/length_predict')
def length_predict():
    return render_template('length_predict.html')

@bp.route('/predict', methods=['POST'])
def predict():
    try:
        # 兼容 fishType 和 species，防止前端字段不一致
        species = request.json.get('species') or request.json.get('fishType', '')
        length1 = request.json.get('length1', '')
        length2 = request.json.get('length2', '')

        species = str(species).strip()
        length1 = str(length1).strip()
        length2 = str(length2).strip()

        # 校验输入
        if not species or not length1 or not length2:
            return jsonify({"error": "All fields are required."}), 400

        try:
            length1 = float(length1)
            length2 = float(length2)
        except ValueError:
            return jsonify({"error": "Length1 and Length2 must be valid numbers."}), 400

        # 调用预测函数
        prediction = predict_species_length(species, length1, length2)

        return jsonify({
            "fish_type": species,
            "length3": prediction
        })
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# 对话
@bp.route('/chat.html')
def chat():
    return render_template('chat.html')

@bp.route('/chat', methods=['POST'])
def chat_route():
    try:
        # 获取用户输入
        user_message = request.json.get('message', '').strip()
        print(f"User message: {user_message}")  # 调试输出

        # 校验输入
        if not user_message:
            return jsonify({"error": "Message field is required."}), 400

        # 调用 chat 函数处理对话
        #print("=+++===++++")
        try:
            response_message = bchat(user_message)
            #print("===============")
        except Exception as e:
            print(f"bchat error: {e}")  # 加上这行
            return jsonify({"error": f"Failed to process chat: {str(e)}"}), 500
        print(f"Response message: {response_message}")  # 调试输出
        print("===============")
        # 返回对话结果
        return jsonify({
            "user_message": user_message,
            "reply": response_message
        })
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# 图片上传和处理
@bp.route('/image')
def image():
    return render_template('image.html')

@bp.route('/upload', methods=['POST'])
def upload():
    try:
        # 获取上传的图片和问题
        image_file = request.files.get('image')
        question = request.form.get('question')

        if not image_file or not question:
            return jsonify({"error": "图片和问题均为必填项"}), 400

        # 保存图片到指定文件夹
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)  # 图片保存逻辑在这里

        # 调用处理函数
        answer = process_image_with_question(image_path, question)

        # 返回结果
        return jsonify({"reply": answer})

    except Exception as e:
        print(f"Error in /upload route: {e}")
        return jsonify({"error": "服务器内部错误"}), 500