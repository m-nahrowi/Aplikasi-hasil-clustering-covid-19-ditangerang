from flask import render_template, redirect, session, url_for, flash, jsonify
from app.models.User import *
from app.controllers.algoritma import *
import bcrypt

import pandas as pd
import requests
from bs4 import BeautifulSoup
from functools import reduce

import os
import json

columns = [
	'Nama Desa','Suspek Aktif Dirawat', 'Konfirmasi Total', 
	'Konfirmasi Dirawat','Konfirmasi Sembuh', 'Konfirmasi Meninggal']

def index_front():
	geo_data = open('static/geo.json')
	geo_data = json.loads(geo_data.read())
	# algoritma = algoritm()
	label_data, df, hasil_label = algoritm()
	print('====== DATAFRAME =====')
	print(df)
	for f in range(len(geo_data['features'])):
		geo_kota = geo_data['features'][f]['properties']['name']
		search   = df.loc[df['Nama Desa'] == geo_kota]
		if search is not None:
			geo_data['features'][f]['properties']['cluster'] = search['clustering'].to_numpy()[0]
		else:
			geo_data['features'][f]['properties']['cluster'] = 0
	

	data       = list()
	_sum_data  = list()
	_total_sum = 0
	if(os.path.exists('static/data_covid_kota_tangearng.csv')):
		data        = pd.read_csv('static/data_covid_kota_tangearng.csv')
		_sum        = data.iloc[:,2:].sum(axis=0, skipna = True)
		_sum_column = data.iloc[:,2:].columns

		_sum_data = list()
		for n in range(len(_sum)):
			_sum_data.append({ 'key':_sum_column[n], 'val':_sum[n]})
			_total_sum += int(_sum[n])
	print('TOTAL SUM')
	print(_total_sum)
			
	return render_template('pages/frontend/index.html', 
		geo = geo_data, label_data=label_data, df=df,
		columns=columns, data=data, _sum_data=_sum_data, _total_sum=_total_sum)

def index():
	data = list()
	_sum_data = list()
	if(os.path.exists('static/data_covid_kota_tangearng.csv')):
		data = pd.read_csv('static/data_covid_kota_tangearng.csv')
		_sum        = data.iloc[:,2:].sum(axis=0, skipna = True)
		_sum_column = data.iloc[:,2:].columns

		_sum_data   = list()
		for n in range(len(_sum)):
			_sum_data.append({ 'key':_sum_column[n], 'val':_sum[n]})
		print(_sum_data)
	return render_template('pages/dashboard.html', columns=columns, data=data, _sum_data=_sum_data)


def scrapingData(is_redirect=True):
	respon    = requests.get('https://covid19.tangerangkota.go.id/')
	html_text = respon.text

	source       = BeautifulSoup(html_text, 'html.parser')
	tables_tag   = source.find_all('table')
	table_source = reduce(lambda x, y: x+y, map(lambda s: str(s), tables_tag))
	table_df     = pd.read_html(table_source)

	columns = [
	'Nama Desa','Suspek Aktif Dirawat', 'Konfirmasi Total', 
	'Konfirmasi Dirawat','Konfirmasi Sembuh', 'Konfirmasi Meninggal']

	table_df[0].index

	for df in table_df:
		df.drop(df.columns[[6, 7]], inplace=True, axis=1, )
		df.set_axis(columns, axis=1, inplace=True)
	dfs = pd.concat(table_df)
	dfs.reset_index(inplace=True)

	# dfs.filter(like='', axis=1)
	dfs.drop(dfs[dfs['Nama Desa'] == 'Total'].index, inplace=True)
	dfs.to_csv("static/data_covid_kota_tangearng.csv", index=False)
	if is_redirect == True:
		return redirect(url_for("index_admin"))
	else:
		return "OK"

def checkDataset():
	geo_data = open('static/geo.json', 'rb')
	geo_data = json.loads(geo_data.read())
	# algoritma = algoritm()
	label_data, df, hasil_label = algoritm()
	for f in range(len(geo_data['features'])):
		geo_kota = geo_data['features'][f]['properties']['name']
		search   = df.loc[df['Nama Desa'] == geo_kota]
		if search is not None:
			geo_data['features'][f]['properties']['cluster'] = int(search['clustering'].to_numpy()[0])
		else:
			geo_data['features'][f]['properties']['cluster'] = 0
	

	data       = list()
	_sum_data  = list()
	_total_sum = 0
	if(os.path.exists('static/data_covid_kota_tangearng.csv')):
		data        = pd.read_csv('static/data_covid_kota_tangearng.csv')
		_sum        = data.iloc[:,2:].sum(axis=0, skipna = True)
		_sum_column = data.iloc[:,2:].columns

		_sum_data = list()
		for n in range(len(_sum)):
			_sum_data.append({ 'key':_sum_column[n], 'val':_sum[n]})
			_total_sum += int(_sum[n])
	to_return = {
		'geo' 			: geo_data,
		'_total_sum' 	: int(_total_sum)
	}
	return jsonify(returnAPI(True, 200, 'Success', to_return))

def renew_html():
	geo_data = open('static/geo.json')
	geo_data = json.loads(geo_data.read())
	# algoritma = algoritm()
	label_data, df, hasil_label = algoritm()
	print('====== DATAFRAME =====')
	print(df)
	for f in range(len(geo_data['features'])):
		geo_kota = geo_data['features'][f]['properties']['name']
		search   = df.loc[df['Nama Desa'] == geo_kota]
		if search is not None:
			geo_data['features'][f]['properties']['cluster'] = search['clustering'].to_numpy()[0]
		else:
			geo_data['features'][f]['properties']['cluster'] = 0
	

	data       = list()
	_sum_data  = list()
	_total_sum = 0
	if(os.path.exists('static/data_covid_kota_tangearng.csv')):
		data        = pd.read_csv('static/data_covid_kota_tangearng.csv')
		_sum        = data.iloc[:,2:].sum(axis=0, skipna = True)
		_sum_column = data.iloc[:,2:].columns

		_sum_data = list()
		for n in range(len(_sum)):
			_sum_data.append({ 'key':_sum_column[n], 'val':_sum[n]})
			_total_sum += int(_sum[n])
	print('TOTAL SUM')
	print(_total_sum)
			
	return render_template('pages/frontend/partials/tables_data.html', 
		geo = geo_data, label_data=label_data, df=df,
		columns=columns, data=data, _sum_data=_sum_data, _total_sum=_total_sum)

def returnAPI(success, status_code, message, data = None, additional_data = None):
    result = {
        "success": success,
        "status_code": status_code,
        "message": message,
    }
    if data is not None:
        result.update({
            "data" : data
        })
    if additional_data is not None:
        result.update({
            "additional_data" : additional_data
        })
    return result
##AUTH
def login():
	if "user" in session:
		return redirect(url_for("index_admin"))
	else:
		return render_template('pages/login.html')

def doLogin(data):
	try:
		user = User.get_by_username(data['username'])
		print(user)
		if user == None:
			flash('Username tidak terdaftar.!', 'danger')
			return redirect(url_for('login'))
		if bcrypt.checkpw(data['password'].encode('utf8'), user['password'].encode('utf8')):
			session['user'] = user
			return redirect(url_for("index_admin"))
		else:
			flash('Password yang dimasukan salah.!', 'danger')
			return redirect(url_for('login'))
	except Exception as e:
		raise e
	

def logout():
	if "user" in session:
		session.pop("user", None)

	return redirect(url_for("login"))