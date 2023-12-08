import sys
import os
import json
from flask import Flask, render_template, request, jsonify, Response
sys.path.append(os.path.join('.','src'))  # Add the src folder to the Python path
from src.utils import datanft  # Import the datanft function

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/set_env', methods=['POST'])
def set_env():
    try:
        if len(request.form['lagrangeApiKey']) == 0 or len(request.form['mcsApiKey']) == 0 or len(request.form['privateKey']) == 0 or len(request.form['walletAddress']) == 0:
            raise Exception("Please fill in all the fields")
        os.environ['LAGRANGE_API_KEY'] = request.form['lagrangeApiKey']
        os.environ['MCS_API_KEY'] = request.form['mcsApiKey']
        os.environ['PRIVATE_KEY'] = request.form['privateKey']
        os.environ['WALLET_ADDRESS'] = request.form['walletAddress']
        os.environ['SPACE_UUID'] = '9f62111c-16aa-4111-bb24-e66b9923b0d0'
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})
        

@app.route('/generate', methods=['POST'])
def generate():
    for field in request.form:
        if request.form[field] == '':
            return jsonify({'error': f'Please fill in required fields'})
    space_uuid = request.form['spaceID']  
    dataset_name = request.form['datasetName']
    # pos_text_prompt = request.form['posTextPrompt']
    # neg_text_prompt = request.form['negTextPrompt']

    # Call the datanft function from your utils.py
    try:
            mcs_img_link, contract_address, dataset_address,license_ipfs_uri, license_mint_hash = datanft(
                dataset_name, space_uuid, SEED=-1, UI=True
            )
            print({
                'mcs_img_link': mcs_img_link,
                'contract_address': contract_address,
                'dataset_address': dataset_address,
                'license_ipfs_uri': license_ipfs_uri,
                'license_mint_hash': license_mint_hash
            })
            return jsonify({
                'mcs_img_link': mcs_img_link,
                'contract_address': contract_address,
                'dataset_address': dataset_address,
                'license_ipfs_uri': license_ipfs_uri,
                'license_mint_hash': license_mint_hash
            })
        
        
    except Exception as e:
        print(e)
        return jsonify({'error': str(e) + "\nCheck your environment variables and try again. If the problem persists, please contact us at tomyang@nbai.io"})

if __name__ == '__main__':
    app.run(debug=True)
