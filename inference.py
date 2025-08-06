from alith import Agent, LazAIClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# LazAI config
LAZAI_IDAO_ADDRESS = "0xc3e98E8A9aACFc9ff7578C2F3BA48CA4477Ecf49"
private_key = os.getenv("PRIVATE_KEY")  
if not private_key:
    raise ValueError("PRIVATE_KEY not set in .env")

# Groq config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in .env")

# LazAI client
client = LazAIClient(private_key=private_key)

# User setup
DEPOSIT_AMOUNT = 10000000
try:
    address = client.get_user(client.wallet.address)
    print(" User already exists:", address)
except Exception:
    print(" User does not exist, creating...")
    try:
        client.add_user(DEPOSIT_AMOUNT)
        client.deposit(DEPOSIT_AMOUNT * 2)
        client.deposit_inference(LAZAI_IDAO_ADDRESS, DEPOSIT_AMOUNT)
        print(f" Successfully added user and deposited {DEPOSIT_AMOUNT}")
    except Exception as e:
        print(" Error adding user or depositing:", e)


file_id = 10  

url = "https://api.groq.com/openai"  #change the URL if needed

# Extra headers: combine LazAI settlement headers + Groq key
extra_headers = client.get_request_headers(LAZAI_IDAO_ADDRESS, file_id=file_id)
extra_headers["Authorization"] = f"Bearer {GROQ_API_KEY}"

# Create Groq Agent
agent = Agent(
    model="deepseek/deepseek-r1-0528",  #Change the model you used 
    base_url=f"{url}/v1",
    extra_headers=extra_headers,
)

print(agent.prompt("what is LazAi"))
