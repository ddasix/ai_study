from flask import Flask, render_template, request, session, redirect
import pymysql
import time

from module import db_module

app = Flask(__name__)
app.secret_key = 'ddasix_key'

@app.route('/admin', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('/admin/screens/login/login.html')
    elif request.method == 'POST':
        userid = request.form['userid']
        userpw = request.form['userpw']
        print('{},{}'.format(userid, userpw))

        db = db_module.Database()

        sql = """
            select
                name, level, img
            from
                member
            where
                userid = '%s' and userpw = password('%s')
        """ % (userid, userpw)

        rows = db.executeOne(sql)

        print(rows)
        
        if rows:
            session['session_id'] = userid
            session['session_name'] = rows['name']
            session['session_level'] = rows['level']
            session['session_img'] = rows['img']

            return redirect('/admin/main')
        else:
            return render_template('/admin/screens/login/login.html', msg='아이디 또는 비밀번호를 확인해주세요.')

@app.route('/admin/main')
def admin_main():
    if session['session_id'] == False:
        return redirect('/admin')
    else:
        member = {
            'name': session['session_name'],
            'level': session['session_level'],
            'avatar': session['session_img'],
        }
        return render_template('/admin/screens/main/main.html', member = member)

@app.route('/admin/logout')
def admin_logout():
    session = False
    return redirect('/admin')