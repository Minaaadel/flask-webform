from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# الاتصال بقاعدة البيانات
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789',         # غيّرها لو عندك باسورد
        database='tast_1'
    )

# الصفحة الرئيسية - فقط للتأكد من تشغيل السيرفر
@app.route('/')
def home():
    return '✅ Flask server is running and ready to receive data!'

# الراوت اللي بيستقبل البيانات من الفورم (GET للمراجعة، POST للإرسال)
@app.route('/save-data', methods=['GET', 'POST'])
def save_data():
    if request.method == 'GET':
        return '''
        <h3>📥 برجاء استخدام POST لإرسال البيانات</h3>
        <form method="POST">
          الاسم: <input type="text" name="name"><br>
          الإيميل: <input type="email" name="email"><br>
          <input type="submit" value="إرسال">
        </form>
        '''

    # استقبال البيانات من POST
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        return '❌ الاسم أو الإيميل ناقصين', 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        conn.close()
        return '✅ تم حفظ البيانات بنجاح!'
    except Exception as e:
        return f'❌ حصل خطأ: {str(e)}', 500

# تشغيل السيرفر
if __name__ == '__main__':
    app.run(debug=True)
