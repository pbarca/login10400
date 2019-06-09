from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


def herokudb():
    Host = 'ec2-54-75-238-138.eu-west-1.compute.amazonaws.com'
    Database = 'dc2a08o9htumor'
    User = 'gdsgmkwokjvdiw'
    Password = '00b7fdc9304e7fdd19305955324e6e029cd6a3821e3131aae973d7d7a8168d1b'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password)


def gravar(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (usr text, pwd text)")
    db.execute("INSERT INTO usr VALUES ( %s, %s)", (v1, v2))
    ficheiro.commit()
    ficheiro.close()
    return


def alterar(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET pwd = %s WHERE usr = %s", (v2, v1))
    ficheiro.commit()
    ficheiro.close()
    return


def existe(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE usr = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor = None
    return valor


def eliminar(v1):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE usr = %s", (v1,))
    ficheiro.commit()
    ficheiro.close()
    return


def log(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE usr = %s and pwd = %s", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


@app.route('/newpass', methods=['POST', 'GET'])
def newpass():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
            erro = 'A palavra passe foi alterada.'
    return render_template('newpass.html', erro=erro)


@app.route('/registo', methods=['POST', 'GET'])
def registo():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if existe(v1):
            erro = 'O Utilizador já existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2)
            erro = 'Utilizador registado com Sucesso.'
    return render_template('registo.html', erro=erro)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A senha está incorreta.'
        else:
            erro = 'Bem-vindo.'
    return render_template('login.html', erro=erro)


@app.route('/apagar', methods=['POST', 'GET'])
def apagar():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A senha está incorreta.'
        else:
            eliminar(v1)
            erro = 'Conta eliminada com Sucesso.'
    return render_template('apagar.html', erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
