from flask import Flask, render_template
import atexit # 애플리케이션 종료시 실행을 요청 (ex. DB연결 종료)

app = Flask(__name__)  # Flask 앱 초기화

# 조회
@app.route('/maptest', methods=['GET'])
def index():
    return render_template('maptest.html')

if __name__ == '__main__':
    app.run(port=8888, debug=True) 
