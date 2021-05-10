from flask import Flask, flash, render_template, request, session, redirect
import pymysql
import time
import os
from PIL import Image as PILImage

from module import db_module

app = Flask(__name__)
app.secret_key = 'ddasix_key'

upload_url="static/upload/news/"

@app.route('/admin', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('/admin/screens/login/login.html')
    elif request.method == 'POST':
        userid = request.form['userid']
        userpw = request.form['userpw']

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
        bread_crumbs = [
            {
                'href': '/admin/main',
                'label': 'Home'
            },
            {
                'href': '',
                'label': 'Starter Page'
            }
        ]
        return render_template('/admin/screens/main/main.html', member = member, variable=1234, bread_crumbs=bread_crumbs, title='Starter Page')

@app.route('/admin/news')
def admin_news_list():
    if session['session_id'] == False:
        return redirect('/admin')
    else:
        db = db_module.Database()

        sql = """
            select
                *
            from
                news
            order by
                id desc
        """

        rows = db.executeAll(sql)

        bread_crumbs = [
            {
                'href': '/admin/main',
                'label': 'Home'
            },
            {
                'href': '',
                'label': '뉴스관리'
            }
        ]
        return render_template('/admin/screens/news/list.html', news_items=rows, bread_crumbs=bread_crumbs, title='뉴스관리')

@app.route('/admin/news/<news_id>')
def admin_news(news_id):
    if news_id == None:
        return redirect('/admin/news')
    else:
        sql = """
        select
            *
        from
            news
        where
            id = '%s'
        """ % (news_id)
        db = db_module.Database()
        news_item = db.executeOne(sql)

        bread_crumbs = [
            {
                'href': '/admin/main',
                'label': 'Home'
            },
            {
                'href': '/admin/news',
                'label': '뉴스관리'
            },
            {
                'href': '',
                'label': 'News'
            }
        ]
        return render_template('/admin/screens/news/detail.html', news_item=news_item, bread_crumbs=bread_crumbs, title='News')


@app.route('/admin/news/<news_id>/edit', methods=['GET'])
def admin_news_edit(news_id):
    if session['session_id'] == False:
        return redirect('/admin')

    if news_id == None:
        return redirect('/admin/news')
    else:
        sql = """
            select
                *
            from
                news
            where
                id = '%s'
            """ % (news_id)
        db = db_module.Database()
        news_item = db.executeOne(sql)

        if news_item['userid'] != session['session_id']:
            flash('작성권한이 없습니다.')
            return redirect(request.referrer)
        else:

            bread_crumbs = [
                {
                    'href': '/admin/main',
                    'label': 'Home'
                },
                {
                    'href': '/admin/news',
                    'label': '뉴스관리'
                },
                {
                    'href': '',
                    'label': '뉴스수정'
                }
            ]
            return render_template('/admin/screens/news/edit.html', news_item=news_item, bread_crumbs=bread_crumbs,title='뉴스수정')


@app.route('/admin/news/edit', methods=['POST'])
def admin_news_update():
    if session['session_id'] == False:
        return redirect('/admin')
    if request.method == 'POST':
        sql = """
            select
                *
            from
                news
            where
                id = '%s'
            """ % (request.form['id'])
        db = db_module.Database()
        news_item = db.executeOne(sql)

        if news_item == None:
            flash('작성권한이 없습니다.')
            return redirect(request.referrer)

        if news_item['userid'] != session['session_id']:
            flash('작성권한이 없습니다.')
            return redirect(request.referrer)
        else:
            file = request.files['img1']
            now_datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            sql = """
                update news set
                    category='%s',
                    subject='%s',
                    content='%s',
                    name='%s',
                    userid='%s'
                """ % (
                    request.form['category'],
                    request.form['subject'].replace("'","\\'").replace('"', '\\"'),
                    request.form['content'].replace("'","\\'").replace('"', '\\"'),
                    session['session_name'],
                    session['session_id'],
                )

            if file:
                filename, ext = os.path.splitext(file.filename)
                file1 = now_datetime + ext
                file.save(upload_url + file1)

                # Large 이미지
                img1 = now_datetime + '_1' + ext
                with PILImage.open(upload_url + file1) as im:
                    im.thumbnail((1200,625))
                    im.save(upload_url + img1)
                # Middle 이미지
                img2 = now_datetime + '_2' + ext
                with PILImage.open(upload_url + file1) as im:
                    im.thumbnail((600,400))
                    im.save(upload_url + img2)
                # Small 이미지
                img3 = now_datetime + '_3' + ext
                with PILImage.open(upload_url + file1) as im:
                    im.thumbnail((120,90))
                    im.save(upload_url + img3)
                os.remove(upload_url + file1)
                sql = sql + ",img1='%s', img2='%s', img3='%s'" % (img1, img2, img3)

                if news_item['img1'] and os.path.exists(upload_url + news_item['img1']):
                    os.remove(upload_url + news_item['img1'])
                if news_item['img2'] and os.path.exists(upload_url + news_item['img2']):
                    os.remove(upload_url + news_item['img2'])
                if news_item['img3'] and os.path.exists(upload_url + news_item['img3']):
                    os.remove(upload_url + news_item['img3'])

            sql = sql + """ where id = '%s';""" % (request.form['id'])
            print(sql)
            db = db_module.Database()
            db.execute(sql)
            db.commit()
            return redirect('/admin/news/' + request.form['id'])

@app.route('/admin/news/<news_id>/delete')
def admin_news_delete(news_id):
    if session['session_id'] == False:
        return redirect('/admin')
    if news_id == None:
        return redirect('/admin/news')
    else:
        sql = """
            select
                *
            from
                news
            where
                id = '%s'
            """ % (news_id)
        db = db_module.Database()
        news_item = db.executeOne(sql)

        if news_item['userid'] != session['session_id']:
            flash('삭제권한이 없습니다.')
            return redirect('/admin/news')
        else:
            delete_sql = """
                delete from news
                where id = '%s'
            """ % (news_id)
            db = db_module.Database()
            db.execute(delete_sql)
            db.commit()

            if news_item['img1'] and os.path.exists(upload_url + news_item['img1']):
                os.remove(upload_url + news_item['img1'])
            if news_item['img2'] and os.path.exists(upload_url + news_item['img2']):
                os.remove(upload_url + news_item['img2'])
            if news_item['img3'] and os.path.exists(upload_url + news_item['img3']):
                os.remove(upload_url + news_item['img3'])
            return redirect('/admin/news')

@app.route('/admin/news/write', methods=['GET', 'POST'])
def admin_news_write():

    bread_crumbs = [
        {
            'href': '/admin/main',
            'label': 'Home'
        },
        {
            'href': '',
            'label': '뉴스관리'
        }
    ]

    if request.method == 'GET':
        
        bread_crumbs = [
            {
                'href': '/admin/main',
                'label': 'Home'
            },
            {
                'href': '/admin/news',
                'label': '뉴스관리'
            },
            {
                'href': '',
                'label': '기사쓰기'
            }
        ]
        return render_template('/admin/screens/news/write.html',bread_crumbs=bread_crumbs, title='뉴스관리')
    elif request.method == 'POST':
        file = request.files['img1']
        now_datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        sql = """
            insert into news set
                category='%s',
                subject='%s',
                content='%s',
                name='%s',
                userid='%s',
                comment = '%s'
            """ % (
                request.form['category'],
                request.form['subject'].replace("'","\\'").replace('"', '\\"'),
                request.form['content'].replace("'","\\'").replace('"', '\\"'),
                session['session_name'],
                session['session_id'],
                request.form['comment'].replace("'","\\'").replace('"', '\\"')
            )

        if file:
            filename, ext = os.path.splitext(file.filename)
            file1 = now_datetime + ext
            file.save(upload_url + file1)

            # Large 이미지
            img1 = now_datetime + '_1' + ext
            with PILImage.open(upload_url + file1) as im:
                im.thumbnail((1200,625))
                im.save(upload_url + img1)
            # Middle 이미지
            img2 = now_datetime + '_2' + ext
            with PILImage.open(upload_url + file1) as im:
                im.thumbnail((600,400))
                im.save(upload_url + img2)
            # Small 이미지
            img3 = now_datetime + '_3' + ext
            with PILImage.open(upload_url + file1) as im:
                im.thumbnail((120,90))
                im.save(upload_url + img3)
            os.remove(upload_url + file1)
            sql = sql + ",img1='%s', img2='%s', img3='%s'" % (img1, img2, img3)

        sql = sql + ';'
        db = db_module.Database()
        lastId = db.insert(sql)
        db.commit()

        return redirect('/admin/news/' + str(lastId))
    

@app.route('/admin/logout')
def admin_logout():
    session = False
    return redirect('/admin')