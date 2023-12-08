# DataNFT Project

## Description

Welcome to the `Swan Chain DataNFT` project. We used [Lagrange APIs and Chainlink Functions](https://github.com/lagrangedao/python-lag-sdk/tree/dev) to create data NFTs, allowing owners to embed usage terms in the NFT metadata. These NFTs are developed on the Sepolia and Mumbai testnets.

## Installation

To set up the DataNFT Project, ensure you have a compatible virtual environment. Follow these steps to install the necessary dependencies:

```bash
# Clone the repository
git clone https://github.com/TomYang-TZ/Generative-DataNFT.git

# Navigate to the project directory
cd DataNFT-Project

# Run the setup script
./setup.sh
```

## Usage

### Running Locally

To run the DataNFT application locally:

1. Navigate to the `DataNFT-V2` folder:
   ```bash
   cd DataNFT-V2
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

## For Developers

### Core Function

The core functionality of this application is encapsulated in the `datanft()` function, which can be found in `src/utils.py`.

### Setup

1. API Configuration:
   - Create a `.env` file in the root directory.
   - Follow the template provided to set up your API keys and other configurations.

2. Using the `datanft()` Function:
   - Here's an example to illustrate the usage of `datanft()`:
     ```py
     mcs_img_link, contract_address, dataset_address, license_ipfs_uri, license_mint_hash = datanft(
         dataset_name, pos_text_prompt, neg_text_prompt, space_uuid, seed
     )
     ```
