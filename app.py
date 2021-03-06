# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, session
from models.executeSqlite3 import executeSelectOne, executeSelectAll, executeSQL
from functools import wraps
from models.user_manager import UserManager
from models.user_type_manager import UserTypeManager
from models.base_manager import SNBaseManager
import os
# створюємо головний об'єкт сайту класу Flask
from models.post_manager import PostManager
from models.user_friend_manager import UserRelationManager
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


# добавляємо секретний ключ для сайту щоб шифрувати дані сессії
# при кожнаму сапуску фласку буде генечитись новий рандомний ключ з 24 символів
app.secret_key = os.urandom(24)
# app.secret_key = '125'


# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_SERVER'] = 'smtp.ukr.net'
#якщо не працює то міняти порт на 465 або на 587 і коментувати use tls  abo use ssl
app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ustym.hanyk@ukr.net'
app.config['MAIL_PASSWORD'] = 'dfgfsggfgsbsbfgfsgsgsgsfgsfgsdfgfsdghgsh'
mail = Mail(app)
mail.init_app(app)

socketio = SocketIO(app)
socketio.init_app(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            if UserManager.load_models.get(session['username'], None):
                return f(*args, **kwargs)
        return redirect(url_for('login'))
    return wrap
@app.route('/group')
@login_required
def group():

    return render_template('group.html')
@app.route('/chat')
@login_required
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = UserManager.load_models[session['username']]
    # session['username'] = 'test name'
    session['room'] = 'test room'
    # name = session.get('username', '')
    room = session.get('room', '')
    return render_template('chat.html', name=name, room=room)

# @app.route('/chat/<chat_id>',methods=['POST']) #як зробити щоб воно сюди видавало id чату
# @login_required
# def private_room():
#         context = {}
#         login_user_manager = UserManager.load_models[session['username']]
#         context['loginUser'] = login_user_manager
#         login_user_id = login_user_manager.object.id
#         search_user_manager = UserManager()
#         # nickname = #як сюди передати нік того юзера на сторінці якого ми були?
#         search_user_manager.select().And([('nickname','=',nickname)]).run()
#         search_user_id = search_user_manager.object.id
#         context['user'] = search_user_manager
#         relation = UserRelationManager()
#         if relation.isFriend(login_user_id,search_user_id):
#             if not relation.isFriend(login_user_id,search_user_id):
#                 return redirect(url_for('/'))
#             user_id = int(request.form.get('id', 0))
#             user = UserManager.load_models[session['username']]
#             user.create_room(id=user_id)
#         return redirect(url_for('/chat/<name>'))

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    print(session.get('username'))
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room,broadcast=True)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    print(session.get('username'))
    emit('message', {'msg': session.get('username') + ':' + message['msg']}, room=room,broadcast=True)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('username') + ' has left the room.'}, room=room,broadcast=True)

@app.route("/msg")
def send_msg():
    msg = Message("Thanks for registration",
                  sender="ustym.hanyk@ukr.net",
                  recipients=["bozayats@gmail.com"])
    mail.send(msg)
    return redirect('request.referrer')



# @app.route('/quick_login', methods=["GET", "POST"])
# def logins():
#         # якщо метод пост дістаємо дані з форми і звіряємо чи є такий користвач в базі данних
#         # якшо є то в дану сесію добавляєм ключ username
#         # і перекидаємо користувача на домашню сторінку
#         user = UserManager()
#         if user.quickloginUser:
#             addToSession(user)
#         return redirect(url_for('home'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # якщо метод пост дістаємо дані з форми і звіряємо чи є такий користвач в базі данних
        # якшо є то в дану сесію добавляєм ключ username
        # і перекидаємо користувача на домашню сторінку
        user = UserManager()
        if user.loginUser(request.form):
            addToSession(user)
            return redirect(url_for('home'))

    return render_template('login.html')




# описуємо роут для вилогінення
# сіда зможуть попадати тільки GET запроси
@app.route('/logout')
@login_required
def logout():
    user = session.get('username', None)
    if user:
        # якщо в сесії є username тоді видаляємо його
        del session['username']
    return redirect(url_for('login'))

@app.route('/del_follow/<search_user_id>',methods=['POST'])
@login_required
def del_follow(search_user_id):
    login_user_manager = UserManager.load_models[session['username']]
    login_user_id = login_user_manager.object.id
    rel = UserRelationManager()
    # fol = rel.isFollower(login_user_id, search_user_id)
    rel.delete().And([('user1', '=', login_user_id), ('user2', '=', search_user_id)]).run()
    return redirect(request.referrer)

@app.route('/<nickname>',methods=['GET'])
@login_required
def user_page(nickname):
    context = {}
    login_user_manager = UserManager.load_models[session['username']]
    context['loginUser'] = login_user_manager
    login_user_id = login_user_manager.object.id
    search_user_manager = UserManager()
    search_user_manager.select().And([('nickname','=',nickname)]).run()
    search_user_id = search_user_manager.object.id
    context['user'] = search_user_manager
    relation = UserRelationManager()
    # fol = relation.isFollower(login_user_id,search_user_id)
    # context["fol"] = fol
    if relation.isFollower(login_user_id,search_user_id):
        context["friend_button_name"] = 'Cancel request'
    elif relation.isFollowed(login_user_id,search_user_id):
        context["friend_button_name"] = 'Accept request'
    elif relation.isFriend(login_user_id,search_user_id):
        context["friend_button_name"] = 'Is Friends'
    elif not relation.isFriend(login_user_id,search_user_id):
        context["friend_button_name"] = 'Isnt Friends'
    return render_template('home.html', context=context)
# @app.route('/<nickname>',methods=['GET'])
# @login_required
# def user_page(nickname):
#     context = {}
#     if session.get('username', None):
#         user = UserManager.load_models[session['username']]
#         context['loginUser'] = user
#     user_one = user.object.id
#     selectUser = UserManager()
#     selectUser.select().And([('nickname','=',nickname)]).run()
#     context['user'] = selectUser
#     rel = UserRelationManager()
#     # rel.object.user_one
#     friend_checker = rel.isFollower(user_one,selectUser)
#     context['friend_checker'] = friend_checker
#     return render_template('home.html', context=context)

# описуємо домашній роут
# сіда зможуть попадати тільки GET запроси
@app.route('/')
@login_required
def home():
    context = {}
    if session.get('username', None):
        user = UserManager.load_models[session['username']]
        # якщо в сесії є username тоді дістаємо його дані
        # добавляємо їх в словник для передачі в html форму
        context['user'] = user
        context['loginUser'] = user
    return render_template('home.html', context=context)


def addToSession(user):
    session['username'] = user.object.nickname


@app.route('/registration', methods=["GET", "POST"])
def registr():
    context = {'Error': []}
    user_type = UserTypeManager()
    user_type.getTypeUser()
    if session.get('username', None):
        user = UserManager.load_models[session['username']]
        user_type.getTypeGroup()
        context['user'] = user
    context['type'] = user_type

    if request.method == 'POST':
        user = UserManager().getModelFromForm(request.form)
        if user.check_user():
            context['Error'].append('wrong name or email')
        if user.object.type.type_name == 'user':
            if not user.object.password :
                context['Error'].append('incorrect password')
        if context['Error']:
            return render_template('registration.html', context=context)
        if user.save():
            UserManager.load_models[user.object.nickname] = user
            addToSession(user)
            return redirect(url_for('home'))
        context['Error'].append('incorrect data')
    return render_template('registration.html', context=context)

@app.route('/add_post', methods=['GET','POST'])
@login_required
def add_post():
    if request.method == 'POST':
        post = PostManager()
        print(list(request.form.keys()))
        user = UserManager.load_models[session['username']]
        post.save_post(request.form, user)
    return render_template('add_post.html')

@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    context = {}
    user = UserManager.load_models[session['username']]
    context['user'] = user
    if request.method == 'POST':
        user.getModelFromForm(request.form)
        user.save()
    return render_template('edit.html', context=context)

@app.route('/block_friend', methods=['POST'])
@login_required
def block_friend():
    user_id = int(request.form.get('id', 0))
    user = UserManager.load_models[session['username']]
    user.block_friend(id=user_id)
    return redirect(request.referrer)

@app.route('/delete_friend', methods=['POST'])
@login_required
def delete_friend():
    user_id = int(request.form.get('id', 0))
    user = UserManager.load_models[session['username']]
    user.del_friend(id=user_id)
    return redirect(request.referrer)
# @app.route('/add_friend', methods=['POST'])
# @login_required
# def add_friend():
#     user_id = int(request.form.get('id', 0))
#     user = UserManager.load_models[session['username']]
#     user.create_room(id=user_id)
#     return redirect(request.referrer)

@app.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    user_id = int(request.form.get('id',0))
    user = UserManager.load_models[session['username']]
    user.add_friend(id=user_id)
    return redirect(request.referrer)

@app.route('/accept_friend_request', methods=['POST'])
@login_required
def accept_friend_request():
    user_id = int(request.form.get('id', 0))
    user = UserManager.load_models[session['username']]
    user.accept_friend_request(id=user_id)
    return redirect(request.referrer)

@app.route('/friend_list',methods=['POST'])
@login_required
def view_friends():

    return render_template(home.html)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=7485)
