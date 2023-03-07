from app_web import app
from flask import render_template, request, redirect, flash, session
from app_web.models.participante import Participante
from app_web.config.payment import procesar
from app_web.models.user import User
from app_web.models.post import Post
import json
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

app.secret_key = 'secret_key'

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/noticias')
def news():
   posts = Post.get_posts()
   return render_template('noticias.html', posts = posts)

@app.route('/galeria')
def gallery():
   return render_template('galeria.html')

@app.route('/inscripcion', methods=['POST', 'GET'])
def inscription():
   if request.method=='POST':

      name = request.form['name']
      document = request.form['tipo_documento']
      n_document = request.form['documento']
      country = request.form['pais']
      city = request.form['ciudad']
      mail = request.form['email']
      phone = request.form['telefono']
      institution = request.form['institucion']
      ocupation = request.form['ocupacion']
      payment = request.form.get('forma_pago')
      participation = request.form['participacion']
      conference = request.form.get('ponencia')
      english = request.form.get('ingles')
      comment = request.form.get('comentario')
      nombre_razon_social = request.form.get('nombre_razon_social')
      ruc = request.form.get('ruc')
      if conference == '':
         conference = None
      if english == '':
         english = None
      if comment == '':
         comment = None
      if nombre_razon_social == '':
         nombre_razon_social = None
      if ruc == '':
         ruc = None

      data = {
         'name': name,
         'document': document,
         'n_document': n_document,
         'country': country,
         'city': city,
         'mail': mail,
         'phone': phone,
         'institution': institution,
         'ocupation': ocupation,
         'payment': payment,
         'participation': participation,
         'conference': conference,
         'english': english,
         'comment': comment,
         'nombre_razon_social': nombre_razon_social,
         'ruc': ruc
      }

      if Participante.validate_form(request.form):
         id = Participante.save(data)
         response, f_pago = procesar(data, id)
         all = json.loads(response)
         if all['respuesta'] == True or all['respuesta'] == "true":
            #si la respuesta es true me redirecciona a la pagina de pago
            token_received = all['resultado'][0]['data']
            return render_template("redirect.html", token_received=token_received, f_pago=f_pago)
         else:# de ser falso me recarga la pagina y me salta un mensaje
            flash("El pago no se ha realizado. Vuelva a intentarlo porfavor.")
            return redirect('/inscripcion')
      else:
         flash("Los datos no son correctos")

   return render_template('form_inscripcion.html')

@app.route('/respuesta', methods=['POST'])
def reply_pagopar():
   data = request.get_json()
   #TODO: Colocar datos de la transaccion en la BD
   return json.dumps(data['resultado'])

@app.route('/login', methods=['POST', 'GET'])
def login():
   if not session.get('user_id') == None:
      return redirect('/dashboard')
   else:
      if request.method == 'POST':
         # ver si el correo de usuario proporcionado existe en la base de datos
         data = {
            "email" : request.form.get("email")
         }
         user_in_db = User.get_by_email(data)
         # usuario no está registrado en la base de datos
         if not user_in_db:
            flash("Email/Password erroneos")
            return redirect("/login")
         if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            # si obtenemos False después de verificar la contraseña
            flash("Email/Password erroneos")
            return redirect('/login')
         # si las contraseñas coinciden, configuramos el user_id en sesión
         session['user_id'] = user_in_db.id
         return redirect("/dashboard")
      else:
         return render_template('login.html')

#-----------------DASHBOARD-----------------#

@app.route('/dashboard')
def dashboard():
   if session.get('user_id') == None:
      return redirect('/login')
   else:
      return render_template('dashboard.html')

@app.route('/dashboard/post')
def post():
   posts = Post.get_posts()
   return render_template('post.html', posts=posts)

@app.route('/dashboard/post_add')
def post_add():
   return render_template('post_add.html')

@app.route('/dashboard/post_edit/<int:id>')
def post_edit(id):

   data = {
      'id': id
   }
   post = Post.getPostById(data)

   return render_template('post_edit.html', post = post)

@app.route('/dashboard/update_post/<int:id>', methods=['POST','GET'])
def update_post(id):
   if request.method == 'POST':
      datos ={
         "id": id,
         "titulo" : request.form['titulo'],
         "cuerpo" : request.form['cuerpo']
      }
      
      Post.update(datos)
      return redirect('/dashboard/post')

@app.route('/dashboard/add_post', methods=['POST','GET'])
def add_post():
   if request.method == 'POST':
      data ={
         "titulo" : request.form['titulo'],
         "cuerpo" : request.form['cuerpo']
      }
      Post.save(data)
      return redirect('/dashboard/post')
   else:
      return redirect('/dashboard/post_add')

@app.route('/dashboard/usuarios')
def user_list():
   usuarios = User.get_all_users()
   return render_template('usuarios.html', usuarios=usuarios)

@app.route('/dashboard/usuarios/add')
def user_add():
   return render_template('user_add.html')

@app.route('/dashboard/register', methods=['POST','GET'])
def register():
   if request.method == 'POST':
      if request.form['password'] == request.form['cpassword']:
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            data = {
               "username" : request.form['username'],
               "email" : request.form['email'],
               "passw" : pw_hash
            }
            if User.validar_usuario(request.form):
               usuario = User.save_user(data)
               session['id'] = usuario.id
               return redirect('/dashboard/usuarios')
            else:
               return redirect('/dashboard/usuarios/add')
      else:
            flash("Password must be the same")
            return redirect('/dashboard/usuarios/add')
            
   return redirect('/dashboard/usuarios')

@app.route('/dashboard/logout')
def logout():
   session.clear()
   return redirect('/login')