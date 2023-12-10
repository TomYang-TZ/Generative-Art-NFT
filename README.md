# <img src="https://www.gitbook.com/cdn-cgi/image/width=36,dpr=2,height=36,fit=contain,format=auto/https%3A%2F%2F576435799-files.gitbook.io%2F~%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-MauK7Ig3eWeXC35bZV7%252Ficon%252FUuoj67jxo8XNDYmZKupy%252Flogo_transparent.png%3Falt%3Dmedia%26token%3D8e053c6b-b5b3-4055-86dc-380c9f0a609d" width="30" height="30"/> Generative Art NFT with Lagrange AI and Chainlink Functions


## Sample Outputs
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmZKsSQ9WMSAtn1hw71Jr2DXVNnVsHvh8KS9s14JPEiJFc)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmWjVP4D2CS2oimANTv9KkxngFwcBDBRMyuZRnHTJFp5tF)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmXqov8MCyRx8BbHDSn4FHoL8zYztF856ZP4qafdiWTHHZ)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmdrxbZhqqEvxdJxjGGPqZQPWRgZmHSsh9UVm792WtvhRE?filename=9dc765db-a705-49df-aa04-6013ea286252.png)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmUKfRNnNECdZpYhEhYbU9p4hbafK9tdUjnCcA3yeutiEy?filename=cf76663c-e987-48cb-a583-f85c6a94396b.png)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmWvDX1gP98wM4QJi4hdkDDb2HqDNxHZVzXxLXvwoTytCH)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmeyRegd2cKZNsC8dvBxc447rBrwgwZz7Wedw9fmU7w5Ta)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmaQ6wGJ4zPvyLnWZoDBrrxCSLooUdbed3rWufdRhPp2Zd)
![](https://a8ef60452885.acl.multichain.storage/ipfs/QmaP8dUtkjaevACwCSowxAcHzGZmTBYk2P2w41sKN3H5zS)

### [OpenSea Market Place](https://testnets.opensea.io/collection/swan-chainlink)

## Description

Welcome to the `Swan Chain DataNFT` project. We used [Lagrange APIs and Chainlink Functions](https://github.com/lagrangedao/python-lag-sdk/tree/dev) to create data NFTs, allowing owners to embed usage terms in the NFT metadata. These NFTs are developed on the Sepolia and Mumbai testnets.

## Installation

To set up the DataNFT Project, ensure you have a compatible virtual environment. Follow these steps to install the necessary dependencies:

```bash
# Clone the repository
git clone https://github.com/TomYang-TZ/Generative-DataNFT.git

# Navigate to the project directory
cd Generative-DataNFT 

# Create a virtual environment first
conda create -n "VIRTUAL_ENV_NAME" python=3.9

# Run the setup script
./setup.sh
```

## Usage
Note that all our functions run locally, your information is not collected.
### Running Locally

To run the DataNFT application locally:

1. Navigate to the `DataNFT-V2` folder:
   ```bash
   cd Generative-DataNFT 
   ```

2. Start the Flask application:
   ```py
   python app.py
   ```

### Running in Docker

To run the application using Docker:

1. Build the Docker image:
   ```bash
   docker build -t datanft-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 datanft-app # Remember to change the exposed port in the Dockerfile accordingly
   ```

   The Dockerfile is located at `DataNFT-V2/Dockerfile`.

## NFT Campaign  
To launch our NFT Campaign, which is themed around constellation, advanced technology, cosmic phenomena, and surreal sci-fi environments, we have crafted a comprehensive collection of both positive and negative text prompts. These prompts are systematically selected at random to ensure a diverse and captivating representation in our project. To modify and design your own campain, see [below](#setup)

## For Developers

### Core Function

The core functionality of this application is encapsulated in the `datanft()` function, which can be found in `src/utils.py`.

### Setup

1. API Configuration:
   - Create a `.env` file in the root directory.
   - Follow the template provided to set up your API keys and other configurations.
   - Please remember to use your personal API token from your ***[Lagrange Testnet](https://testnet.lagrangedao.org/main)*** account as the Lagrange API key.

2. Using the `datanft()` Function:
   - Here's an example to illustrate the usage of `datanft()`:
     ```py
      mcs_img_link, chainlink_function_contract_address, nft_contract_address, dataset_address, license_mint_hash  = datanft(POS_TEXT_PROMPT=POS_TEXT_PROMPT, NEG_TEXT_PROMPT=NEG_TEXT_PROMPT)
     )
     ```
     You can craft your own text prompts and create unique NFTs using Lagrange AI and Chainlink Functions
