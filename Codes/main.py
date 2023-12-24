# İçeri Aktarma
from flask import Flask, render_template,request, redirect
# Veritabanı kütüphanesini içe aktarma
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# SQLite ile bağlantı kurma 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gunluk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB oluşturma
db = SQLAlchemy(app)

#Görev #1. DB tablosu oluşturma

class Gunluk(db.Model):
    #Gunlugun numarasi
    id = db.Column(db.Integer, primary_key=True)
    
    #Gunlugun basligi
    title = db.Column(db.String(100), nullable=False)
    
    #Gunlugun altbasligi
    subtitle = db.Column(db.String(100), nullable=False)
    
    #Gunlugun yazisi
    text = db.Column(db.String(400), nullable=False)



with app.app_context():
    db.create_all()





# İçerik sayfasını çalıştırma
@app.route('/')
def index():
    # DB nesnelerini görüntüleme
    # Görev #2. DB'deki nesneleri index.html'de görüntülem
    gunlukler = Gunluk.query.order_by(Gunluk.id).all()

    return render_template('index.html',
                           #kartlar = kartlar
                            gunlukler=gunlukler
                           )

# Kartla sayfayı çalıştırma
@app.route('/card/<int:id>')
def card(id):
    # Görev #2. Id'ye göre doğru kartı görüntüleme
    gunluk = Gunluk.query.get(id)

    return render_template('card.html', gunluk=gunluk)

# Sayfayı çalıştırma ve kart oluşturma
@app.route('/create')
def create():
    return render_template('create_card.html')

# Kart formu
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Görev #2. Verileri DB'de depolamak için bir yol oluşturma
        gunluk = Gunluk(title=title, subtitle=subtitle, text=text)
        db.session.add(gunluk)
        db.session.commit()




        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
