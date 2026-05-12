import io
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
import uvicorn

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Online", "message": "Background Remover is Ready!"}

@app.post("/remove")
async def remove_bg(image: UploadFile = File(...)):
    """
    এই মেথডটি সরাসরি ইমেজ ফাইল গ্রহণ করবে এবং 
    ব্যাকগ্রাউন্ড রিমুভ করে ইমেজ রিটার্ন করবে।
    """
    try:
        # ১. ইমেজ ডাটা রিড করা
        input_image = await image.read()
        
        # ২. ব্যাকগ্রাউন্ড রিমুভ করা
        output_image = remove(input_image)
        
        # ৩. প্রসেস করা ইমেজটি স্ট্রিমিং রেসপন্স হিসেবে পাঠানো
        return StreamingResponse(
            io.BytesIO(output_image), 
            media_type="image/png"
        )
        
    except Exception as e:
        # কোনো এরর হলে সেটি রিটার্ন করবে
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
