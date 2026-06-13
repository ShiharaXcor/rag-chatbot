import  os  
from dotenv  import  load_dotenv    

###  create  the  function   


load_dotenv()    


###  get   the    keys  form  the  .env  file    

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
EMBEDDING_MODEL     = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LLM_MODEL           = os.getenv("LLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
MAX_FILE_SIZE_MB    = int(os.getenv("MAX_FILE_SIZE_MB", 20))
MAX_FILES           = int(os.getenv("MAX_FILES", 10))


###    make  the  directory  to   upload  the  pdf  vector store  api   


UPLOAD_DIR      = "uploads"
VECTORSTORE_DIR = "vectorstore"
CHAT_HISTORY_FILE = "chat_history.json"

##  make  sure  the  files  save  in  the right  location    

os.makedirs(UPLOAD_DIR, exist_ok=True)    
os.makedirs(VECTORSTORE_DIR, exist_ok=  True)   
