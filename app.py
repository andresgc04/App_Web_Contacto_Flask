from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

#MySQL Connection:
def connection():
    server = 'localhost'
    user = 'root'
    password = ''
    db = 'flask_contacts_db'
    charset = 'utf8mb4'

    return pymysql.connect(host=server, user=user, password=password, database=db, charset=charset)


app = Flask(__name__)

#Settings:
app.secret_key = 'mySecretKey'

@app.route('/')
def index():

    connection_db = connection()

    with connection_db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT contact_id, full_name, phone_number, email FROM contacts')
        contacts_data = cursor.fetchall()

    return render_template('index.html', contacts_data = contacts_data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':

        connection_db = connection()

        fullName = request.form['fullName']
        phoneNumber = request.form['phoneNumber']
        email = request.form['email']

        with connection_db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                'INSERT INTO contacts (full_name, phone_number, email) VALUES (%s, %s, %s)', (fullName, phoneNumber, email))

            connection_db.commit()

        flash('Contacto Agregado Satisfactoriamente.')

        return redirect(url_for('index'))


@app.route('/edit/<contact_id>')
def get_contact(contact_id):

    connection_db = connection()

    with connection_db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT contact_id, full_name, phone_number, email FROM contacts WHERE contact_id = %s', (contact_id))

        contact_data = cursor.fetchall()

        return render_template('edit-contact.html', contact_data = contact_data[0])
    
@app.route('/update_contact/<contact_id>', methods=['POST'])
def update_contact(contact_id):

    if request.method == 'POST':

        full_name = request.form['fullName']
        phone_number = request.form['phoneNumber']
        email = request.form['email']
        
        connection_db = connection()
        
        with connection_db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('UPDATE contacts SET full_name = %s, phone_number = %s, email = %s WHERE contact_id = %s', (full_name, phone_number, email, contact_id))

            connection_db.commit()

        flash('Contacto Modificado Satisfactoriamente.')

        return redirect(url_for('index'))


@app.route('/delete/<string:contact_id>')
def delete_contact(contact_id):

    connection_db = connection()

    with connection_db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('DELETE FROM contacts WHERE contact_id = {0}'.format(contact_id))

        connection_db.commit()
    
    flash('Contacto Eliminado Satisfactoriamente.')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
