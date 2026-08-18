import datetime
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

# 仅对 API 开放跨域；网页本身通过同源接口调用后端。
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.root_path, "index.html")


@app.route("/health", methods=["GET"])
def health():
    return "oracle backend alive"


def get_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY 环境变量")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

@app.route('/api/meihua', methods=['POST'])
def meihua_qigua():
    data = request.get_json(silent=True) or {}
    city = data.get("city", "深圳")
    user_goal = data.get("goal", "未说明")
    
    # 1. 计算真太阳时
    geo_map = {"深圳": 114.05, "合肥": 117.27, "北京": 116.40, "上海": 121.47}
    lng = geo_map.get(city, 120.0)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    bj_time = now_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    solar_diff = (lng - 120) * 4
    solar_time = bj_time + datetime.timedelta(minutes=solar_diff)
    
    # 2. 锁定你最满意的解卦逻辑
    system_prompt = """
    # Role: 「六爻 × 人生潮汐」深度解卦引擎（硬核版）
    你是一位精通《增删卜易》的断卦宗师。
    
    【核心任务】
    你的目标不是简单的翻译，而是根据卦象技术指标，为用户的“心中所求”提供精准的商业/情感逻辑支撑。
    
    【输出结构 - 严格执行】
    ### 【一】 卦象构造与古籍回响
    * 描述卦象（本卦、变卦、关键动爻）。
    * **必须引用**《增删卜易》或《卜筮正宗》的原典断语。
    * 白话转译：解释这句古文在逻辑上如何成立。

    ### 【二】 人生潮汐定位
    * 根据世爻、动爻的状态，定义当前相位（潜龙在渊、飞龙在天等）。
    * 技术锚点：简述理由（如：月破代表能量溃散，旬空代表暂时失实）。

    ### 【三】 深度节律解析（核心：必须结合心中所求）
    * **深度结合用户问的事情**，将古籍中的吉凶转化为“能量趋势”。
    * 如果用户问事业，就谈职场势能；问情感，就谈关系张力。
    * 解释当前是应该“顺流而下”还是“逆流调整”。

    ### 【四】 典籍赠言
    * 结合卦辞，给出一句深邃、温暖且有力量的建议。必须针对“心中所求”给出一个具体的心理导向。
    """
    
    user_prompt = f"""
    【时刻】北京时间 {bj_time.strftime('%Y-%m-%d %H:%M')} (准太阳时 {solar_time.strftime('%H:%M')})
    【地点】{city}
    【心中所求】{user_goal}
    
    请严格按照以上四个板块，为用户进行全中文深度解读。
    """

    try:
        client = get_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        return jsonify({
            "ok": True, 
            "result": response.choices[0].message.content,
            "solar_time": solar_time.strftime('%H:%M')
        })
    except Exception as e:
        # 增加错误捕获，方便手机端排查
        return jsonify({"ok": False, "result": f"时空链路异常: {str(e)}"})

if __name__ == '__main__':
    # 获取服务器分配的端口，如果没有就默认 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
