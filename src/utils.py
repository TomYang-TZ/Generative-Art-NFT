import os
import json
import requests
import random
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
              seed=985454925,cfg_scale=14,steps=30,width=1024,height=1024):
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
        image = image.resize((512,512))
    except Exception as e:
        print(e)
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

def generate_prompt():
    # Expanded positive traits library with a sci-fi and specific themes
    positive_prompt_pool = {
        "technology": ["Space Station", "Advanced Telescope", "Intergalactic Spacecraft", 
                       "Alien Observatory", "Quantum Computer", "Hyperspace Engine", 
                       "Teleportation Device", "Force Field Generator", "Nano Robots", "Time Machine", 
                       "Antimatter Reactor", "Orbital Habitat", "Deep Space Probe"],
        "lighting": ["Stellar Glow", "Cosmic Ambient Light", "Supernova Explosion Light", 
                     "Bioluminescence", "Auroral Light", "Reflection from Planetary Rings", 
                     "Laser Comms Beam", "Neutron Star Light", "Dark Energy Glow"],
        "viewpoint": ["First Person View", "Aerial View", "View from a Spacecraft", 
                      "Telescope Zoom", "Panoramic View", "Through an Alien's Eyes", 
                      "Microscopic Quantum Level", "Galactic Scale", "Multiverse Perspective"],
        "colorScheme": ["Galactic Blues and Purples", "Nebula Reds and Oranges", 
                        "Cold Space Grays", "Warm Planetary Yellows and Greens", 
                        "Alien Planet Pastels", "Black Hole Black and White", 
                        "Quantum Fluctuation Hues", "Supernova Spectrum", "Dark Matter Shades"],
        "SciFiObject": ["Futuristic Military Cyborg", "Advanced Spacecraft", "Alien Technology", 
                        "Interstellar Station", "Quantum Device", "Extraterrestrial Artifact", 
                        "Robotic Drone", "Energy Shield", "Space Elevator", "Artificial Moon"],
        "SciFiEnvironment": ["Dystopian City", "Cyberpunk Streets", "Futuristic Metropolis", 
                             "Interstellar Space", "Alien Landscape", "High-Tech Laboratory", 
                             "Underground Colony", "Orbital Habitat", "Virtual Reality Landscape", 
                             "Parallel Universe"],
        "SciFiPhenomena": ["Wormhole Travel", "Artificial Intelligence Uprising", 
                           "Galactic Federation", "Time Paradox", "Quantum Anomalies", 
                           "Virtual Reality Worlds", "Alien Invasion", "Space-Time Continuum", 
                           "Singularity Event", "Cosmic Storm"],
        "SciFiTechnology": ["Teleportation Gates", "Nano Tech", "Cybernetic Enhancements", 
                            "Fusion Reactors", "Artificial Gravity", "Holographic Displays", 
                            "Laser Weapons", "Antimatter Bomb", "Cloaking Device", "Brain-Computer Interface"],
        "LightingAndEffects": ["Neon Lights", "Volumetric Lighting", "Ambient Light", 
                               "Real-Time VFX", "Digital 3D Effects", "HDR Lighting", 
                               "Bioluminescent Glow", "Plasma Energy", "Strobe Effects", "Quantum Flare"],
        "CharacterAndDesign": ["Cyberpunk Character", "Stealth Warframe", "Armored Warrior", 
                               "Smooth and Detailed Face", "Intricate Details", "Symmetrical Design", 
                               "Alien Life Form", "Mechanical Exoskeleton", "Virtual Avatar", "Augmented Human"]
    }

    negative_prompt_pool = {
        "AvoidFeatures": ["Mouth", "Ears", "Holes", "Out of Frame", "Bad Art", "Blurry", 
                          "Bad Proportions", "Gross Proportions", "Duplicate", "Bad Anatomy", 
                          "Deformed", "Ugly", "Long Neck", "Cropped Head", "Cartoon", "Anime", 
                          "Overexposed", "Underexposed", "Unnatural Poses", "Cluttered Composition"],
        "AvoidArtStyles": ["Digital Painting", "Anime Style", "Cartoon Style", 
                           "Low-Quality Artwork", "Watermarked Images", "Signature", 
                           "Abstract Art", "Minimalist Art", "Impressionist Art", "Surreal Art"],
        "AvoidScenes": ["Portrait of a Girl", "Face Close Up", "Pointy Ears", "Dress", 
                        "Half-Closed Eyes", "Jewelry", "Sitting", "Strapless Dress", "Breasts", 
                        "Bare Shoulders", "Tiara", "Cleavage", "Long Hair", "Braid", "Grey Hair", 
                        "Long Eyelashes", "Elf", "Crowded Scenes", "Busy Cityscapes", "Ordinary Daily Life"],
        "SpecificAvoidances": ["Curvy", "Plump", "Fat", "Muscular Female", "3D Face", "Cropped", 
                               "Detailed Realistic Human Spaceman", "Working on Mars", 
                               "Everyday Clothing", "Modern Day Technology", "Contemporary Vehicles", 
                               "Realistic Animals", "Typical Office Environments"]
    }

    positive_prompt = ""
    positive_attributes = []

    # Iterate through the positive traits library
    for trait, values in positive_prompt_pool.items():
        rno1,rno2,rno3= random.sample(range(len(values)),3)
        if positive_prompt:
            positive_prompt += ", " + values[rno1] + ', ' + values[rno2] + ', ' + values[rno3] 
        else:
            positive_prompt = values[rno1] + ', ' + values[rno2] + ', ' + values[rno3] 
        positive_attributes.append({"trait_type": trait, "value": values[rno1] + ', ' + values[rno2] + ', ' + values[rno3]})
    QualityAndDetail =["Highly Detailed", "UHD Quality", "Dreamlike Art", "3D Render", 
                             "Hard Surface Modeling", "Ultra Detailed Texture", "Surreal Imagery", 
                             "High Fidelity Graphics", "Dynamic Composition", "Cinematic Style"]
    for trait in random.sample(QualityAndDetail,3):
        positive_prompt += ", " + trait
        positive_attributes.append({"trait_type": "Quality and Detail", "value": trait})
    negative_prompt = ""
    negative_attributes = []

    # Iterate through the negative traits library
    for trait, values in negative_prompt_pool.items():
        rno1,rno2,rno3 = random.sample(range(len(values)),3)
        if negative_prompt:
            negative_prompt += ", " + values[rno1] + ', ' + values[rno2] + ', ' + values[rno3] 
        else:
            negative_prompt = values[rno1] + ', ' + values[rno2] + ', ' + values[rno3] 
        negative_attributes.append({"trait_type": trait, "value": values[rno1] + ', ' + values[rno2]})

    TechnicalAvoidances = ["Worst Quality", "Low Quality", "Depth of Field Issues", 
                                "Blurriness", "Greyscale", "Monochrome", "Low Resolution", 
                                "Text in Image", "JPEG Artifacts", "Trademark", "Watermark", 
                                "Multiple Views", "Reference Sheet", "Strabismus", 
                                "Pixelation", "Color Banding", "Lens Flare", "Motion Blur"]
    for trait in TechnicalAvoidances:
        negative_prompt += ", " + trait
        negative_attributes.append({"trait_type": "Technical Avoidances", "value": trait})
    return positive_prompt, positive_attributes, negative_prompt, negative_attributes

def datanft(dataset_name = "chain_link_space6",
            POS_TEXT_PROMPT = "mountain, river, tree, cats",
            NEG_TEXT_PROMPT = 'violent',
            SPACE_UUID = "9f62111c-16aa-4111-bb24-e66b9923b0d0",
            SEED = -1,
            UI=False):
    global lagrange_api_key,private_key,wallet_address,mumbai_rpc,api_client,lag_client,chain_id
    
    dot_env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if not UI: load_dotenv(dot_env_path)
    POS_TEXT_PROMPT, positive_attributes_list, NEG_TEXT_PROMPT, negative_attributes_list = generate_prompt()
    print("Positive Prompt:", POS_TEXT_PROMPT)
    print("Negative Prompt:", NEG_TEXT_PROMPT)
    lagrange_api_key = os.getenv("LAGRANGE_API_KEY")
    private_key = os.getenv("PRIVATE_KEY") 
    wallet_address = os.getenv("WALLET_ADDRESS")

    mumbai_rpc = 'https://rpc-mumbai.maticvigil.com'
    api_client = APIClient(lagrange_api_key,private_key,mumbai_rpc,True, True)
    lag_client = LagAPI(api_client)
    chain_id = 80001
    
    # First, we need to retreive the link to the diffusion model hosted on a lagrange space through its space uuid
    SPACE_UUID = os.environ.get("SPACE_UUID")
    res = lag_client.get_result_uri_from_space_uuid(SPACE_UUID)
    if DEBUG: print(res)
    try:
        url = res['data']['job_result_uri']
    except Exception as e:
        print(str(e))
        raise Exception("Error getting url from LAG")
        
    # Then we can use the url to generate an image and upload it to the Lagrange dataset
    
    image = get_image(prompt=POS_TEXT_PROMPT,negative_prompt=NEG_TEXT_PROMPT,url=url,seed=SEED)
    img_name = str(uuid.uuid4()) + ".png"
    img_path = f"{os.path.dirname(__file__)}/" + img_name
    image.save(img_path)
    if DEBUG:print(img_path)
    upload_img2lag(img_path,dataset_name,1)
    
    # Next we upload the image to IPFS, to a bucket named DataNFT on MCS
    
    try:
        img_link = save_to_MCS_bucket(initialize_bucket=True,overwrite_file=True,
                                  bucket_name='DataNFT',file_path=img_path,name=img_name)
    except Exception as e:
        print(str(e))
        raise Exception("Error saving image to MCS bucket") 
    # print("Image Link on MCS: ", img_link)
    
    # Now we can create a data NFT
    print("Creating data NFT")
    res = lag_client.data_nft_request(chain_id,wallet_address,dataset_name)
    start = time.time()
    print("Waiting for data NFT to be created")
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
    # Example usage
    mcs_img_link,contract_address,dataset_address,license_ipfs_uri,license_mint_hash = datanft()
    print("MCS Image Link: ",mcs_img_link)
    print("Contract address: ",contract_address)
    # print("Dataset name: ",dataset_name)
    print("Dataset license ipfs uri: ",license_ipfs_uri)
    print("Dataset license transaction hash: ","https://mumbai.polygonscan.com/tx/" + license_mint_hash)
    