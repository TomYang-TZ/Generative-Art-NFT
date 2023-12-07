import os
import json
import requests
import io
import base64
import time
import uuid

from PIL import Image
from dotenv import load_dotenv

from swan_lag.api_client import APIClient
from swan_lag.api.lag_client import LagAPI

DEBUG = False

def get_image(url='https://pgmwn8b5xu.meta.crosschain.computer',
              username='admin',password='admin1234',
              prompt='a green apple',negative_prompt='violent',
              sampler_name='DPM++ 2M Karras',
              seed=985454925,cfg_scale=7,steps=20,width=512,height=512):
    # Encode the username and password in Base64
    credentials = f'{username}:{password}'
    credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }
    # construct payload as a dictionary
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "sampler_name": sampler_name,
        "seed": seed,
        "cfg_scale": cfg_scale,
        "steps": steps,
        "width": width,
        "height": height,
    }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload, headers=headers)  
    try:
        r = response.json()  
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    except:
        raise Exception("Error getting image from diffusion model")
    return image


def save_to_MCS_bucket( bucket_name="diffusion2",file_path="output.png",name="output.png",
                       overwrite_file=False,initialize_bucket=True):
    from swan_mcs import APIClient,BucketAPI
    def initialize_client(api_key,chain="polygon.mumbai",):
        mcs_api = APIClient(api_key, chain  )
        return BucketAPI(mcs_api)
    bucket_client = initialize_client(api_key=os.getenv("MCS_API_KEY"))
    if initialize_bucket: bucket_client.create_bucket(bucket_name)   
    if overwrite_file:
        print(f"Overwriting file {name}")
        bucket_client.delete_file(bucket_name, name)
    file_data = bucket_client.upload_file(bucket_name, name , file_path) 
    if not file_data:
        print("upload failed")
        raise Exception("upload failed") 
    file_data = json.loads(file_data.to_json())
    print(file_data)
    return file_data["ipfs_url"]  


def upload_img2lag(img_file_path,dataset_name,is_public):
    
    #Sample files format
    files = {"file": (img_file_path, open(img_file_path, "rb"))}
    lag_client.create_dataset(dataset_name, is_public)
    #Upload_files_to_dataset
    res = lag_client.upload_dataset_file(dataset_name,files)
    if DEBUG:print(res)
    if res['status'] != 'success':
        raise Exception("Error uploading file to LAG")

def datanft(dataset_name = "chain_link_space6",
            POS_TEXT_PROMPT = "mountain, river, tree, cats",
            NEG_TEXT_PROMPT = 'violent',
            SPACE_UUID = "eccbf673-4277-4f54-a71d-0286d5be8771",
            SEED = 4242):
    load_dotenv()
    global lagrange_api_key,private_key,wallet_address,mumbai_rpc,api_client,lag_client,chain_id
    
    lagrange_api_key = os.getenv("LAGRANGE_API_KEY")
    private_key = os.getenv("PRIVATE_KEY") 
    wallet_address = os.getenv("WALLET_ADDRESS")

    mumbai_rpc = 'https://rpc-mumbai.maticvigil.com'
    api_client = APIClient(lagrange_api_key,private_key,mumbai_rpc,True, True)
    lag_client = LagAPI(api_client)
    chain_id = 80001
    
    # First, we need to retreive the link to the diffusion model hosted on a lagrange space through its space uuid
    # 用户输入，optional，default=eccbf673-4277-4f54-a71d-0286d5be8771
    # SPACE_UUID = os.environ.get("SPACE_UUID")
    res = lag_client.get_result_uri_from_space_uuid(SPACE_UUID)
    if DEBUG: print(res)
    try:
        url = res['data']['job_result_uri']
    except:
        raise Exception("Error getting url from LAG")
        
    # Then we can use the url to generate an image and upload it to the Lagrange dataset
    
    image = get_image(prompt=POS_TEXT_PROMPT,negative_prompt=NEG_TEXT_PROMPT,url=url,seed=SEED)
    img_name = str(uuid.uuid4()) + ".png"
    img_path = f"{os.path.dirname(__file__)}/" + img_name
    image.save(img_path)
    if DEBUG:print(img_path)
    upload_img2lag(img_path,dataset_name,1)
    
    # Next we upload the image to IPFS
    
    try:
        img_link = save_to_MCS_bucket(initialize_bucket=True,overwrite_file=True,
                                  bucket_name='trial',file_path=img_path,name=img_name)
    except Exception as e:
        print(str(e))
        raise Exception("Error saving image to MCS bucket") 
    # print("Image Link on MCS: ", img_link)
    
    # Now we can create a data NFT
    res = lag_client.data_nft_request(chain_id,wallet_address,dataset_name)
    start = time.time()
    while True:
        res = lag_client.try_claim_data_nft(wallet_address,dataset_name)
        if DEBUG:print(res)
        claimable = 'not claimable' not in res['message']
        res = lag_client.get_data_nft_info(wallet_address,dataset_name)
        if DEBUG:print(res)
        nft = res['data']['nft']
        contract_address = nft['contract_address']
        
        if contract_address and claimable: break
        if contract_address and not claimable: 
            print("Not claimable")
            break
        
        time.sleep(10)
        now = time.time()
        # if the time to create datanft is more than 2 minutes, break
        if now - start > 120:
            print("Time out")
            raise Exception("Time out")
    if claimable: 
        print("Data NFT claimable")
        
        # print("Data NFT contract address: ",contract_address)
    
    # Finally we create a dataset license
    res = lag_client.create_dataset_license(wallet_address,dataset_name,contract_address,chain_id,wallet_address)
    if res['status'] != 'success':
        raise Exception("Error creating dataset license")
    print("Dataset license created")
    # license_contract_address = res['data']['contract_address']
    license_ipfs_uri = res['data']['ipfs_uri']
    license_mint_hash = res['data']['mint_hash']
    if DEBUG: print(res)
    
    os.remove(img_path)
    dataset_address = f"https://testnet.lagrangedao.org/datasets/{wallet_address}/{dataset_name}/files"
    
    return img_link,contract_address,dataset_address,license_ipfs_uri,license_mint_hash
    
    
    
if __name__ == "__main__":
    mcs_img_link,contract_address,dataset_address,license_ipfs_uri,license_mint_hash = datanft()
    print("MCS Image Link: ",mcs_img_link)
    print("Contract address: ",contract_address)
    # print("Dataset name: ",dataset_name)
    print("Dataset license ipfs uri: ",license_ipfs_uri)
    print("Dataset license transaction hash: ","https://mumbai.polygonscan.com/tx/" + license_mint_hash)
    