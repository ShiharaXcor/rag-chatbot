from  fastapi  import FastAPI   
from  fastapi.middleware.cors    import CORSMiddleware    
from routes.upload import router as upload_router
from routes.chat import router as chat_router   

###    projects  metadata     
app    =  FastAPI(
   title="Company Knowledge RAG Chatbot",
    description="Secure RAG chatbot for internal company knowledge base",
    version="1.0.0"
)


###  create the  cors  for  give   the accass for  the  frontend  


app.add_middleware(
   CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")   



###  create  the  root     
@app.get("/")   
def  root()  :   
    return  {"status": "ok", "message": "RAG Chatbot API is running"}  

### create  the  another  root  for check  the  health   
@app.get("/health")
def health():   
    return   {"status": "healthy"}



